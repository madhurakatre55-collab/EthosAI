const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Auto-resize textarea
userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if (this.value === '') this.style.height = 'auto';
});

// Send on Enter (Shift+Enter for newline)
userInput.addEventListener('keydown', function (e) {
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

// Global store for reports to avoid escaping issues in HTML attributes
window.__ethosReports = window.__ethosReports || {};

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

    // Interaction Report Logic
    let contentHTML = '';
    if (sender === 'bot' && isCSV(text)) {
        // Separate CSV data from prose if present
        const csvMatch = text.match(/Sector,Attribute Analyzed,Bias Detected[\s\S]*?(?=\n\nNote:|\nNote:|$)/);
        const csvData = csvMatch ? csvMatch[0] : text;
        const prose = text.replace(csvData, '').trim();

        const reportId = 'report_' + Date.now();
        window.__ethosReports[reportId] = csvData;

        contentHTML = `
            ${prose ? `<div class="prose-box" style="margin-bottom: 12px;">${marked.parse(prose)}</div>` : ''}
            <div class="report-card" onclick="openDashboard('${reportId}')">
                <div class="report-icon-sm">
                    <i class="fa-solid fa-file-invoice"></i>
                </div>
                <div class="report-meta">
                    <h5>Bias Audit Report Ready</h5>
                    <p>Click to open the visual fairness dashboard</p>
                </div>
            </div>
            <p style="font-size: 0.8rem; color: #64748B; margin: 10px 0; font-style: italic;">
                Review the dashboard carefully. If you approve the fixes, type <b>'Update the model'</b>.
            </p>
        `;
    } else {
        contentHTML = sender === 'bot' ? marked.parse(text) : text;
    }

    msgDiv.innerHTML = `
        ${avatarHTML}
        <div class="bubble">${contentHTML}</div>
    `;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// --- DASHBOARD HELPERS ---

let biasChartInstance = null;

function isCSV(text) {
    return text.includes('Sector') && text.includes('Attribute Analyzed') && text.includes('Bias Detected');
}

function openDashboard(reportId) {
    const rawContent = window.__ethosReports[reportId];
    if (!rawContent) return;

    const overlay = document.getElementById('reportOverlay');
    overlay.classList.add('active');

    // CONTEXTUAL TITLE: Audit vs Resolution
    const sheetTitle = document.querySelector('.sheet-header h3');
    if (rawContent.toLowerCase().includes('resolution') || rawContent.toLowerCase().includes('after') || rawContent.toLowerCase().includes('status')) {
        sheetTitle.innerHTML = `<i class="fa-solid fa-circle-check" style="color:#10b981;"></i> EthosAI | Model Resolution Log`;
    } else {
        sheetTitle.innerHTML = `<i class="fa-solid fa-file-invoice" style="color:#7c3aed;"></i> EthosAI | Fairness Audit Report`;
    }

    // Update Timestamp
    document.getElementById('reportTimestamp').textContent = `Generated on ${new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}`;

    // Split Prose from CSV Data Block
    let proseContent = rawContent;
    let csvData = "";

    if (rawContent.includes('--- DOCUMENT END ---')) {
        const parts = rawContent.split('--- DOCUMENT END ---');
        proseContent = parts[0].trim();
        csvData = parts[1].trim();
    } else if (isCSV(rawContent)) {
        // Fallback for older raw CSV reports
        csvData = rawContent;
        proseContent = "# Technical Audit Summary\n\n*Note: This is a legacy raw data report.*";
    }

    // Render the long-form document
    const docContainer = document.getElementById('reportDocument');
    docContainer.innerHTML = marked.parse(proseContent);

    // If technical charts or tables are needed as 'Figures', we can inject them 
    // but for now, the user wants the "explicitly texted" comprehensive report.
    // I'll append the technical table at the very end as an Appendix.
    if (csvData) {
        const appendix = document.createElement('div');
        appendix.style.marginTop = "60px";
        appendix.innerHTML = `
            <hr>
            <h3>Appendix A: Structured Audit Data</h3>
            <p>The following table tracks the technical parity metrics used for automated mitigation.</p>
            ${renderDashboardTable(csvData)}
        `;
        docContainer.appendChild(appendix);

        // Update the global store for automation (Phase 2 needs the CSV)
        window.__ethosReports[reportId] = csvData;
    }
}

function closeDashboard() {
    document.getElementById('reportOverlay').classList.remove('active');
}

function renderDashboardTable(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    let html = '<table class="audit-table"><thead><tr>';
    headers.forEach(h => html += `<th>${h.trim()}</th>`);
    html += '</tr></thead><tbody>';

    for (let i = 1; i < lines.length; i++) {
        const row = lines[i].match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g);
        if (!row) continue;
        html += '<tr>';
        row.forEach((cell, idx) => {
            let val = cell.replace(/^"|"$/g, '').trim();
            if (headers[idx].includes('Bias Detected')) {
                const isYes = val.toLowerCase() === 'yes';
                val = `<span style="color: ${isYes ? '#ef4444' : '#22c55e'}; font-weight: 700;">${val}</span>`;
            }
            html += `<td>${val}</td>`;
        });
        html += '</tr>';
    }
    return html + '</tbody></table>';
}

function exportReport(format) {
    const rawContent = document.getElementById('reportDocument').innerText;
    const reportTimestamp = new Date().toISOString().replace(/[:.]/g, '-');
    let fileName = `EthosAI_Audit_Report_${reportTimestamp}`;
    let blobContent = '';
    let mimeType = '';

    if (format === 'json') {
        const data = {
            project: "EthosAI Audit",
            timestamp: new Date().toLocaleString(),
            report_body: rawContent,
            technical_appendix: window.__ethosReports[Object.keys(window.__ethosReports).pop()]
        };
        blobContent = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
        fileName += '.json';
    } else if (format === 'csv') {
        // Find the last stored CSV from any report session
        blobContent = window.__ethosReports[Object.keys(window.__ethosReports).pop()] || "No CSV data available";
        mimeType = 'text/csv';
        fileName += '.csv';
    } else {
        blobContent = rawContent;
        mimeType = 'text/plain';
        fileName += '.txt';
    }

    const blob = new Blob([blobContent], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
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
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 8px;" id="thinking-text">Processing request...</div>
        </div>
    `;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Dynamically update text based on input
    const inputVal = userInput.value.trim().toLowerCase();
    const hasFile = fileInput.files.length > 0;

    setTimeout(() => {
        const textElement = document.getElementById(id).querySelector('#thinking-text');
        if (hasFile || inputVal.includes('http') || inputVal.includes('.csv')) {
            textElement.textContent = "Running Phase 1 Auditing Crew (Agents 1-3)...";
        } else if (inputVal.includes('update') || inputVal.includes('fix') || inputVal.includes('approve')) {
            textElement.textContent = "Running Phase 2 Execution (Agent 4)...";
        } else {
            textElement.textContent = "Thinking...";
        }
    }, 100);

    return id;
}
