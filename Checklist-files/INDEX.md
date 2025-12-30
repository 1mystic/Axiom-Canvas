# 🎓 Axiom Canvas - Complete Documentation Index

Welcome to Axiom Canvas! This document serves as your central navigation hub for all project documentation.

---

## 🚀 Quick Start (5 Minutes)

**New to the project? Start here:**

1. **Read:** [README.md](README.md) - Overview and setup instructions
2. **Get API Key:** https://makersuite.google.com/app/apikey
3. **Run locally:**
   ```bash
   # Windows
   .\start.ps1
   
   # Linux/Mac
   ./start.sh
   ```
4. **Test:** Open http://localhost:5000 and try: "plot y = x^2"

---

## 📚 Documentation Guide

### For End Users

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[README.md](README.md)** | Project overview, setup, deployment | First time setup |
| **[TEST_PROMPTS.md](TEST_PROMPTS.md)** | Example prompts to try | Learning to use the app |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Quick commands and tips | Day-to-day reference |

### For Developers

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | High-level architecture overview | Understanding the system |
| **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** | Deep technical details | Developing features |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Visual diagrams and flows | Understanding interactions |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Code snippets and commands | During development |

### For DevOps/Deployment

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** | Step-by-step deployment guide | Deploying to production |
| **[README.md](README.md)** | Vercel setup instructions | Initial deployment |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Common commands | Troubleshooting |

---

## 📁 Project Structure

```
FLASK-APP/
│
├── 📄 Core Application Files
│   ├── api/
│   │   └── index.py                    # Flask backend (serverless)
│   ├── static/
│   │   ├── style.css                   # Application styling
│   │   └── main.js                     # Frontend logic
│   ├── templates/
│   │   └── index.html                  # Main HTML page
│   ├── vercel.json                     # Vercel deployment config
│   └── requirements.txt                # Python dependencies
│
├── 🔧 Configuration Files
│   ├── .env.example                    # Environment variable template
│   ├── .gitignore                      # Git ignore rules
│   ├── start.sh                        # Linux/Mac startup script
│   └── start.ps1                       # Windows startup script
│
├── 📚 Documentation Files
│   ├── README.md                       # Main documentation
│   ├── PROJECT_SUMMARY.md              # Project overview
│   ├── IMPLEMENTATION_GUIDE.md         # Technical deep dive
│   ├── ARCHITECTURE.md                 # System architecture
│   ├── DEPLOYMENT_CHECKLIST.md         # Deployment guide
│   ├── TEST_PROMPTS.md                 # Testing scenarios
│   ├── QUICK_REFERENCE.md              # Quick reference
│   └── INDEX.md                        # This file
│
└── 🔒 Local Files (not in repo)
    ├── .env                            # Your API keys
    ├── .venv/ or venv/                 # Python virtual environment
    └── .vercel/                        # Vercel deployment data
```

---

## 🎯 Common Tasks

### I want to...

#### ...understand what this project does
→ Read: [README.md](README.md) → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

#### ...set up the project locally
→ Read: [README.md](README.md) "Local Development Setup" section  
→ Or run: `./start.ps1` (Windows) or `./start.sh` (Linux/Mac)

#### ...deploy to Vercel
→ Read: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)  
→ Follow: Step-by-step deployment instructions

#### ...understand how it works technically
→ Read: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)  
→ Then: [ARCHITECTURE.md](ARCHITECTURE.md) for visual diagrams

#### ...test the application
→ Read: [TEST_PROMPTS.md](TEST_PROMPTS.md)  
→ Try: Example prompts in the chat

#### ...modify the code
→ Read: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)  
→ Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for snippets

#### ...troubleshoot an issue
→ Check: [README.md](README.md) "Troubleshooting" section  
→ Or: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) "Troubleshooting"  
→ Or: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) "Error Messages"

#### ...add a new feature
→ Read: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)  
→ Use: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) code snippets  
→ Test: With [TEST_PROMPTS.md](TEST_PROMPTS.md)

---

## 🔑 Key Concepts

### The "Big Picture"

**Axiom Canvas** = Desmos Calculator + AI Chat + RAG

```
User Input → AI (Gemini) → JSON Response → Frontend → Graph Update
                ↑
           PDF Context (RAG)
```

### Core Technologies

- **Frontend**: Vanilla HTML/CSS/JavaScript + Desmos API
- **Backend**: Python Flask + Google Gemini
- **RAG**: PyMuPDF + FAISS + Gemini Embeddings
- **Deployment**: Vercel Serverless Functions

