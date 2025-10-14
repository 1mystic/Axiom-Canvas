# Axiom Canvas - AI Math Visualizer

An AI-powered mathematical visualization tool that combines a Desmos graphing calculator with a natural language AI chat interface. Ask questions, plot functions, and get visual explanations of mathematical concepts.

![Axiom Canvas](https://img.shields.io/badge/AI-Math%20Visualizer-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Gemini](https://img.shields.io/badge/Gemini-API-orange)

## Features

- **Split-Screen Interface**: Interactive Desmos calculator on the left, AI chat on the right
- **Natural Language Control**: Command the graph using plain English
  - "plot y = x^2 - 3"
  - "add the line y = 2x + 1 in red"
  - "zoom in on the intersection points"
- **Visual Explanations**: AI uses both text and graphs to explain mathematical concepts
- **PDF Upload & RAG**: Upload textbooks or documents and ask questions with visual answers
- **Free Deployment**: Designed to run on Vercel's free tier

## Tech Stack

### Frontend
- **Vanilla HTML/CSS/JavaScript** - No frameworks, fast and simple
- **Desmos API v1.7** - Professional graphing calculator
- **Responsive Design** - Works on desktop and mobile

### Backend
- **Python 3.11+** with Flask
- **Google Gemini API** - AI language model
- **PyMuPDF** - PDF text extraction
- **FAISS** - Vector similarity search for RAG
- **Vercel Serverless Functions** - Deployment platform

## Project Structure

```
FLASK-APP/
├── api/
│   └── index.py              # Flask backend (serverless function)
├── static/
│   ├── style.css             # Application styling
│   └── main.js               # Frontend logic & Desmos integration
├── templates/
│   └── index.html            # Main application page
├── vercel.json               # Vercel deployment configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-math-visualizer/FLASK-APP
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   
   Create a `.env` file in the FLASK-APP directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```
   
   Or set them directly:
   ```bash
   # On Windows (PowerShell)
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   $env:FLASK_SECRET_KEY="your_secret_key_here"
   
   # On macOS/Linux
   export GEMINI_API_KEY="your_gemini_api_key_here"
   export FLASK_SECRET_KEY="your_secret_key_here"
   ```

5. **Run the application**
   ```bash
   cd api
   python index.py
   ```
   
   The app will be available at `http://localhost:5000`

## Deployment to Vercel

### Prerequisites
- A Vercel account ([Sign up here](https://vercel.com/signup))
- Vercel CLI installed: `npm install -g vercel`

### Deployment Steps

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Set environment variables in Vercel**
   
   You can do this via the Vercel dashboard or CLI:
   ```bash
   vercel env add GEMINI_API_KEY
   # Paste your Gemini API key when prompted
   
   vercel env add FLASK_SECRET_KEY
   # Paste a random secret key
   ```

3. **Deploy**
   ```bash
   cd FLASK-APP
   vercel --prod
   ```

4. **Access your app**
   
   Vercel will provide you with a URL like `https://your-app.vercel.app`

### Alternative: Deploy via Vercel Dashboard

1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your GitHub repository
5. Set the root directory to `FLASK-APP`
6. Add environment variables:
   - `GEMINI_API_KEY`
   - `FLASK_SECRET_KEY`
7. Click "Deploy"

## Usage Guide

### Basic Plotting
```
You: plot y = x^2
AI: I've plotted the parabola y = x². Notice its vertex at the origin.
```

### Multiple Functions
```
You: show me sin(x) and cos(x) in different colors
AI: I've plotted sin(x) in blue and cos(x) in red. Notice how cos(x) is just sin(x) shifted left by π/2.
```

### Conceptual Explanations
```
You: explain what a derivative is
AI: A derivative represents the rate of change... [includes visual plots of f(x) and f'(x)]
```

### PDF Context
```
1. Click "Upload PDF" and select your math textbook
2. Ask: "Explain the quadratic formula from chapter 3"
3. AI uses the PDF content and creates visual explanations
```

### Graph Commands
```
You: zoom in on the region from -5 to 5
You: clear the graph
You: mark the intersection points
You: change the parabola to red
```

## API Endpoints

### `GET /`
Serves the main application page

### `POST /api/chat`
Handles chat messages and returns AI responses with graph commands

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
  "chatResponse": "I've plotted the parabola y = x².",
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

### `POST /api/upload_pdf`
Processes uploaded PDF files for RAG

**Request:** Multipart form data with `pdf` file and `sessionId`

**Response:**
```json
{
  "success": true,
  "message": "Successfully processed 42 text chunks",
  "chunks": 42
}
```

## Graph Command Schema

The AI can issue these commands to control the Desmos calculator:

### `setExpression`
Add or update a mathematical expression
```json
{
  "command": "setExpression",
  "params": {
    "id": "expr1",
    "latex": "y=x^2",
    "color": "#2563eb",
    "lineStyle": "SOLID",
    "lineWidth": 2.5
  }
}
```

### `removeExpression`
Remove an expression
```json
{
  "command": "removeExpression",
  "params": {"id": "expr1"}
}
```

### `setMathBounds`
Set viewport bounds
```json
{
  "command": "setMathBounds",
  "params": {
    "left": -10,
    "right": 10,
    "bottom": -10,
    "top": 10
  }
}
```

### `clearExpressions`
Clear all expressions
```json
{
  "command": "clearExpressions",
  "params": {}
}
```

## Architecture Details

### AI Integration
- Uses Google Gemini 1.5 Flash for fast, accurate responses
- Structured prompting ensures consistent JSON output
- Conversation history maintained for context
- RAG implementation for PDF document understanding

### RAG (Retrieval-Augmented Generation)
1. PDF text extracted using PyMuPDF
2. Text split into overlapping chunks (1000 chars, 200 overlap)
3. Each chunk embedded using Gemini's embedding model
4. FAISS index created for fast similarity search
5. Relevant chunks retrieved and prepended to user queries

### Serverless Design
- Single `api/index.py` file contains entire Flask app
- Vercel automatically creates serverless function
- Session data stored in-memory (consider Redis for production)
- Stateless design for scalability

## Limitations & Considerations

### Free Tier Constraints
- **Vercel**: 100GB bandwidth/month, 100 hours serverless execution
- **Gemini**: 60 requests/minute, 1500 requests/day (free tier)
- Session data lost on function restart (use persistent storage for production)

### Known Issues
- PDF processing may timeout on very large files
- Session data not persistent across serverless function restarts
- FAISS index stored in memory (limited by Lambda memory)

## Future Enhancements

- [ ] Persistent session storage (Redis/Upstash)
- [ ] User authentication
- [ ] Save/load graph states
- [ ] Export graphs as images
- [ ] 3D graphing support
- [ ] Collaborative sessions
- [ ] More AI models (Claude, GPT-4)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## Acknowledgments

- [Desmos](https://www.desmos.com/) for their excellent graphing calculator API
- [Google](https://ai.google.dev/) for the Gemini API
- [Vercel](https://vercel.com/) for generous free tier hosting

---

Built with ❤️ for math education and exploration
