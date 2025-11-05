# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anonymous_id = models.UUIDField(default=uuid.uuid4, unique=True)
    subscription_tier = models.CharField(
        max_length=20, 
        choices=[('free', 'Free'), ('premium', 'Premium')], 
        default='free'
    )
    daily_message_count = models.IntegerField(default=0)
    last_message_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User Profile - {self.subscription_tier}"

class Conversation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    conversation_id = models.UUIDField(default=uuid.uuid4, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.CharField(
        max_length=10, 
        choices=[('user', 'User'), ('ai', 'AI')]
    )
    detected_emotion = models.CharField(max_length=50, blank=True)
    detected_intent = models.CharField(max_length=50, blank=True)
    crisis_flag = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']

class ConversationReview(models.Model):
    """For the human-supervised learning loop"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    ai_message = models.ForeignKey(Message, on_delete=models.CASCADE)
    quality_rating = models.IntegerField(
        choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Excellent')]
    )
    human_feedback = models.TextField(blank=True)
    suggested_response = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.CharField(max_length=100, default="VINAYAK TIWARI")
