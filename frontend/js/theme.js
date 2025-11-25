// ==================== THEME MANAGEMENT ====================

// Theme state
let currentTheme = 'light';

document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeUIUtilities();
});

// ==================== INITIALIZE THEME ====================
function initializeTheme() {
    // Load saved theme
    const savedTheme = localStorage.getItem('naina_theme') || 'light';
    setTheme(savedTheme);
    
    // Setup theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

// ==================== SET THEME ====================
function setTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('naina_theme', theme);
    
    // Update theme toggle icon if exists
    updateThemeIcon(theme);
}

// ==================== TOGGLE THEME ====================
function toggleTheme() {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

// ==================== UPDATE THEME ICON ====================
function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    
    if (theme === 'dark') {
        icon.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
            </svg>
        `;
    } else {
        icon.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
            </svg>
        `;
    }
}

// ==================== INITIALIZE UI UTILITIES ====================
function initializeUIUtilities() {
    // Mobile sidebar toggle
    setupMobileSidebar();
    
    // Smooth scroll
    setupSmoothScroll();
    
    // Tooltips
    setupTooltips();
    
    // Auto-save forms
    setupAutoSave();
}

// ==================== MOBILE SIDEBAR ====================
function setupMobileSidebar() {
    const sidebarBtn = document.getElementById('mobileSidebarBtn');
    const sidebar = document.querySelector('.sidebar, .dashboard-sidebar');
    
    if (sidebarBtn && sidebar) {
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
        
        // Toggle sidebar
        sidebarBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        });
        
        // Close on overlay click
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }
}

// ==================== SMOOTH SCROLL ====================
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ==================== TOOLTIPS ====================
function setupTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const text = e.target.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    tooltip.className = 'fixed bg-gray-900 text-white text-xs px-3 py-2 rounded-lg z-50';
    tooltip.textContent = text;
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
    tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
}

function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    if (tooltip) tooltip.remove();
}

// ==================== AUTO-SAVE FORMS ====================
function setupAutoSave() {
    const forms = document.querySelectorAll('[data-autosave]');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                saveFormData(form.id, input.name, input.value);
            });
        });
        
        // Load saved data
        loadFormData(form.id);
    });
}

function saveFormData(formId, fieldName, value) {
    const key = `naina_form_${formId}_${fieldName}`;
    localStorage.setItem(key, value);
}

function loadFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        const key = `naina_form_${formId}_${input.name}`;
        const savedValue = localStorage.getItem(key);
        if (savedValue) {
            input.value = savedValue;
        }
    });
}

// ==================== COPY TO CLIPBOARD ====================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// ==================== SHOW NOTIFICATION ====================
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-xl shadow-lg z-50 fade-in ${
        type === 'success' ? 'bg-green-50 border-2 border-green-500 text-green-900' :
        type === 'error' ? 'bg-red-50 border-2 border-red-500 text-red-900' :
        'bg-blue-50 border-2 border-blue-500 text-blue-900'
    }`;
    
    notification.innerHTML = `
        <div class="flex items-center gap-3">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                ${type === 'success' ? 
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>' :
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
                }
            </svg>
            <span class="font-medium">${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== LOADING SPINNER ====================
function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.className = 'fixed inset-0 bg-black/50 flex items-center justify-center z-50';
    loader.innerHTML = `
        <div class="bg-white rounded-2xl p-8 flex flex-col items-center">
            <div class="w-16 h-16 border-4 border-coral border-t-transparent rounded-full animate-spin"></div>
            <p class="mt-4 font-semibold text-gray-700">Loading...</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) loader.remove();
}

// ==================== DEBOUNCE UTILITY ====================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== FORMAT DATE ====================
function formatDate(date, format = 'short') {
    const d = new Date(date);
    
    if (format === 'short') {
        return d.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric' 
        });
    } else if (format === 'long') {
        return d.toLocaleDateString('en-US', { 
            weekday: 'long',
            month: 'long', 
            day: 'numeric', 
            year: 'numeric' 
        });
    } else if (format === 'time') {
        return d.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    return d.toISOString();
}

// ==================== VALIDATE EMAIL ====================
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// ==================== VALIDATE PHONE ====================
function validatePhone(phone) {
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
    return re.test(phone);
}

// ==================== EXPORT UTILITIES ====================
window.NainaUtils = {
    showNotification,
    showLoader,
    hideLoader,
    copyToClipboard,
    debounce,
    formatDate,
    validateEmail,
    validatePhone,
    toggleTheme,
    setTheme
};

console.log('✅ Theme.js loaded successfully!');
