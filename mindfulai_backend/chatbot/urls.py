# chatbot/urls.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
from django.urls import path
from . import views

urlpatterns = [
    # Chat
    path('', views.chat, name='chat'),
    
    # History
    path('history/', views.get_conversation_history, name='history'),
    path('history/<uuid:conversation_id>/', views.get_conversation_history, name='history-detail'),
    
    # Delete
    path('conversation/<uuid:conversation_id>/delete/', views.delete_conversation, name='delete'),
    
    # Stats
    path('stats/', views.get_user_stats, name='stats'),
]
