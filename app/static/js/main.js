// app/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const messagesContainer = document.getElementById('messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const errorMessage = document.getElementById('error-message');
    const sendButton = document.getElementById('send-button');

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const prompt = userInput.value.trim();
        if (!prompt) {
            showError('Please enter a message');
            return;
        }

        // Add user message to chat
        addMessage(prompt, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';
        hideError();

        // Show typing indicator
        showTypingIndicator();

        try {
            // Disable send button during request
            sendButton.disabled = true;

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error');
            }

            // Add bot response to chat
            addMessage(data.response, 'bot');
        } catch (error) {
            console.error('Chat error:', error);
            showError(error.message || 'Failed to get response. Please try again.');
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            // Hide typing indicator and enable button
            hideTypingIndicator();
            sendButton.disabled = false;
            userInput.focus();
        }
    });

    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = content;
        
        const timestampDiv = document.createElement('div');
        timestampDiv.classList.add('timestamp');
        timestampDiv.textContent = getCurrentTime();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timestampDiv);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showTypingIndicator() {
        typingIndicator.style.display = 'flex';
        messagesContainer.appendChild(typingIndicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        setTimeout(hideError, 5000);
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Focus input on load
    userInput.focus();
    
    // Set initial timestamp
    document.querySelector('.timestamp[data-time="initial"]').textContent = getCurrentTime();
});
