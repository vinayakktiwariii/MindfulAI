const API_BASE = 'http://127.0.0.1:5000/api';
const userId = localStorage.getItem('userId') || 'guest_' + Date.now();

document.addEventListener('DOMContentLoaded', loadInsights);

async function loadInsights() {
    try {
        // Load insights
        const insightsRes = await fetch(`${API_BASE}/analytics/insights/?user_id=${userId}`);
        const insights = await insightsRes.json();
        
        // Load context
        const contextRes = await fetch(`${API_BASE}/analytics/context/?user_id=${userId}`);
        const context = await contextRes.json();
        
        // Render insights
        renderTrajectory(insights);
        renderThemes(insights.primary_themes || {});
        renderIntents(insights.primary_intents || {});
        renderRecommendations(insights.recommendations || []);
        renderStats(context);
        
    } catch (error) {
        console.error('Insights load error:', error);
        document.body.innerHTML = '<p style="padding: 20px; color: #888;">No insights available yet. Start chatting to generate insights!</p>';
    }
}

function renderTrajectory(insights) {
    const trajectoryDiv = document.getElementById('trajectoryBadge');
    const textDiv = document.getElementById('trajectoryText');
    
    const trajectory = insights.emotion_trajectory || 'stable';
    trajectoryDiv.textContent = trajectory;
    trajectoryDiv.className = `trajectory-badge ${trajectory}`;
    
    const trajectoryMessages = {
        'improving': 'Your emotional state is showing positive progress. Keep up the good work and continue with what\'s helping you!',
        'worsening': 'We notice your emotional state may be declining. Consider reaching out to someone you trust or seeking professional support.',
        'stable': 'Your emotional state remains consistent. This is a good foundation to build upon.'
    };
    
    textDiv.textContent = trajectoryMessages[trajectory];
}

function renderThemes(themes) {
    const container = document.getElementById('themesContent');
    container.innerHTML = '';
    
    if (Object.keys(themes).length === 0) {
        container.innerHTML = '<p style="color: #888; grid-column: 1 / -1;">No themes recorded yet</p>';
        return;
    }
    
    Object.entries(themes).forEach(([theme, count]) => {
        const badge = document.createElement('div');
        badge.className = 'theme-badge';
        badge.innerHTML = `
            <div class="theme-name">${theme}</div>
            <div class="theme-count">${count}</div>
        `;
        container.appendChild(badge);
    });
}

function renderIntents(intents) {
    const container = document.getElementById('intentsContent');
    container.innerHTML = '';
    
    if (Object.keys(intents).length === 0) {
        container.innerHTML = '<p style="color: #888; grid-column: 1 / -1;">No intents recorded yet</p>';
        return;
    }
    
    Object.entries(intents).forEach(([intent, count]) => {
        const badge = document.createElement('div');
        badge.className = 'intent-badge';
        badge.innerHTML = `
            <div class="intent-name">${intent}</div>
            <div class="intent-count">${count}</div>
        `;
        container.appendChild(badge);
    });
}

function renderRecommendations(recommendations) {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';
    
    if (recommendations.length === 0) {
        container.innerHTML = '<li>Continue your wellness journey and maintain open communication.</li>';
        return;
    }
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        container.appendChild(li);
    });
}

function renderStats(context) {
    document.getElementById('totalInteractions').textContent = context.total_interactions || 0;
    document.getElementById('primaryTheme').textContent = context.primary_theme || '-';
    document.getElementById('primaryIntent').textContent = context.primary_intent || '-';
}
