# data/crisis_api_server.py - OPTIMIZED FOR SPEED & CONVERSATION
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import time
from urllib.parse import urlparse
import threading

# Get API key from environment
BYTEZ_API_KEY = os.getenv('BYTEZ_API_KEY', '05bb0c56a16725d749100641b2dceaf2')
print(f"🔑 API Key loaded: {BYTEZ_API_KEY[:15]}...")

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from bytez import Bytez
    from mindfulai_backend.chatbot.ai_engine.crisis_detector import CrisisDetector, get_crisis_response
    from mindfulai_backend.chatbot.ai_engine.emotion_classifier import EmotionClassifier
    from mindfulai_backend.analytics.conversation_db import ConversationDatabase
    from mindfulai_backend.analytics.models import UserProfile
    from mindfulai_backend.analytics.nlp_engine import AdvancedNLPEngine
    from mindfulai_backend.analytics.context_memory import ContextMemory
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

try:
    sdk = Bytez(BYTEZ_API_KEY)
    model = sdk.model("Qwen/Qwen2.5-3B-Instruct")
    print("✅ Bytez SDK initialized")
except Exception as e:
    print(f"⚠️ Bytez initialization failed: {e}")
    model = None

detector = CrisisDetector()
emotion_classifier = EmotionClassifier()
user_conversations = {}

print("="*80)
print("NAINA v6.0 - OPTIMIZED (FAST & CONVERSATIONAL)")
print("="*80)
print("✅ Crisis Detection: ACTIVE")
print("✅ Emotion Analysis: ACTIVE")
print("✅ Conversational Mode: ACTIVE")
print("✅ Response Time: OPTIMIZED (30s timeout)")
print("="*80 + "\n")


class NAINAHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        try:
            if self.path == '/api/chat/chat/':
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body)
                
                user_message = data.get('message', '').strip()
                user_id = data.get('user_id', 'default')
                
                if not user_message:
                    self.send_json_response({'error': 'Empty message'}, 400)
                    return
                
                print(f"\n[USER] {user_message}")
                
                # Create user profile
                UserProfile.create_user(user_id, f"User_{user_id[-6:]}")
                
                # Initialize conversation history
                if user_id not in user_conversations:
                    user_conversations[user_id] = {
                        'messages': [],
                        'crisis_count': 0,
                        'negative_count': 0
                    }
                
                user_conversations[user_id]['messages'].append({
                    'role': 'user',
                    'content': user_message
                })
                
                start_time = time.time()
                
                # Crisis detection
                crisis_result = detector.detect(user_message)
                
                # IMPROVED: Only respond with crisis help if TRULY severe
                if crisis_result['is_crisis'] and crisis_result['severity'] in ['HIGH', 'CRITICAL']:
                    print(f"[CRITICAL CRISIS] {crisis_result['severity']}")
                    user_conversations[user_id]['crisis_count'] += 1
                    
                    # Only suggest professional help after repeated crises
                    if user_conversations[user_id]['crisis_count'] >= 3:
                        crisis_response = get_crisis_response(crisis_result['severity'])
                    else:
                        # First crisis responses - be supportive, not dismissive
                        crisis_response = self.get_supportive_crisis_response(user_message)
                    
                    response_time = time.time() - start_time
                    
                    ContextMemory.store_context(user_id, 'crisis', 'crisis', ['emergency'], 'crisis')
                    ConversationDatabase.save_message(
                        user_id, user_message, crisis_response, 
                        'crisis', response_time, is_crisis=True
                    )
                    
                    user_conversations[user_id]['messages'].append({
                        'role': 'assistant',
                        'content': crisis_response
                    })
                    
                    self.send_json_response({
                        'response': crisis_response,
                        'type': 'crisis',
                        'emotion': 'crisis',
                        'confidence': 1.0
                    }, 200)
                    return
                
                # Emotion analysis
                emotion_result = emotion_classifier.classify(user_message)
                emotion, intensity, confidence = AdvancedNLPEngine.analyze_emotion_intensity(user_message)
                print(f"[EMOTION] {emotion} (intensity: {intensity:.2f})")
                
                # Track negative emotions
                if emotion in ['sad', 'anxious', 'stressed', 'angry']:
                    user_conversations[user_id]['negative_count'] += 1
                else:
                    user_conversations[user_id]['negative_count'] = max(0, user_conversations[user_id]['negative_count'] - 1)
                
                # Intent & theme
                intent, intent_confidence, intent_keywords = AdvancedNLPEngine.detect_intent(user_message)
                theme, theme_confidence, theme_keywords = AdvancedNLPEngine.extract_conversation_theme(user_message)
                
                # OPTIMIZED: Fast response with 30s timeout
                ai_response = self.generate_fast_response(user_id, emotion, intensity)
                response_time = time.time() - start_time
                print(f"[RESPONSE TIME] {response_time:.2f}s")
                
                user_conversations[user_id]['messages'].append({
                    'role': 'assistant',
                    'content': ai_response
                })
                
                # Store context
                all_keywords = theme_keywords + intent_keywords
                ContextMemory.store_context(user_id, theme, intent, all_keywords, emotion)
                ConversationDatabase.save_message(
                    user_id, user_message, ai_response,
                    emotion, response_time, is_crisis=False
                )
                
                self.send_json_response({
                    'response': ai_response,
                    'type': 'conversation',
                    'emotion': emotion,
                    'intensity': intensity,
                    'intent': intent,
                    'theme': theme,
                    'confidence': confidence
                }, 200)
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({'error': str(e)}, 500)
    
    def do_GET(self):
        if self.path == '/':
            self.send_json_response({
                'message': 'NAINA API v6.0 - Fast & Conversational',
                'status': 'active',
                'health': '/api/chat/health/',
                'chat': '/api/chat/chat/'
            }, 200)
        
        elif self.path == '/api/chat/health/':
            self.send_json_response({
                'status': 'healthy',
                'version': 'v6.0',
                'model': 'Qwen2.5-3B-Instruct',
                'provider': 'Bytez.com',
                'timeout': '30s',
                'mode': 'conversational',
                'active_conversations': len(user_conversations)
            }, 200)
        
        elif self.path.startswith('/api/analytics/'):
            from mindfulai_backend.analytics.views import handle_analytics_api
            query_params = {}
            query_string = urlparse(self.path).query
            if query_string:
                for param in query_string.split('&'):
                    if '=' in param:
                        k, v = param.split('=', 1)
                        query_params[k] = [v]
            response_data, status_code = handle_analytics_api(self.path, query_params)
            self.send_json_response(response_data, status_code)
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_supportive_crisis_response(self, message):
        """Supportive response for crisis situations - conversational first"""
        responses = {
            'default': "I hear you, and what you're feeling is valid. Sometimes our thoughts can feel overwhelming. I'm here with you right now. Can you tell me more about what brought this on?",
            'suicide': "I'm really concerned about you right now. These feelings can be incredibly painful, but they don't have to be permanent. You reached out to me, which shows incredible strength. What's making you feel this way?",
            'self_harm': "Thank you for trusting me with this. Those urges can be really intense. Let's work through this together. What usually helps you when you feel this way?",
            'hopeless': "I understand feeling like there's no way forward. But you're still here, and that matters. Let's take this one moment at a time. What's the hardest part right now?"
        }
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['suicide', 'kill myself', 'end it all', 'no point living']):
            return responses['suicide']
        elif any(word in message_lower for word in ['hurt myself', 'self harm', 'cutting']):
            return responses['self_harm']
        elif any(word in message_lower for word in ['no hope', 'hopeless', 'give up', 'no point']):
            return responses['hopeless']
        else:
            return responses['default']
    
    def generate_fast_response(self, user_id: str, emotion: str, intensity: float) -> str:
        """OPTIMIZED: Fast response with 30s timeout"""
        
        # Build conversational context
        messages = [
            {
                "role": "system",
                "content": """You are NAINA, a warm and empathetic mental health AI companion. 

YOUR PERSONALITY:
- Be conversational, not clinical
- Use active listening techniques
- Ask follow-up questions
- Validate emotions before suggesting solutions
- Be present and engaged, not detached

CONVERSATION RULES:
1. ALWAYS respond conversationally first
2. Ask about their feelings/thoughts
3. Only suggest professional help if they're in real danger (suicidal)
4. For sadness, stress, anxiety → listen, validate, help them process
5. Keep responses under 100 words
6. Use empathetic phrases: "I hear you", "That sounds tough", "Tell me more"

DO NOT:
- Jump to "talk to a friend" immediately
- Give generic advice without understanding context
- Be dismissive of their feelings
- Suggest professional help unless truly critical

REMEMBER: You're a supportive listener first, advisor second."""
            }
        ]
        
        # Add recent conversation history (last 6 messages for speed)
        messages.extend(user_conversations[user_id]['messages'][-6:])
        
        # Try AI response with SHORT timeout
        if model is not None:
            try:
                result_container = {'output': None, 'error': None}
                
                def call_bytez():
                    try:
                        result = model.run(messages)
                        result_container['output'] = result
                    except Exception as e:
                        result_container['error'] = str(e)
                
                thread = threading.Thread(target=call_bytez)
                thread.daemon = True
                thread.start()
                thread.join(timeout=30.0)  # REDUCED from 120s to 30s
                
                if thread.is_alive():
                    print("[TIMEOUT] Switching to fast fallback")
                    return self.fast_fallback_response(user_conversations[user_id]['messages'][-1]['content'], emotion, intensity)
                
                if result_container['error']:
                    return self.fast_fallback_response(user_conversations[user_id]['messages'][-1]['content'], emotion, intensity)
                
                result = result_container['output']
                
                if result and hasattr(result, 'output') and result.output:
                    if isinstance(result.output, str):
                        response = result.output.strip()
                        # Ensure response is conversational and not too long
                        if len(response) > 500:
                            response = response[:497] + "..."
                        return response
                    elif isinstance(result.output, dict) and 'content' in result.output:
                        return result.output['content'].strip()
                
                return self.fast_fallback_response(user_conversations[user_id]['messages'][-1]['content'], emotion, intensity)
            
            except Exception as e:
                print(f"[ERROR] {e}")
                return self.fast_fallback_response(user_conversations[user_id]['messages'][-1]['content'], emotion, intensity)
        else:
            return self.fast_fallback_response(user_conversations[user_id]['messages'][-1]['content'], emotion, intensity)
    
    def fast_fallback_response(self, message: str, emotion: str, intensity: float) -> str:
        """Fast, intelligent fallback responses - CONVERSATIONAL"""
        
        message_lower = message.lower()
        
        # Emotion-specific conversational responses
        responses = {
            'sad': [
                "I can hear the sadness in what you're saying. What's been weighing on you?",
                "That sounds really tough. How long have you been feeling this way?",
                "I'm here with you. Tell me more about what's making you feel sad."
            ],
            'anxious': [
                "Anxiety can feel so overwhelming. What's triggering these feelings right now?",
                "I understand how unsettling anxiety can be. What's been on your mind?",
                "Let's work through this together. What specifically is making you anxious?"
            ],
            'stressed': [
                "Stress can be exhausting. What's causing the most pressure right now?",
                "I hear you. What's been the biggest source of stress lately?",
                "That sounds like a lot to handle. Want to talk about what's stressing you most?"
            ],
            'angry': [
                "It's okay to feel angry. What happened that's making you feel this way?",
                "Anger is a valid emotion. Tell me what's frustrating you.",
                "I can sense your frustration. What's been building up?"
            ],
            'neutral': [
                "I'm listening. Tell me more about what's on your mind.",
                "How have things been going for you lately?",
                "What would you like to talk about today?"
            ],
            'happy': [
                "It's wonderful to hear some positivity! What's been going well?",
                "I'm glad things are looking up. Tell me more!",
                "That's great to hear. What's been making you feel good?"
            ]
        }
        
        # Get responses for current emotion
        emotion_responses = responses.get(emotion, responses['neutral'])
        
        # Rotate through responses for variety
        import random
        return random.choice(emotion_responses)
    
    def send_json_response(self, data, status_code):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), NAINAHandler)
    print(f"🚀 NAINA v6.0 Server running on port {port}")
    print("⚡ Optimized for speed (30s timeout)")
    print("💬 Conversational mode enabled")
    server.serve_forever()
