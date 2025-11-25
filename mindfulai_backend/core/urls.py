from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'MindfulAI API - Mental Wellness Chatbot',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'chat': '/api/chat/',
            'history': '/api/chat/history/',
            'stats': '/api/chat/stats/',
            'admin': '/admin/'
        },
        'status': 'operational'
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('mindfulai_backend.users.urls')),  # ✅ FIXED: Changed to 'users'
    path('api/chat/', include('mindfulai_backend.chatbot.urls')),
    path('api/', api_root),  # API root
    path('', api_root),  # Root endpoint
]
