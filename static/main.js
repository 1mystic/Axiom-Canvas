// Axiom Canvas - Frontend Logic

// --- 1. INITIALIZE DESMOS CALCULATOR ---
const elt = document.getElementById('calculator');
let calculator; // Declare calculator here, initialize later

// --- 5. INITIALIZATION ---

// Resizable Divider Logic
const dragHandle = document.getElementById('drag-handle');
const chatPanel = document.getElementById('chat-panel');
let isDragging = false;

dragHandle.addEventListener('mousedown', (e) => {
    isDragging = true;
    dragHandle.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    e.preventDefault(); // Prevent text selection
});

document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;

    // Width = Total Window Width - Mouse X Position
    // We resize form the right, so:
    let newWidth = window.innerWidth - e.clientX;

    // Bounds Check (CSS handles min/max-width too, but good to clamp here)
    if (newWidth < 300) newWidth = 300;
    if (newWidth > window.innerWidth * 0.7) newWidth = window.innerWidth * 0.7;

    chatPanel.style.width = `${newWidth}px`;

    // Notify Desmos to resize
    if (calculator) calculator.resize();
});

document.addEventListener('mouseup', () => {
    if (isDragging) {
        isDragging = false;
        dragHandle.classList.remove('dragging');
        document.body.style.cursor = 'default';
        if (calculator) calculator.resize();
    }
});

// Init
calculator = Desmos.GraphingCalculator(elt, {
    keypad: true,
    expressions: true,
    settingsMenu: true,
    zoomButtons: true,
    invertedColors: true, // Dark mode default
    xAxisLabel: 'x',
    yAxisLabel: 'y'
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
            currentExpressions: currentExpressions,
            ...(userApiConfig && userApiConfig.apiKey
                ? { userApiConfig: { provider: userApiConfig.provider, model: userApiConfig.model, apiKey: userApiConfig.apiKey } }
                : {})
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
            addMessage(`Error: ${data.chatResponse || 'Unknown error'} `, 'ai error');
            updateConnectionStatus(true);
        }

    } catch (error) {
        removeThinking(thinkingId);
        console.error('Chat Error:', error);
        addMessage("Sorry, I couldn't connect to the server. Please check your connection.", 'ai error');
        updateConnectionStatus(true);
    }
}

