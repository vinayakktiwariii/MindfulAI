from .conversation_db import ConversationDatabase
from .models import UserProfile
from .nlp_engine import AdvancedNLPEngine
from .context_memory import ContextMemory

def handle_analytics_api(path, query_params):
    """Route analytics API requests"""
    
    user_id = query_params.get('user_id', ['guest'])[0]
    
    if path == '/api/analytics/history/':
        limit = int(query_params.get('limit', ['50'])[0])
        history = ConversationDatabase.get_conversation_history(user_id, limit)
        return {'messages': history}, 200
    
    elif path == '/api/analytics/stats/':
        stats = ConversationDatabase.get_conversation_analytics(user_id)
        return stats, 200
    
    elif path == '/api/analytics/export/':
        format_type = query_params.get('format', ['json'])[0]
        export_data = ConversationDatabase.export_conversation(user_id, format_type)
        if export_data:
            return export_data, 200
        else:
            return {'error': 'No data to export'}, 404
    
    elif path == '/api/user/profile/':
        user_data = UserProfile.get_user(user_id)
        if user_data:
            return user_data, 200
        else:
            return {'error': 'User not found'}, 404
    
    # NEW: Insights endpoint
    elif path == '/api/analytics/insights/':
        conv_file = ConversationDatabase.CONVERSATIONS_DIR / f"{user_id}.json"
        if conv_file.exists():
            import json
            with open(conv_file, 'r') as f:
                data = json.load(f)
            insights = AdvancedNLPEngine.generate_conversation_insights(data)
            if insights:
                return insights, 200
        return {'error': 'No insights available'}, 404
    
    # NEW: Context summary endpoint
    elif path == '/api/analytics/context/':
        summary = ContextMemory.get_conversation_summary(user_id)
        if summary:
            return summary, 200
        else:
            return {'error': 'No context available'}, 404
    
    return {'error': 'Not found'}, 404
