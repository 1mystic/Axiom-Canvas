# Axiom Canvas - Architecture Diagrams

This document contains ASCII diagrams and visual representations of the system architecture.

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Request Flow](#request-flow)
3. [RAG Pipeline](#rag-pipeline)
4. [Component Interaction](#component-interaction)
5. [Deployment Architecture](#deployment-architecture)

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                                   │
│                                                                          │
│  ┌────────────────────────────────┬─────────────────────────────────┐   │
│  │     LEFT PANEL                 │      RIGHT PANEL                │   │
│  │  ┌──────────────────────────┐  │  ┌──────────────────────────┐   │   │
│  │  │                          │  │  │  Chat Header             │   │   │
│  │  │   DESMOS CALCULATOR      │  │  │  - Axiom Canvas          │   │   │
│  │  │                          │  │  └──────────────────────────┘   │   │
│  │  │   ┌────────────────┐     │  │  ┌──────────────────────────┐   │   │
│  │  │   │  Graph Canvas  │     │  │  │  PDF Upload Section      │   │   │
│  │  │   │                │     │  │  └──────────────────────────┘   │   │
│  │  │   │  y = x²        │     │  │  ┌──────────────────────────┐   │   │
│  │  │   │                │     │  │  │  Chat Messages           │   │   │
│  │  │   │     /\         │     │  │  │  ┌────────────────────┐  │   │   │
│  │  │   │    /  \        │     │  │  │  │ User: plot y=x²    │  │   │   │
│  │  │   │   /    \       │     │  │  │  └────────────────────┘  │   │   │
│  │  │   │  /      \      │     │  │  │  ┌────────────────────┐  │   │   │
│  │  │   └────────────────┘     │  │  │  │ AI: I've plotted.. │  │   │   │
│  │  │                          │  │  │  └────────────────────┘  │   │   │
│  │  │   Controls & Tools       │  │  │  (Scrollable)            │   │   │
│  │  │                          │  │  └──────────────────────────┘   │   │
│  │  └──────────────────────────┘  │  ┌──────────────────────────┐   │   │
│  │                                 │  │  Chat Input              │   │   │
│  │  Powered by Desmos API v1.7     │  │  [Send Button]           │   │   │
│  │                                 │  └──────────────────────────┘   │   │
│  └────────────────────────────────┴─────────────────────────────────┘   │
│                                                                          │
│  Technologies: HTML5, CSS3, Vanilla JavaScript                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        VERCEL PLATFORM                                   │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │           FLASK SERVERLESS FUNCTION (api/index.py)                 │ │
│  │                                                                    │ │
│  │  Routes:                                                           │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │ │
│  │  │ GET /        │  │ POST         │  │ POST                 │    │ │
│  │  │ Serve HTML   │  │ /api/chat    │  │ /api/upload_pdf      │    │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘    │ │
│  │                                                                    │ │
│  │  Session Storage (In-Memory):                                     │ │
│  │  ┌────────────────────────────────────────────────────────┐       │ │
│  │  │ session_data = {                                       │       │ │
│  │  │   'session_123': {                                     │       │ │
│  │  │     'faiss_index': <index>,                            │       │ │
│  │  │     'text_chunks': [...],                              │       │ │
│  │  │     'pdf_name': 'textbook.pdf'                         │       │ │
│  │  │   }                                                     │       │ │
│  │  │ }                                                       │       │ │
│  │  └────────────────────────────────────────────────────────┘       │ │
│  │                                                                    │ │
│  │  Libraries: Flask, PyMuPDF, FAISS, NumPy                          │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│                                    │ API Calls                           │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    EXTERNAL: Google Gemini API                     │ │
│  │                                                                    │ │
│  │  Models Used:                                                      │ │
│  │  • gemini-1.5-flash (Chat & Generation)                           │ │
│  │  • embedding-001 (Text Embeddings)                                │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Request Flow

### Chat Message Flow

```
┌─────────────┐
│    USER     │
│ Types msg   │
└──────┬──────┘
       │
       │ 1. User types "plot y = x^2" and clicks Send
       ▼
┌──────────────────────┐
│  Frontend (main.js)  │
│                      │
│  • Capture input     │
│  • Display user msg  │
│  • Show loading      │
└──────┬───────────────┘
       │
       │ 2. POST /api/chat
       │    {message, sessionId, history}
       ▼
┌──────────────────────────────────────┐
│  Flask Backend (api/index.py)        │
│                                      │
│  3. Receive request                  │
│     ↓                                │
│  4. Check for RAG context?           │
│     ├─ Yes → Retrieve from FAISS     │
│     └─ No → Continue                 │
│     ↓                                │
│  5. Build conversation context       │
│     • System prompt                  │
│     • RAG context (if any)           │
│     • History                        │
│     • Current message                │
└──────┬───────────────────────────────┘
       │
       │ 6. API call with context
       ▼
┌─────────────────────┐
│   Gemini API        │
│                     │
│  • Process prompt   │
│  • Generate JSON    │
└──────┬──────────────┘
       │
       │ 7. Return JSON response
       │    {chatResponse, graphCommands}
       ▼
┌──────────────────────────────────────┐
│  Flask Backend                       │
│                                      │
│  8. Parse JSON                       │
│     • Extract chatResponse           │
│     • Extract graphCommands          │
│     • Handle markdown wrapping       │
└──────┬───────────────────────────────┘
       │
       │ 9. Return to frontend
       │    {chatResponse, graphCommands}
       ▼
┌──────────────────────────────────────┐
│  Frontend (main.js)                  │
│                                      │
│  10. Process response                │
│      ↓                               │
│  11. Display chat message            │
│      ↓                               │
│  12. Execute graph commands          │
│      • Parse commands array          │
│      • Call Desmos API methods       │
│      ↓                               │
│  13. Hide loading                    │
└──────┬───────────────────────────────┘
       │
       │ 14. Graph updated!
       ▼
┌─────────────────────┐
│  Desmos Calculator  │
│                     │
│  y = x² displayed   │
└─────────────────────┘
```

---

## RAG Pipeline

### PDF Processing and Retrieval

```
UPLOAD PHASE
════════════

┌─────────────┐
│    USER     │
│ Uploads PDF │
└──────┬──────┘
       │
       │ 1. Select PDF file
       ▼
┌──────────────────────┐
│  Frontend            │
│  handlePdfUpload()   │
└──────┬───────────────┘
       │
       │ 2. POST /api/upload_pdf
       │    FormData{pdf, sessionId}
       ▼
┌──────────────────────────────────────────────┐
│  Flask: upload_pdf()                         │
│                                              │
│  3. Save PDF to temp file                    │
│     ↓                                        │
│  4. Extract text with PyMuPDF                │
│     ┌──────────────────────────────┐         │
│     │ doc = fitz.open(pdf_path)    │         │
│     │ for page in doc:             │         │
│     │     text += page.get_text()  │         │
│     └──────────────────────────────┘         │
│     ↓                                        │
│  5. Split into chunks                        │
│     ┌──────────────────────────────────────┐ │
│     │ Chunk 1: chars 0-1000                │ │
│     │ Chunk 2: chars 800-1800 (overlap)    │ │
│     │ Chunk 3: chars 1600-2600             │ │
│     │ ...                                  │ │
│     └──────────────────────────────────────┘ │
│     ↓                                        │
│  6. Generate embeddings                      │
└──────┬───────────────────────────────────────┘
       │
       │ For each chunk
       ▼
┌──────────────────────────────┐
│  Gemini API                  │
│  embed_content()             │
│                              │
│  Model: embedding-001        │
│  Task: retrieval_document    │
│  Output: 768-dim vector      │
└──────┬───────────────────────┘
       │
       │ Return embeddings array
       ▼
┌──────────────────────────────────────────────┐
│  Flask: create_faiss_index()                 │
│                                              │
│  7. Create FAISS index                       │
│     ┌──────────────────────────────────┐     │
│     │ index = IndexFlatL2(768)         │     │
│     │ index.add(embeddings)            │     │
│     └──────────────────────────────────┘     │
│     ↓                                        │
│  8. Store in session                         │
│     ┌──────────────────────────────────┐     │
│     │ session_data[session_id] = {     │     │
│     │   'faiss_index': index,          │     │
│     │   'text_chunks': chunks,         │     │
│     │   'pdf_name': filename           │     │
│     │ }                                │     │
│     └──────────────────────────────────┘     │
└──────────────────────────────────────────────┘

RETRIEVAL PHASE
═══════════════

┌─────────────┐
│    USER     │
│ Asks query  │
└──────┬──────┘
       │
       │ "Explain quadratic formula from the PDF"
       ▼
┌──────────────────────────────────────────────┐
│  Flask: chat() endpoint                      │
│                                              │
│  1. Check if session has FAISS index         │
│     ↓                                        │
│  2. Call retrieve_relevant_context()         │
└──────┬───────────────────────────────────────┘
       │
       │ Query text
       ▼
┌──────────────────────────────┐
│  Gemini API                  │
│  embed_content()             │
│                              │
│  Model: embedding-001        │
│  Task: retrieval_query       │
│  Output: 768-dim vector      │
└──────┬───────────────────────┘
       │
       │ Query embedding
       ▼
┌──────────────────────────────────────────────┐
│  FAISS Index Search                          │
│                                              │
│  3. index.search(query_embedding, k=3)       │
│     ↓                                        │
│  4. Find 3 most similar chunks               │
│     ┌──────────────────────────────────┐     │
│     │ Distance │ Index │ Content       │     │
│     │ 0.234    │  42   │ "Quad formula"│     │
│     │ 0.456    │  18   │ "ax²+bx+c..." │     │
│     │ 0.678    │  91   │ "Roots are..."│     │
│     └──────────────────────────────────┘     │
│     ↓                                        │
│  5. Retrieve chunk texts                     │
│     ┌──────────────────────────────────┐     │
│     │ chunks[42] + chunks[18] + ...    │     │
│     └──────────────────────────────────┘     │
└──────┬───────────────────────────────────────┘
       │
       │ Concatenated relevant text
       ▼
┌──────────────────────────────────────────────┐
│  Flask: Build prompt with RAG context        │
│                                              │
│  Conversation context:                       │
│  [                                           │
│    {role: 'user',                            │
│     parts: ['Context from PDF:\n\n' +        │
│             relevant_chunks]},               │
│    {role: 'model',                           │
│     parts: ['I will use this context']},     │
│    {role: 'user',                            │
│     parts: [user_query]}                     │
│  ]                                           │
└──────┬───────────────────────────────────────┘
       │
       │ Enhanced prompt → Gemini → Response
       ▼
   Better, context-aware answer!
```

---

## Component Interaction

### Frontend Components

```
┌────────────────────────────────────────────────────────────┐
│                    index.html                              │
│                                                            │
│  <div id="calculator">                                     │
│    ↓                                                       │
│    Rendered by Desmos API                                  │
│  </div>                                                    │
│                                                            │
│  <div id="chat-panel">                                     │
│    ├─ <div id="chat-messages">                            │
│    │    └─ Managed by main.js                             │
│    │                                                       │
│    ├─ <input id="pdf-upload">                             │
│    │    └─ Event: handlePdfUpload()                       │
│    │                                                       │
│    └─ <textarea id="chat-input">                          │
│         ├─ Event: Enter key → sendMessage()               │
│         └─ Event: input → auto-resize                     │
│  </div>                                                    │
└────────────────────────────────────────────────────────────┘
                         │
                         │ Styled by
                         ▼
┌────────────────────────────────────────────────────────────┐
│                    style.css                               │
│                                                            │
│  Variables:                                                │
│  • --primary-color                                         │
│  • --panel-bg                                              │
│  • --border-color                                          │
│                                                            │
│  Layout:                                                   │
│  • .container → flexbox (50/50 split)                     │
│  • #calculator-panel → width: 50%                         │
│  • #chat-panel → width: 50%                               │
│                                                            │
│  Components:                                               │
│  • .message (user/ai)                                     │
│  • .chat-input                                            │
│  • .send-btn                                              │
│  • @media queries for responsive                          │
└────────────────────────────────────────────────────────────┘
                         │
                         │ Controlled by
                         ▼
┌────────────────────────────────────────────────────────────┐
│                    main.js                                 │
│                                                            │
│  Global State:                                             │
│  ┌──────────────────────────────────────────────┐         │
│  │ calculator: Desmos instance                  │         │
│  │ sessionId: Unique session ID                 │         │
│  │ conversationHistory: Message array           │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
│  Functions:                                                │
│  ┌──────────────────────────────────────────────┐         │
│  │ initializeCalculator()                       │         │
│  │   └─ Creates Desmos instance                 │         │
│  │                                              │         │
│  │ sendMessage()                                │         │
│  │   ├─ Capture input                           │         │
│  │   ├─ Display user message                    │         │
│  │   ├─ fetch('/api/chat', {...})               │         │
│  │   └─ Process response                        │         │
│  │                                              │         │
│  │ executeGraphCommands(commands)               │         │
│  │   └─ Switch on command type                  │         │
│  │       ├─ setExpression                       │         │
│  │       ├─ removeExpression                    │         │
│  │       └─ setMathBounds...                    │         │
│  │                                              │         │
│  │ handlePdfUpload(file)                        │         │
│  │   └─ POST to /api/upload_pdf                 │         │
│  └──────────────────────────────────────────────┘         │
└────────────────────────────────────────────────────────────┘
```

### Backend Components

```
┌────────────────────────────────────────────────────────────┐
│                    api/index.py                            │
│                                                            │
│  Configuration:                                            │
│  ┌──────────────────────────────────────────────┐         │
│  │ Flask app initialization                     │         │
│  │ Gemini API configuration                     │         │
│  │ Session data storage (dict)                  │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
│  Routes:                                                   │
│  ┌──────────────────────────────────────────────┐         │
│  │ @app.route('/')                              │         │
│  │   └─ render_template('index.html')           │         │
│  │                                              │         │
│  │ @app.route('/api/chat', methods=['POST'])    │         │
│  │   ├─ Extract message, sessionId, history     │         │
│  │   ├─ Check for RAG context                   │         │
│  │   ├─ Build conversation context              │         │
│  │   ├─ Call Gemini API                         │         │
│  │   ├─ Parse JSON response                     │         │
│  │   └─ Return {chatResponse, graphCommands}    │         │
│  │                                              │         │
│  │ @app.route('/api/upload_pdf', methods...)    │         │
│  │   ├─ Save PDF to temp file                   │         │
│  │   ├─ extract_text_from_pdf()                 │         │
│  │   ├─ create_embeddings()                     │         │
│  │   ├─ create_faiss_index()                    │         │
│  │   └─ Store in session_data                   │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
│  Helper Functions:                                         │
│  ┌──────────────────────────────────────────────┐         │
│  │ extract_text_from_pdf(path, chunk, overlap)  │         │
│  │   └─ PyMuPDF text extraction + chunking      │         │
│  │                                              │         │
│  │ create_embeddings(chunks)                    │         │
│  │   └─ Gemini embedding API calls              │         │
│  │                                              │         │
│  │ create_faiss_index(embeddings)               │         │
│  │   └─ FAISS IndexFlatL2 creation              │         │
│  │                                              │         │
│  │ retrieve_relevant_context(session, query)    │         │
│  │   ├─ Embed query                             │         │
│  │   ├─ FAISS search                            │         │
│  │   └─ Return top-k chunks                     │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
│  Global Data:                                              │
│  ┌──────────────────────────────────────────────┐         │
│  │ SYSTEM_PROMPT: Detailed AI instructions      │         │
│  │ session_data: {sessionId: {index, chunks}}   │         │
│  └──────────────────────────────────────────────┘         │
└────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

### Local Development

```
┌─────────────────────────────────────────┐
│        Developer Machine                │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Python Virtual Environment       │  │
│  │  (venv/)                          │  │
│  │                                   │  │
│  │  Dependencies:                    │  │
│  │  • Flask                          │  │
│  │  • google-generativeai            │  │
│  │  • PyMuPDF                        │  │
│  │  • faiss-cpu                      │  │
│  │  • numpy                          │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Flask Development Server         │  │
│  │  (api/index.py)                   │  │
│  │                                   │  │
│  │  Running on:                      │  │
│  │  http://localhost:5000            │  │
│  │                                   │  │
│  │  Serves:                          │  │
│  │  • templates/index.html           │  │
│  │  • static/style.css               │  │
│  │  • static/main.js                 │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Environment Variables:                 │
│  • GEMINI_API_KEY                       │
│  • FLASK_SECRET_KEY                     │
└─────────────────────────────────────────┘
```

### Production (Vercel)

```
┌────────────────────────────────────────────────────────────────┐
│                        VERCEL PLATFORM                         │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               Edge Network (CDN)                         │  │
│  │                                                          │  │
│  │  Caches:                                                 │  │
│  │  • static/style.css                                      │  │
│  │  • static/main.js                                        │  │
│  │  • Desmos API script                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                 │
│                              │ Route: /static/*                │
│                              ▼                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Serverless Function (Lambda)                     │  │
│  │                                                          │  │
│  │  Runtime: Python 3.11                                    │  │
│  │  Entry: api/index.py                                     │  │
│  │  Memory: 1024 MB                                         │  │
│  │  Timeout: 10 seconds                                     │  │
│  │                                                          │  │
│  │  Environment Variables:                                  │  │
│  │  • GEMINI_API_KEY (encrypted)                            │  │
│  │  • FLASK_SECRET_KEY (encrypted)                          │  │
│  │                                                          │  │
│  │  Installed Packages:                                     │  │
│  │  └─ From requirements.txt                                │  │
│  │                                                          │  │
│  │  Routes:                                                 │  │
│  │  • GET /        → index.html                             │  │
│  │  • POST /api/chat                                        │  │
│  │  • POST /api/upload_pdf                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                 │
│                              │ External API Call               │
│                              ▼                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           External: Google Gemini API                    │  │
│  │                                                          │  │
│  │  • gemini-1.5-flash (generation)                         │  │
│  │  • embedding-001 (embeddings)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Vercel Configuration (vercel.json):                           │
│  ┌────────────────────────────────────────────────┐           │
│  │ {                                              │           │
│  │   "builds": [                                  │           │
│  │     {"src": "api/index.py",                    │           │
│  │      "use": "@vercel/python",                  │           │
│  │      "config": {"maxLambdaSize": "15mb"}}      │           │
│  │   ],                                           │           │
│  │   "routes": [                                  │           │
│  │     {"/static/*" → static files},              │           │
│  │     {"/*" → api/index.py}                      │           │
│  │   ]                                            │           │
│  │ }                                              │           │
│  └────────────────────────────────────────────────┘           │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
                    ┌──────────────────┐
                    │   User Browser   │
                    │                  │
                    │  your-app.       │
                    │  vercel.app      │
                    └──────────────────┘
```

### Data Flow in Production

```
User Browser
    │
    │ 1. HTTPS Request
    ▼
Vercel Edge (Global CDN)
    │
    ├─ Static files? → Serve from cache
    │
    └─ Dynamic route? ─────────┐
                               │
                               ▼
                    Serverless Function
                         (Cold Start?)
                         ├─ Yes → Initialize (~2-3s)
                         └─ No → Use warm instance (~100ms)
                               │
                               ├─ Load environment variables
                               ├─ Import dependencies
                               ├─ Initialize Flask
                               │
                               ▼
                         Process Request
                               │
                               ├─ /api/chat
                               │    ├─ Check session_data
                               │    ├─ Call Gemini API
                               │    └─ Return JSON
                               │
                               └─ /api/upload_pdf
                                    ├─ Save to /tmp
                                    ├─ Extract text
                                    ├─ Generate embeddings
                                    ├─ Create FAISS index
                                    └─ Store in session_data
                               │
                               ▼
                         Return Response
                               │
                               ▼
                         User Browser
```

---

## State Management

### Session Data Structure

```
session_data = {
    'session_abc123': {
        'faiss_index': <FAISS.IndexFlatL2 object>,
        'text_chunks': [
            'Chunk 1: In mathematics, the quadratic...',
            'Chunk 2: The formula x = (-b ± √...',
            'Chunk 3: This allows us to solve...',
            ...
        ],
        'pdf_name': 'algebra_textbook_ch3.pdf',
        'upload_time': 1728936000,
        'chunk_count': 127
    },
    'session_xyz789': {
        ...
    }
}
```

### Conversation History (Frontend)

```javascript
conversationHistory = [
    {
        role: 'user',
        content: 'plot y = x^2'
    },
    {
        role: 'assistant',
        content: 'I\'ve plotted the parabola y = x²...'
    },
    {
        role: 'user',
        content: 'now add its derivative'
    },
    {
        role: 'assistant',
        content: 'I\'ve added y = 2x, which is the derivative...'
    }
]
```

---

This architecture enables:
✅ Scalable serverless deployment
✅ Fast static asset delivery
✅ Intelligent RAG-enhanced responses
✅ Smooth real-time graph updates
✅ Session-based PDF context
✅ Cost-effective free-tier usage
