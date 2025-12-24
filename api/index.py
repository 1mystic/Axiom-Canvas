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

# Optional OpenAI Import
try:
    from openai import OpenAI
    OPENAI_SUPPORT = True
except ImportError:
    OPENAI_SUPPORT = False
    print("OpenAI Support disabled (openai package not found)")

# Import Smart Brain
import axiom_brain

# Load environment variables
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

try:
    import faiss
    FAISS_SUPPORT = True
except ImportError:
    FAISS_SUPPORT = False
    print("FAISS Support disabled")

app = Flask(__name__, 
            template_folder=str(parent_dir / 'templates'),
            static_folder=str(parent_dir / 'static'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

# --- CLIENTS ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
gemini_client = None
if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        print("✓ Gemini Client Ready")
    except Exception as e: print(f"Gemini Init Error: {e}")

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
openrouter_client = None
if OPENAI_SUPPORT and OPENROUTER_API_KEY:
    try:
        openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
        print("✓ OpenRouter Client Ready")
    except Exception as e: print(f"OpenRouter Init Error: {e}")

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai_client = None
if OPENAI_SUPPORT and OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✓ OpenAI Client Ready")
    except Exception as e: print(f"OpenAI Init Error: {e}")

GEMINI_MODELS = ['gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-2.5-flash']
OPENROUTER_MODELS = ['google/gemini-2.0-flash-exp:free', 'meta-llama/llama-3.3-70b-instruct:free']

session_data = {}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/favicon.ico')
def favicon(): return send_from_directory(os.path.join(app.root_path, '../static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def generate_with_fallback(agnostic_messages):
    last_error = None

    # 1. Gemini
    if gemini_client:
        try:
            gemini_contents = []
            for msg in agnostic_messages:
                gemini_contents.append(types.Content(
                    role=msg['role'], 
                    parts=[types.Part.from_text(text=str(msg['content']))]
                ))
            for model in GEMINI_MODELS:
                try:
                    response = gemini_client.models.generate_content(
                        model=model,
                        contents=gemini_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=axiom_brain.SYSTEM_INSTRUCTION,
                            temperature=1.0
                        )
                    )
                    if response.text: return response.text
                except Exception as e:
                    print(f"Gemini {model} Error: {e}")
                    last_error = e
        except Exception as e: last_error = e

    # Adapter for OpenAI/OpenRouter
    openai_msgs = [{"role": "system", "content": axiom_brain.SYSTEM_INSTRUCTION}] + agnostic_messages

    # 2. OpenRouter
    if openrouter_client:
        for model in OPENROUTER_MODELS:
            try:
                resp = openrouter_client.chat.completions.create(
                    model=model, messages=openai_msgs, temperature=1.0
                )
                if resp.choices[0].message.content: return resp.choices[0].message.content
            except Exception as e:
                print(f"OpenRouter {model} Error: {e}")
                last_error = e

    # 3. OpenAI
    if openai_client:
        try:
            resp = openai_client.chat.completions.create(
                model="gpt-4o-mini", messages=openai_msgs, temperature=1.0, response_format={"type": "json_object"}
            )
            return resp.choices[0].message.content
        except Exception as e: last_error = e

    raise last_error or Exception("All providers failed")

def repair_json(json_str):
    """
    Advanced JSON repair for LLM output.
    Handles unescaped newlines within strings, which is the #1 cause of parse errors.
    """
    if not json_str: return "{}"
    
    # 1. Fix LaTeX backslashes first (basic)
    # Replace single backslash with double, but verify it's not already escaped
    # This is tricky with regex, simpler approach:
    # We want \theta -> \\theta,    # 1. Fix LaTeX backslashes first (basic)
    # json_str = re.sub(r'(?<!\\)\\(?![\\"/bfnrtu])', r'\\\\', json_str) 

    # 1b. Fix Single Quotes on Keys (Common in weak models)
    # Replaces 'key': with "key":
    json_str = re.sub(r"'([^']+)'\s*:", r'"\1":', json_str)

    # 2. Handle Unescaped Newlines in JSON Values
    # We iterate character by character to track "inside string" state
    new_chars = []
    in_string = False
    escaped = False
    
    for c in json_str:
        if in_string:
            if c == '\\':
                escaped = not escaped
                new_chars.append(c)
            elif c == '"' and not escaped:
                in_string = False
                new_chars.append(c)
            elif c == '\n':
                # Replace literal newline inside string with \n
                new_chars.append('\\n')
                escaped = False
            elif c == '\r':
                new_chars.append('') # Ignore CR
                escaped = False
            elif c == '\t':
                new_chars.append('\\t')
                escaped = False
            else:
                new_chars.append(c)
                escaped = False
        else:
            if c == '"':
                in_string = True
            new_chars.append(c)
            
    repaired = "".join(new_chars)
    return repaired

def extract_json(text):
    """
    Robust extraction logic. 
    1. Finds the outer-most { }.
    2. Runs repair.
    """
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    start = text.find('{')
    end = text.rfind('}')
    
    if start == -1 or end == -1: return None
    
    candidate = text[start:end+1]
    return repair_json(candidate)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not (gemini_client or openrouter_client or openai_client):
            return jsonify({'chatResponse': 'Configuration Error: No AI Providers available.', 'graphCommands': []}), 500
        
        data = request.get_json()
        user_msg = data.get('message', '')
        if not user_msg: return jsonify({'chatResponse': 'Empty message', 'graphCommands': []}), 400

        # RAG
        rag_ctx = ""
        sid = data.get('sessionId', 'default')
        if sid in session_data and 'faiss_index' in session_data[sid]:
            rag_ctx = retrieve_relevant_context(sid, user_msg)
        
        # Context
        msgs = axiom_brain.build_smart_context(data.get('history', []), data.get('currentExpressions', []), rag_ctx)
        msgs.append({"role": "user", "content": user_msg})

        # Generate
        raw_text = generate_with_fallback(msgs)
        print(f"RAW AI OUT ({len(raw_text)} chars): {raw_text[:50]}...")

        # Parse
        json_str = extract_json(raw_text)
        chat_resp = ""
        graph_cmds = []

        if json_str:
            chat_resp = None
            graph_cmds = []
            
            # --- STAGE 1: Standard JSON ---
            try:
                parsed = json.loads(json_str)
                chat_resp = parsed.get('chatResponse')
                graph_cmds = parsed.get('graphCommands', [])
            except json.JSONDecodeError:
                # --- STAGE 2: Python AST (Single quotes/Trailing commas) ---
                try:
                    import ast
                    # Safety cleanup for AST
                    ast_str = json_str.replace("true", "True").replace("false", "False").replace("null", "None")
                    parsed = ast.literal_eval(ast_str)
                    if isinstance(parsed, dict):
                        chat_resp = parsed.get('chatResponse')
                        graph_cmds = parsed.get('graphCommands', [])
                except Exception:
                    # --- STAGE 3: Emergency Regex Extraction ---
                    print("⚠️ parsing failed stages 1 & 2. Attempting regex...")
                    
                    # Extract chatResponse
                    # Match "chatResponse": "..." OR 'chatResponse': '...'
                    # Non-greedy match until the next quote that is NOT escaped
                    cr_match = re.search(r'[\"\']chatResponse[\"\']\s*:\s*([\"\'])(.*?)(?<!\\)\1', json_str, re.DOTALL)
                    if cr_match:
                        # Unescape the captured string
                        raw_cr = cr_match.group(2)
                        chat_resp = raw_cr.replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
                    
                    # Emergency Command Rescue (Critical for "setBlank")
                    # If we see "setBlank" anywhere, we trigger it.
                    if "setBlank" in json_str or "clearExpressions" in json_str:
                         graph_cmds.append({"command": "setBlank"})

            # Final Fallback if chatResponse is still missing
            if chat_resp is None:
                chat_resp = raw_text # Fallback to raw text so user sees SOMETHING

        else:
            chat_resp = raw_text
            # Even in raw text, check for clear command intent
            if "setBlank" in raw_text:
                graph_cmds.append({"command": "setBlank"})

        return jsonify({'chatResponse': chat_resp, 'graphCommands': graph_cmds})

    except Exception as e:
        print(f"Endpoint Error: {e}")
        traceback.print_exc()
        return jsonify({'chatResponse': f"Error: {str(e)}", 'graphCommands': []}), 500

# --- HELPER FUNCTIONS FOR RAG (Assuming Gemini for embeddings) ---
def retrieve_relevant_context(sid, query):
    if not gemini_client: return ""
    try:
        idx = session_data[sid].get('faiss_index')
        chunks = session_data[sid].get('text_chunks')
        resp = gemini_client.models.embed_content(model="text-embedding-004", contents=query)
        vec = np.array([resp.embeddings[0].values], dtype='float32')
        _, indices = idx.search(vec, 3)
        return "\n\n".join([chunks[i] for i in indices[0] if i < len(chunks)])
    except: return ""

@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        if not PDF_SUPPORT or not FAISS_SUPPORT:
            return jsonify({'success': False, 'error': 'PDF dependencies missing.'}), 500
        
        if 'pdf' not in request.files: return jsonify({'success': False, 'error': 'No file'}), 400
        pdf_file = request.files['pdf']
        session_id = request.form.get('sessionId', 'default')
        
        if pdf_file.filename == '': return jsonify({'success': False, 'error': 'No filename'}), 400
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_file.save(tmp_file.name)
            pdf_path = tmp_file.name
        
        try:
            text_chunks = extract_text_from_pdf(pdf_path)
            if not text_chunks: return jsonify({'success': False, 'error': 'No text extracted'}), 400
            
            embeddings, chunks = create_embeddings(text_chunks)
            index = create_faiss_index(embeddings)
            
            if session_id not in session_data: session_data[session_id] = {}
            session_data[session_id]['faiss_index'] = index
            session_data[session_id]['text_chunks'] = chunks
            session_data[session_id]['pdf_name'] = pdf_file.filename
            
            return jsonify({'success': True, 'chunks': len(chunks)})
        finally:
            os.unlink(pdf_path)
    except Exception as e:
        print(f"Upload Error: {e}")
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
    if not gemini_client: raise Exception("Gemini Direct Client required for embeddings")
    embeddings = []
    valid_chunks = []
    model_name = "text-embedding-004"
    for chunk in text_chunks:
        try:
            response = gemini_client.models.embed_content(
                model=model_name,
                contents=chunk,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
            )
            if response.embeddings:
                embeddings.append(response.embeddings[0].values)
                valid_chunks.append(chunk)
        except Exception as e:
            print(f"Embedding Error: {e}")
            continue
    return np.array(embeddings, dtype='float32'), valid_chunks

def create_faiss_index(embeddings):
    if len(embeddings) == 0: raise Exception("No embeddings generated")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

if __name__ == '__main__':
    app.run(debug=True, port=5000)
