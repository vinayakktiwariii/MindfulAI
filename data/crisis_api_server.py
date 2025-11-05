# data/crisis_api_server.py - PRODUCTION (WITH API KEY PROTECTION)
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from bytez import Bytez
import time
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable (NOT hardcoded)
BYTEZ_API_KEY = os.getenv('')

if not BYTEZ_API_KEY:
    print("❌ ERROR: BYTEZ_API_KEY not found in environment variables")
    print("Create a .env file with: BYTEZ_API_KEY=your_key_here")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent.parent))

from mindfulai_backend.chatbot.ai_engine.crisis_detector import CrisisDetector, get_crisis_response
from mindfulai_backend.chatbot.ai_engine.emotion_classifier import EmotionClassifier
from mindfulai_backend.analytics.conversation_db import ConversationDatabase
from mindfulai_backend.analytics.models import UserProfile
from mindfulai_backend.analytics.nlp_engine import AdvancedNLPEngine
from mindfulai_backend.analytics.context_memory import ContextMemory

# Bytez SDK with API key from environment
sdk = Bytez(BYTEZ_API_KEY)
model = sdk.model("Qwen/Qwen2.5-3B-Instruct")

detector = CrisisDetector()
emotion_classifier = EmotionClassifier()
user_conversations = {}

