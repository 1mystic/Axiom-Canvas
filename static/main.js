// Axiom Canvas - Frontend Logic

// --- 1. INITIALIZE DESMOS CALCULATOR ---
const elt = document.getElementById('calculator');
const calculator = Desmos.GraphingCalculator(elt, {
    keypad: true,
    graphpaper: true,
    expressions: true,
    settingsMenu: true,
    zoomButtons: true,
    expressionsCollapsed: false,
    invertedColors: true, // Dark mode for Desmos
    xAxisLabel: 'x',
    yAxisLabel: 'y',
});

// Configure default view
calculator.setMathBounds({
    left: -10,
    right: 10,
    bottom: -10,
    top: 10
});

// --- 2. CHAT & STATE MANAGEMENT ---
let conversationHistory = [];
let sessionId = Date.now().toString(); // Simple session ID

const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('chat-messages');
const uploadBtn = document.getElementById('upload-btn');
const pdfInput = document.getElementById('pdf-upload');

// --- 3. EVENT LISTENERS ---

// Auto-resize textarea
chatInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    sendBtn.disabled = this.value.trim() === '';
});

// Send on Enter (Shift+Enter for new line)
chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

// PDF Upload
uploadBtn.addEventListener('click', () => pdfInput.click());
pdfInput.addEventListener('change', handleFileUpload);


// --- 4. CORE FUNCTIONS ---

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // UI: Add User Message
    addMessage(text, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';
    sendBtn.disabled = true;

    // Show Thinking Bubble
    const thinkingId = showThinking();

    try {
        // Collect current graph state to give context to AI
        const currentExpressions = calculator.getExpressions();

        // Prepare payload
        const payload = {
            message: text,
            sessionId: sessionId,
            history: conversationHistory,
            currentExpressions: currentExpressions
        };

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Remove Thinking Bubble
        removeThinking(thinkingId);

        if (response.ok) {
            // UI: Add AI Response
            addMessage(data.chatResponse, 'ai');

            // Execute Graph Commands
            if (data.graphCommands && data.graphCommands.length > 0) {
                executeGraphCommands(data.graphCommands);
            }

            // Update History
            conversationHistory.push({ role: 'user', content: text });
            conversationHistory.push({ role: 'model', content: data.chatResponse });

            updateConnectionStatus(false);
        } else {
            addMessage(`Error: ${data.chatResponse || 'Unknown error'}`, 'ai error');
            updateConnectionStatus(true);
        }

    } catch (error) {
        console.error('Chat Error:', error);
        addMessage("Sorry, I couldn't connect to the server. Please check your connection.", 'ai error');
        updateConnectionStatus(true);
    } finally {
        setLoading(false);
    }
}

function addMessage(markdownText, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    // Avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    const img = document.createElement('img');
    img.src = sender === 'user'
        ? 'https://ui-avatars.com/api/?name=User&background=0D8ABC&color=fff' // Placeholder for user
        : '/static/axiom_icon.svg'; // AI Icon
    avatarDiv.appendChild(img);

    // Content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Parse Markdown & Math
    if (sender === 'ai' || sender === 'ai error') {
        // 1. Render Markdown
        let htmlContent = marked.parse(markdownText);
        contentDiv.innerHTML = htmlContent;

        // 2. Render Math (KaTeX)
        renderMathInElement(contentDiv, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '\\(', right: '\\)', display: false },
                { left: '\\[', right: '\\]', display: true }
            ],
            throwOnError: false
        });

        // 3. Highlight Code
        contentDiv.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });

    } else {
        contentDiv.textContent = markdownText;
    }

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function executeGraphCommands(commands) {
    const validCommands = commands.filter(c => c && c.command);
    if (validCommands.length === 0) return;

    console.log("Executing Commands:", validCommands);

    validCommands.forEach(cmd => {
        try {
            switch (cmd.command) {
                case 'setExpression':
                    calculator.setExpression(cmd.params);
                    break;
                case 'removeExpression':
                    if (cmd.params.id) calculator.removeExpression(cmd.params);
                    break;
                case 'setMathBounds':
                    calculator.setMathBounds(cmd.params);
                    break;
                case 'setBlank':
                case 'clearExpressions':
                    calculator.setBlank();
                    break;
                default:
                    console.warn("Unknown command:", cmd.command);
            }
        } catch (e) {
            console.error("Graph Command Error:", e);
        }
    });
}

// --- 5. PDF UPLOAD LOGIC ---
async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const statusDiv = document.getElementById('upload-status');
    statusDiv.textContent = "Uploading & Analyzing PDF...";
    statusDiv.style.color = "var(--accent)";

    const formData = new FormData();
    formData.append('pdf', file);
    formData.append('sessionId', sessionId);

    try {
        const res = await fetch('/api/upload_pdf', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        if (data.success) {
            statusDiv.textContent = `✓ Uploaded: ${file.name} (${data.chunks} chunks)`;
            statusDiv.style.color = "#10b981";
            addMessage(`I've uploaded **${file.name}**. You can now ask questions about its content!`, 'ai');
            conversationHistory.push({ role: 'system', content: `User uploaded PDF: ${file.name}` });
        } else {
            statusDiv.textContent = `Error: ${data.error}`;
            statusDiv.style.color = "#ef4444";
        }
    } catch (err) {
        console.error(err);
        statusDiv.textContent = "Upload failed.";
        statusDiv.style.color = "#ef4444";
    }
}

// --- 6. UTILITIES ---
function showThinking() {
    const id = 'thinking-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai thinking';
    messageDiv.id = id;

    // Avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    const img = document.createElement('img');
    img.src = '/static/axiom_icon.svg';
    avatarDiv.appendChild(img);

    // Content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = `
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
        <span>Thinking...</span>
    `;

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return id;
}

function removeThinking(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function updateConnectionStatus(isError) {
    const badge = document.getElementById('connection-status');
    const text = badge.querySelector('.status-text');
    if (isError) {
        badge.classList.remove('connected');
        badge.style.borderColor = '#ef4444';
        badge.style.color = '#ef4444';
        text.textContent = 'Offline';
    } else {
        badge.classList.add('connected');
        badge.style.borderColor = 'rgba(16, 185, 129, 0.2)';
        badge.style.color = '#10b981';
        text.textContent = 'Online';
    }
}
