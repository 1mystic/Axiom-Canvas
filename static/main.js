// Global Variables
let calculator;
let sessionId = generateSessionId();
let conversationHistory = [];

// Initialize Desmos Calculator
function initializeCalculator() {
    const element = document.getElementById('calculator');
    calculator = Desmos.GraphingCalculator(element, {
        expressionsCollapsed: false,
        settingsMenu: true,
        zoomButtons: true,
        expressions: true,
        keypad: true,
        graphpaper: true,
        lockViewport: false,
        invertedColors: false
    });
    
    // Set default viewport
    calculator.setMathBounds({
        left: -10,
        right: 10,
        bottom: -10,
        top: 10
    });
    
    console.log('Desmos calculator initialized');
}

// Generate a unique session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Simple Markdown to HTML converter
function markdownToHtml(text) {
    // Escape HTML to prevent XSS
    let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Convert markdown to HTML
    html = html
        // Bold: **text** or __text__ (non-greedy)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.+?)__/g, '<strong>$1</strong>')
        // Italic: *text* or _text_ (but not inside bold)
        .replace(/(?<!\*)\*([^*]+?)\*(?!\*)/g, '<em>$1</em>')
        .replace(/(?<!_)_([^_]+?)_(?!_)/g, '<em>$1</em>')
        // Inline code: `code`
        .replace(/`([^`]+?)`/g, '<code>$1</code>');
    
    // Numbered lists: 1. item, 2. item, etc.
    html = html.replace(/^(\d+)\.\s+(.+)$/gm, '<div class="list-item numbered">$1. $2</div>');
    
    // Bullet lists: - item or * item
    html = html.replace(/^[-*]\s+(.+)$/gm, '<div class="list-item">• $1</div>');
    
    // Line breaks (convert remaining newlines to <br>)
    html = html.replace(/\n/g, '<br>');
    
    return html;
}

// Add message to chat
function addMessage(text, type = 'user') {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'user' ? 'U' : 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Use innerHTML for AI messages to render markdown, textContent for user messages for security
    if (type === 'ai') {
        content.innerHTML = markdownToHtml(text);
    } else {
        content.textContent = text;
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    // Render LaTeX for AI messages after adding to DOM
    if (type === 'ai') {
        setTimeout(() => {
            if (typeof renderMathInElement !== 'undefined') {
                renderMathInElement(content, {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\[', right: '\\]', display: true},
                        {left: '\\(', right: '\\)', display: false}
                    ],
                    throwOnError: false
                });
            }
        }, 10);
    }
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Add error message
function addErrorMessage(text) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message error';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '!';
    avatar.style.background = '#dc2626';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Show/hide loading indicator
function setLoading(isLoading) {
    const loadingIndicator = document.getElementById('loading-indicator');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    
    if (isLoading) {
        loadingIndicator.style.display = 'flex';
        sendBtn.disabled = true;
        chatInput.disabled = true;
    } else {
        loadingIndicator.style.display = 'none';
        sendBtn.disabled = false;
        chatInput.disabled = false;
    }
}

// Execute graph commands
function executeGraphCommands(commands) {
    if (!commands || !Array.isArray(commands)) {
        console.log('No graph commands to execute');
        return;
    }
    
    console.log('Executing graph commands:', commands);
    
    commands.forEach(cmd => {
        try {
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
                    // Get all expressions and remove them
                    const state = calculator.getState();
                    state.expressions.list.forEach(expr => {
                        calculator.removeExpression({ id: expr.id });
                    });
                    break;
                    
                case 'setBlank':
                    calculator.setBlank();
                    break;
                    
                default:
                    console.warn('Unknown graph command:', cmd.command);
            }
        } catch (error) {
            console.error('Error executing graph command:', cmd, error);
        }
    });
}

// Send message to backend
async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    conversationHistory.push({ role: 'user', content: message });
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // Show loading
    setLoading(true);
    
    try {
        // Get current graph state
        const graphState = calculator.getState();
        const currentExpressions = graphState.expressions.list
            .filter(expr => expr.type === 'expression' && expr.latex)
            .map(expr => ({
                id: expr.id,
                latex: expr.latex,
                color: expr.color
            }));
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                sessionId: sessionId,
                history: conversationHistory.slice(-10), // Send last 10 messages
                currentExpressions: currentExpressions // Send current graph state
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display AI response
        if (data.chatResponse) {
            addMessage(data.chatResponse, 'ai');
            conversationHistory.push({ role: 'assistant', content: data.chatResponse });
        }
        
        // Execute graph commands
        if (data.graphCommands) {
            executeGraphCommands(data.graphCommands);
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        addErrorMessage('Sorry, something went wrong. Please try again.');
    } finally {
        setLoading(false);
        chatInput.focus();
    }
}

// Handle PDF upload
async function handlePdfUpload(file) {
    const uploadStatus = document.getElementById('upload-status');
    uploadStatus.textContent = 'Uploading...';
    
    const formData = new FormData();
    formData.append('pdf', file);
    formData.append('sessionId', sessionId);
    
    try {
        const response = await fetch('/api/upload_pdf', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            uploadStatus.textContent = `✓ ${file.name} uploaded`;
            uploadStatus.style.color = '#059669';
            addMessage(`PDF "${file.name}" has been uploaded and processed. You can now ask questions about its content!`, 'ai');
            
            // Clear status after 3 seconds
            setTimeout(() => {
                uploadStatus.textContent = '';
            }, 3000);
        } else {
            throw new Error(data.error || 'Upload failed');
        }
        
    } catch (error) {
        console.error('Error uploading PDF:', error);
        uploadStatus.textContent = '✗ Upload failed';
        uploadStatus.style.color = '#dc2626';
        addErrorMessage('Failed to upload PDF. Please try again.');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Desmos
    initializeCalculator();
    
    // Send button click
    const sendBtn = document.getElementById('send-btn');
    sendBtn.addEventListener('click', sendMessage);
    
    // Enter key to send (Shift+Enter for new line)
    const chatInput = document.getElementById('chat-input');
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Upload button click
    const uploadBtn = document.getElementById('upload-btn');
    const pdfUpload = document.getElementById('pdf-upload');
    
    uploadBtn.addEventListener('click', () => {
        pdfUpload.click();
    });
    
    pdfUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file && file.type === 'application/pdf') {
            handlePdfUpload(file);
        } else if (file) {
            addErrorMessage('Please upload a valid PDF file.');
        }
        // Reset input
        e.target.value = '';
    });
    
    // Welcome message
    setTimeout(() => {
        addMessage('Hello! I\'m Axiom Canvas, your AI math visualizer. Ask me to plot functions, explain concepts, or help with math problems. I can use the graph to show you visual explanations!', 'ai');
    }, 500);
});
