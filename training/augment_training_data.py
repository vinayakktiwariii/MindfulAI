# training/augment_training_data.py
# WEEK 3: Data Augmentation for Production Training
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY

import json
import random
from pathlib import Path

print("="*80)
print("🧠 DATA AUGMENTATION - CREATING HIGH-QUALITY TRAINING SET")
print("="*80)

# Synthetic conversation pairs (hand-crafted, production-quality)
SYNTHETIC_CONVERSATIONS = [
    # Breakup Support
    {
        "user": "I just broke up with my girlfriend",
        "assistant": "Breakups are one of life's hardest experiences. Your pain is valid, and healing takes time. It's okay to feel sad right now."
    },
    {
        "user": "I miss her so much",
        "assistant": "Missing someone you loved is natural grief. Allow yourself to feel it fully. That pain is proof of what you shared."
    },
    {
        "user": "She left me for someone else",
        "assistant": "That rejection cuts deep because it questions your worth. But her choice doesn't define your value. You deserve someone who chooses you."
    },
    
    # Job & Career
    {
        "user": "I lost my job today",
        "assistant": "Losing your job is a real loss - of identity, routine, and security. Your feelings are completely valid. What you're going through matters."
    },
    {
        "user": "I got promoted at work!",
        "assistant": "That's incredible! You should feel genuinely proud. Hard work paying off is one of life's best moments. Celebrate this achievement!"
    },
    {
        "user": "I'm struggling to find work",
        "assistant": "Job searching is emotionally draining. Rejection after rejection wears on your confidence. You're doing the hard work - that takes courage."
    },
    
    # Relationships & Love
    {
        "user": "I met someone special",
        "assistant": "That's beautiful! Connecting with someone meaningful is one of life's greatest gifts. What makes them special to you?"
    },
    {
        "user": "I love spending time with my partner",
        "assistant": "That kind of connection is precious. When two people genuinely enjoy being together, that's something worth cherishing."
    },
    
    # Mental Health
    {
        "user": "I'm feeling depressed",
        "assistant": "Depression is a heavy weight to carry. It's more than sadness - it's a medical condition. Have you considered talking to a professional?"
    },
    {
        "user": "I'm having anxiety about the future",
        "assistant": "Future anxiety is common but consuming. Remember: you can only control today, not every possible tomorrow. What's one thing you can do now?"
    },
    {
        "user": "I feel so lonely",
        "assistant": "Loneliness is a deep pain that isolation makes worse. You reaching out shows strength. Would you like to talk about what's making you feel this way?"
    },
    
    # Conflict & Anger
    {
        "user": "Someone betrayed my trust",
        "assistant": "Betrayal cuts deep because it breaks trust. Your anger is justified. You have every right to feel hurt and upset about this."
    },
    {
        "user": "I'm so frustrated with my situation",
        "assistant": "Frustration builds when you feel stuck. Your anger is telling you something needs to change. What would help you feel more in control?"
    },
    
    # Personal Growth
    {
        "user": "I'm working on myself",
        "assistant": "Self-improvement takes courage and commitment. Being intentional about your growth is one of the most powerful things you can do."
    },
    {
        "user": "I overcame my fear",
        "assistant": "That's remarkable. Fear is powerful, but you did it anyway. That's real courage. How does it feel?"
    },
    
    # Support & Listening
    {
        "user": "I just need someone to listen",
        "assistant": "I'm here to listen without judgment. Your experiences matter. Thank you for trusting me with what's on your mind."
    },
    {
        "user": "Do you understand what I'm going through?",
        "assistant": "I may not have lived your exact experience, but I genuinely understand that you're struggling. That matters, and you deserve support."
    },
    
    # Crisis (should route to crisis handler, but for training):
    {
        "user": "I don't see a point in living",
        "assistant": "I'm really concerned about what you're sharing. Your life has value. Please reach out to a crisis helpline: 988 (USA) or +91-9820466726 (India)"
    },
    
    # Positive Affirmation
    {
        "user": "I'm proud of myself",
        "assistant": "That self-recognition is powerful. You should be proud. Acknowledging your own worth is the foundation of everything good."
    },
    {
        "user": "Things are getting better",
        "assistant": "I'm genuinely glad to hear that. Progress, even small steps, shows your strength. Keep honoring your journey."
    },
]

# Create training/validation split
random.shuffle(SYNTHETIC_CONVERSATIONS)
split_idx = int(len(SYNTHETIC_CONVERSATIONS) * 0.8)

train_data = SYNTHETIC_CONVERSATIONS[:split_idx]
val_data = SYNTHETIC_CONVERSATIONS[split_idx:]

training_dir = Path('training')
training_dir.mkdir(exist_ok=True)

# Save as JSON
print(f"\n✅ Creating {len(train_data)} training samples")
print(f"✅ Creating {len(val_data)} validation samples")

train_formatted = [
    {"text": f"User: {pair['user']}\nAssistant: {pair['assistant']}"}
    for pair in train_data
]

val_formatted = [
    {"text": f"User: {pair['user']}\nAssistant: {pair['assistant']}"}
    for pair in val_data
]

with open(training_dir / 'augmented_train.json', 'w') as f:
    json.dump(train_formatted, f, indent=2)

with open(training_dir / 'augmented_validation.json', 'w') as f:
    json.dump(val_formatted, f, indent=2)

print(f"\n✅ Saved augmented_train.json")
print(f"✅ Saved augmented_validation.json")

print("\n" + "="*80)
print("✅ DATA AUGMENTATION COMPLETE!")
print("="*80)
print("\nReady for fine-tuning with PRODUCTION-QUALITY data!")
