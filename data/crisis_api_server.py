# data/crisis_api_server.py - RAILWAY COMPATIBLE
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import time
from urllib.parse import urlparse, parse_qs

# Get API key DIRECTLY from environment (Railway sets this)
BYTEZ_API_KEY = os.getenv('BYTEZ_API_KEY', '05bb0c56a16725d749100641b2dceaf2')

print(f"🔑 API Key from environment: {BYTEZ_API_KEY[:15]}...")

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
    print(f"❌ Bytez initialization failed: {e}")
    print("Continuing with fallback mode...")
    model = None

detector = CrisisDetector()
emotion_classifier = EmotionClassifier()
user_conversations = {}

print("="*80)
print("NAINA v5.0 - PRODUCTION (RAILWAY COMPATIBLE)")
print("="*80)
print("✅ Crisis Detection: ACTIVE")
print("✅ Emotion Classification: ACTIVE")
print("✅ Advanced NLP: ACTIVE")
print("✅ Analytics: ACTIVE")
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
                
                UserProfile.create_user(user_id, f"User_{user_id[-6:]}")
                
                if user_id not in user_conversations:
                    user_conversations[user_id] = {'messages': []}
                
                user_conversations[user_id]['messages'].append({
                    'role': 'user',
                    'content': user_message
                })
                
                start_time = time.time()
                
                crisis_result = detector.detect(user_message)
                if crisis_result['is_crisis']:
                    print(f"[CRISIS] {crisis_result['severity']}")
                    crisis_response = get_crisis_response(crisis_result['severity'])
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
                
                emotion_result = emotion_classifier.classify(user_message)
                emotion, intensity, confidence = AdvancedNLPEngine.analyze_emotion_intensity(user_message)
                print(f"[EMOTION] {emotion} (intensity: {intensity:.2f})")
                
                intent, intent_confidence, intent_keywords = AdvancedNLPEngine.detect_intent(user_message)
                print(f"[INTENT] {intent}")
                
                theme, theme_confidence, theme_keywords = AdvancedNLPEngine.extract_conversation_theme(user_message)
                print(f"[THEME] {theme}")
                
                start_time = time.time()
                ai_response = self.generate_response(user_id)
                response_time = time.time() - start_time
                print(f"[RESPONSE TIME] {response_time:.2f}s")
                
                user_conversations[user_id]['messages'].append({
                    'role': 'assistant',
                    'content': ai_response
                })
                
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
        query = urlparse(self.path).query
        query_params = urlparse(self.path).query.split('&') if urlparse(self.path).query else []
        
        if self.path.startswith('/api/analytics/'):
            from mindfulai_backend.analytics.views import handle_analytics_api
            query_dict = {}
            for param in query_params:
                if '=' in param:
                    k, v = param.split('=', 1)
                    query_dict[k] = [v]
            response_data, status_code = handle_analytics_api(self.path, query_dict)
            self.send_json_response(response_data, status_code)
        
        elif self.path == '/api/chat/health/':
            self.send_json_response({
                'status': 'healthy',
                'model': 'Qwen2.5-3B-Instruct',
                'provider': 'Bytez.com',
                'timeout': '120s',
                'active_conversations': len(user_conversations),
                'analytics': 'ACTIVE'
            }, 200)
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_response(self, user_id: str) -> str:
        if model is None:
            return self.fallback_conversational(user_id)
        
        messages = [
            {
                "role": "system",
                "content": "You are NAINA, a compassionate mental health AI."
            }
        ]
        
        messages.extend(user_conversations[user_id]['messages'][-10:])
        
        try:
            print("[SDK] Calling Bytez API...")
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
                return self.fallback_conversational(user_id)
            
            if result_container['error']:
                return self.fallback_conversational(user_id)
            
            result = result_container['output']
            
            if result and hasattr(result, 'output') and result.output:
                if isinstance(result.output, str):
                    return result.output.strip()
                elif isinstance(result.output, dict) and 'content' in result.output:
                    return result.output['content'].strip()
            
            return self.fallback_conversational(user_id)
        
        except Exception as e:
            print(f"[ERROR] {e}")
            return self.fallback_conversational(user_id)
    
    def fallback_conversational(self, user_id: str) -> str:
        return "I'm here to listen. What's on your mind?"
    
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
    print(f"🚀 NAINA Server running on port {port}")
    server.serve_forever()
