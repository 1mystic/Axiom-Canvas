# Axiom Canvas - Project Summary

## 🎯 Project Overview

**Axiom Canvas** is an AI-powered mathematical visualization tool that seamlessly combines a Desmos graphing calculator with a natural language AI chat interface powered by Google's Gemini API. The application enables users to explore mathematics through conversational interaction, where the AI can both explain concepts and visualize them on the graph.

## ✨ Key Features

### 1. **Dual-Panel Interface**
- **Left Panel**: Interactive Desmos graphing calculator
- **Right Panel**: AI-powered chat interface
- Responsive design works on desktop and mobile

### 2. **Natural Language Graph Control**
Users can command the graph using plain English:
- "plot y = x^2 - 3"
- "add the line y = 2x + 1 in red"
- "zoom in on the intersection points"
- "clear the graph"

### 3. **Visual Mathematical Explanations**
The AI uses both text and graphs to explain concepts:
- Derivative visualizations with tangent lines
- Trigonometric function comparisons
- Intersection point highlighting
- Function transformation demonstrations

### 4. **RAG-Enhanced Document Understanding**
- Upload PDF documents (textbooks, notes, etc.)
- Ask questions about the content
- AI retrieves relevant context using FAISS vector search
- Provides visual explanations based on document content

### 5. **Free Deployment**
Designed specifically for Vercel's free tier:
- Serverless architecture
- Minimal dependencies
- Efficient resource usage

## 🏗️ Technical Architecture

### Frontend Stack
```
HTML5 + CSS3 + Vanilla JavaScript
└── Desmos API v1.7 (Graphing)
└── Fetch API (Backend Communication)
└── CSS Grid/Flexbox (Layout)
```

### Backend Stack
```
Python 3.11+ with Flask
├── Google Gemini API (AI)
├── PyMuPDF (PDF Processing)
├── FAISS (Vector Search)
└── NumPy (Numerical Operations)
```

### Deployment
```
Vercel Serverless Functions
├── Single serverless entry point (api/index.py)
├── Static file serving
└── Environment variable management
```

## 📁 Project Structure

```
FLASK-APP/
├── api/
│   └── index.py                    # Flask backend (serverless function)
│
├── static/
│   ├── style.css                   # Application styling
│   └── main.js                     # Frontend logic & Desmos integration
│
├── templates/
│   └── index.html                  # Main application page
│
├── vercel.json                     # Vercel deployment config
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
│
├── README.md                       # User documentation
├── IMPLEMENTATION_GUIDE.md         # Developer documentation
├── DEPLOYMENT_CHECKLIST.md         # Deployment guide
├── TEST_PROMPTS.md                 # Testing scenarios
│
├── start.sh                        # Linux/Mac startup script
└── start.ps1                       # Windows startup script
```

## 🔑 Core Components

### 1. AI System Prompt (`api/index.py`)

The system prompt is carefully designed to ensure consistent JSON output:

```python
SYSTEM_PROMPT = """You are Axiom Canvas...
CRITICAL: You must ALWAYS respond with valid JSON in this exact format:
{
  "chatResponse": "Your explanation...",
  "graphCommands": [{"command": "...", "params": {...}}]
}
"""
```

### 2. Graph Command System

Five command types control the Desmos calculator:

| Command | Purpose | Example |
|---------|---------|---------|
| `setExpression` | Add/update expression | `{id: "f1", latex: "y=x^2", color: "#2563eb"}` |
| `removeExpression` | Remove expression | `{id: "f1"}` |
| `setMathBounds` | Set viewport | `{left: -10, right: 10, bottom: -10, top: 10}` |
| `clearExpressions` | Clear all | `{}` |
| `setBlank` | Reset calculator | `{}` |

### 3. RAG Pipeline

**5-Step Process:**

1. **PDF Upload**: User uploads PDF document
2. **Text Extraction**: PyMuPDF extracts text, splits into chunks
3. **Embedding**: Gemini generates vector embeddings for each chunk
4. **Indexing**: FAISS creates searchable index
5. **Retrieval**: On query, similar chunks retrieved and prepended to prompt

### 4. Frontend Graph Controller

JavaScript executes graph commands from AI responses:

```javascript
function executeGraphCommands(commands) {
    commands.forEach(cmd => {
        switch (cmd.command) {
            case 'setExpression':
                calculator.setExpression(cmd.params);
                break;
            // ... other commands
        }
    });
}
```

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone <repo-url>
cd ai-math-visualizer/FLASK-APP

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run application
cd api
python index.py

# 6. Access at http://localhost:5000
```

### Vercel Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Add environment variables
vercel env add GEMINI_API_KEY
vercel env add FLASK_SECRET_KEY

# Deploy
cd FLASK-APP
vercel --prod
```

## 🧪 Testing

### Basic Test Prompts

```
✅ "plot y = x^2"
✅ "plot y = sin(x) in red"
✅ "explain the derivative of x^2"
✅ "where do y = x^2 and y = 2x + 1 intersect?"
✅ "clear the graph"
```

