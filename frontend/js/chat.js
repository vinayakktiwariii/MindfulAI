// chat.js - NAINA v5.0 Production with Theme Support
const API_URL = 'https://mindfulai-arqonx-ai.up.railway.app/api/chat/chat/';
const HEALTH_URL = 'https://mindfulai-arqonx-ai.up.railway.app/api/chat/health/';
const API_BASE = 'https://mindfulai-arqonx-ai.up.railway.app/api';

let userId = 'user_' + Date.now();
let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 NAINA v5.0 Initializing...');
    
    initElements();
    setupListeners();
    loadWelcome();
    checkHealth();
    
    localStorage.setItem('userId', userId);
    
    console.log('✅ NAINA Ready');
});

const els = {};

function initElements() {
    els.messagesContainer = document.getElementById('messagesContainer');
    els.messageInput = document.getElementById('messageInput');
    els.sendBtn = document.getElementById('sendBtn');
    els.newChatBtn = document.getElementById('newChatBtn');
    els.settingsBtn = document.getElementById('settingsBtn');
    els.helpBtn = document.getElementById('helpBtn');
    els.chatHistory = document.getElementById('chatHistory');
}

function setupListeners() {
    els.sendBtn.addEventListener('click', sendMessage);
    els.messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    els.messageInput.addEventListener('input', autoResize);
    els.newChatBtn.addEventListener('click', newChat);
}

function autoResize(e) {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 100) + 'px';
}

function addMessage(role, text) {
    const msg = document.createElement('div');
    msg.className = `message ${role}`;
    
    const time = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const avatarBg = role === 'bot' 
        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
        : 'var(--bg-tertiary)';
    
    const avatarText = role === 'bot' ? 'N' : 'U';
    
    msg.innerHTML = `
        <div class="message-avatar" style="background: ${avatarBg};">${avatarText}</div>
        <div class="message-body">
            <div class="message-text">${escapeHtml(text)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    els.messagesContainer.appendChild(msg);
    els.messagesContainer.scrollTop = els.messagesContainer.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showTyping() {
    const typing = document.createElement('div');
    typing.className = 'message bot';
    typing.id = 'typing';
    typing.innerHTML = `
        <div class="message-avatar" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">N</div>
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
    `;
    els.messagesContainer.appendChild(typing);
    els.messagesContainer.scrollTop = els.messagesContainer.scrollHeight;
}

function hideTyping() {
    const typing = document.getElementById('typing');
    if (typing) typing.remove();
}

async function sendMessage() {
    const text = els.messageInput.value.trim();
    if (!text || isLoading) return;
    
    isLoading = true;
    addMessage('user', text);
    els.messageInput.value = '';
    els.messageInput.style.height = 'auto';
    showTyping();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, user_id: userId })
        });
        
        hideTyping();
        
        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        
        const data = await response.json();
        addMessage('bot', data.response);
        
    } catch (error) {
        hideTyping();
        console.error('Error:', error);
        addMessage('bot', '❌ Error connecting to server. Please ensure the backend is running.');
    } finally {
        isLoading = false;
        els.messageInput.focus();
    }
}

function loadWelcome() {
    addMessage('bot', `Hello! I'm NAINA, your AI mental wellness companion. I'm here to listen, understand your emotions, and provide support.

Whether you're dealing with stress, anxiety, or just need someone to talk to, I'm here for you. Our conversations are safe, private, and judgment-free.

How are you feeling today?`);
}

function newChat() {
    if (confirm('Start new conversation?')) {
        els.messagesContainer.innerHTML = '';
        userId = 'user_' + Date.now();
        localStorage.setItem('userId', userId);
        loadWelcome();
    }
}

async function checkHealth() {
    try {
        const response = await fetch(HEALTH_URL);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Server online:', data);
        }
    } catch (e) {
        console.warn('⚠️ Server offline');
    }
}

// Mobile Sidebar Toggle
const hamburgerBtn = document.getElementById('hamburgerBtn');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

if (hamburgerBtn) {
    hamburgerBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
        hamburgerBtn.classList.toggle('active');
    });
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarOverlay.classList.remove('active');
        hamburgerBtn.classList.remove('active');
    });
}

// Close sidebar when clicking on a link (mobile)
if (window.innerWidth <= 768) {
    document.querySelectorAll('.sidebar a, .sidebar button').forEach(el => {
        el.addEventListener('click', () => {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            hamburgerBtn.classList.remove('active');
        });
    });
}
