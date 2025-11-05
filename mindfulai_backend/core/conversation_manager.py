import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Use existing data directory
CONVERSATIONS_DIR = Path("data/conversations")
CONVERSATIONS_DIR.mkdir(exist_ok=True)

class ConversationManager:
    @staticmethod
    def save_message(user_id, user_msg, ai_response, emotion, response_time, is_crisis=False):
        """Save individual message with metadata"""
        conv_file = CONVERSATIONS_DIR / f"{user_id}.json"
        
        message_data = {
            "id": datetime.now().timestamp(),
            "timestamp": datetime.now().isoformat(),
            "user_message": user_msg,
            "ai_response": ai_response,
            "emotion": emotion,
            "response_time": response_time,
            "is_crisis": is_crisis,
            "message_length": len(user_msg),
            "response_length": len(ai_response)
        }
        
        if conv_file.exists():
            with open(conv_file, 'r') as f:
                data = json.load(f)
        else:
            data = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "metadata": {
                    "total_messages": 0,
                    "total_crises": 0,
                    "emotions": {},
                    "avg_response_time": 0
                }
            }
        
        data['messages'].append(message_data)
        data['metadata']['total_messages'] = len(data['messages'])
        
        if is_crisis:
            data['metadata']['total_crises'] += 1
        
        if emotion:
            if emotion not in data['metadata']['emotions']:
                data['metadata']['emotions'][emotion] = 0
            data['metadata']['emotions'][emotion] += 1
        
        # Calculate average response time
        response_times = [msg['response_time'] for msg in data['messages']]
        data['metadata']['avg_response_time'] = sum(response_times) / len(response_times) if response_times else 0
        
        with open(conv_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return message_data
    
    @staticmethod
    def get_conversation_history(user_id, limit=50):
        """Get last N messages"""
        conv_file = CONVERSATIONS_DIR / f"{user_id}.json"
        
        if not conv_file.exists():
            return []
        
        with open(conv_file, 'r') as f:
            data = json.load(f)
        
        return data['messages'][-limit:]
    
    @staticmethod
    def get_conversation_analytics(user_id):
        """Get conversation statistics"""
        conv_file = CONVERSATIONS_DIR / f"{user_id}.json"
        
        if not conv_file.exists():
            return {
                "total_messages": 0,
                "total_conversations": 0,
                "crisis_count": 0,
                "emotions": {},
                "avg_response_time": 0
            }
        
        with open(conv_file, 'r') as f:
            data = json.load(f)
        
        return {
            "total_messages": data['metadata']['total_messages'],
            "total_conversations": len(set(msg['timestamp'].split('T')[0] for msg in data['messages'])),
            "crisis_count": data['metadata']['total_crises'],
            "emotions": data['metadata']['emotions'],
            "avg_response_time": round(data['metadata']['avg_response_time'], 2),
            "created_at": data['created_at']
        }
    
    @staticmethod
    def export_conversation(user_id, format_type='json'):
        """Export conversation history"""
        conv_file = CONVERSATIONS_DIR / f"{user_id}.json"
        
        if not conv_file.exists():
            return None
        
        with open(conv_file, 'r') as f:
            data = json.load(f)
        
        if format_type == 'json':
            return data
        
        elif format_type == 'txt':
            text = f"NAINA Conversation Export - {user_id}\n"
            text += f"Created: {data['created_at']}\n"
            text += "="*80 + "\n\n"
            
            for msg in data['messages']:
                text += f"[{msg['timestamp']}]\n"
                text += f"You: {msg['user_message']}\n"
                text += f"NAINA: {msg['ai_response']}\n"
                text += f"Emotion: {msg['emotion']} | Response Time: {msg['response_time']:.2f}s\n"
                text += "-"*80 + "\n"
            
            return text
        
        return None