See `TEST_PROMPTS.md` for comprehensive test scenarios.

## 📊 System Flow

```
User Input
    ↓
Frontend (main.js)
    ↓
POST /api/chat
    ↓
Flask Backend (index.py)
    ↓
Check for RAG Context?
    ├── Yes → Retrieve from FAISS
    └── No → Continue
    ↓
Build Conversation Context
    ↓
Call Gemini API
    ↓
Parse JSON Response
    ↓
Return {chatResponse, graphCommands}
    ↓
Frontend Displays & Executes
    ├── Show chat message
    └── Update Desmos graph
```

## 🎨 Design Decisions

### Why Vanilla JavaScript?
- No build process needed
- Faster load times
- Simpler deployment
- Easier to understand and modify

### Why Gemini API?
- Generous free tier (60 req/min, 1500 req/day)
- Excellent at following structured prompts
- Built-in embedding model for RAG
- Good at mathematical reasoning

### Why FAISS?
- Fast similarity search
- Works well for small datasets
- CPU version works on Vercel
- Simple API

### Why Serverless?
- No server management
- Auto-scaling
- Pay only for usage
- Perfect for free tier deployment

## 🔒 Security Considerations

### Implemented
- ✅ API keys in environment variables
- ✅ `.env` in `.gitignore`
- ✅ HTTPS on Vercel (automatic)
- ✅ File type validation (PDF only)
- ✅ Input sanitization in chat display

### Recommended for Production
- 🔲 Rate limiting (Flask-Limiter)
- 🔲 User authentication
- 🔲 CORS configuration
- 🔲 Content Security Policy
- 🔲 Request size limits

## 📈 Scalability Considerations

### Current Limitations
- **Session Storage**: In-memory (lost on function restart)
- **Concurrent Users**: Limited by Gemini free tier
- **PDF Size**: 15MB max on Vercel
- **Memory**: Limited by Lambda memory

### Production Improvements
- Use Redis/Upstash for session persistence
- Implement user accounts with database
- Add caching for common queries
- Use job queue for PDF processing
- Implement rate limiting per user

## 🎓 Educational Use Cases

### For Students
- Visualize complex functions
- Understand derivatives and integrals
- Explore function transformations
- Get instant visual feedback
- Upload textbook chapters for help

### For Teachers
- Create interactive demonstrations
- Explain concepts visually
- Show multiple representations
- Engage students with AI interaction
- Generate custom examples

### For Self-Learners
- Experiment with mathematics
- Get immediate visual feedback
- Ask "what if" questions
- Explore at own pace
- Combine theory with visualization

## 🛠️ Extension Ideas

### Short-term
- [ ] Save/load graph states
- [ ] Export graphs as images
- [ ] More color themes
- [ ] Keyboard shortcuts
- [ ] Example gallery

### Medium-term
- [ ] User accounts
- [ ] Shared sessions
- [ ] Annotation tools
- [ ] Step-by-step solutions
- [ ] Multiple AI models

### Long-term
- [ ] 3D graphing support
- [ ] Collaborative features
- [ ] Mobile app version
- [ ] Voice input
- [ ] Gamification

## 📚 Documentation

### For Users
- **README.md**: Setup, usage, and deployment
- **TEST_PROMPTS.md**: Example prompts to try

### For Developers
- **IMPLEMENTATION_GUIDE.md**: Deep technical documentation
- **DEPLOYMENT_CHECKLIST.md**: Step-by-step deployment guide
- **Code Comments**: Inline documentation throughout

## 🌟 Key Achievements

✅ **Zero Framework Dependency**: Pure HTML/CSS/JS frontend
✅ **Structured AI Output**: Reliable JSON from Gemini
✅ **Visual Math Education**: Text + graph explanations
✅ **RAG Integration**: Document-aware responses
✅ **Free Deployment**: Vercel serverless architecture
✅ **Comprehensive Docs**: Implementation and deployment guides
✅ **Responsive Design**: Works on all devices
✅ **Clean Code**: Well-organized and commented

## 📝 License

MIT License - Free for educational and commercial use

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional graph commands
- UI/UX improvements
- Performance optimization
- Additional AI models
- Documentation improvements

## 📧 Support

- **Issues**: GitHub Issues
- **Documentation**: README.md, IMPLEMENTATION_GUIDE.md
- **Testing**: TEST_PROMPTS.md
- **Deployment**: DEPLOYMENT_CHECKLIST.md

## 🎉 Acknowledgments

- **Desmos**: Excellent graphing calculator API
- **Google**: Gemini API for AI capabilities
- **Vercel**: Generous free tier hosting
- **Community**: Open source libraries used

---

## Next Steps

1. **Get API Key**: https://makersuite.google.com/app/apikey
2. **Setup Locally**: Follow Quick Start above
3. **Test Features**: Use TEST_PROMPTS.md
4. **Deploy**: Follow DEPLOYMENT_CHECKLIST.md
5. **Customize**: Extend with your own features

---

**Built with ❤️ for mathematics education and exploration**

*Making math visual, interactive, and accessible through AI*
