// ==================== DASHBOARD ANALYTICS ====================

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

// ==================== INITIALIZE DASHBOARD ====================
function initializeDashboard() {
    loadDashboardStats();
    animateProgressBars();
    animateCharts();
}

// ==================== LOAD DASHBOARD STATS ====================
async function loadDashboardStats() {
    try {
        // TODO: Replace with actual API endpoint
        const response = await fetch('http://127.0.0.1:8000/api/analytics/stats/');
        const data = await response.json();
        
        updateStats(data);
    } catch (error) {
        console.error('Error loading stats:', error);
        
        // Use mock data for now
        const mockData = {
            total_conversations: 24,
            active_days: 18,
            average_mood: 7.8,
            wellness_score: 85,
            mood_trend: 12,
            activity_trend: 8
        };
        
        updateStats(mockData);
    }
}

// ==================== UPDATE STATS ====================
function updateStats(data) {
    // Update stat values with animation
    animateValue('totalConversations', 0, data.total_conversations, 1000);
    animateValue('activeDays', 0, data.active_days, 1000);
    animateValue('averageMood', 0, data.average_mood, 1000, 1);
    animateValue('wellnessScore', 0, data.wellness_score, 1000);
}

// ==================== ANIMATE VALUE ====================
function animateValue(elementId, start, end, duration, decimals = 0) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = decimals > 0 ? current.toFixed(decimals) : Math.floor(current);
    }, 16);
}

// ==================== ANIMATE PROGRESS BARS ====================
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });
}

// ==================== ANIMATE CHARTS ====================
function animateCharts() {
    const bars = document.querySelectorAll('.bar');
    
    bars.forEach((bar, index) => {
        const targetHeight = bar.style.height;
        bar.style.height = '0%';
        
        setTimeout(() => {
            bar.style.height = targetHeight;
        }, 100 + (index * 50));
    });
}

// ==================== LOAD RECENT ACTIVITY ====================
async function loadRecentActivity() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/analytics/activity/');
        const activities = await response.json();
        
        displayActivities(activities);
    } catch (error) {
        console.error('Error loading activity:', error);
    }
}

// ==================== DISPLAY ACTIVITIES ====================
function displayActivities(activities) {
    const activityList = document.getElementById('activityList');
    if (!activityList) return;
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-icon ${activity.type === 'chat' ? 'coral' : 'mint'}">
                ${getActivityIcon(activity.type)}
            </div>
            <div class="activity-content">
                <p class="activity-title">${activity.title}</p>
                <p class="activity-description">${activity.description}</p>
                <p class="activity-time">${formatTime(activity.timestamp)}</p>
            </div>
        </div>
    `).join('');
}

// ==================== GET ACTIVITY ICON ====================
function getActivityIcon(type) {
    const icons = {
        chat: '<svg class="w-5 h-5" style="color: #ff6b6b;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>',
        mood: '<svg class="w-5 h-5" style="color: #4ecdc4;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>',
        achievement: '<svg class="w-5 h-5" style="color: #ff6b6b;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
    };
    
    return icons[type] || icons.chat;
}

// ==================== FORMAT TIME ====================
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 60) return `${minutes} minutes ago`;
    if (hours < 24) return `${hours} hours ago`;
    return `${days} days ago`;
}

console.log('✅ Dashboard.js loaded successfully!');
