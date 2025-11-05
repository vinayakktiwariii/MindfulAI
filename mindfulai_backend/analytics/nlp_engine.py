from datetime import datetime
from collections import defaultdict
import re
from pathlib import Path

class AdvancedNLPEngine:
    """Advanced NLP for emotion intensity, context tracking, and intent detection"""
    
    # Sentiment keywords database
    SENTIMENT_KEYWORDS = {
        'positive': ['good', 'great', 'happy', 'better', 'excellent', 'amazing', 'wonderful', 'lovely', 'fantastic'],
        'negative': ['bad', 'terrible', 'awful', 'horrible', 'sad', 'depressed', 'stressed', 'anxious', 'worried'],
        'neutral': ['fine', 'okay', 'alright', 'normal', 'usual', 'average'],
        'crisis': ['suicide', 'hurt', 'self-harm', 'die', 'death', 'kill', 'fatal', 'emergency']
    }
    
    INTENT_KEYWORDS = {
        'vent': ['frustrated', 'angry', 'mad', 'upset', 'annoyed', 'ugh', 'argh'],
        'advice': ['what should', 'how to', 'help me', 'suggestions', 'tips', 'advice', 'guidance'],
        'support': ['sad', 'lonely', 'struggling', 'difficult', 'hard', 'need help', 'can\'t'],
        'crisis': ['suicide', 'hurt', 'harm', 'die', 'emergency'],
        'reflection': ['thinking about', 'wondering', 'question', 'why', 'reason']
    }
    
    CONTEXT_THEMES = {
        'relationships': ['love', 'partner', 'girlfriend', 'boyfriend', 'spouse', 'marriage', 'breakup', 'divorce'],
        'work': ['job', 'work', 'boss', 'career', 'promotion', 'fired', 'quit', 'stress', 'deadline'],
        'family': ['mom', 'dad', 'parent', 'sibling', 'brother', 'sister', 'family', 'home'],
        'health': ['sick', 'illness', 'pain', 'doctor', 'health', 'disease', 'medical', 'hospital'],
        'mental': ['anxiety', 'depression', 'stress', 'panic', 'ocd', 'ptsd', 'trauma', 'mental'],
        'finance': ['money', 'bills', 'debt', 'loan', 'expensive', 'poor', 'broke', 'financial'],
        'social': ['friends', 'lonely', 'alone', 'social', 'meet', 'hangout', 'connection']
    }
    
    @staticmethod
    def analyze_emotion_intensity(text):
        """
        Analyze emotion with intensity level (0-1)
        Returns: (emotion, intensity, confidence)
        """
        text_lower = text.lower()
        
        # Calculate sentiment scores
        positive_score = sum(1 for word in AdvancedNLPEngine.SENTIMENT_KEYWORDS['positive'] if word in text_lower)
        negative_score = sum(1 for word in AdvancedNLPEngine.SENTIMENT_KEYWORDS['negative'] if word in text_lower)
        neutral_score = sum(1 for word in AdvancedNLPEngine.SENTIMENT_KEYWORDS['neutral'] if word in text_lower)
        crisis_score = sum(1 for word in AdvancedNLPEngine.SENTIMENT_KEYWORDS['crisis'] if word in text_lower)
        
        total_score = positive_score + negative_score + neutral_score + crisis_score
        
        if crisis_score > 0:
            return 'crisis', min(1.0, crisis_score / 5), 1.0
        
        if total_score == 0:
            return 'neutral', 0.5, 0.3
        
        if positive_score > negative_score:
            intensity = min(1.0, positive_score / 5)
            return 'happy', intensity, 0.8
        elif negative_score > positive_score:
            intensity = min(1.0, negative_score / 5)
            return 'sad', intensity, 0.8
        else:
            return 'neutral', 0.5, 0.6
    
    @staticmethod
    def detect_intent(text):
        """
        Detect user's intent
        Returns: (intent_type, confidence, keywords_found)
        """
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, keywords in AdvancedNLPEngine.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            intent_scores[intent] = score
        
        if not any(intent_scores.values()):
            return 'conversation', 0.5, []
        
        top_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(1.0, intent_scores[top_intent] / 3)
        keywords = [kw for kw in AdvancedNLPEngine.INTENT_KEYWORDS[top_intent] if kw in text_lower]
        
        return top_intent, confidence, keywords
    
    @staticmethod
    def extract_conversation_theme(text, previous_themes=None):
        """
        Extract primary conversation theme
        Returns: (theme, confidence, keywords_found)
        """
        text_lower = text.lower()
        theme_scores = {}
        
        for theme, keywords in AdvancedNLPEngine.CONTEXT_THEMES.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            theme_scores[theme] = score
        
        if not any(theme_scores.values()):
            if previous_themes:
                return previous_themes[0] if previous_themes else 'general', 0.3, []
            return 'general', 0.3, []
        
        top_theme = max(theme_scores, key=theme_scores.get)
        confidence = min(1.0, theme_scores[top_theme] / 4)
        keywords = [kw for kw in AdvancedNLPEngine.CONTEXT_THEMES[top_theme] if kw in text_lower]
        
        return top_theme, confidence, keywords
    
    @staticmethod
    def generate_conversation_insights(conversation_data):
        """
        Generate wellness insights from conversation history
        Returns: dict with insights
        """
        if not conversation_data or 'messages' not in conversation_data:
            return None
        
        messages = conversation_data['messages']
        
        if len(messages) < 3:
            return None
        
        # Analyze emotion progression
        emotions = [AdvancedNLPEngine.analyze_emotion_intensity(msg['user_message'])[0] for msg in messages]
        
        # Analyze themes
        themes = defaultdict(int)
        intents = defaultdict(int)
        
        for msg in messages:
            theme, _, _ = AdvancedNLPEngine.extract_conversation_theme(msg['user_message'])
            intent, _, _ = AdvancedNLPEngine.detect_intent(msg['user_message'])
            themes[theme] += 1
            intents[intent] += 1
        
        # Detect emotion trajectory
        recent_emotions = emotions[-5:] if len(emotions) > 5 else emotions
        recent_has_positive = 'happy' in recent_emotions
        recent_has_negative = 'sad' in recent_emotions
        
        if recent_has_positive and recent_emotions[-1] == 'happy':
            trajectory = 'improving'
        elif recent_has_negative and recent_emotions[-1] == 'sad':
            trajectory = 'worsening'
        else:
            trajectory = 'stable'
        
        # Generate recommendations
        recommendations = []
        
        if themes['mental'] > len(messages) * 0.4:
            recommendations.append("Consider speaking with a mental health professional for ongoing support.")
        
        if 'vent' in intents and intents['vent'] > len(messages) * 0.5:
            recommendations.append("It seems you need more space to express yourself. Keep sharing - talking helps.")
        
        if themes['social'] > 0 and 'support' in intents:
            recommendations.append("Reaching out to friends or family might provide additional support.")
        
        if trajectory == 'improving':
            recommendations.append("You're showing positive progress! Keep building on this momentum.")
        elif trajectory == 'worsening':
            recommendations.append("Consider reaching out to someone you trust for additional support.")
        
        return {
            'emotion_trajectory': trajectory,
            'primary_themes': dict(sorted(themes.items(), key=lambda x: x[1], reverse=True)[:3]),
            'primary_intents': dict(sorted(intents.items(), key=lambda x: x[1], reverse=True)[:2]),
            'recommendations': recommendations,
            'analysis_date': datetime.now().isoformat(),
            'total_messages': len(messages),
            'crisis_detected': any('crisis' in msg.get('emotion', '').lower() for msg in messages)
        }
