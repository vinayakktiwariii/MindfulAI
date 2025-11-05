# data/conversational_ai_module.py
# Conversational AI for NAINA - Week 2

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from pathlib import Path

print("="*80)
print("🧠 NAINA CONVERSATIONAL AI MODULE - WEEK 2")
print("="*80)

# Load pre-trained model for mental health conversations
print("\n📥 Loading pre-trained conversational model...")

try:
    # Using DistilGPT-2 for faster, lighter responses
    model_name = "distilgpt2"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Move to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    
    print(f"✅ Model loaded: {model_name}")
    print(f"✅ Device: {device}")
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("⚠️  Will use fallback responses")

# Load emotion dataset for sentiment analysis
print("\n📥 Loading sentiment analysis model...")

try:
    emotion_pipe = pipeline("text-classification", 
                           model="distilbert-base-uncased-finetuned-sst-2-english")
    print("✅ Emotion classifier loaded")
except Exception as e:
    print(f"⚠️  Emotion classifier failed: {e}")
    emotion_pipe = None

# Conversation memory
conversation_memory = {}

def generate_response(user_message: str, user_id: str = "default") -> dict:
    """
    Generate empathetic response using LLM
    
    Args:
        user_message: User's input text
        user_id: Track conversation per user
    
    Returns:
        {
            'response': str,
            'emotion': str,
            'confidence': float
        }
    """
    
    try:
        # Analyze emotion
        emotion = "neutral"
        confidence = 0.5
        
        if emotion_pipe:
            result = emotion_pipe(user_message[:512])[0]
            emotion = result['label']
            confidence = result['score']
        
        # Generate response prompt
        prompts = {
            'sad': "User said they're sad. Empathetic response: ",
            'angry': "User expressed anger. Compassionate response: ",
            'neutral': "User message: '{}'".format(user_message),
            'POSITIVE': "User is happy. Supportive response: ",
        }
        
        prompt = prompts.get(emotion, f"User: {user_message}\nAssistant: ")
        
        # Generate response
        inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)
        
        outputs = model.generate(
            inputs,
            max_length=100,
            num_beams=2,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_p=0.9
        )
        
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response_text.replace(prompt, '').strip()
        
        # Store in memory
        if user_id not in conversation_memory:
            conversation_memory[user_id] = []
        
        conversation_memory[user_id].append({
            'user': user_message,
            'assistant': response,
            'emotion': emotion
        })
        
        return {
            'response': response if response else "I'm here to listen. Tell me more.",
            'emotion': emotion,
            'confidence': float(confidence)
        }
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return {
            'response': "I understand. I'm here to support you. What would help?",
            'emotion': 'neutral',
            'confidence': 0.5
        }

def get_conversation_history(user_id: str = "default") -> list:
    """Get conversation history for a user"""
    return conversation_memory.get(user_id, [])

# Test
if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧪 TESTING CONVERSATIONAL AI")
    print("="*80)
    
    test_messages = [
        "I feel really sad today",
        "Things are getting better",
        "I'm anxious about tomorrow",
    ]
    
    for msg in test_messages:
        response = generate_response(msg)
        print(f"\n👤 User: {msg}")
        print(f"🤖 NAINA: {response['response']}")
        print(f"   Emotion: {response['emotion']} ({response['confidence']:.2f})")

print("\n" + "="*80)
print("✅ CONVERSATIONAL AI MODULE READY!")
print("="*80)
