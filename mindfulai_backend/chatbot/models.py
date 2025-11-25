from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    """User profile for chatbot - FIXED"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ✅ FIXED - was User
        on_delete=models.CASCADE,
        related_name='chatbot_profile'
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chatbot_user_profiles'
    
    def __str__(self):
        return self.username