function addMessage(markdownText, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender} `;

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

// --- 7. API KEY SETTINGS ---

let userApiConfig = null;

const PROVIDER_MODELS = {
    // Native Gemini API — model names per https://ai.google.dev/gemini-api/docs/models
    gemini: [
        { value: '',                        label: '— Default (gemini-2.5-flash) —' },
        { value: 'gemini-2.5-flash',        label: 'Gemini 2.5 Flash ★ Recommended' },
        { value: 'gemini-2.5-flash-lite',   label: 'Gemini 2.5 Flash-Lite (fastest)' },
        { value: 'gemini-2.5-pro',          label: 'Gemini 2.5 Pro (most capable)' },
        { value: 'gemini-2.0-flash',        label: 'Gemini 2.0 Flash (deprecated)' },
        { value: '__custom__',              label: 'Custom model…' },
    ],
    // Native OpenAI API — model names per https://platform.openai.com/docs/models
    openai: [
        { value: '',              label: '— Default (gpt-4o-mini) —' },
        { value: 'gpt-4o-mini',  label: 'GPT-4o Mini' },
        { value: 'gpt-4o',       label: 'GPT-4o' },
        { value: 'gpt-4.1-nano', label: 'GPT-4.1 Nano (fastest/cheapest)' },
        { value: 'gpt-4.1-mini', label: 'GPT-4.1 Mini' },
        { value: 'gpt-4.1',      label: 'GPT-4.1' },
        { value: 'o4-mini',      label: 'o4-mini (reasoning)' },
        { value: '__custom__',   label: 'Custom model…' },
    ],
    // Native Anthropic API — model IDs per https://docs.anthropic.com/en/about-claude/models/overview
    anthropic: [
        { value: '',                         label: '— Default (claude-sonnet-4-6) —' },
        { value: 'claude-sonnet-4-6',        label: 'Claude Sonnet 4.6 ★ Recommended' },
        { value: 'claude-opus-4-6',          label: 'Claude Opus 4.6 (most capable)' },
        { value: 'claude-haiku-4-5',         label: 'Claude Haiku 4.5 (fastest)' },
        { value: '__custom__',               label: 'Custom model…' },
    ],
    // OpenRouter — provider/model format per https://openrouter.ai/docs
    openrouter: [
        { value: '',                                              label: '— Default (openai/gpt-4o-mini) —' },
        // Free models
        { value: 'google/gemini-2.0-flash-lite-001',             label: 'Gemini 2.0 Flash Lite (Free)' },
        { value: 'meta-llama/llama-3.3-70b-instruct:free',       label: 'Llama 3.3 70B (Free)' },
        { value: 'deepseek/deepseek-r1-distill-llama-70b:free',  label: 'DeepSeek R1 Distill 70B (Free)' },
        { value: 'microsoft/phi-3-medium-128k-instruct:free',    label: 'Phi-3 Medium (Free)' },
        // Paid models
        { value: 'openai/gpt-4.1-nano',                          label: 'GPT-4.1 Nano (Paid)' },
        { value: 'openai/gpt-4o-mini',                           label: 'GPT-4o Mini (Paid)' },
        { value: 'openai/gpt-4o',                                label: 'GPT-4o (Paid)' },
        { value: 'google/gemini-2.5-flash',                      label: 'Gemini 2.5 Flash (Paid)' },
        { value: 'anthropic/claude-3.5-sonnet',                  label: 'Claude 3.5 Sonnet (Paid)' },
        { value: '__custom__',                                   label: 'Custom model…' },
    ],
    aipipe: [
        // AiPipe token from aipipe.org/login — provider/model format → /openrouter/v1.
        // Plain OpenAI names (no slash) → /openai/v1. See aipipe.org/playground for all models.
        { value: '',                                              label: '— Default (openai/gpt-4.1-nano) —' },
        // OpenAI via OpenRouter proxy
        { value: 'openai/gpt-4.1-nano',                          label: 'GPT-4.1 Nano ★ Recommended' },
        { value: 'openai/gpt-4.1-mini',                          label: 'GPT-4.1 Mini' },
        { value: 'openai/gpt-4o-mini',                           label: 'GPT-4o Mini' },
        { value: 'openai/gpt-4o',                                label: 'GPT-4o' },
        // Google via OpenRouter proxy (confirmed IDs per aipipe docs)
        { value: 'google/gemini-2.0-flash-lite-001',             label: 'Gemini 2.0 Flash Lite' },
        { value: 'google/gemini-2.5-flash',                      label: 'Gemini 2.5 Flash' },
        { value: 'google/gemini-2.5-pro',                        label: 'Gemini 2.5 Pro' },
        // Anthropic via OpenRouter proxy
        { value: 'anthropic/claude-3.5-sonnet',                  label: 'Claude 3.5 Sonnet' },
        { value: 'anthropic/claude-3.5-haiku',                   label: 'Claude 3.5 Haiku' },
        // Free models via OpenRouter proxy
        { value: 'meta-llama/llama-3.3-70b-instruct:free',       label: 'Llama 3.3 70B (Free)' },
        { value: 'deepseek/deepseek-r1-distill-llama-70b:free',  label: 'DeepSeek R1 Distill 70B (Free)' },
        { value: '__custom__',                                    label: 'Custom model…' },
    ],
};

function loadApiConfig() {
    try {
        const saved = localStorage.getItem('axiom_api_config');
        if (saved) {
            userApiConfig = JSON.parse(saved);
            updateApiKeyIndicator();
        }
    } catch (e) { userApiConfig = null; }
}

function saveApiConfig(config) {
    try { localStorage.setItem('axiom_api_config', JSON.stringify(config)); } catch (e) {}
}

function clearApiConfig() {
    try { localStorage.removeItem('axiom_api_config'); } catch (e) {}
    userApiConfig = null;
    updateApiKeyIndicator();
}

function updateApiKeyIndicator() {
    const btn = document.getElementById('api-key-btn');
    const banner = document.getElementById('api-active-banner');
    if (!btn) return;
    if (userApiConfig && userApiConfig.apiKey) {
        btn.classList.add('active');
        if (banner) banner.style.display = 'flex';
    } else {
        btn.classList.remove('active');
        if (banner) banner.style.display = 'none';
    }
}

function setupApiKeyModal() {
    const btn         = document.getElementById('api-key-btn');
    const overlay     = document.getElementById('api-modal-overlay');
    const closeBtn    = document.getElementById('api-modal-close');
    const saveBtn     = document.getElementById('api-key-save');
    const clearBtn    = document.getElementById('api-key-clear');
    const providerSel = document.getElementById('api-provider');
    const modelSel    = document.getElementById('api-model');
    const modelCustom = document.getElementById('api-model-custom');
    const modelGroup  = document.getElementById('model-group');
    const keyInput    = document.getElementById('api-key-input');

    function populateModels(provider, savedModel) {
        const options = PROVIDER_MODELS[provider] || [];
        modelSel.innerHTML = '';

        if (!provider || options.length === 0) {
            modelGroup.style.display = 'none';
            return;
        }
        modelGroup.style.display = 'flex';

        options.forEach(opt => {
            const el = document.createElement('option');
            el.value = opt.value;
            el.textContent = opt.label;
            modelSel.appendChild(el);
        });

        // Restore saved model selection
        const match = savedModel && Array.from(modelSel.options).find(o => o.value === savedModel);
        if (match) {
            modelSel.value = savedModel;
            modelCustom.style.display = 'none';
        } else if (savedModel) {
            modelSel.value = '__custom__';
            modelCustom.value = savedModel;
            modelCustom.style.display = 'block';
        } else {
            modelSel.value = '';
            modelCustom.style.display = 'none';
        }
    }

    function getSelectedModel() {
        return modelSel.value === '__custom__' ? modelCustom.value.trim() : modelSel.value;
    }

    // Toggle custom input when "Custom model…" is picked
    modelSel.addEventListener('change', () => {
        modelCustom.style.display = modelSel.value === '__custom__' ? 'block' : 'none';
        if (modelSel.value === '__custom__') modelCustom.focus();
    });

    // Open
    btn.addEventListener('click', () => {
        const cfg = userApiConfig || {};
        providerSel.value = cfg.provider || '';
        keyInput.value    = cfg.apiKey   || '';
        populateModels(cfg.provider || '', cfg.model || '');
        updateApiKeyIndicator();
        overlay.classList.add('visible');
    });

    // Close
    closeBtn.addEventListener('click', () => overlay.classList.remove('visible'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('visible'); });

    // Provider change
    providerSel.addEventListener('change', () => populateModels(providerSel.value, ''));

    // Save
    saveBtn.addEventListener('click', () => {
        const provider = providerSel.value;
        const model    = getSelectedModel();
        const apiKey   = keyInput.value.trim();

        if (!provider) {
            clearApiConfig();
            overlay.classList.remove('visible');
            return;
        }
        if (!apiKey) {
            keyInput.focus();
            keyInput.style.borderColor = '#ef4444';
            setTimeout(() => keyInput.style.borderColor = '', 1500);
            return;
        }
        userApiConfig = { provider, model, apiKey };
        saveApiConfig(userApiConfig);
        updateApiKeyIndicator();
        overlay.classList.remove('visible');
    });

    // Clear
    clearBtn.addEventListener('click', () => {
        clearApiConfig();
        providerSel.value = '';
        keyInput.value    = '';
        populateModels('', '');
        overlay.classList.remove('visible');
    });
}

// Init API key feature
loadApiConfig();
setupApiKeyModal();
