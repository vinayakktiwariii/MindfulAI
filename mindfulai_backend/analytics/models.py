import json
from datetime import datetime
from pathlib import Path

class UserProfile:
    """User profile management"""
    
    USERS_DIR = Path("data/users")
    USERS_DIR.mkdir(exist_ok=True)
    
    @staticmethod
    def create_user(user_id, username, email="guest@naina.local"):
        """Create new user profile"""
        user_file = UserProfile.USERS_DIR / f"{user_id}.json"
        
        if user_file.exists():
            with open(user_file, 'r') as f:
                return json.load(f)
        
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
                "crisis_detections": 0
            }
        }
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return user_data
    
    @staticmethod
    def get_user(user_id):
        """Get user profile"""
        user_file = UserProfile.USERS_DIR / f"{user_id}.json"
        
        if user_file.exists():
            with open(user_file, 'r') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def update_user(user_id, updates):
        """Update user profile"""
        user_file = UserProfile.USERS_DIR / f"{user_id}.json"
        
        if user_file.exists():
            user_data = json.load(open(user_file))
            user_data.update(updates)
            user_data['last_login'] = datetime.now().isoformat()
            
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            
            return user_data
        return None
