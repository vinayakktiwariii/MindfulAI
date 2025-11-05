// theme.js - Dark/Light Mode Toggle

const THEME_KEY = 'naina_theme';
const DARK_THEME = 'dark';
const LIGHT_THEME = 'light';

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', initializeTheme);

function initializeTheme() {
    // Get saved theme or default to dark
    const savedTheme = localStorage.getItem(THEME_KEY) || DARK_THEME;
    setTheme(savedTheme);
    setupThemeToggle();
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    updateThemeButton(theme);
}

function toggleTheme() {
    const currentTheme = localStorage.getItem(THEME_KEY) || DARK_THEME;
    const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    setTheme(newTheme);
}

function updateThemeButton(theme) {
    const btn = document.getElementById('themeToggleBtn');
    const label = document.getElementById('themeLabel');
    
    if (theme === DARK_THEME) {
        btn.innerHTML = '<span class="theme-icon">🌙</span><span class="theme-label">Dark</span>';
    } else {
        btn.innerHTML = '<span class="theme-icon">☀️</span><span class="theme-label">Light</span>';
    }
}

function setupThemeToggle() {
    const btn = document.getElementById('themeToggleBtn');
    if (btn) {
        btn.addEventListener('click', toggleTheme);
    }
}

// Export for use in other files
window.themeUtils = {
    setTheme,
    toggleTheme,
    getCurrentTheme: () => localStorage.getItem(THEME_KEY) || DARK_THEME
};
