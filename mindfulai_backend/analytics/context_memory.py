import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class ContextMemory:
    """Maintain conversation context and memory"""
    
    MEMORY_DIR = Path("data/memory")
    MEMORY_DIR.mkdir(exist_ok=True)
    
    @staticmethod
    def store_context(user_id, theme, intent, keywords, emotion):
        """Store conversation context for future reference"""
        memory_file = ContextMemory.MEMORY_DIR / f"{user_id}_context.json"
        
        context_entry = {
            "timestamp": datetime.now().isoformat(),
            "theme": theme,
            "intent": intent,
            "keywords": keywords,
            "emotion": emotion
        }
        
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                memory_data = json.load(f)
        else:
            memory_data = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "contexts": [],
                "theme_history": defaultdict(int),
                "intent_history": defaultdict(int)
            }
        
        memory_data['contexts'].append(context_entry)
        
        # Keep only last 100 contexts
        if len(memory_data['contexts']) > 100:
            memory_data['contexts'] = memory_data['contexts'][-100:]
        
        # Update theme and intent history
        if theme not in memory_data['theme_history']:
            memory_data['theme_history'][theme] = 0
        memory_data['theme_history'][theme] += 1
        
        if intent not in memory_data['intent_history']:
            memory_data['intent_history'][intent] = 0
        memory_data['intent_history'][intent] += 1
        
        with open(memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        return context_entry
    
    @staticmethod
    def get_user_context(user_id):
        """Get user's conversation context and memory"""
        memory_file = ContextMemory.MEMORY_DIR / f"{user_id}_context.json"
        
        if not memory_file.exists():
            return None
        
        with open(memory_file, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def get_primary_themes(user_id):
        """Get top themes for user"""
        context = ContextMemory.get_user_context(user_id)
        
        if not context:
            return []
        
        themes = sorted(
            context['theme_history'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [theme[0] for theme in themes[:3]]
    
    @staticmethod
    def get_conversation_summary(user_id):
        """Generate summary of user's conversation patterns"""
        context = ContextMemory.get_user_context(user_id)
        
        if not context or not context['contexts']:
            return None
        
        recent_contexts = context['contexts'][-10:]
        
        emotions = [c['emotion'] for c in recent_contexts]
        themes = [c['theme'] for c in recent_contexts]
        intents = [c['intent'] for c in recent_contexts]
        
        return {
            "total_interactions": len(context['contexts']),
            "recent_emotion": emotions[-1] if emotions else None,
            "primary_theme": max(set(themes), key=themes.count) if themes else None,
            "primary_intent": max(set(intents), key=intents.count) if intents else None,
            "emotion_distribution": dict(defaultdict(int, {e: emotions.count(e) for e in set(emotions)})),
            "theme_history": dict(context['theme_history']),
            "intent_history": dict(context['intent_history'])
        }