print("="*80)
print("NAINA v4.0 - PRODUCTION (WEEK 5 - ADVANCED NLP)")
print("="*80)
print("Crisis Detection: ACTIVE")
print("Emotion Classification: ACTIVE")
print("Advanced NLP: ACTIVE (Intensity, Intent, Context)")
print("AI Model: Qwen2.5-3B-Instruct (Bytez)")
print("API Timeout: 120 seconds (natural)")
print("Analytics: ACTIVE")
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
                
                # Create/update user profile
                UserProfile.create_user(user_id, f"User_{user_id[-6:]}")
                
                if user_id not in user_conversations:
                    user_conversations[user_id] = {'messages': []}
                
                # Store user message
                user_conversations[user_id]['messages'].append({
                    'role': 'user',
                    'content': user_message
                })
                
                # Start timing
                start_time = time.time()
                
                # Crisis check
                crisis_result = detector.detect(user_message)
                if crisis_result['is_crisis']:
                    print(f"[CRISIS] {crisis_result['severity']}")
                    crisis_response = get_crisis_response(crisis_result['severity'])
                    response_time = time.time() - start_time
                    
                    # Store context in memory
                    ContextMemory.store_context(user_id, 'crisis', 'crisis', ['emergency'], 'crisis')
                    
                    # SAVE TO HISTORY
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
                
                # ADVANCED NLP - Emotion classification with intensity
                emotion_result = emotion_classifier.classify(user_message)
                emotion, intensity, confidence = AdvancedNLPEngine.analyze_emotion_intensity(user_message)
                print(f"[EMOTION] {emotion} (intensity: {intensity:.2f})")
                
                # Intent detection
                intent, intent_confidence, intent_keywords = AdvancedNLPEngine.detect_intent(user_message)
                print(f"[INTENT] {intent} (confidence: {intent_confidence:.2f})")
                
                # Theme extraction
                theme, theme_confidence, theme_keywords = AdvancedNLPEngine.extract_conversation_theme(user_message)
                print(f"[THEME] {theme}")
                
                # Generate AI response
                start_time = time.time()
                ai_response = self.generate_response(user_id)
                response_time = time.time() - start_time
                print(f"[RESPONSE TIME] {response_time:.2f}s")
                
                # Store assistant response
                user_conversations[user_id]['messages'].append({
                    'role': 'assistant',
                    'content': ai_response
                })
                
                # Store context in memory
                all_keywords = theme_keywords + intent_keywords
                ContextMemory.store_context(user_id, theme, intent, all_keywords, emotion)
                
                # Store message with analytics data
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
                    'confidence': confidence,
                    'color': emotion_result.get('color', '#667eea')
                }, 200)
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"[ERROR] {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({'error': str(e)}, 500)
    
    def do_GET(self):
        query = urlparse(self.path).query
        query_params = parse_qs(query)
        
        if self.path.startswith('/api/analytics/'):
            # Route to analytics API
            from mindfulai_backend.analytics.views import handle_analytics_api
            
            response_data, status_code = handle_analytics_api(self.path, query_params)
            self.send_json_response(response_data, status_code)
        
        elif self.path.startswith('/api/user/'):
            # Route to user API
            from mindfulai_backend.analytics.views import handle_analytics_api
            
            response_data, status_code = handle_analytics_api(self.path, query_params)
            self.send_json_response(response_data, status_code)
        
        elif self.path == '/api/chat/health/':
            self.send_json_response({
                'status': 'healthy',
                'model': 'Qwen2.5-3B-Instruct',
                'provider': 'Bytez.com',
                'timeout': '120s',
                'active_conversations': len(user_conversations),
                'analytics': 'ACTIVE',
                'advanced_nlp': 'ACTIVE'
            }, 200)
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_response(self, user_id: str) -> str:
        """Generate using Bytez SDK with 120-second timeout"""
        
        messages = [
            {
                "role": "system",
                "content": "You are NAINA, a compassionate mental health AI by ArqonX (Vinayak Tiwari). Be warm, empathetic, and supportive. Ask thoughtful follow-up questions. Keep responses conversational and helpful, around 2-3 sentences."
            }
        ]
        
        # Add last 10 messages for context
        messages.extend(user_conversations[user_id]['messages'][-10:])
        
        try:
            print("[SDK] Calling Bytez API (120s timeout)...")
            
            import threading
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
            thread.join(timeout=120.0)
            
            if thread.is_alive():
                print("[TIMEOUT] Bytez took >120s, using fallback")
                return self.fallback_conversational(user_id)
            
            if result_container['error']:
                print(f"[SDK ERROR] {result_container['error']}")
                return self.fallback_conversational(user_id)
            
            result = result_container['output']
            
            if result and hasattr(result, 'output') and result.output:
                if isinstance(result.output, dict) and 'content' in result.output:
                    output = result.output['content'].strip()
                    print(f"[SDK SUCCESS] Response length: {len(output)} chars")
                    return output if output else self.fallback_conversational(user_id)
                elif isinstance(result.output, str):
                    output = result.output.strip()
                    print(f"[SDK SUCCESS] Response length: {len(output)} chars")
                    return output if output else self.fallback_conversational(user_id)
            
            print("[SDK] No valid output, using fallback")
            return self.fallback_conversational(user_id)
        
        except Exception as e:
            print(f"[SDK ERROR] {e}")
            import traceback
            traceback.print_exc()
            return self.fallback_conversational(user_id)
    
    def fallback_conversational(self, user_id: str) -> str:
        """Context-aware fallback when API fails"""
        
        recent_messages = user_conversations[user_id]['messages']
        is_first = len(recent_messages) <= 1
        
        if is_first:
            return "Hi! Thanks for reaching out to NAINA. What's on your mind today?"
        
        prev_msg = recent_messages[-2]['content'].lower() if len(recent_messages) >= 2 else ""
        
        if any(word in prev_msg for word in ['broke', 'breakup', 'relationship', 'girlfriend', 'boyfriend']):
            return "That breakup pain is real. How long has it been since it happened?"
        elif any(word in prev_msg for word in ['job', 'work', 'fired', 'quit']):
            return "Losing a job is tough. What's worrying you most right now?"
        elif any(word in prev_msg for word in ['lonely', 'alone', 'isolated']):
            return "Loneliness is hard. Have you been able to talk to anyone about this?"
        elif any(word in prev_msg for word in ['sad', 'depressed', 'down', 'hopeless']):
            return "That sounds heavy. Want to tell me more about what's been happening?"
        elif any(word in prev_msg for word in ['anxious', 'anxiety', 'worried', 'panic']):
            return "Anxiety can feel overwhelming. What situations trigger this most for you?"
        elif any(word in prev_msg for word in ['family', 'parents', 'mom', 'dad']):
            return "Family dynamics can be complex. What's been the hardest part?"
        else:
            return "Tell me more about that. I'm listening."
    
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
    server = HTTPServer(('127.0.0.1', 5000), NAINAHandler)
    print("🚀 NAINA Server Running: http://127.0.0.1:5000")
    print("📊 Analytics: http://127.0.0.1:5000/api/analytics/stats/?user_id=test")
    print("📄 Chat History: http://127.0.0.1:5000/api/analytics/history/?user_id=test")
    print("💡 Insights: http://127.0.0.1:5000/api/analytics/insights/?user_id=test")
    print("🧠 Context: http://127.0.0.1:5000/api/analytics/context/?user_id=test")
    print("⏱️  API Timeout: 120 seconds\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped gracefully")
