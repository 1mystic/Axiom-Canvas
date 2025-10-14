# Axiom Canvas - Complete Implementation Guide

## Overview
This document provides a comprehensive guide for understanding and extending the Axiom Canvas AI Math Visualizer application.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Component Breakdown](#component-breakdown)
3. [AI System Prompt Design](#ai-system-prompt-design)
4. [Graph Command System](#graph-command-system)
5. [RAG Implementation](#rag-implementation)
6. [Deployment Guide](#deployment-guide)
7. [Testing Guide](#testing-guide)
8. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### High-Level Architecture
```
┌─────────────────┐         ┌──────────────────┐
│   User Browser  │         │  Vercel Platform │
│                 │         │                  │
│ ┌─────────────┐ │         │ ┌──────────────┐ │
│ │  Desmos API │ │         │ │ Flask Backend│ │
│ │  (Left)     │ │         │ │ (Serverless) │ │
│ └─────────────┘ │  HTTP   │ └──────────────┘ │
│                 │◄────────►│        │         │
│ ┌─────────────┐ │         │        │         │
│ │  Chat UI    │ │         │        ▼         │
│ │  (Right)    │ │         │ ┌──────────────┐ │
│ └─────────────┘ │         │ │  Gemini API  │ │
│                 │         │ └──────────────┘ │
└─────────────────┘         └──────────────────┘
```

### Request Flow

1. **User Input**: User types message in chat
2. **Frontend**: JavaScript captures input, sends POST to `/api/chat`
3. **Backend**: Flask receives request, forwards to Gemini API
4. **AI Processing**: Gemini generates structured JSON response
5. **Backend**: Parses JSON, returns to frontend
6. **Frontend**: Displays chat response and executes graph commands
7. **Graph Update**: Desmos API updates visualization

---

## Component Breakdown

### Frontend Components

#### 1. HTML Structure (`templates/index.html`)

**Key Elements:**
- `#calculator`: Container for Desmos graph
- `#chat-panel`: Container for chat interface
- `#chat-messages`: Scrollable message display
- `#chat-input`: User input textarea
- `#pdf-upload`: Hidden file input for PDFs

**Design Decisions:**
- Semantic HTML for accessibility
- Flexbox layout for responsive design
- Inline SVG icons to avoid external dependencies
- Script tags load Desmos API and custom JS

#### 2. Styling (`static/style.css`)

**CSS Variables:**
```css
:root {
    --primary-color: #2563eb;
    --panel-bg: #ffffff;
    --border-color: #e2e8f0;
    /* ... more variables */
}
```

**Key Features:**
- 50/50 split screen layout
- Smooth animations for messages
- Custom scrollbar styling
- Responsive breakpoints at 1024px and 768px
- Gradient headers for visual appeal

**Color Scheme:**
- Primary Blue (#2563eb): User messages, buttons
- Purple (#8b5cf6): AI avatar
- Light Gray (#f8fafc): Backgrounds, inputs
- Red (#dc2626): Errors

#### 3. JavaScript Logic (`static/main.js`)

**Global State:**
```javascript
let calculator;              // Desmos calculator instance
let sessionId;               // Unique session identifier
let conversationHistory = []; // Chat history array
```

**Key Functions:**

**`initializeCalculator()`**
- Creates Desmos GraphingCalculator instance
- Sets default viewport (-10 to 10 on both axes)
- Configures calculator options (keypad, zoom, etc.)

**`addMessage(text, type)`**
- Creates message DOM elements
- Adds avatar and content
- Animates message appearance
- Auto-scrolls to latest message

**`sendMessage()`**
- Captures user input
- Displays user message
- Makes fetch POST to `/api/chat`
- Handles loading state
- Processes AI response
- Executes graph commands

**`executeGraphCommands(commands)`**
- Iterates through command array
- Switch statement for command types
- Calls appropriate Desmos API methods
- Error handling for invalid commands

**`handlePdfUpload(file)`**
- Creates FormData with PDF file
- POSTs to `/api/upload_pdf`
- Updates upload status UI
- Displays success/error messages

**Event Listeners:**
- DOMContentLoaded: Initialize calculator
- Send button click: Send message
- Enter key (not Shift+Enter): Send message
- Input event: Auto-resize textarea
- Upload button: Trigger file input

### Backend Components

#### 1. Flask Application (`api/index.py`)

**Configuration:**
```python
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Gemini API setup
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
```

**Session Storage:**
```python
session_data = {
    'session_123': {
        'faiss_index': <FAISS index object>,
        'text_chunks': ['chunk1', 'chunk2', ...],
        'pdf_name': 'textbook.pdf'
    }
}
```

**Routes:**

**`GET /`**
- Renders `index.html` using Jinja2
- Simple route, no complex logic

**`POST /api/chat`**
- Receives: `{ message, sessionId, history }`
- Builds conversation context
- Checks for RAG context
- Calls Gemini API
- Parses JSON response
- Returns: `{ chatResponse, graphCommands }`

**`POST /api/upload_pdf`**
- Receives: FormData with PDF file
- Extracts text using PyMuPDF
- Chunks text (1000 chars, 200 overlap)
- Generates embeddings via Gemini
- Creates FAISS index
- Stores in session_data
- Returns: `{ success, message, chunks }`

**Helper Functions:**

**`extract_text_from_pdf(pdf_path, chunk_size, overlap)`**
```python
def extract_text_from_pdf(pdf_path, chunk_size=1000, overlap=200):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    chunks = []
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks
```

**`create_embeddings(text_chunks)`**
- Uses Gemini's `embedding-001` model
- Task type: `retrieval_document`
- Returns numpy array of embeddings

**`create_faiss_index(embeddings)`**
- Uses `IndexFlatL2` (L2 distance)
- Dimension based on embedding size (typically 768)
- Simple but effective for small datasets

**`retrieve_relevant_context(session_id, query, top_k=3)`**
- Embeds query with task type `retrieval_query`
- Searches FAISS index
- Returns top_k most similar chunks
- Joins chunks with double newlines

---

## AI System Prompt Design

### Prompt Structure

The system prompt is critical for reliable graph control. It has three main sections:

#### 1. Role Definition
```
You are Axiom Canvas, an AI-powered mathematical visualization assistant.
You help users understand mathematics through both textual explanations 
and visual representations on a Desmos graphing calculator.
```

#### 2. Output Format Specification
```
CRITICAL: You must ALWAYS respond with valid JSON in this exact format:
{
  "chatResponse": "Your natural language response",
  "graphCommands": [ {...} ]
}
```

#### 3. Command Reference
Detailed documentation of all available commands with examples.

### Why This Approach Works

**Structured Output:**
- Forces consistent JSON format
- Separates text from commands
- Easy to parse in frontend

**Clear Examples:**
- Shows exact syntax for each command
- Demonstrates color usage
- Illustrates multi-command responses

**Educational Guidelines:**
- Emphasizes visual explanations
- Encourages multiple expressions
- Promotes color-coded graphs

### Handling Gemini's Response

Sometimes Gemini wraps JSON in markdown:
````
```json
{
  "chatResponse": "...",
  "graphCommands": [...]
}
```
````

Our parsing handles this:
```python
if '```json' in response_text:
    json_start = response_text.find('```json') + 7
    json_end = response_text.find('```', json_start)
    response_text = response_text[json_start:json_end].strip()
```

---

## Graph Command System

### Command Types

#### setExpression
**Purpose:** Add or update a mathematical expression

**Parameters:**
- `id` (required): Unique identifier
- `latex` (required): Mathematical expression in LaTeX
- `color` (optional): Hex color code
- `lineStyle` (optional): "SOLID", "DASHED", "DOTTED"
- `lineWidth` (optional): Number (default 2.5)
- `lineOpacity` (optional): 0-1
- `pointStyle` (optional): "POINT", "OPEN", "CROSS"
- `fillOpacity` (optional): For inequalities
- `hidden` (optional): Boolean

**Examples:**
```javascript
// Simple function
{
  "command": "setExpression",
  "params": {
    "id": "f1",
    "latex": "y=x^2"
  }
}

// Styled function
{
  "command": "setExpression",
  "params": {
    "id": "sine",
    "latex": "y=\\sin(x)",
    "color": "#2563eb",
    "lineStyle": "DASHED",
    "lineWidth": 3
  }
}

// Point
{
  "command": "setExpression",
  "params": {
    "id": "vertex",
    "latex": "(0, 0)",
    "color": "#dc2626",
    "pointStyle": "POINT"
  }
}
```

#### removeExpression
**Purpose:** Remove an expression from the graph

```javascript
{
  "command": "removeExpression",
  "params": {
    "id": "f1"
  }
}
```

#### setMathBounds
**Purpose:** Change the viewport

```javascript
{
  "command": "setMathBounds",
  "params": {
    "left": -5,
    "right": 5,
    "bottom": -3,
    "top": 3
  }
}
```

#### clearExpressions
**Purpose:** Remove all expressions

```javascript
{
  "command": "clearExpressions",
  "params": {}
}
```

#### setBlank
**Purpose:** Reset calculator to blank state

```javascript
{
  "command": "setBlank",
  "params": {}
}
```

### Frontend Execution

```javascript
function executeGraphCommands(commands) {
    commands.forEach(cmd => {
        switch (cmd.command) {
            case 'setExpression':
                calculator.setExpression(cmd.params);
                break;
            case 'removeExpression':
                calculator.removeExpression(cmd.params);
                break;
            case 'setMathBounds':
                calculator.setMathBounds(cmd.params);
                break;
            case 'clearExpressions':
                const state = calculator.getState();
                state.expressions.list.forEach(expr => {
                    calculator.removeExpression({ id: expr.id });
                });
                break;
            case 'setBlank':
                calculator.setBlank();
                break;
        }
    });
}
```

---

## RAG Implementation

### Overview

RAG (Retrieval-Augmented Generation) allows the AI to answer questions based on uploaded PDF content.

### Pipeline Steps

#### 1. PDF Upload & Text Extraction
```python
def extract_text_from_pdf(pdf_path, chunk_size=1000, overlap=200):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    # Sliding window chunking
    chunks = []
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks
```

**Why chunk_size=1000?**
- Balances context vs. granularity
- Fits well within Gemini's context window
- Overlap ensures continuity

#### 2. Embedding Generation
```python
def create_embeddings(text_chunks):
    embeddings = []
    valid_chunks = []
    
    for chunk in text_chunks:
        result = genai.embed_content(
            model="models/embedding-001",
            content=chunk,
            task_type="retrieval_document"
        )
        embeddings.append(result['embedding'])
        valid_chunks.append(chunk)
    
    return np.array(embeddings, dtype='float32'), valid_chunks
```

**Gemini Embedding Model:**
- Model: `embedding-001`
- Dimension: 768
- Task types: `retrieval_document`, `retrieval_query`

#### 3. FAISS Index Creation
```python
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]  # 768 for embedding-001
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index
```

**Why IndexFlatL2?**
- Simple and accurate
- Good for small datasets (<10,000 chunks)
- L2 distance works well for normalized embeddings

#### 4. Query-Time Retrieval
```python
def retrieve_relevant_context(session_id, query, top_k=3):
    # Get stored index and chunks
    index = session_data[session_id]['faiss_index']
    chunks = session_data[session_id]['text_chunks']
    
    # Embed query
    result = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query"
    )
    query_embedding = np.array([result['embedding']], dtype='float32')
    
    # Search
    distances, indices = index.search(query_embedding, top_k)
    
    # Retrieve chunks
    relevant_chunks = [chunks[i] for i in indices[0]]
    return "\n\n".join(relevant_chunks)
```

#### 5. Context Integration
```python
# In /api/chat endpoint
if session_id in session_data and 'faiss_index' in session_data[session_id]:
    rag_context = retrieve_relevant_context(session_id, user_message)
    if rag_context:
        conversation_context.append({
            'role': 'user',
            'parts': [f"Context from uploaded PDF:\n\n{rag_context}"]
        })
```

### RAG Best Practices

**Chunking Strategies:**
- **Fixed-size**: Simple, consistent (current approach)
- **Sentence-based**: More semantic, requires NLP
- **Paragraph-based**: Good for well-structured documents

**Overlap Benefits:**
- Prevents context loss at boundaries
- 20% overlap (200/1000) is a good default
- Can increase for dense technical content

**Top-k Selection:**
- Start with k=3
- Increase if answers lack detail
- Decrease if getting irrelevant context

---

## Deployment Guide

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your_key"
   $env:FLASK_SECRET_KEY="random_secret"
   
   # Linux/Mac
   export GEMINI_API_KEY="your_key"
   export FLASK_SECRET_KEY="random_secret"
   ```

3. **Run Flask**
   ```bash
   cd api
   python index.py
   ```

4. **Access**
   Open http://localhost:5000

### Vercel Deployment

#### Method 1: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Add secrets
vercel env add GEMINI_API_KEY
vercel env add FLASK_SECRET_KEY

# Deploy
cd FLASK-APP
vercel --prod
```

#### Method 2: GitHub Integration

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure:
   - Root Directory: `FLASK-APP`
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. Add Environment Variables
5. Deploy

### Environment Variables

**Required:**
- `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- `FLASK_SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`

**Optional:**
- `FLASK_ENV`: Set to `production` (default)
- `MAX_CONTENT_LENGTH`: Max file upload size in bytes

### Vercel Configuration

**vercel.json breakdown:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {"maxLambdaSize": "15mb"}
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

- `@vercel/python`: Uses Python runtime
- `maxLambdaSize`: Allows larger packages (FAISS, PyMuPDF)
- Routes: Static files served directly, everything else to Flask

---

## Testing Guide

### Manual Testing Checklist

**Basic Functionality:**
- [ ] Page loads without errors
- [ ] Desmos calculator renders
- [ ] Chat input accepts text
- [ ] Send button works
- [ ] Welcome message appears

**Plotting:**
- [ ] Simple function: "plot y = x^2"
- [ ] Styled function: "plot y = sin(x) in red"
- [ ] Multiple functions: "plot y = x, y = x^2, y = x^3"
- [ ] Clear graph: "clear the graph"

**Math Concepts:**
- [ ] Derivatives: "explain the derivative of x^2"
- [ ] Trigonometry: "show me sin(x) and cos(x)"
- [ ] Intersection: "find where y=x^2 and y=2x+1 intersect"

**PDF Upload:**
- [ ] Upload button clickable
- [ ] PDF uploads successfully
- [ ] Status message appears
- [ ] Can ask questions about PDF content

**Edge Cases:**
- [ ] Empty message (should not send)
- [ ] Very long message
- [ ] Invalid LaTeX from AI (should error gracefully)
- [ ] Network error during chat
- [ ] Large PDF file

### Automated Testing

Create `tests/test_backend.py`:
```python
import pytest
from api.index import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Axiom Canvas' in response.data

def test_chat_endpoint(client):
    response = client.post('/api/chat', json={
        'message': 'plot y=x^2',
        'sessionId': 'test',
        'history': []
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'chatResponse' in data
    assert 'graphCommands' in data
```

Run tests:
```bash
pytest tests/
```

---

## Troubleshooting

### Common Issues

#### 1. "GEMINI_API_KEY not set"
**Symptom:** Error message in chat or backend logs

**Solution:**
```bash
# Check if set
echo $env:GEMINI_API_KEY  # Windows
echo $GEMINI_API_KEY      # Linux/Mac

# Set it
$env:GEMINI_API_KEY="your_key"  # Windows
export GEMINI_API_KEY="your_key"  # Linux/Mac
```

#### 2. Desmos Not Loading
**Symptom:** Blank left panel

**Solutions:**
- Check browser console for errors
- Verify Desmos API script tag in HTML
- Check network tab for failed requests
- Try different browser

#### 3. AI Returns Plain Text
**Symptom:** No graph commands, only text response

**Diagnosis:**
- Check backend logs for JSON parsing errors
- AI might have ignored JSON format instruction

**Solution:**
- Improve system prompt emphasis
- Add more examples to prompt
- Try different Gemini model (gemini-1.5-pro)

#### 4. PDF Upload Fails
**Symptom:** Upload error message

**Possible Causes:**
- File too large (>15MB on Vercel)
- PyMuPDF not installed
- FAISS not installed
- Insufficient memory

**Solutions:**
```bash
# Verify dependencies
pip list | grep -i pymupdf
pip list | grep -i faiss

# Reinstall
pip install --upgrade PyMuPDF faiss-cpu
```

#### 5. Vercel Deployment Fails
**Symptom:** Build or runtime errors

**Common Errors:**

**"Module not found"**
```bash
# Check requirements.txt
# Ensure all dependencies listed
# Try specifying versions
```

**"Function timeout"**
- PDF processing too slow
- Reduce chunk size or file size
- Use async processing

**"Memory exceeded"**
- FAISS index too large
- Reduce number of chunks
- Use FAISS compression

### Debug Mode

Enable Flask debug mode locally:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Check browser console:
```javascript
// In main.js
console.log('Sending message:', message);
console.log('AI response:', data);
console.log('Executing commands:', commands);
```

### Performance Optimization

**Frontend:**
- Debounce textarea input
- Lazy load messages
- Virtual scrolling for long conversations

**Backend:**
- Cache Gemini responses
- Batch PDF chunk processing
- Use Redis for session storage

**Deployment:**
- Enable Vercel Edge Network
- Compress static assets
- Use CDN for Desmos API

---

## Extension Ideas

### 1. Save/Load Graph States
```javascript
// Save state
const state = calculator.getState();
localStorage.setItem('graph_state', JSON.stringify(state));

// Load state
const state = JSON.parse(localStorage.getItem('graph_state'));
calculator.setState(state);
```

### 2. Export Graph as Image
```javascript
calculator.screenshot(function(data) {
    const link = document.createElement('a');
    link.download = 'graph.png';
    link.href = data;
    link.click();
});
```

### 3. Multiple AI Models
```python
# Add model selection
model_choice = request.json.get('model', 'gemini')

if model_choice == 'claude':
    # Use Claude API
elif model_choice == 'gpt4':
    # Use OpenAI API
```

### 4. Collaborative Sessions
- Use WebSockets for real-time updates
- Share session IDs between users
- Sync graph states across browsers

### 5. Voice Input
```javascript
// Web Speech API
const recognition = new webkitSpeechRecognition();
recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chat-input').value = transcript;
};
```

---

## Security Considerations

### API Key Protection
- Never commit `.env` to Git
- Use Vercel environment variables
- Rotate keys periodically

### Input Validation
```python
# Validate file uploads
if not file.filename.endswith('.pdf'):
    return error_response('Invalid file type')

# Limit file size
if file.content_length > 15 * 1024 * 1024:  # 15MB
    return error_response('File too large')
```

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("60 per minute")
def chat():
    # ...
```

### XSS Prevention
- Sanitize user input displayed in chat
- Use textContent instead of innerHTML
- Escape LaTeX expressions

---

## Conclusion

Axiom Canvas demonstrates how to build a powerful AI-powered educational tool using modern web technologies and serverless architecture. The combination of natural language processing, mathematical visualization, and document understanding creates a unique learning experience.

Key takeaways:
- Structured AI prompts enable reliable command generation
- Desmos API provides professional graphing capabilities
- RAG with FAISS enables document-aware responses
- Vercel serverless functions simplify deployment
- Clean separation of concerns makes the code maintainable

Happy coding and math exploring! 🚀📊🧮
