from flask import Flask, render_template, request, jsonify, session, send_from_directory
from google import genai
from google.genai import types
import os
import sys
import json
import tempfile
from pathlib import Path
import traceback
import re
import time
import ast

# Optional OpenAI Import
try:
    from openai import OpenAI
    OPENAI_SUPPORT = True
except ImportError:
    OPENAI_SUPPORT = False
    print("OpenAI Support disabled (openai package not found)")

# Ensure imports work on Render (Gunicorn) and Local
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import axiom_brain
from dotenv import load_dotenv
parent_dir = Path(__file__).parent.parent
load_dotenv(parent_dir / '.env')

# Phase 4 Imports
try:
    import fitz
    import numpy as np
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("PDF Support disabled")

# FAISS removed for Vercel optimization (using numpy dot product instead)
FAISS_SUPPORT = False

app = Flask(__name__, 
            template_folder=str(parent_dir / 'templates'),
            static_folder=str(parent_dir / 'static'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

# --- INTELLIGENT ROUTER CONFIG ---

# Clients
gemini_client = None
if os.environ.get('GEMINI_API_KEY'):
    try:
        gemini_client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
        print("✓ Gemini Ready")
    except: pass

openrouter_client = None
if OPENAI_SUPPORT and os.environ.get('OPENROUTER_API_KEY'):
    try:
        openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get('OPENROUTER_API_KEY'))
        print("✓ OpenRouter Ready")
    except: pass

openai_client = None
if OPENAI_SUPPORT and os.environ.get('OPENAI_API_KEY'):
    try:
        openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        print("✓ OpenAI Ready")
    except: pass

# Model Pools (Prioritized)
MODELS_GEMINI = ['gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-2.5-flash']
MODELS_OPENROUTER = [
    'google/gemini-2.0-flash-exp:free', 
    'meta-llama/llama-3.3-70b-instruct:free',
    'deepseek/deepseek-r1-distill-llama-70b:free',
    'microsoft/phi-3-medium-128k-instruct:free'
]
MODELS_OPENAI = ['gpt-4o-mini'] # Paid fallback

# Health Tracker: { 'provider_name': last_failure_timestamp }
# If failure was < 60s ago, skip.
API_HEALTH = {
    'gemini': 0,
    'openrouter': 0,
    'openai': 0
}
COOLDOWN_SECONDS = 60

# Session storage for RAG
session_data = {}

def is_healthy(provider_name):
    """Check if provider is available (not in cooldown)"""
    if time.time() - API_HEALTH[provider_name] < COOLDOWN_SECONDS:
        return False
    return True

def mark_sick(provider_name):
    """Mark provider as failing (start cooldown)"""
    print(f"⚠️ Marking {provider_name} as SICK (Cooldown {COOLDOWN_SECONDS}s)")
    API_HEALTH[provider_name] = time.time()

# --- GENERATION LOGIC ---

def generate_smartly(agnostic_messages):
    """
    Intelligent routing based on model health and availability.
    """
    last_error = None
    
    # 1. Try Gemini (Fastest, High Quality)
    if gemini_client and is_healthy('gemini'):
        try:
            # Adapter
            gemini_contents = [
                types.Content(role=dict(m)['role'], parts=[types.Part.from_text(text=str(dict(m)['content']))]) 
                for m in agnostic_messages
            ]
            
            for model in MODELS_GEMINI:
                try:
                    # print(f"Trying Gemini: {model}")
                    response = gemini_client.models.generate_content(
                        model=model,
                        contents=gemini_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=axiom_brain.SYSTEM_INSTRUCTION,
                            temperature=0.7 # Slightly lower for JSON stability
                        )
                    )
                    if response.text: return response.text
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        print(f"Gemini 429 Quota Exceeded on {model}")
                    else:
                        print(f"Gemini Error {model}: {e}")
            # If loop finishes without return, all Gemini models failed.
            # Mark sick only if it was a quota issue (heuristic: usually is)
            mark_sick('gemini')
            
        except Exception as e:
            print(f"Gemini Critical Fail: {e}")
            mark_sick('gemini')
            last_error = e

    # Adapter for OpenAI/OpenRouter
    openai_msgs = [{"role": "system", "content": axiom_brain.SYSTEM_INSTRUCTION}] + agnostic_messages

    # 2. Try OpenRouter (Free Tier, Diverse)
    if openrouter_client and is_healthy('openrouter'):
        # print("Attempting OpenRouter...")
        for model in MODELS_OPENROUTER:
            try:
                # print(f"Trying OpenRouter: {model}")
                resp = openrouter_client.chat.completions.create(
                    model=model,
                    messages=openai_msgs,
                    temperature=0.7
                )
                txt = resp.choices[0].message.content
                if txt: return txt
            except Exception as e:
                # print(f"OpenRouter Error {model}: {e}")
                # Don't mark sick immediately on one model fail, but if loop fails...
                continue
        # If we got here, all OpenRouter models failed
        mark_sick('openrouter')
    
    # 3. Try OpenAI (Paid, Reliable)
    if openai_client and is_healthy('openai'):
        print("Fallback to OpenAI...")
        try:
            resp = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=openai_msgs,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {e}")
            mark_sick('openai')
            last_error = e

    raise last_error or Exception("All Available AI Routes Exhausted.")

