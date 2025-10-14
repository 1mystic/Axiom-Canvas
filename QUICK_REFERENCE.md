# Axiom Canvas - Quick Reference Guide

Quick reference for common tasks, commands, and troubleshooting.

## 📋 Table of Contents
- [Common Commands](#common-commands)
- [File Locations](#file-locations)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Graph Commands](#graph-commands)
- [Error Messages](#error-messages)
- [Useful Code Snippets](#useful-code-snippets)

---

## Common Commands

### Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
cd api
python index.py

# Deactivate virtual environment
deactivate
```

### Vercel Deployment

```bash
# Install CLI
npm install -g vercel

# Login
vercel login

# Deploy preview
vercel

# Deploy production
vercel --prod

# View logs
vercel logs

# List deployments
vercel list

# Add environment variable
vercel env add VARIABLE_NAME

# Remove deployment
vercel remove [deployment-name]
```

### Git Commands

```bash
# Initialize repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote
git remote add origin [repo-url]

# Push to GitHub
git push -u origin main

# Check status
git status
```

---

## File Locations

### Project Structure
```
FLASK-APP/
├── api/index.py                    # Flask backend
├── static/
│   ├── style.css                   # Styling
│   └── main.js                     # Frontend logic
├── templates/
│   └── index.html                  # Main page
├── vercel.json                     # Vercel config
├── requirements.txt                # Python deps
├── .env                            # Env variables (local)
└── .env.example                    # Template
```

### Important Files

| File | Purpose | Edit Frequency |
|------|---------|----------------|
| `api/index.py` | Backend logic, routes, AI integration | Often |
| `static/main.js` | Frontend logic, Desmos control | Often |
| `static/style.css` | Styling, layout | Sometimes |
| `templates/index.html` | HTML structure | Rarely |
| `vercel.json` | Deployment config | Rarely |
| `requirements.txt` | Dependencies | When adding packages |
| `.env` | Local secrets | Once (setup) |

---

## Environment Variables

### Required

```env
# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIza...

# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
FLASK_SECRET_KEY=a1b2c3d4...
```

### Optional

```env
# Flask environment (default: production)
FLASK_ENV=development

# Debug mode (default: False)
FLASK_DEBUG=True

# Max file upload size in bytes (default: 16MB)
MAX_CONTENT_LENGTH=16777216
```

### Set Locally

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_key"
$env:FLASK_SECRET_KEY="your_secret"
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_key"
export FLASK_SECRET_KEY="your_secret"
```

### Set in Vercel

**Via CLI:**
```bash
vercel env add GEMINI_API_KEY
# Paste your key when prompted
```

**Via Dashboard:**
1. Go to project settings
2. Navigate to "Environment Variables"
3. Add key-value pairs
4. Select environments (Production, Preview, Development)
5. Save

---

## API Endpoints

### GET /
**Purpose:** Serve main application page  
**Response:** HTML page  
**Example:**
```bash
curl https://your-app.vercel.app/
```

### POST /api/chat
**Purpose:** Process chat messages  
**Request Body:**
```json
{
  "message": "plot y = x^2",
  "sessionId": "session_123",
  "history": [
    {"role": "user", "content": "previous message"},
    {"role": "assistant", "content": "previous response"}
  ]
}
```
**Response:**
```json
{
  "chatResponse": "I've plotted the parabola...",
  "graphCommands": [
    {
      "command": "setExpression",
      "params": {
        "id": "parabola",
        "latex": "y=x^2",
        "color": "#2563eb"
      }
    }
  ]
}
```

### POST /api/upload_pdf
**Purpose:** Upload and process PDF for RAG  
**Request:** `multipart/form-data`
- `pdf`: PDF file
- `sessionId`: Session identifier

**Response:**
```json
{
  "success": true,
  "message": "Successfully processed 42 text chunks",
  "chunks": 42
}
```

---

## Graph Commands

### setExpression
**Add or update mathematical expression**

**Basic:**
```json
{
  "command": "setExpression",
  "params": {
    "id": "f1",
    "latex": "y=x^2"
  }
}
```

**With styling:**
```json
{
  "command": "setExpression",
  "params": {
    "id": "sine",
    "latex": "y=\\sin(x)",
    "color": "#2563eb",
    "lineStyle": "DASHED",
    "lineWidth": 3,
    "lineOpacity": 0.8
  }
}
```

**Point:**
```json
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

**Available lineStyle:**
- `"SOLID"` (default)
- `"DASHED"`
- `"DOTTED"`

**Available pointStyle:**
- `"POINT"` (filled circle)
- `"OPEN"` (hollow circle)
- `"CROSS"` (× mark)

### removeExpression
**Remove expression by ID**
```json
{
  "command": "removeExpression",
  "params": {
    "id": "f1"
  }
}
```

### setMathBounds
**Set viewport bounds**
```json
{
  "command": "setMathBounds",
  "params": {
    "left": -10,
    "right": 10,
    "bottom": -5,
    "top": 5
  }
}
```

### clearExpressions
**Remove all expressions**
```json
{
  "command": "clearExpressions",
  "params": {}
}
```

### setBlank
**Reset to blank state**
```json
{
  "command": "setBlank",
  "params": {}
}
```

---

## Error Messages

### "GEMINI_API_KEY not set"
**Cause:** Environment variable missing  
**Fix:**
```bash
# Set locally
export GEMINI_API_KEY="your_key"

# Or in Vercel
vercel env add GEMINI_API_KEY
```

### "Module not found: google.generativeai"
**Cause:** Dependency not installed  
**Fix:**
```bash
pip install google-generativeai
# or
pip install -r requirements.txt
```

### "Function execution timed out"
**Cause:** PDF too large or processing too slow  
**Fix:**
- Reduce PDF size
- Split PDF into smaller chunks
- Increase timeout in `vercel.json`:
```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 30
    }
  }
}
```

### "Failed to parse JSON"
**Cause:** AI returned non-JSON response  
**Fix:** Check system prompt, ensure JSON examples are clear

### "CORS error"
**Cause:** Cross-origin request blocked  
**Fix:** Add CORS headers in Flask:
```python
from flask_cors import CORS
CORS(app)
```

---

## Useful Code Snippets

### Add New Graph Command

**1. Update system prompt in `api/index.py`:**
```python
SYSTEM_PROMPT = """
...
6. setPointLabel - Add label to a point
   Example: {"command": "setPointLabel", "params": {"id": "p1", "label": "Vertex"}}
"""
```

**2. Update frontend handler in `static/main.js`:**
```javascript
function executeGraphCommands(commands) {
    commands.forEach(cmd => {
        switch (cmd.command) {
            // ... existing commands
            case 'setPointLabel':
                calculator.setExpression({
                    id: cmd.params.id,
                    label: cmd.params.label,
                    showLabel: true
                });
                break;
        }
    });
}
```

### Add Rate Limiting

**Install:**
```bash
pip install flask-limiter
```

**In `api/index.py`:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    # ...
```

### Add Custom Color Schemes

**In `static/style.css`:**
```css
/* Dark mode */
[data-theme="dark"] {
    --primary-color: #60a5fa;
    --panel-bg: #1e293b;
    --text-primary: #f8fafc;
}

/* High contrast */
[data-theme="high-contrast"] {
    --primary-color: #000000;
    --panel-bg: #ffffff;
    --border-color: #000000;
}
```

**In `static/main.js`:**
```javascript
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}
```

### Save Graph State

**In `static/main.js`:**
```javascript
function saveGraphState() {
    const state = calculator.getState();
    localStorage.setItem('graph_state', JSON.stringify(state));
    console.log('Graph state saved');
}

function loadGraphState() {
    const savedState = localStorage.getItem('graph_state');
    if (savedState) {
        calculator.setState(JSON.parse(savedState));
        console.log('Graph state loaded');
    }
}

// Auto-save every 30 seconds
setInterval(saveGraphState, 30000);
```

### Export Graph as Image

**In `static/main.js`:**
```javascript
function exportGraph() {
    calculator.asyncScreenshot(function(data) {
        const link = document.createElement('a');
        link.download = 'graph_' + Date.now() + '.png';
        link.href = data;
        link.click();
    });
}

// Add button
<button onclick="exportGraph()">Export as PNG</button>
```

### Add Voice Input

**In `static/main.js`:**
```javascript
function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('chat-input').value = transcript;
        sendMessage();
    };
    
    recognition.start();
}

// Add button
<button onclick="startVoiceInput()">🎤 Voice Input</button>
```

---

## Color Reference

### Default Colors
```javascript
const colors = {
    primary: '#2563eb',      // Blue
    success: '#059669',      // Green
    error: '#dc2626',        // Red
    warning: '#d97706',      // Orange
    purple: '#8b5cf6',       // Purple
    cyan: '#0891b2',         // Cyan
    pink: '#db2777'          // Pink
};
```

### Usage in Graph Commands
```json
{
  "command": "setExpression",
  "params": {
    "id": "f1",
    "latex": "y=x^2",
    "color": "#2563eb"  // Blue
  }
}
```

---

## LaTeX Reference

### Common Expressions

| Math | LaTeX |
|------|-------|
| y = x² | `y=x^2` |
| y = √x | `y=\\sqrt{x}` |
| y = 1/x | `y=\\frac{1}{x}` |
| y = sin(x) | `y=\\sin(x)` |
| y = e^x | `y=e^x` |
| y = log(x) | `y=\\log(x)` |
| Point (2, 3) | `(2, 3)` |

### Subscripts/Superscripts
```
x_1              → x₁
x^{2}            → x²
x_{n+1}          → xₙ₊₁
```

---

## Keyboard Shortcuts

### Chat Interface (can be added)

```javascript
// In main.js
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to send
    if (e.ctrlKey && e.key === 'Enter') {
        sendMessage();
    }
    
    // Ctrl+K to clear
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        clearChat();
    }
    
    // Ctrl+L to clear graph
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        executeGraphCommands([{command: 'clearExpressions', params: {}}]);
    }
});
```

---

## Testing Quick Commands

```bash
# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"plot y=x^2","sessionId":"test","history":[]}'

# Test with httpie (prettier output)
http POST http://localhost:5000/api/chat \
  message="plot y=x^2" \
  sessionId="test" \
  history:='[]'
```

---

## Performance Tips

### Frontend
- Use `requestAnimationFrame` for smooth animations
- Debounce rapid user inputs
- Lazy load chat messages
- Use CSS `will-change` for animated elements

### Backend
- Cache common Gemini responses
- Batch embedding generation
- Use async/await for concurrent operations
- Implement request queuing

### Deployment
- Enable Vercel Analytics
- Use Edge Functions for static content
- Compress large responses
- Implement CDN caching

---

## Resources

### Official Documentation
- [Desmos API](https://www.desmos.com/api/v1.7/docs/index.html)
- [Google Gemini](https://ai.google.dev/docs)
- [Flask](https://flask.palletsprojects.com/)
- [Vercel](https://vercel.com/docs)

### Tools
- [Gemini API Studio](https://makersuite.google.com/)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [FAISS Documentation](https://faiss.ai/)

### Learning
- [LaTeX Math Symbols](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)
- [Python Flask Tutorial](https://flask.palletsprojects.com/tutorial/)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

**Keep this guide handy for quick reference!** 📚
