# mindfulai_backend/chatbot/ai_engine/emotion_classifier.py
# WEEK 2 - FIXED EMOTION DETECTION
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY

class EmotionClassifier:
    """Detect emotions in user messages"""
    
    def __init__(self):
        """Initialize emotion detection"""
        self.device = "cpu"
        
        # Comprehensive emotion keywords
        self.emotion_patterns = {
            'sadness': [
                'sad', 'depressed', 'crying', 'cry', 'heartbroken', 'lonely', 'devastated', 
                'unhappy', 'miserable', 'down', 'broke up', 'breakup', 'break up', 'lost', 'hurt', 'pain',
                'grief', 'mourning', 'disappointed', 'disappointing', 'failed', 'failure',
                'want her back', 'want him back', 'want them back', 'miss', 'missing',
                'terrible', 'awful', 'horrible', 'sucks', 'cant', "can't", 'ending my life',
                'end my life', 'feel like dying', 'rather be dead', 'no point',
            ],
            'joy': [
                'happy', 'happiness', 'excited', 'excitement', 'great', 'wonderful', 'amazing', 'fantastic',
                'achieved', 'achieve', 'won', 'win', 'love', 'awesome', 'brilliant', 'thrilled',
                'delighted', 'celebrate', 'celebration', 'pride', 'proud', 'best', 'excellent',
                'got a job', 'got job', 'promoted', 'passed', 'success', 'succeed', 'wonderful',
                'congratulations', 'amazing news', 'good news', 'great news',
            ],
            'anger': [
                'angry', 'anger', 'furious', 'rage', 'hate', 'mad', 'pissed', 'frustrated',
                'annoyed', 'irritated', 'livid', 'enraged', 'upset', 'betrayed',
                'infuriated', 'outraged', 'boiling', 'seething',
            ],
            'fear': [
                'scared', 'scaring', 'anxious', 'anxiety', 'worried', 'worry', 'afraid', 'nervous',
                'terrified', 'terror', 'panic', 'frightened', 'trembling', 'dread',
                'uncertain', 'uncertain', 'worried about', 'afraid of', 'scared of',
            ],
        }
        
        print("✅ Emotion classifier initialized")
    
    def classify(self, text: str) -> dict:
        """Classify emotion in text"""
        
        if not text or not text.strip():
            return {
                'emotion': 'neutral',
                'confidence': 0.5,
                'color': '#95A5A6'
            }
        
        text_lower = text.lower().strip()
        
        # Score each emotion
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    score += 1
            
            if score > 0:
                emotion_scores[emotion] = score
        
        # Return highest scoring emotion
        if emotion_scores:
            top_emotion = max(emotion_scores, key=emotion_scores.get)
            score_value = emotion_scores[top_emotion]
            confidence = min(0.9, 0.5 + (score_value * 0.15))
            
            color_map = {
                'sadness': '#FF6B6B',
                'joy': '#FFD93D',
                'anger': '#FF4757',
                'fear': '#A29BFE',
            }
            
            return {
                'emotion': top_emotion,
                'confidence': confidence,
                'color': color_map.get(top_emotion, '#95A5A6')
            }
        
        return {
            'emotion': 'neutral',
            'confidence': 0.5,
            'color': '#95A5A6'
        }
