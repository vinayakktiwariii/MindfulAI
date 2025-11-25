# chatbot/views.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from bytez import Bytez

# Uncomment when you have models set up
# from mindfulai_backend.analytics.models import Conversation, Message, EmotionLog, CrisisEvent
# from .ai_engine.crisis_detector import CrisisDetector, get_crisis_response

# Initialize Bytez SDK
BYTEZ_API_KEY = "05bb0c56a16725d749100641b2dceaf2"
sdk = Bytez(BYTEZ_API_KEY)
model = sdk.model("Qwen/Qwen2.5-3B-Instruct")

# Initialize crisis detector (when ready)
# crisis_detector = CrisisDetector()


def generate_ai_response(user_message, conversation_history=None):
    """Generate AI response using Bytez Qwen SDK"""
    
    system_prompt = """You are NAINA, a compassionate AI mental wellness companion created by Vinayak Tiwari from ArqonX AI Technology.

Be:
- Warm and empathetic
- Brief (2-3 sentences max)
- Supportive without being medical
- Ask follow-up questions

Never diagnose. Always encourage professional help for serious issues."""
    
    try:
        print(f"\n🤖 Calling Bytez Qwen2.5-3B...")
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Call Bytez model
        result = model.run(messages)

        if result.error:
            print(f"❌ Bytez Error: {result.error}")
            return "I'm here to listen. Tell me what's on your mind."

        if result.output and 'content' in result.output:
            ai_response = result.output['content']
            print(f"✅ AI Response: {ai_response}")
            return ai_response.strip()
        else:
            print(f"⚠️ No output received")
            return "I'm here to support you. How can I help today?"
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return "I'm here to listen. What's on your mind?"


def detect_crisis(user_message):
    """Simple crisis detection"""
    crisis_keywords = [
        'suicide', 'kill myself', 'end my life', 'want to die', 
        'hurt myself', 'self harm', 'end it all', 'no reason to live'
    ]
    
    message_lower = user_message.lower()
    for keyword in crisis_keywords:
        if keyword in message_lower:
            return True, 'high'
    
    return False, 'normal'


def get_crisis_response(crisis_level):
    """Get crisis response"""
    if crisis_level == 'high':
        return """I'm really concerned about what you're sharing. Please reach out for immediate help:

🆘 **India Crisis Helplines:**
- AASRA: 9820466726
- Vandrevala Foundation: 1860 2662 345
- Emergency: 112 / 102

You matter, and there are people who want to help. Would you like to talk about what's troubling you?"""
    return "I'm here to support you. How can I help?"


@api_view(['POST'])
@permission_classes([AllowAny])
def chat(request):
    """Public chat endpoint with Bytez Qwen AI"""
    user_message = request.data.get('message', '').strip()
    conversation_id = request.data.get('conversation_id')
    conversation_history = request.data.get('history', [])
    
    if not user_message:
        return Response({'error': 'Message cannot be empty'}, status=400)
    
    try:
        print(f"\n{'='*60}")
        print(f"💬 NEW MESSAGE (Public)")
        print(f"📝 Message: {user_message}")
        print(f"{'='*60}")
        
        # Detect crisis
        crisis_detected, crisis_level = detect_crisis(user_message)
        
        # Generate response
        if crisis_detected:
            ai_response = get_crisis_response(crisis_level)
            print(f"🚨 CRISIS DETECTED: {crisis_level}")
        else:
            ai_response = generate_ai_response(user_message, conversation_history)
        
        return Response({
            'response': ai_response,
            'conversation_id': conversation_id,
            'emotion': 'neutral',
            'crisis_detected': crisis_detected,
            'crisis_level': crisis_level,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ CHAT ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'response': "I'm here to listen. What would you like to talk about?",
            'error': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_conversation_history(request, conversation_id=None):
    """Get conversation history"""
    # TODO: Implement when database models are ready
    return Response({'conversations': []})


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_conversation(request, conversation_id):
    """Delete conversation"""
    # TODO: Implement when database models are ready
    return Response({'message': 'Deleted successfully'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_stats(request):
    """Get user stats"""
    # TODO: Implement when database models are ready
    return Response({
        'total_conversations': 0,
        'total_messages': 0,
        'recent_crisis_events': []
    })
