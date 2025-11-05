# mindfulai_backend/core/urls.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Initialize the API router (we'll add endpoints here later)
router = routers.DefaultRouter()

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # REST API base
    path('api/', include(router.urls)),
    
    path('api/chat/', include('mindfulai_backend.chatbot.urls')),  # NEW LINE
    # Chatbot URLs (we'll create these in the chatbot app later)
    # path('api/chat/', include('mindfulai_backend.chatbot.urls')),
]
