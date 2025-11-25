// ==================== INSIGHTS PAGE ====================

document.addEventListener('DOMContentLoaded', function() {
    initializeInsights();
});

// ==================== INITIALIZE INSIGHTS ====================
function initializeInsights() {
    loadAIInsights();
    loadRecommendations();
    loadStrengths();
    animateProgressBars();
}

// ==================== LOAD AI INSIGHTS ====================
async function loadAIInsights() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/insights/ai/');
        const data = await response.json();
        
        displayAIInsight(data);
    } catch (error) {
        console.error('Error loading insights:', error);
        
        // Mock data for testing
        const mockInsight = {
            title: "AI-Powered Insight for Today",
            content: "Based on your recent conversations, you've been managing stress very well! Your coping mechanisms are showing positive results. Consider continuing your breathing exercises and maintaining your sleep schedule.",
            tags: ["Stress Management", "Sleep Health"],
            confidence: 0.92
        };
        
        displayAIInsight(mockInsight);
    }
}

// ==================== DISPLAY AI INSIGHT ====================
function displayAIInsight(insight) {
    const container = document.getElementById('aiInsightContainer');
    if (!container) return;
    
    const tagsHTML = insight.tags.map((tag, index) => 
        `<span class="insight-tag ${index % 2 === 0 ? 'coral' : 'mint'}">${tag}</span>`
    ).join('');
    
    container.innerHTML = `
        <div class="ai-insight-card fade-in">
            <div class="ai-insight-header">
                <div class="ai-insight-icon">
                    <svg class="w-6 h-6" style="color: #ff6b6b;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                </div>
                <div class="ai-insight-content">
                    <h3 class="ai-insight-title">${insight.title}</h3>
                    <p class="ai-insight-text">${insight.content}</p>
                    <div class="ai-insight-tags">
                        ${tagsHTML}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// ==================== LOAD RECOMMENDATIONS ====================
async function loadRecommendations() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/insights/recommendations/');
        const data = await response.json();
        
        displayRecommendations(data);
    } catch (error) {
        console.error('Error loading recommendations:', error);
        
        // Mock data
        const mockRecommendations = {
            actions: [
                {
                    title: "Practice mindfulness",
                    description: "5 minutes daily meditation",
                    completed: false
                },
                {
                    title: "Stay connected",
                    description: "Chat with loved ones",
                    completed: false
                },
                {
                    title: "Physical activity",
                    description: "20 minutes of exercise",
                    completed: false
                }
            ]
        };
        
        displayRecommendations(mockRecommendations);
    }
}

// ==================== DISPLAY RECOMMENDATIONS ====================
function displayRecommendations(data) {
    const actionsContainer = document.getElementById('recommendedActions');
    if (!actionsContainer) return;
    
    actionsContainer.innerHTML = data.actions.map((action, index) => `
        <div class="action-item fade-in" style="animation-delay: ${index * 0.1}s">
            <div class="action-checkbox" onclick="toggleAction(${index})">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
            </div>
            <div class="action-content">
                <p class="action-title">${action.title}</p>
                <p class="action-description">${action.description}</p>
            </div>
        </div>
    `).join('');
}

// ==================== TOGGLE ACTION ====================
function toggleAction(index) {
    console.log(`Action ${index} toggled`);
    // TODO: Update backend
}

// ==================== LOAD STRENGTHS ====================
async function loadStrengths() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/insights/strengths/');
        const data = await response.json();
        
        displayStrengths(data);
    } catch (error) {
        console.error('Error loading strengths:', error);
        
        // Mock data
        const mockStrengths = [
            { name: "Self-awareness", score: 85 },
            { name: "Emotional regulation", score: 78 },
            { name: "Resilience", score: 92 }
        ];
        
        displayStrengths(mockStrengths);
    }
}

// ==================== DISPLAY STRENGTHS ====================
function displayStrengths(strengths) {
    const container = document.getElementById('strengthsList');
    if (!container) return;
    
    container.innerHTML = strengths.map((strength, index) => `
        <div class="strength-item fade-in" style="animation-delay: ${index * 0.1}s">
            <div class="strength-header">
                <span class="strength-name">${strength.name}</span>
                <span class="strength-score">${strength.score}%</span>
            </div>
            <div class="strength-bar">
                <div class="strength-fill" style="width: ${strength.score}%"></div>
            </div>
        </div>
    `).join('');
}

// ==================== ANIMATE PROGRESS BARS ====================
function animateProgressBars() {
    setTimeout(() => {
        const bars = document.querySelectorAll('.strength-fill, .progress-fill');
        bars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 500);
}

// ==================== MOOD TRACKER ====================
function selectMood(mood) {
    console.log('Mood selected:', mood);
    
    // TODO: Send to backend
    fetch('http://127.0.0.1:8000/api/insights/mood/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            mood: mood,
            timestamp: new Date().toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Mood saved:', data);
        showNotification('Mood recorded successfully!');
    })
    .catch(error => {
        console.error('Error saving mood:', error);
    });
}

// ==================== SHOW NOTIFICATION ====================
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-white border-2 border-coral rounded-xl px-6 py-3 shadow-lg z-50 fade-in';
    notification.innerHTML = `
        <div class="flex items-center gap-3">
            <svg class="w-5 h-5" style="color: #22c55e;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="font-medium">${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

console.log('✅ Insights.js loaded successfully!');
