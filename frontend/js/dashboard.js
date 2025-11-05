const API_BASE = 'http://127.0.0.1:5000/api';
const userId = localStorage.getItem('userId') || 'guest_' + Date.now();

document.addEventListener('DOMContentLoaded', () => {
    localStorage.setItem('userId', userId);
    loadDashboard();
});

async function loadDashboard() {
    try {
        const statsRes = await fetch(${API_BASE}/analytics/stats/?user_id=${userId});
        const stats = await statsRes.json();
        
        document.getElementById('totalMessages').textContent = stats.total_messages || 0;
        document.getElementById('crisisCount').textContent = stats.crisis_count || 0;
        document.getElementById('avgTime').textContent = (stats.avg_response_time || 0) + 's';
        document.getElementById('conversations').textContent = stats.total_conversations || 0;
        
        renderEmotions(stats.emotions || {});
        
        const historyRes = await fetch(${API_BASE}/analytics/history/?user_id=${userId}&limit=10);
        const history = await historyRes.json();
        
        renderMessages(history.messages || []);
        
    } catch (error) {
        console.error('Dashboard load error:', error);
    }
}

function renderEmotions(emotions) {
    const container = document.getElementById('emotionChart');
    container.innerHTML = '';
    
    if (Object.keys(emotions).length === 0) {
        container.innerHTML = '<p style="color: #888; grid-column: 1 / -1;">No emotions recorded yet</p>';
        return;
    }
    
    Object.entries(emotions).forEach(([emotion, count]) => {
        const bar = document.createElement('div');
        bar.className = 'emotion-bar';
        bar.innerHTML = 
            <div class="emotion-name">${emotion}</div>
            <div class="emotion-count">${count}</div>
        ;
        container.appendChild(bar);
    });
}

function renderMessages(messages) {
    const container = document.getElementById('messagesList');
    container.innerHTML = '';
    
    if (messages.length === 0) {
        container.innerHTML = '<p style="color: #888;">No messages yet</p>';
        return;
    }
    
    messages.reverse().slice(0, 10).forEach(msg => {
        const time = new Date(msg.timestamp).toLocaleString();
        const item = document.createElement('div');
        item.className = 'message-item';
        item.innerHTML = 
            <div class="message-time">${time}</div>
            <div class="message-text"><strong>You:</strong> ${msg.user_message.substring(0, 80)}...</div>
        ;
        container.appendChild(item);
    });
}

async function exportData(format) {
    try {
        const res = await fetch(${API_BASE}/analytics/export/?user_id=${userId}&format=${format});
        const data = await res.json();
        
        let content, filename;
        
        if (format === 'json') {
            content = JSON.stringify(data, null, 2);
            filename = 
aina-export-${userId}.json;
        } else {
            content = data;
            filename = 
aina-export-${userId}.txt;
        }
        
        const element = document.createElement('a');
        element.setAttribute('href', data:text/plain;charset=utf-8,${encodeURIComponent(content)});
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
        
        alert(\✅ Exported as ${filename}\);
    } catch (error) {
        console.error('Export error:', error);
        alert('❌ Export failed');
    }
}
