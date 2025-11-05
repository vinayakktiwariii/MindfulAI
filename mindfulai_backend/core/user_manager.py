import json
import hashlib
from datetime import datetime
from pathlib import Path

# Use existing data directory
USERS_DIR = Path("data/users")
USERS_DIR.mkdir(exist_ok=True)

class UserManager:
    @staticmethod
    def create_user(user_id, username, email="guest@naina.local"):
        """Create new user profile"""
        user_file = USERS_DIR / f"{user_id}.json"
        
        if user_file.exists():
            return json.load(open(user_file))
        
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "preferences": {
                "theme": "dark",
                "notifications": True,
                "language": "en"
            },
            "stats": {
                "total_messages": 0,
                "total_conversations": 0,
                "crisis_detections": 0,
                "average_response_time": 0
            }
        }
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return user_data
    
    @staticmethod
    def get_user(user_id):
        """Get user profile"""
        user_file = USERS_DIR / f"{user_id}.json"
        
        if user_file.exists():
            with open(user_file, 'r') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def update_user(user_id, updates):
        """Update user profile"""
        user_file = USERS_DIR / f"{user_id}.json"
        
        if user_file.exists():
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            user_data.update(updates)
            user_data['last_login'] = datetime.now().isoformat()
            
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            
            return user_data
        return None
    
    @staticmethod
    def update_stats(user_id, stats_dict):
        """Update user statistics"""
        user_data = UserManager.get_user(user_id)
        if user_data:
            user_data['stats'].update(stats_dict)
            UserManager.update_user(user_id, user_data)
            return user_data
        return None
