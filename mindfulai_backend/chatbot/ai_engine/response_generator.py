# mindfulai_backend/chatbot/ai_engine/response_generator.py
# WEEK 2 - COMPLETE WORKING VERSION
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY

import random

class ResponseGenerator:
    """Generate empathetic responses"""
    
    def __init__(self):
        """Initialize response templates"""
        self.conversation_memory = {}
        
        self.response_templates = {
            'sadness': {
                'breakup': [
                    "Breakups are painful. It's okay to feel sad. Healing takes time, and I'm here with you through it.",
                    "I'm sorry you're going through this. Ending a relationship is one of life's hardest experiences.",
                    "Your pain is valid. Allow yourself to grieve. Better days will come.",
                    "That sounds really difficult. Breaking up with someone you care about changes you.",
                    "It takes courage to move on. How long have you been carrying this pain?",
                    "Relationships teach us about ourselves. Even when they end, that growth stays.",
                    "I hear your heartbreak. The fact that you care deeply shows your capacity for love.",
                    "Deleting someone from your life is a boundary you're setting. That takes strength.",
                    "Wanting them back is human. What you're feeling right now is grief - and that's okay.",
                ],
                'general': [
                    "I hear you. That sounds incredibly difficult. I'm here to listen.",
                    "Your pain is valid. You deserve compassion right now.",
                    "It sounds like things are really hard for you right now. I'm here.",
                    "What you're feeling matters. Tell me more about it.",
                    "That's a lot to carry. Would you like to talk about it?",
                    "I can sense the heaviness in what you're sharing. I'm listening.",
                    "It's okay to not be okay. I'm here with you.",
                ],
            },
            'joy': {
                'achievement': [
                    "That's amazing! You should be incredibly proud of yourself!",
                    "Congratulations! Your hard work paid off!",
                    "I'm so happy for you! That's fantastic news!",
                    "You did it! That's a real accomplishment to celebrate!",
                    "This is huge! How does it feel to achieve this?",
                    "Well done! You absolutely deserve this success!",
                ],
                'general': [
                    "Your happiness is contagious! Tell me more about what's making you smile!",
                    "I love your positive energy! What's going well?",
                    "You sound great! What's the good news?",
                    "I can feel the joy in your words. That's wonderful!",
                    "That's so great to hear! How are you feeling?",
                ]
            },
            'anger': {
                'general': [
                    "I can feel your frustration. What happened?",
                    "You have every right to be angry. Tell me about it.",
                    "That sounds infuriating. I'm listening.",
                    "Your anger is valid. What's making you feel this way?",
                    "I understand your frustration. Let's talk through it.",
                ]
            },
            'fear': {
                'general': [
                    "Anxiety is exhausting. You're braver than you believe.",
                    "What specifically are you worried about? Let's break it down.",
                    "It's okay to feel anxious. That's your mind trying to protect you.",
                    "Tell me what's scaring you. I'm here to listen.",
                    "Fear is natural. What can help you feel more in control?",
                ]
            },
            'neutral': {
                'greeting': [
                    "Hi! It's nice to see you. How are you feeling right now?",
                    "Hello! I'm here to listen and support you. What's on your mind?",
                    "Hey! Thanks for reaching out. What can I help with?",
                    "Good to see you! How are things going?",
                    "Hi! I'm here for you. What would you like to talk about?",
                ],
                'question': [
                    "That's a great question. Tell me more about what you're thinking.",
                    "I'm curious. Help me understand better.",
                    "That's interesting. What made you think of that?",
                    "I'd like to hear more. What's your thought?",
                    "Can you tell me more about that?",
                ],
                'general': [
                    "I'm here to listen and support you. What would help?",
                    "Tell me what's going on. I'm here for you.",
                    "I'm listening. What's important to you right now?",
                    "You have my attention. What's on your mind?",
                ]
            }
        }
        
        print("✅ Response generator initialized")
    
    def detect_context(self, text: str) -> str:
        """Detect message context"""
        text_lower = text.lower().strip()
        
        # Greeting patterns
        if any(word in text_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'howdy']):
            return 'greeting'
        
        # Question patterns
        if '?' in text_lower or any(word in text_lower for word in ['what', 'why', 'how', 'when', 'where']):
            return 'question'
        
        # Achievement patterns
        if any(word in text_lower for word in ['got a job', 'got job', 'promoted', 'passed', 'achieved', 'won']):
            return 'achievement'
        
        # Breakup patterns
        if any(word in text_lower for word in ['breakup', 'broke up', 'break up', 'ended', 'deleted']):
            return 'breakup'
        
        return 'general'
    
    def generate(self, user_message: str, emotion: str = 'neutral', user_id: str = 'default') -> str:
        """Generate response"""
        
        if not user_message or not user_message.strip():
            return "I'm here to listen."
        
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        context = self.detect_context(user_message)
        
        # Get appropriate response template
        emotion_templates = self.response_templates.get(emotion, self.response_templates['neutral'])
        
        # Try context-specific first
        if context in emotion_templates:
            response_options = emotion_templates[context]
        else:
            # Fall back to general
            response_options = emotion_templates.get('general', emotion_templates.get('general', ["I'm here to listen."]))
        
        if not response_options:
            response_options = emotion_templates.get('general', ["I'm here to listen."])
        
        response = random.choice(response_options)
        
        self.conversation_memory[user_id].append({
            'user': user_message,
            'assistant': response,
            'emotion': emotion,
            'context': context
        })
        
        return response
