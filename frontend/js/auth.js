// ==================== AUTHENTICATION & SESSION MANAGEMENT ====================

// Prevent multiple initializations
let authInitialized = false;

// Check if user is logged in on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!authInitialized) {
        authInitialized = true;
        initializeAuth();
    }
});

// ==================== INITIALIZE AUTHENTICATION ====================
function initializeAuth() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const protectedPages = ['chat.html', 'analytics.html', 'insights.html', 'profile.html'];
    const authPages = ['login.html', 'signup.html'];
    
    const user = getCurrentUser();
    
    console.log('=== AUTH INIT ===');
    console.log('Current page:', currentPage);
    console.log('User exists:', !!user);
    
    // IMPORTANT: Don't redirect if we're in the middle of login/signup
    const isProcessingAuth = sessionStorage.getItem('processing_auth');
    if (isProcessingAuth === 'true') {
        console.log('Auth in progress, skipping redirect');
        sessionStorage.removeItem('processing_auth');
        return;
    }
    
    // Redirect logic
    if (protectedPages.includes(currentPage) && !user) {
        console.log('Not logged in, redirecting to login...');
        window.location.href = 'login.html';
        return;
    }
    
    // Update UI if user is logged in
    if (user) {
        updateUserProfile(user);
    }
}

// ==================== GET CURRENT USER ====================
function getCurrentUser() {
    try {
        const userStr = localStorage.getItem('naina_user');
        const token = localStorage.getItem('naina_user_token');
        
        console.log('LocalStorage user:', userStr);
        console.log('LocalStorage token:', token);
        
        if (userStr && token) {
            return JSON.parse(userStr);
        }
    } catch (e) {
        console.error('Error getting user:', e);
    }
    return null;
}

// ==================== UPDATE USER PROFILE UI ====================
function updateUserProfile(user) {
    console.log('Updating UI for user:', user.fullname);
    
    // Update all avatar elements
    const avatars = document.querySelectorAll('#headerAvatar, #sidebarAvatar');
    avatars.forEach(avatar => {
        if (user.fullname) {
            const initials = user.fullname
                .split(' ')
                .map(n => n[0])
                .join('')
                .toUpperCase()
                .slice(0, 2);
            avatar.textContent = initials;
        }
    });
    
    // Update username displays
    const usernameElements = document.querySelectorAll('#sidebarUsername');
    usernameElements.forEach(elem => {
        elem.textContent = user.fullname || user.username;
    });
}

// ==================== LOGIN FUNCTION ====================
async function handleLogin(identifier, password) {
    console.log('=== LOGIN ATTEMPT ===');
    console.log('Identifier:', identifier);
    
    // Mark that we're processing authentication
    sessionStorage.setItem('processing_auth', 'true');
    
    // Create mock user (since backend is not available)
    let fullname = identifier.split('@')[0] || 'User';
    fullname = fullname.charAt(0).toUpperCase() + fullname.slice(1).toLowerCase();
    
    const mockUser = {
        id: Date.now(),
        fullname: fullname,
        username: identifier,
        email: identifier.includes('@') ? identifier : `${identifier}@example.com`,
        created_at: new Date().toISOString()
    };
    
    console.log('Creating mock user:', mockUser);
    
    // Save to localStorage
    localStorage.setItem('naina_user', JSON.stringify(mockUser));
    localStorage.setItem('naina_user_token', 'mock_token_' + Date.now());
    
    // Verify it was saved
    const savedUser = localStorage.getItem('naina_user');
    const savedToken = localStorage.getItem('naina_user_token');
    
    console.log('Saved user:', savedUser);
    console.log('Saved token:', savedToken);
    
    if (savedUser && savedToken) {
        console.log('✅ Login successful! Redirecting...');
        
        // Use window.location.replace to prevent back button issues
        window.location.replace('chat.html');
        
        return { success: true };
    } else {
        console.error('❌ Failed to save user data');
        sessionStorage.removeItem('processing_auth');
        return { success: false, error: 'Failed to save login data' };
    }
}

// ==================== SIGNUP FUNCTION ====================
async function handleSignup(firstname, surname, username, contact, password) {
    console.log('=== SIGNUP ATTEMPT ===');
    
    // Mark that we're processing authentication
    sessionStorage.setItem('processing_auth', 'true');
    
    const mockUser = {
        id: Date.now(),
        fullname: `${firstname} ${surname}`,
        username: username,
        email: contact.includes('@') ? contact : `${contact}@example.com`,
        phone: !contact.includes('@') ? contact : null,
        created_at: new Date().toISOString()
    };
    
    console.log('Creating user:', mockUser);
    
    // Save to localStorage
    localStorage.setItem('naina_user', JSON.stringify(mockUser));
    localStorage.setItem('naina_user_token', 'mock_token_' + Date.now());
    
    // Verify
    const savedUser = localStorage.getItem('naina_user');
    const savedToken = localStorage.getItem('naina_user_token');
    
    console.log('Saved user:', savedUser);
    console.log('Saved token:', savedToken);
    
    if (savedUser && savedToken) {
        console.log('✅ Signup successful! Redirecting...');
        window.location.replace('chat.html');
        return { success: true };
    } else {
        console.error('❌ Failed to save user data');
        sessionStorage.removeItem('processing_auth');
        return { success: false, error: 'Failed to save signup data' };
    }
}

// ==================== LOGOUT FUNCTION ====================
function logout() {
    console.log('Logging out...');
    
    localStorage.removeItem('naina_user');
    localStorage.removeItem('naina_user_token');
    localStorage.removeItem('currentConversationId');
    sessionStorage.clear();
    
    window.location.replace('landing.html');
}

// ==================== ATTACH TO LOGIN FORM ====================
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    console.log('Login form found, attaching listener');
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('=== LOGIN FORM SUBMITTED ===');
        
        const identifier = document.getElementById('identifier').value.trim();
        const password = document.getElementById('password').value.trim();
        
        if (!identifier || !password) {
            alert('Please enter both email/username and password');
            return;
        }
        
        // Disable submit button
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <svg class="animate-spin h-5 w-5 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            `;
        }
        
        const result = await handleLogin(identifier, password);
        
        if (!result.success) {
            alert(result.error || 'Login failed. Please try again.');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Login';
            }
        }
    });
}

// ==================== ATTACH TO SIGNUP FORM ====================
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    console.log('Signup form found, attaching listener');
    
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('=== SIGNUP FORM SUBMITTED ===');
        
        const firstname = document.getElementById('firstname').value.trim();
        const surname = document.getElementById('surname').value.trim();
        const username = document.getElementById('username').value.trim();
        const contact = document.getElementById('contact').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (!firstname || !surname || !username || !contact || !password) {
            alert('Please fill in all fields');
            return;
        }
        
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        if (password.length < 8) {
            alert('Password must be at least 8 characters long!');
            return;
        }
        
        // Disable submit button
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <svg class="animate-spin h-5 w-5 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            `;
        }
        
        const result = await handleSignup(firstname, surname, username, contact, password);
        
        if (!result.success) {
            alert(result.error || 'Signup failed. Please try again.');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Create Account';
            }
        }
    });
}

console.log('✅ Auth.js loaded successfully!');