# --- PARSING LOGIC (3-Stage) ---
def parse_response(raw_text):
    chat_resp = None
    graph_cmds = []
    
    # Clean code blocks
    text = re.sub(r'```json\s*', '', raw_text)
    text = re.sub(r'```\s*', '', text)
    
    # Extract JSON candidate bounds
    start = text.find('{')
    end = text.rfind('}')
    json_candidate = text[start:end+1] if (start != -1 and end != -1) else text
    
    # --- STAGE 1: JSON ---
    try:
        parsed = json.loads(json_candidate)
        chat_resp = parsed.get('chatResponse')
        graph_cmds = parsed.get('graphCommands', [])
    except:
        # --- STAGE 2: AST ---
        try:
            # Fix booleans/nulls for Python AST
            ast_safe = json_candidate.replace("true", "True").replace("false", "False").replace("null", "None")
            parsed = ast.literal_eval(ast_safe)
            if isinstance(parsed, dict):
                chat_resp = parsed.get('chatResponse')
                graph_cmds = parsed.get('graphCommands', [])
        except:
             # --- STAGE 3: Regex Rescue ---
            # print("Applying Regex Rescue...")
            match = re.search(r'[\"\']chatResponse[\"\']\s*:\s*([\"\'])(.*?)(?<!\\)\1', raw_text, re.DOTALL)
            if match:
                raw_cr = match.group(2)
                chat_resp = raw_cr.replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
    
    # Scan for implicit commands (The "Ghost Response" Fix)
    if "setBlank" in raw_text or "clearExpressions" in raw_text:
        # Check if setBlank is already in cmds
        has_clear = any(c.get('command') == 'setBlank' for c in graph_cmds)
        if not has_clear:
            # Prepend clear command
            graph_cmds.insert(0, {"command": "setBlank"})

    if chat_resp is None:
        chat_resp = raw_text # Absolute fallback
        
    return chat_resp, graph_cmds

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get('message', '')
        if not user_msg: return jsonify({'chatResponse': '?', 'graphCommands': []})
        
        # RAG Context
        rag_ctx = ""
        sid = data.get('sessionId', 'default')
        if sid in session_data and 'faiss_index' in session_data[sid]:
            rag_ctx = retrieve_relevant_context(sid, user_msg)

        # Build Context
        msgs = axiom_brain.build_smart_context(
            data.get('history', []), 
            data.get('currentExpressions', []), 
            rag_ctx
        )
        msgs.append({"role": "user", "content": user_msg})

        # Generate
        raw_text = generate_smartly(msgs)
        # print(f"AI Output: {raw_text[:60]}...")
        
        # Parse
        chat_resp, graph_cmds = parse_response(raw_text)
        
        return jsonify({'chatResponse': chat_resp, 'graphCommands': graph_cmds})

    except Exception as e:
        print(f"Server Error: {e}")
        # traceback.print_exc()
        return jsonify({'chatResponse': f"Error: {str(e)}", 'graphCommands': []}), 500

# --- RAG HELPERS (NumPy Optimized) ---
def retrieve_relevant_context(sid, query):
    if not gemini_client or not is_healthy('gemini'): return ""
    try:
        # Get stored embeddings and chunks
        embeddings = session_data[sid].get('embeddings') # Shape: (N, 768)
        chunks = session_data[sid].get('text_chunks')
        if embeddings is None or not chunks: return ""

        # Embed query
        resp = gemini_client.models.embed_content(model="text-embedding-004", contents=query)
        query_vec = np.array(resp.embeddings[0].values, dtype='float32') # Shape: (768,)

        # Cosine Similarity (Dot product since normalized)
        # scores = dot(embeddings, query_vec)
        scores = np.dot(embeddings, query_vec)
        
        # Get top 3 indices
        top_k = 3
        if len(scores) < top_k: top_k = len(scores)
        
        # Argsort returns indices of sorted array (ascending), so we take last k and reverse
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        return "\n\n".join([chunks[i] for i in top_indices])
    except Exception as e:
        print(f"RAG Error: {e}")
        return ""

@app.route('/')
def index(): return render_template('index.html')

@app.route('/favicon.ico')
def favicon(): return send_from_directory(os.path.join(app.root_path, '../static'), 'favicon.ico')

# PDF Upload - NumPy Version
@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        if not PDF_SUPPORT:
            return jsonify({'success': False, 'error': 'PDF dependencies missing.'}), 500
        
        if 'pdf' not in request.files: return jsonify({'success': False, 'error': 'No file'}), 400
        pdf_file = request.files['pdf']
        session_id = request.form.get('sessionId', 'default')
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_file.save(tmp_file.name)
            pdf_path = tmp_file.name
        
        try:
            text_chunks = extract_text_from_pdf(pdf_path)
            if not text_chunks: return jsonify({'success': False, 'error': 'No text extracted'}), 400
            
            # Create Embeddings (NumPy array)
            embeddings, chunks = create_embeddings(text_chunks)
            
            if session_id not in session_data: session_data[session_id] = {}
            # Store raw embeddings instead of FAISS index
            session_data[session_id]['embeddings'] = embeddings
            session_data[session_id]['text_chunks'] = chunks
            
            return jsonify({'success': True, 'chunks': len(chunks)})
        finally:
            os.unlink(pdf_path)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def extract_text_from_pdf(pdf_path, chunk_size=1000, overlap=200):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc: full_text += page.get_text()
    chunks = []
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip(): chunks.append(chunk)
    return chunks

def create_embeddings(text_chunks):
    if not gemini_client: raise Exception("Gemini required for embeddings")
    embeddings = []
    valid_chunks = []
    for chunk in text_chunks:
        try:
            r = gemini_client.models.embed_content(model="text-embedding-004", contents=chunk)
            embeddings.append(r.embeddings[0].values)
            valid_chunks.append(chunk)
        except: continue
    return np.array(embeddings, dtype='float32'), valid_chunks

if __name__ == '__main__':
    app.run(debug=True, port=5000)
