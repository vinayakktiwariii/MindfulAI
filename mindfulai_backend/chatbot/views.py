# mindfulai_backend/chatbot/views.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .ai_engine.crisis_detector import CrisisDetector, get_crisis_response

# Initialize crisis detector
crisis_detector = CrisisDetector()


@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    """
    Main chat endpoint - handles user messages through the safety pipeline.
    NO REST FRAMEWORK DEPENDENCIES - PURE DJANGO
    """
    try:
        # Parse JSON request body
        body = request.body.decode('utf-8')
        data = json.loads(body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'error': 'Message cannot be empty'
            }, status=400)
        
        # TIER 1: Crisis Detection (THE CORE SAFETY SYSTEM)
        crisis_result = crisis_detector.detect(user_message)
        
        # If crisis detected, return crisis response
        if crisis_result['is_crisis']:
            return JsonResponse({
                'response': get_crisis_response(crisis_result['severity']),
                'type': 'crisis',
                'severity': crisis_result['severity'],
                'confidence': crisis_result['confidence'],
                'metadata': {
                    'message': crisis_result['message']
                }
            }, status=200)
        
        # Normal conversation response (TODO: integrate LLM later)
        return JsonResponse({
            'response': "I hear you. I'm here to listen. What would you like to talk about?",
            'type': 'normal',
            'severity': crisis_result['severity'],
            'confidence': 0.5
        }, status=200)
        
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        return JsonResponse({
            'error': 'Invalid JSON format',
            'details': str(e)
        }, status=400)
    except Exception as e:
        print(f"Error in chat view: {str(e)}")
        print(f"Error type: {type(e)}")
        return JsonResponse({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }, status=500)


@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'MindfulAI API is running',
        'author': 'VINAYAK TIWARI | ARQONX-AI TECHNOLOGY'
    }, status=200)
