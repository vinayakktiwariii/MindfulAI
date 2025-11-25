// ==================== CONFIGURATION ====================
const API_BASE_URL = 'http://127.0.0.1:8000/api';
let conversationId = null;
let isTyping = false;
let hasStartedChat = false;

// ==================== DOM ELEMENTS ====================
const messagesContainer = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const welcomeState = document.getElementById('welcomeState');
const suggestionChips = document.getElementById('suggestionChips');

// ==================== INITIALIZE ====================
document.addEventListener('DOMContentLoaded', function() {
    // Load previous conversation if exists
    const savedConvId = localStorage.getItem('currentConversationId');
    if (savedConvId) {
        conversationId = savedConvId;
    }
    
    // Setup suggestion chips
    setupSuggestionChips();
    
    // Auto-focus input
    if (messageInput) {
        messageInput.focus();
    }
});

// ==================== SETUP SUGGESTION CHIPS ====================
function setupSuggestionChips() {
    if (suggestionChips) {
        const chips = suggestionChips.querySelectorAll('.suggestion-chip');
        chips.forEach(chip => {
            chip.addEventListener('click', function() {
                const message = this.getAttribute('data-message');
                if (message) {
                    messageInput.value = message;
                    handleSendMessage();
                }
            });
        });
    }
}

// ==================== SEND MESSAGE ====================
async function handleSendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isTyping) return;
    
    // Hide welcome state and suggestions on first message
    if (!hasStartedChat && welcomeState) {
        welcomeState.style.display = 'none';
        hasStartedChat = true;
    }
    
    // Display user message
    displayMessage(message, 'user');
    
    // Clear input and reset height
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });
        
        const data = await response.json();
        
        // Update conversation ID
        if (data.conversation_id && !conversationId) {
            conversationId = data.conversation_id;
            localStorage.setItem('currentConversationId', conversationId);
        }
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Display AI response
        if (data.response) {
            displayMessage(data.response, 'ai');
        }
        
        // Handle crisis detection
        if (data.crisis_detected) {
            displayCrisisAlert();
        }
        
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        displayMessage('Sorry, I encountered an error. Please try again.', 'ai');
    }
}

// ==================== DISPLAY MESSAGE ====================
function displayMessage(text, role) {
    // Remove welcome state if it exists
    if (welcomeState && welcomeState.style.display !== 'none') {
        welcomeState.style.display = 'none';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-animate mb-6';
    
    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="flex items-start justify-end space-x-3">
                <div class="user-message-bubble">${escapeHtml(text)}</div>
                <div class="user-avatar">${getUserInitials()}</div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="ai-avatar">
                    <img src="app-icon-logo-design--minimalist-abstract-symbol--.png" alt="NAINA" class="w-full h-full object-cover rounded-xl">
                </div>
                <div class="ai-message-bubble">${escapeHtml(text)}</div>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// ==================== GET USER INITIALS ====================
function getUserInitials() {
    const user = getCurrentUser();
    if (user && user.fullname) {
        return user.fullname
            .split(' ')
            .map(n => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);
    }
    return 'U';
}

// ==================== ESCAPE HTML ====================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== TYPING INDICATOR ====================
function showTypingIndicator() {
    isTyping = true;
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'flex items-start space-x-3 mb-6';
    typingDiv.innerHTML = `
        <div class="ai-avatar">
            <img src="app-icon-logo-design--minimalist-abstract-symbol--.png" alt="NAINA" class="w-full h-full object-cover rounded-xl">
        </div>
        <div class="bg-white border border-gray-200 px-4 py-3 rounded-2xl">
            <div class="flex space-x-2">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    isTyping = false;
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

// ==================== CRISIS ALERT ====================
function displayCrisisAlert() {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'bg-red-50 border-2 border-red-200 rounded-2xl p-6 mb-6 message-animate';
    alertDiv.innerHTML = `
        <div class="flex items-start space-x-3">
            <svg class="w-6 h-6 text-red-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <div>
                <h4 class="font-bold text-red-900 mb-2">Crisis Support Resources</h4>
                <p class="text-sm text-red-800 mb-3">If you're in crisis, please reach out for immediate help:</p>
                <ul class="text-sm text-red-800 space-y-1">
                    <li><strong>India AASRA:</strong> 9820466726</li>
                    <li><strong>Vandrevala Foundation:</strong> 1860 2662 345</li>
                    <li><strong>Emergency:</strong> 112 / 102</li>
                </ul>
            </div>
        </div>
    `;
    messagesContainer.appendChild(alertDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// ==================== NEW CHAT ====================
const newChatBtn = document.getElementById('newChatBtn');
if (newChatBtn) {
    newChatBtn.addEventListener('click', function() {
        conversationId = null;
        localStorage.removeItem('currentConversationId');
        messagesContainer.innerHTML = '';
        if (welcomeState) {
            welcomeState.style.display = 'block';
        }
        hasStartedChat = false;
        messageInput.focus();
    });
}

// ==================== EVENT LISTENERS ====================
if (sendBtn) {
    sendBtn.addEventListener('click', handleSendMessage);
}

if (messageInput) {
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
}

console.log('✅ Chat.js loaded successfully!');
