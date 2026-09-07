document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('qa-form');
    const input = document.getElementById('query-input');
    const chatHistory = document.getElementById('chat-history');
    const citationsList = document.getElementById('citations-list');
    const evidenceStatus = document.getElementById('evidence-status');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = input.value.trim();
        if (!query) return;

        // Add user message
        addMessage(query, 'user-message');
        input.value = '';
        input.disabled = true;
        submitBtn.disabled = true;

        // Show loading
        const loadingId = addLoadingIndicator();
        citationsList.innerHTML = '<div class="empty-state">Searching rulebook...</div>';
        evidenceStatus.textContent = 'Searching...';

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            
            // Remove loading
            document.getElementById(loadingId).remove();

            // Add system response
            addSystemMessage(data);

            // Update citations panel
            updateCitations(data.retrieved_chunks);
            evidenceStatus.textContent = `${data.retrieved_chunks.length} chunks analyzed`;

        } catch (error) {
            document.getElementById(loadingId).remove();
            addMessage('Sorry, an error occurred while connecting to the server.', 'system-message');
            citationsList.innerHTML = '<div class="empty-state">Error retrieving evidence.</div>';
            evidenceStatus.textContent = 'Error';
        } finally {
            input.disabled = false;
            submitBtn.disabled = false;
            input.focus();
        }
    });

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        div.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addSystemMessage(data) {
        const div = document.createElement('div');
        div.className = 'message system-message';
        
        let statusTag = '';
        if (data.status === 'answered') statusTag = '<span class="status-tag status-answered">Answered</span><br>';
        else if (data.status === 'conflict') statusTag = '<span class="status-tag status-conflict">Conflict Detected</span><br>';
        else if (data.status === 'not_covered') statusTag = '<span class="status-tag status-not_covered">Not Covered</span><br>';
        else if (data.status === 'error') statusTag = '<span class="status-tag status-error">Error</span><br>';

        let citationsHtml = '';
        if (data.citations && data.citations.length > 0) {
            citationsHtml = `
                <div class="citations-footer">
                    <strong>Sources Used:</strong>
                    <ul>
                        ${data.citations.map(c => `<li>${escapeHtml(c)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        const answerHtml = escapeHtml(data.answer).replace(/\n/g, '<br>');

        div.innerHTML = `
            <div class="bubble">
                ${statusTag}
                ${answerHtml}
                ${citationsHtml}
            </div>
        `;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function addLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'message system-message';
        div.innerHTML = `
            <div class="bubble" style="background: transparent; border: none; box-shadow: none;">
                <div class="loading-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        `;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return id;
    }

    function updateCitations(chunks) {
        if (!chunks || chunks.length === 0) {
            citationsList.innerHTML = '<div class="empty-state">No relevant sections found in the rulebook.</div>';
            return;
        }

        citationsList.innerHTML = chunks.map(chunk => `
            <div class="citation-card">
                <div class="citation-header">
                    <div class="citation-title">${escapeHtml(chunk.file)} - ${escapeHtml(chunk.section)}</div>
                    <div class="citation-score">${(chunk.score * 100).toFixed(1)}% match</div>
                </div>
                <div class="citation-text">${escapeHtml(chunk.text)}</div>
            </div>
        `).join('');
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
