# mindfulai_backend/chatbot/ai_engine/crisis_detector.py
# WEEK 2 - CRITICAL FIX: Crisis detection must be bulletproof
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES

import re
from typing import Dict, List, Tuple

class CrisisDetector:
    """Detect crisis keywords - UPDATED WITH MISSING KEYWORDS"""
    
    def __init__(self):
        """Initialize crisis detection patterns"""
        
        # TIER 1: IMMEDIATE DANGER - MOST CRITICAL
        self.critical_keywords = [
            r'\bsuicide\b', r'\bkill myself\b', r'\bkilling myself\b', r'\bend my life\b', 
            r'\bwant to die\b', r'\bwanna die\b', r'\bhurt myself\b',
            r'\bcut myself\b', r'\btake my life\b', r'\bno reason to live\b',
            r'\bself harm\b', r'\bself-harm\b', r'\bcutting\b',
            r'\bburning myself\b', r'\bstarving myself\b',
            r'\boverdose\b', r'\bhang myself\b', r'\bjump off\b',
            r'\bshoot myself\b', r'\bdrown myself\b',
            r'\bgoodbye forever\b', r'\blast time\b', r'\bend it all\b',
            r'\bcan\'t go on\b', r'\bbetter off dead\b',
            r'\bending my life\b',  # ← ADDED: Was missing!
            r'\bwanna end it\b',  # ← ADDED: Was missing!
            r'\bwanna die\b',  # ← ADDED: Suicide indicator
            r'\bsuicidal\b',  # ← ADDED: Direct term
        ]
        
        # TIER 2: SEVERE DISTRESS
        self.severe_distress_keywords = [
            r'\bcan\'t take it anymore\b', r'\bgive up\b', r'\bhopeless\b',
            r'\bno point\b', r'\bworthless\b', r'\bburden\b',
            r'\beveryone would be better without me\b',
            r'\bdon\'t want to be alive\b', r'\btoo much pain\b',
            r'\bcan\'t handle this\b', r'\bcan\'t cope\b',
        ]
        
        # TIER 3: ELEVATED CONCERN
        self.elevated_concern_keywords = [
            r'\bextremely depressed\b', r'\bcan\'t cope\b', 
            r'\boverwhelmed\b', r'\bscared of myself\b',
            r'\bthoughts are dark\b', r'\blost control\b',
        ]
        
        # Compile regex patterns
        self.critical_patterns = [re.compile(kw, re.IGNORECASE) for kw in self.critical_keywords]
        self.severe_patterns = [re.compile(kw, re.IGNORECASE) for kw in self.severe_distress_keywords]
        self.elevated_patterns = [re.compile(kw, re.IGNORECASE) for kw in self.elevated_concern_keywords]
        
        print("✅ Crisis detector initialized with updated keywords")
    
    def detect(self, message: str) -> Dict:
        """Analyze a user message for crisis indicators"""
        
        message = message.strip().lower()
        
        # TIER 1: Check for critical keywords (IMMEDIATE DANGER)
        critical_matches = []
        for pattern in self.critical_patterns:
            if pattern.search(message):
                critical_matches.append(pattern.pattern)
        
        if critical_matches:
            print(f"[CRISIS] CRITICAL detected: {critical_matches}")
            return {
                'is_crisis': True,
                'severity': 'critical',
                'matched_keywords': critical_matches,
                'confidence': 1.0,
                'message': 'Immediate crisis detected. Emergency intervention required.'
            }
        
        # TIER 2: Check for severe distress
        severe_matches = []
        for pattern in self.severe_patterns:
            if pattern.search(message):
                severe_matches.append(pattern.pattern)
        
        if len(severe_matches) >= 2:
            print(f"[CRISIS] SEVERE detected: {severe_matches}")
            return {
                'is_crisis': True,
                'severity': 'severe',
                'matched_keywords': severe_matches,
                'confidence': 0.9,
                'message': 'Severe emotional distress detected. Crisis protocol activated.'
            }
        elif len(severe_matches) == 1:
            print(f"[CRISIS] SEVERE (single) detected: {severe_matches}")
            return {
                'is_crisis': False,
                'severity': 'severe',
                'matched_keywords': severe_matches,
                'confidence': 0.7,
                'message': 'High distress level. Monitor closely and offer support resources.'
            }
        
        # TIER 3: Check for elevated concern
        elevated_matches = []
        for pattern in self.elevated_patterns:
            if pattern.search(message):
                elevated_matches.append(pattern.pattern)
        
        if elevated_matches:
            print(f"[CONCERN] Elevated concern detected: {elevated_matches}")
            return {
                'is_crisis': False,
                'severity': 'elevated',
                'matched_keywords': elevated_matches,
                'confidence': 0.5,
                'message': 'Elevated emotional distress. Provide empathetic support.'
            }
        
        print(f"[NORMAL] No crisis indicators detected")
        return {
            'is_crisis': False,
            'severity': 'normal',
            'matched_keywords': [],
            'confidence': 0.0,
            'message': 'No immediate crisis indicators detected.'
        }


CRISIS_RESOURCES = {
    'global': {
        'name': '988 Suicide & Crisis Lifeline (USA)',
        'phone': '988',
        'text': 'Text "HELLO" to 741741',
        'available': '24/7',
    },
    'india': {
        'name': 'AASRA (India)',
        'phone': '+91-9820466726',
        'website': 'http://www.aasra.info',
        'available': '24/7',
    },
    'emergency': {
        'name': 'Emergency Services',
        'phone': '112 (India) | 911 (USA) | 999 (UK)',
        'message': 'If you are in immediate danger, call emergency services NOW.',
    }
}


def get_crisis_response(severity: str = 'critical') -> str:
    """Generate the appropriate crisis intervention message - NO EMOJIS"""
    
    if severity == 'critical':
        return """I'M REALLY CONCERNED ABOUT WHAT YOU'VE SHARED WITH ME.

You're not alone, and help is available RIGHT NOW:

IMMEDIATE HELP (USA):
988 Suicide & Crisis Lifeline
Call: 988
Text: "HELLO" to 741741
Available: 24/7

IMMEDIATE HELP (INDIA):
AASRA Mental Health Support
Call: +91-9820466726
Website: www.aasra.info
Available: 24/7

EMERGENCY SERVICES:
India: 112
USA: 911
UK: 999
Call if you're in immediate danger.

PLEASE REACH OUT TO ONE OF THESE SERVICES NOW.

They are trained professionals who genuinely want to help. You deserve that support.

Your life has value. This moment of pain is NOT the end of your story.

I'm here, but please also talk to a real human who can give you the support you truly need right now."""
    
    elif severity == 'severe':
        return """I can sense you're going through something incredibly difficult right now.

If you're having thoughts of harming yourself, PLEASE reach out:

National Suicide Prevention Lifeline: 988 (USA)
AASRA: +91-9820466726 (India)

These are trained professionals available 24/7. You don't have to face this alone.

I'm here to listen, but professional support can provide what you truly need right now."""
    
    else:
        return """I hear that you're struggling right now. That takes courage to share.

Remember:
- You're talking to an AI, and I have limits
- Professional support is available 24/7 if things feel overwhelming
- 988 (USA) or +91-9820466726 (India)

Would you like to talk about what's on your mind, or would coping strategies help?"""
