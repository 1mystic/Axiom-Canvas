from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os
import sys
import json
import tempfile
import numpy as np
from pathlib import Path
import traceback

# Load environment variables from .env file
from dotenv import load_dotenv

# Get the parent directory (FLASK-APP) to find .env and templates
parent_dir = Path(__file__).parent.parent
load_dotenv(parent_dir / '.env')

# For PDF processing (Phase 4)
try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# For RAG (Phase 4)
try:
    import faiss
    FAISS_SUPPORT = True
except ImportError:
    FAISS_SUPPORT = False

# Initialize Flask with correct template and static folders
app = Flask(__name__, 
            template_folder=str(parent_dir / 'templates'),
            static_folder=str(parent_dir / 'static'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    print(f"✓ Gemini API key loaded (starts with: {GEMINI_API_KEY[:10]}...)")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print(f"✓ Gemini model initialized: gemini-2.5-flash")
else:
    model = None
    print("❌ WARNING: GEMINI_API_KEY not set!")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   .env file location: {parent_dir / '.env'}")
    print(f"   .env file exists: {(parent_dir / '.env').exists()}")

# Print template folder info
print(f"\n📁 Flask Configuration:")
print(f"   Template folder: {app.template_folder}")
print(f"   Static folder: {app.static_folder}")
print(f"   Template folder exists: {Path(app.template_folder).exists()}")
print(f"   Static folder exists: {Path(app.static_folder).exists()}")


# Session storage for PDF embeddings (in-memory for simplicity)
# In production, consider using Redis or a database
session_data = {}

# System prompt for Gemini
SYSTEM_PROMPT = """You are Axiom Canvas, an AI-powered mathematical visualization assistant. You help users understand mathematics through both textual explanations and visual representations on a Desmos graphing calculator.

CRITICAL: You must ALWAYS respond with valid JSON in this exact format:
{
  "chatResponse": "Your natural language response to the user",
  "graphCommands": [
    {
      "command": "commandName",
      "params": { }
    }
  ]
}

Available Graph Commands:

1. setExpression - Add or update an expression
   Example: {"command": "setExpression", "params": {"id": "expr1", "latex": "y=x^2", "color": "#2563eb"}}
   
   Optional params:
   - color: hex color (e.g., "#2563eb", "#dc2626")
   - lineStyle: "SOLID", "DASHED", "DOTTED"
   - lineWidth: number (default 2.5)
   - lineOpacity: number 0-1
   - pointStyle: "POINT", "OPEN", "CROSS"
   - fillOpacity: number 0-1 (for inequalities)
   - hidden: boolean

2. removeExpression - Remove an expression by ID
   Example: {"command": "removeExpression", "params": {"id": "expr1"}}

3. setMathBounds - Set the viewport bounds
   Example: {"command": "setMathBounds", "params": {"left": -10, "right": 10, "bottom": -10, "top": 10}}

4. clearExpressions - Clear all expressions from the graph
   Example: {"command": "clearExpressions", "params": {}}

5. setBlank - Reset the calculator to blank state
   Example: {"command": "setBlank", "params": {}}

CRITICAL DESMOS SYNTAX RULES:
- Functions MUST be in form "y=..." or "x=..." (equations, not bare expressions)
- For points, use ONLY coordinates: "(2, 3)" NOT "A=(2,3)"
- For parametric/vector plots, use proper Desmos syntax
- NO arrow notation (->), use standard function notation
- NO \vec{} or vector notation in latex field - only in chatResponse
- Use simple variable names (x, y, t, theta) not A, B, R
- Expressions must be valid Desmos calculator syntax
- Use DESCRIPTIVE IDs that describe the expression (e.g., "parabola_x2", "line_y2x", "circle_r5")
- Remember IDs you create so you can remove specific expressions later
- When user asks to clear a specific graph, use removeExpression with that ID

CORRECT Desmos Examples:
✓ "y=x^2"                    (function)
✓ "(2, 3)"                   (point)
✓ "y=2x+1"                   (linear function)
✓ "y=\\sin(x)"               (trig function)
✓ "x^2+y^2=25"               (circle equation)
✓ "y=\\sqrt{x}"              (square root)
✓ "(t, t^2)"                 (parametric - automatic)

INCORRECT Desmos Examples (DO NOT USE):
✗ "A \\to (2,3)"             (arrow notation not allowed)
✗ "\\vec{A}=2\\vec{i}+3\\vec{j}"  (vector notation not allowed in latex)
✗ "A=(2,3)"                  (named points - just use coordinates)
✗ "f(x)=x^2" without y=      (use "y=x^2" instead)
✗ "x^2" alone                (must be equation: "y=x^2")

For VECTORS specifically:
- Plot as SEPARATE points and lines, NOT vector notation
- Vector from origin to (2,3): Use TWO expressions:
  1. Point: {"latex": "(2,3)", "color": "#2563eb"}
  2. Line: {"latex": "y=\\frac{3}{2}x\\left\\{0\\le x\\le2\\right\\}", "color": "#2563eb"}
- Or use parametric: {"latex": "(2t, 3t)\\left\\{0\\le t\\le1\\right\\}"}

Guidelines:
- Use descriptive IDs for expressions (e.g., "parabola1", "tangent_line", "vertex_point")
- Use different colors to distinguish different expressions
- When plotting multiple related expressions, use consistent color schemes
- For points, use pointStyle: "POINT" and provide coordinates like "(2, 4)"
- Always provide clear, educational explanations in chatResponse
- If asked to explain a concept, use the graph to illustrate it
- When showing derivatives, plot both the function and tangent lines
- For intersections, mark the points clearly
- You can use LaTeX in chatResponse for math formatting (like $\\vec{A}$)
- But latex field in graphCommands must be valid Desmos syntax only

Examples:

User: "plot y = x^2 - 3"
Response:
{
  "chatResponse": "I've plotted the parabola y = x² - 3. Notice that the vertex is at (0, -3) and the parabola opens upward.",
  "graphCommands": [
    {"command": "setExpression", "params": {"id": "parabola", "latex": "y=x^2-3", "color": "#2563eb"}}
  ]
}

User: "show vector from origin to (3,4)"
Response:
{
  "chatResponse": "I've plotted a vector from the origin to the point (3, 4). The vector is shown as a blue arrow.",
  "graphCommands": [
    {"command": "setExpression", "params": {"id": "vec_line", "latex": "y=\\frac{4}{3}x\\left\\{0\\le x\\le3\\right\\}", "color": "#2563eb"}},
    {"command": "setExpression", "params": {"id": "vec_point", "latex": "(3,4)", "color": "#2563eb", "pointStyle": "POINT"}}
  ]
}

User: "explain the derivative of sin(x)"
Response:
{
  "chatResponse": "The derivative of sin(x) is cos(x). Let me show you visually: I've plotted sin(x) in blue and its derivative cos(x) in red. Notice how the slope of sin(x) at any point matches the value of cos(x) at that point. For example, at x=0, sin(x) has a slope of 1, and cos(0)=1.",
  "graphCommands": [
    {"command": "setExpression", "params": {"id": "sinx", "latex": "y=\\sin(x)", "color": "#2563eb"}},
    {"command": "setExpression", "params": {"id": "cosx", "latex": "y=\\cos(x)", "color": "#dc2626", "lineStyle": "DASHED"}}
  ]
}

User: "clear the graph"
Response:
{
  "chatResponse": "I've cleared the graph. What would you like to explore next?",
  "graphCommands": [
    {"command": "clearExpressions", "params": {}}
  ]
}

User: "remove the parabola" or "clear the x^2 graph"
Response:
{
  "chatResponse": "I've removed the parabola from the graph.",
  "graphCommands": [
    {"command": "removeExpression", "params": {"id": "parabola"}}
  ]
}

User: "keep the parabola but remove the sine wave"
Response:
{
  "chatResponse": "I've removed the sine function while keeping the parabola.",
  "graphCommands": [
    {"command": "removeExpression", "params": {"id": "sinx"}}
  ]
}

Remember: ALWAYS return valid JSON. NEVER return plain text without the JSON structure.
When a user asks to clear/remove a specific graph, use the removeExpression command with the ID you originally assigned to that expression.
"""


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI responses with graph commands"""
    try:
        if not model:
            return jsonify({
                'chatResponse': 'Error: Gemini API key not configured. Please set GEMINI_API_KEY environment variable.',
                'graphCommands': []
            }), 500
        
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('sessionId', 'default')
        history = data.get('history', [])
        current_expressions = data.get('currentExpressions', [])
        
        if not user_message:
            return jsonify({
                'chatResponse': 'Please provide a message.',
                'graphCommands': []
            }), 400
        
        # Build conversation context
        conversation_context = []
        
        # Add system prompt
        conversation_context.append({
            'role': 'user',
            'parts': [SYSTEM_PROMPT]
        })
        conversation_context.append({
            'role': 'model',
            'parts': ['I understand. I will always respond with valid JSON containing chatResponse and graphCommands.']
        })
        
        # Add current graph state if expressions exist
        if current_expressions:
            expr_list = "\n".join([f"- ID: '{expr['id']}', Expression: {expr['latex']}" for expr in current_expressions])
            conversation_context.append({
                'role': 'user',
                'parts': [f"Current expressions on the graph:\n{expr_list}"]
            })
            conversation_context.append({
                'role': 'model',
                'parts': ['I can see the current graph state. I will use these IDs when removing or modifying expressions.']
            })
        
        # Check if we have RAG context for this session
        rag_context = ""
        if session_id in session_data and 'faiss_index' in session_data[session_id]:
            try:
                rag_context = retrieve_relevant_context(session_id, user_message)
                if rag_context:
                    conversation_context.append({
                        'role': 'user',
                        'parts': [f"Context from uploaded PDF:\n\n{rag_context}"]
                    })
                    conversation_context.append({
                        'role': 'model',
                        'parts': ['I will use this context to answer questions.']
                    })
            except Exception as e:
                print(f"Error retrieving RAG context: {e}")
        
        # Add recent conversation history (last 5 exchanges)
        for msg in history[-10:]:
            role = 'user' if msg['role'] == 'user' else 'model'
            conversation_context.append({
                'role': role,
                'parts': [msg['content']]
            })
        
        # Add current user message
        conversation_context.append({
            'role': 'user',
            'parts': [user_message]
        })
        
        # Generate response
        chat_session = model.start_chat(history=conversation_context[:-1])
        response = chat_session.send_message(user_message)
        
        # Parse the response
        response_text = response.text.strip()
        
        print(f"\n=== RAW AI RESPONSE ===")
        print(response_text[:500])  # Print first 500 chars
        print(f"======================\n")
        
        # Try to extract JSON from the response
        # Sometimes the model wraps JSON in markdown code blocks
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # Try to find JSON object if the response contains other text
        if response_text.startswith('{'):
            # Already looks like JSON
            pass
        elif '{' in response_text:
            # Extract JSON from mixed content
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            response_text = response_text[json_start:json_end]
        
        print(f"\n=== EXTRACTED JSON ===")
        print(response_text[:500])  # Print first 500 chars
        print(f"======================\n")
        
        # Parse JSON - try with fixing common LaTeX escape issues
        try:
            parsed_response = json.loads(response_text)
            chat_response = parsed_response.get('chatResponse', '')
            graph_commands = parsed_response.get('graphCommands', [])
            
            print(f"\n=== PARSED SUCCESSFULLY ===")
            print(f"Chat response length: {len(chat_response)}")
            print(f"Graph commands count: {len(graph_commands)}")
            print(f"===========================\n")
            
        except json.JSONDecodeError as e:
            print(f"\n=== JSON PARSE ERROR (trying fix) ===")
            print(f"Error: {e}")
            
            # Try to fix LaTeX backslash escaping issues
            # The AI sometimes generates single backslashes in LaTeX which need to be doubled for valid JSON
            try:
                # Simple approach: escape all backslashes
                # In valid JSON, all backslashes should already be escaped, so single backslashes are errors
                fixed_text = response_text.replace('\\', '\\\\')
                
                print(f"Attempting to parse with escaped backslashes...")
                parsed_response = json.loads(fixed_text)
                chat_response = parsed_response.get('chatResponse', '')
                graph_commands = parsed_response.get('graphCommands', [])
                
                print(f"\n=== PARSED WITH FIX ===")
                print(f"Chat response length: {len(chat_response)}")
                print(f"Graph commands count: {len(graph_commands)}")
                print(f"=======================\n")
                
            except Exception as fix_error:
                print(f"Fix also failed: {fix_error}")
                print(f"========================================\n")
                # Last resort: return as text
                chat_response = response_text
                graph_commands = []
        
        return jsonify({
            'chatResponse': chat_response,
            'graphCommands': graph_commands
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return jsonify({
            'chatResponse': f'An error occurred: {str(e)}',
            'graphCommands': []
        }), 500


@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and process it for RAG"""
    try:
        if not PDF_SUPPORT:
            return jsonify({
                'success': False,
                'error': 'PDF processing not available. PyMuPDF not installed.'
            }), 500
        
        if not FAISS_SUPPORT:
            return jsonify({
                'success': False,
                'error': 'Vector search not available. FAISS not installed.'
            }), 500
        
        if 'pdf' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No PDF file provided'
            }), 400
        
        pdf_file = request.files['pdf']
        session_id = request.form.get('sessionId', 'default')
        
        if pdf_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Save PDF to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_file.save(tmp_file.name)
            pdf_path = tmp_file.name
        
        try:
            # Extract text from PDF
            text_chunks = extract_text_from_pdf(pdf_path)
            
            if not text_chunks:
                return jsonify({
                    'success': False,
                    'error': 'No text extracted from PDF'
                }), 400
            
            # Generate embeddings and create FAISS index
            embeddings, chunks = create_embeddings(text_chunks)
            index = create_faiss_index(embeddings)
            
            # Store in session data
            if session_id not in session_data:
                session_data[session_id] = {}
            
            session_data[session_id]['faiss_index'] = index
            session_data[session_id]['text_chunks'] = chunks
            session_data[session_id]['pdf_name'] = pdf_file.filename
            
            return jsonify({
                'success': True,
                'message': f'Successfully processed {len(chunks)} text chunks',
                'chunks': len(chunks)
            })
            
        finally:
            # Clean up temporary file
            os.unlink(pdf_path)
        
    except Exception as e:
        print(f"Error in upload_pdf endpoint: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def extract_text_from_pdf(pdf_path, chunk_size=1000, overlap=200):
    """Extract text from PDF and split into chunks"""
    doc = fitz.open(pdf_path)
    chunks = []
    
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    # Split into chunks with overlap
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks


def create_embeddings(text_chunks):
    """Generate embeddings using Gemini"""
    if not model:
        raise Exception("Gemini API not configured")
    
    embeddings = []
    valid_chunks = []
    
    for chunk in text_chunks:
        try:
            # Use Gemini's embedding model
            result = genai.embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])
            valid_chunks.append(chunk)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            continue
    
    return np.array(embeddings, dtype='float32'), valid_chunks


def create_faiss_index(embeddings):
    """Create FAISS index from embeddings"""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def retrieve_relevant_context(session_id, query, top_k=3):
    """Retrieve relevant text chunks using FAISS"""
    if session_id not in session_data:
        return ""
    
    index = session_data[session_id].get('faiss_index')
    chunks = session_data[session_id].get('text_chunks')
    
    if not index or not chunks:
        return ""
    
    # Generate embedding for query
    result = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query"
    )
    query_embedding = np.array([result['embedding']], dtype='float32')
    
    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)
    
    # Retrieve relevant chunks
    relevant_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]
    
    return "\n\n".join(relevant_chunks)


# For Vercel serverless deployment
# Vercel will look for 'app' variable
if __name__ == '__main__':
    app.run(debug=True, port=5000)
