# training/prepare_training_data.py
# WEEK 3 - Data Preparation for Fine-tuning
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES

import pandas as pd
import json
from pathlib import Path
import random

print("="*80)
print("🧠 NAINA TRAINING DATA PREPARATION - WEEK 3")
print("Built by ArqonX AI Technologies | Founder: Vinayak Tiwari")
print("="*80)

# Paths
processed_dir = Path('data/processed')
training_dir = Path('training')
training_dir.mkdir(exist_ok=True)

# Load all processed datasets
print("\n📥 Loading processed datasets...")

datasets = []
for csv_file in processed_dir.glob('*_clean.csv'):
    try:
        df = pd.read_csv(csv_file)
        datasets.append(df)
        print(f"✅ Loaded: {csv_file.name} ({len(df)} rows)")
    except Exception as e:
        print(f"⚠️  Failed to load {csv_file.name}: {e}")

if not datasets:
    print("❌ No datasets found! Check data/processed/")
    exit(1)

# Combine all datasets
print("\n🔄 Combining datasets...")
combined_df = pd.concat(datasets, ignore_index=True)
print(f"✅ Total samples: {len(combined_df)}")

# Clean and prepare
print("\n🧹 Cleaning data...")
if 'text' in combined_df.columns:
    combined_df = combined_df[['text']].copy()
elif combined_df.shape[1] > 0:
    combined_df = combined_df.iloc[:, [0]].copy()
    combined_df.columns = ['text']

combined_df['text'] = combined_df['text'].astype(str).str.strip()
combined_df = combined_df[combined_df['text'].str.len() > 10]  # Remove short text
combined_df = combined_df[combined_df['text'].str.len() < 500]  # Remove very long text
combined_df.drop_duplicates(inplace=True)
combined_df.dropna(inplace=True)

print(f"✅ After cleaning: {len(combined_df)} samples")

# Create conversation pairs for training
print("\n💬 Creating conversation pairs...")

# Mental health response templates for training
response_templates = {
    'sadness': [
        "I hear you. That sounds really difficult. I'm here to listen.",
        "Your feelings are valid. Would you like to talk more about it?",
        "I understand this is hard. I'm here with you.",
        "That's a lot to carry. How can I support you right now?",
    ],
    'general_support': [
        "I'm listening. Tell me more about what's on your mind.",
        "Thank you for sharing that with me. How are you feeling?",
        "I'm here to support you. What would help right now?",
        "That's important. I want to understand better.",
    ],
    'crisis_concern': [
        "I'm concerned about what you've shared. Are you in a safe place right now?",
        "Your safety matters to me. Would you like to talk to someone trained in crisis support?",
        "I hear how much pain you're in. Please reach out to a crisis helpline.",
    ]
}

# Detect emotion/context and create pairs
training_pairs = []

for idx, row in combined_df.iterrows():
    user_text = row['text']
    
    # Simple keyword-based categorization
    text_lower = user_text.lower()
    
    # Crisis keywords
    if any(word in text_lower for word in ['suicide', 'kill myself', 'want to die', 'end my life']):
        response = random.choice(response_templates['crisis_concern'])
    # Sadness keywords
    elif any(word in text_lower for word in ['sad', 'depressed', 'lonely', 'hurt', 'pain']):
        response = random.choice(response_templates['sadness'])
    # General support
    else:
        response = random.choice(response_templates['general_support'])
    
    training_pairs.append({
        'prompt': user_text,
        'completion': response
    })

print(f"✅ Created {len(training_pairs)} conversation pairs")

# Split into train/validation (80/20)
print("\n📊 Splitting train/validation...")
random.shuffle(training_pairs)
split_idx = int(len(training_pairs) * 0.8)

train_pairs = training_pairs[:split_idx]
val_pairs = training_pairs[split_idx:]

print(f"✅ Training: {len(train_pairs)} samples")
print(f"✅ Validation: {len(val_pairs)} samples")

# Save for fine-tuning
print("\n💾 Saving training data...")

# Format for Hugging Face fine-tuning
train_data = []
for pair in train_pairs:
    train_data.append({
        'text': f"User: {pair['prompt']}\nAssistant: {pair['completion']}"
    })

val_data = []
for pair in val_pairs:
    val_data.append({
        'text': f"User: {pair['prompt']}\nAssistant: {pair['completion']}"
    })

# Save as JSON
with open(training_dir / 'train.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, indent=2, ensure_ascii=False)

with open(training_dir / 'validation.json', 'w', encoding='utf-8') as f:
    json.dump(val_data, f, indent=2, ensure_ascii=False)

# Also save as text format (for GPT-style models)
with open(training_dir / 'train.txt', 'w', encoding='utf-8') as f:
    for item in train_data:
        f.write(item['text'] + '\n\n')

with open(training_dir / 'validation.txt', 'w', encoding='utf-8') as f:
    for item in val_data:
        f.write(item['text'] + '\n\n')

print(f"✅ Saved to training/train.json")
print(f"✅ Saved to training/validation.json")
print(f"✅ Saved to training/train.txt")
print(f"✅ Saved to training/validation.txt")

# Statistics
print("\n" + "="*80)
print("📊 TRAINING DATA STATISTICS")
print("="*80)
print(f"Total samples: {len(training_pairs)}")
print(f"Training samples: {len(train_pairs)}")
print(f"Validation samples: {len(val_pairs)}")
print(f"Average text length: {combined_df['text'].str.len().mean():.1f} characters")
print(f"Unique samples: {combined_df['text'].nunique()}")

# Sample preview
print("\n📝 SAMPLE TRAINING EXAMPLES:")
print("="*80)
for i, pair in enumerate(random.sample(train_pairs, min(3, len(train_pairs)))):
    print(f"\nExample {i+1}:")
    print(f"User: {pair['prompt'][:100]}...")
    print(f"NAINA: {pair['completion']}")

print("\n" + "="*80)
print("✅ DATA PREPARATION COMPLETE!")
print("="*80)
print("\n🚀 Ready for model training!")
print("Next: Run training/train_model.py")
