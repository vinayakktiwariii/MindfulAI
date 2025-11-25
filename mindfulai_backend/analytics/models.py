from django.db import models
from django.conf import settings
import uuid
from datetime import datetime

class UserProfile(models.Model):
    """User profile with mental health tracking"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics_profile')  # ✅ FIXED
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_conversations = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    average_emotion = models.CharField(max_length=50, default='neutral')
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return self.username
    
    @classmethod
    def create_user(cls, user_id, username):
        """Create or get user profile"""
        profile, created = cls.objects.get_or_create(
            user_id=user_id,
            defaults={'username': username}
        )
        return profile


class Conversation(models.Model):
    """Store conversation metadata"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')  # ✅ FIXED
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    message_count = models.IntegerField(default=0)
    primary_emotion = models.CharField(max_length=50, default='neutral')
    crisis_detected = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.started_at}"


class Message(models.Model):
    """Store individual messages"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')  # ✅ FIXED
    content = models.TextField()
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('assistant', 'Assistant')])
    emotion = models.CharField(max_length=50, blank=True)
    emotion_intensity = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_time = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class EmotionLog(models.Model):
    """Track emotion over time"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emotion_logs')  # ✅ FIXED
    emotion = models.CharField(max_length=50)
    intensity = models.FloatField()
    confidence = models.FloatField()
    message_text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'emotion_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.emotion} ({self.intensity})"


class CrisisEvent(models.Model):
    """Log crisis detection events"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crisis_events')  # ✅ FIXED
    severity = models.CharField(max_length=20)
    keywords_matched = models.JSONField(default=list)
    message_text = models.TextField()
    response_given = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'crisis_events'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.severity} - {self.timestamp}"
