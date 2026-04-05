const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if(this.value === '') this.style.height = 'auto';
});

// Send on Enter (Shift+Enter for newline)
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

const fileInput = document.getElementById('fileInput');
const fileDisplay = document.getElementById('fileDisplay');
const attachBtn = document.getElementById('attachBtn');

attachBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileDisplay.style.display = 'flex';
        fileDisplay.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg> ${fileInput.files[0].name}`;
    } else {
        fileDisplay.style.display = 'none';
        fileDisplay.innerHTML = '';
    }
});

async function sendMessage() {
    const text = userInput.value.trim();
    const file = fileInput.files[0];
    
    if (!text && !file) return;

    // Reset input
    userInput.value = '';
    userInput.style.height = 'auto';
    fileInput.value = '';
    fileDisplay.style.display = 'none';

    // Append User Message
    if (file) {
        appendMessage('user', `**Attached File:** \`${file.name}\`\n\n${text}`);
    } else {
        appendMessage('user', text);
    }

    // Append Thinking Indicator
    const thinkingId = appendThinking();

    const formData = new FormData();
    formData.append('message', text);
    if (file) { formData.append('file', file); }

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        document.getElementById(thinkingId).remove();

        if (data.error) {
            appendMessage('bot', `**Error:** ${data.error}`);
        } else {
            appendMessage('bot', data.response);
        }

    } catch (err) {
        document.getElementById(thinkingId).remove();
        appendMessage('bot', `**Connection Error:** Cannot reach EthosAI backend.`);
    }
}

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;
    
    let avatarHTML = '';
    if (sender === 'bot') {
        avatarHTML = `
            <div class="avatar logo-avatar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="M9 12l2 2 4-4"/>
                </svg>
            </div>`;
    } else {
        avatarHTML = `<div class="avatar user-avatar">U</div>`;
    }

    // Parse Markdown for bot responses using marked.js
    const parsedText = sender === 'bot' ? marked.parse(text) : text;

    msgDiv.innerHTML = `
        ${avatarHTML}
        <div class="bubble">${parsedText}</div>
    `;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendThinking() {
    const id = 'thinking-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = `message bot-message`;
    msgDiv.id = id;
    
    msgDiv.innerHTML = `
        <div class="avatar logo-avatar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <path d="M9 12l2 2 4-4"/>
            </svg>
        </div>
        <div class="bubble">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 8px;">Analyzing across 6 agents... this may take a minute.</div>
        </div>
    `;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}