### Key Files by Function

| Function | Files |
|----------|-------|
| **User Interface** | `templates/index.html`, `static/style.css` |
| **Chat Logic** | `static/main.js` |
| **Graph Control** | `static/main.js` (executeGraphCommands) |
| **AI Integration** | `api/index.py` (chat endpoint) |
| **RAG Pipeline** | `api/index.py` (upload_pdf, embeddings) |
| **Deployment** | `vercel.json`, `requirements.txt` |

---

## 📖 Learning Path

### Beginner Path
1. ✅ Read [README.md](README.md)
2. ✅ Set up locally
3. ✅ Try prompts from [TEST_PROMPTS.md](TEST_PROMPTS.md)
4. ✅ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
5. ✅ Deploy to Vercel using [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

### Developer Path
1. ✅ Complete Beginner Path
2. ✅ Read [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
3. ✅ Study [ARCHITECTURE.md](ARCHITECTURE.md)
4. ✅ Experiment with code using [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
5. ✅ Add custom features

### Advanced Path
1. ✅ Complete Developer Path
2. ✅ Optimize performance
3. ✅ Add new AI models
4. ✅ Implement user authentication
5. ✅ Scale beyond free tier

---

## 🛠️ Development Workflow

### Initial Setup
```bash
1. Clone repository
2. Read README.md
3. Run start.ps1 or start.sh
4. Test locally
5. Read documentation
```

### Daily Development
```bash
1. Activate venv
2. Make changes
3. Test locally
4. Check QUICK_REFERENCE.md for snippets
5. Commit and push
```

### Before Deployment
```bash
1. Review DEPLOYMENT_CHECKLIST.md
2. Test all features locally
3. Check requirements.txt
4. Verify environment variables
5. Deploy to Vercel
```

---

## 🎓 Documentation Deep Dive

### README.md
**Length:** ~300 lines  
**Topics:**
- Project overview
- Feature list
- Tech stack
- Local setup (step-by-step)
- Deployment to Vercel
- Usage guide
- API documentation
- Contributing guidelines

**Best for:** New users, setup, deployment

---

### PROJECT_SUMMARY.md
**Length:** ~400 lines  
**Topics:**
- High-level architecture
- Key features breakdown
- Technical decisions explained
- System flow diagrams
- Design rationale
- Extension ideas
- Security considerations

**Best for:** Understanding the "why" behind design choices

---

### IMPLEMENTATION_GUIDE.md
**Length:** ~800 lines  
**Topics:**
- Complete component breakdown
- AI system prompt design
- Graph command system details
- RAG implementation pipeline
- Code walkthroughs
- Testing strategies
- Performance optimization
- Extension examples

**Best for:** Developers building features

---

### ARCHITECTURE.md
**Length:** ~600 lines  
**Topics:**
- ASCII architecture diagrams
- Request flow visualization
- RAG pipeline illustration
- Component interaction maps
- State management diagrams
- Deployment architecture

**Best for:** Visual learners, system design understanding

---

### DEPLOYMENT_CHECKLIST.md
**Length:** ~500 lines  
**Topics:**
- Pre-deployment checklist
- Vercel setup steps
- Environment configuration
- Post-deployment verification
- Troubleshooting guide
- Rollback procedures
- Monitoring setup

**Best for:** DevOps, first-time deployment

---

### TEST_PROMPTS.md
**Length:** ~300 lines  
**Topics:**
- Basic plotting tests
- Mathematical concept tests
- Graph manipulation tests
- Complex scenarios
- RAG tests
- Edge cases
- Performance tests

**Best for:** QA, learning to use the app

---

### QUICK_REFERENCE.md
**Length:** ~400 lines  
**Topics:**
- Common commands
- Environment variables
- API endpoints reference
- Graph commands reference
- Error messages and fixes
- Code snippets
- LaTeX reference

**Best for:** Day-to-day development, troubleshooting

---

## 🔍 Find Information Fast

### "How do I..."

| Question | Document | Section |
|----------|----------|---------|
| Set up locally? | README.md | Local Development Setup |
| Deploy to Vercel? | DEPLOYMENT_CHECKLIST.md | Deployment Methods |
| Add a graph command? | QUICK_REFERENCE.md | Useful Code Snippets |
| Understand RAG? | IMPLEMENTATION_GUIDE.md | RAG Implementation |
| Fix an error? | QUICK_REFERENCE.md | Error Messages |
| Test features? | TEST_PROMPTS.md | All sections |
| Understand flow? | ARCHITECTURE.md | Request Flow |

### "What is..."

| Question | Document | Section |
|----------|----------|---------|
| The system architecture? | ARCHITECTURE.md | System Architecture |
| The tech stack? | README.md | Tech Stack |
| A graph command? | QUICK_REFERENCE.md | Graph Commands |
| The AI prompt? | IMPLEMENTATION_GUIDE.md | AI System Prompt Design |
| The RAG pipeline? | ARCHITECTURE.md | RAG Pipeline |

---

## 📊 Documentation Statistics

| Document | Lines | Words | Purpose |
|----------|-------|-------|---------|
| README.md | ~300 | ~4,000 | User guide |
| PROJECT_SUMMARY.md | ~400 | ~5,000 | Overview |
| IMPLEMENTATION_GUIDE.md | ~800 | ~10,000 | Technical guide |
| ARCHITECTURE.md | ~600 | ~6,000 | Visual reference |
| DEPLOYMENT_CHECKLIST.md | ~500 | ~6,000 | Deployment guide |
| TEST_PROMPTS.md | ~300 | ~3,000 | Testing guide |
| QUICK_REFERENCE.md | ~400 | ~4,000 | Quick reference |
| **Total** | **~3,300** | **~38,000** | Complete docs |

---

## ✅ Document Checklist

Use this to ensure you've read relevant documentation:

### For First-Time Setup
- [ ] README.md (main documentation)
- [ ] .env.example (configure environment)
- [ ] QUICK_REFERENCE.md (common commands)

### For Development
- [ ] PROJECT_SUMMARY.md (understand project)
- [ ] IMPLEMENTATION_GUIDE.md (technical details)
- [ ] ARCHITECTURE.md (system design)
- [ ] QUICK_REFERENCE.md (code snippets)

### For Deployment
- [ ] DEPLOYMENT_CHECKLIST.md (deployment steps)
- [ ] README.md (Vercel section)
- [ ] QUICK_REFERENCE.md (environment variables)

### For Testing
- [ ] TEST_PROMPTS.md (test scenarios)
- [ ] README.md (usage guide)

---

## 🎯 Next Steps

### If you're a **user**:
1. Read [README.md](README.md)
2. Follow setup instructions
3. Try prompts from [TEST_PROMPTS.md](TEST_PROMPTS.md)
4. Enjoy exploring mathematics!

### If you're a **developer**:
1. Read [README.md](README.md)
2. Study [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
3. Review [ARCHITECTURE.md](ARCHITECTURE.md)
4. Start coding with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### If you're **deploying**:
1. Read [README.md](README.md)
2. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
3. Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
4. Monitor your deployment

---

## 🤝 Contributing

Found an issue or want to improve documentation?

1. Check existing documentation
2. Open an issue on GitHub
3. Submit a pull request
4. Follow coding standards in IMPLEMENTATION_GUIDE.md

---

## 📞 Support

- **Documentation Issues:** Check this INDEX.md
- **Setup Help:** See README.md
- **Technical Questions:** See IMPLEMENTATION_GUIDE.md
- **Deployment Issues:** See DEPLOYMENT_CHECKLIST.md
- **Bug Reports:** GitHub Issues

---

## 🌟 Key Achievements

✅ **Comprehensive Documentation**: 7 detailed documents  
✅ **~38,000 words** of documentation  
✅ **Complete coverage**: Setup → Development → Deployment  
✅ **Multiple formats**: Guides, checklists, references, diagrams  
✅ **User-friendly**: Organized, searchable, well-structured  

---

## 📝 Document Version History

- **v1.0** (Oct 2025): Initial comprehensive documentation set
  - README.md
  - PROJECT_SUMMARY.md
  - IMPLEMENTATION_GUIDE.md
  - ARCHITECTURE.md
  - DEPLOYMENT_CHECKLIST.md
  - TEST_PROMPTS.md
  - QUICK_REFERENCE.md
  - INDEX.md

---

**Happy coding! 🚀**

*This project is built with ❤️ for mathematics education and exploration.*

---

## Quick Links

- [🏠 Home](README.md)
- [📖 Summary](PROJECT_SUMMARY.md)
- [🔧 Implementation](IMPLEMENTATION_GUIDE.md)
- [🏗️ Architecture](ARCHITECTURE.md)
- [🚀 Deployment](DEPLOYMENT_CHECKLIST.md)
- [🧪 Testing](TEST_PROMPTS.md)
- [⚡ Quick Ref](QUICK_REFERENCE.md)
