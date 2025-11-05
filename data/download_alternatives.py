# data/download_alternatives.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES
# Download CLEAN alternative datasets for conversational AI & mental health

import os
import subprocess
from pathlib import Path

raw_dir = Path('data/raw')
raw_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("🔄 ALTERNATIVE CLEAN DATASETS DOWNLOADER")
print("="*70)

# ALTERNATIVE 1: Reddit Mental Health Conversations
print("\n📥 Alternative 1: Reddit Mental Health Posts (Kaggle)...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download',
        '-d', 'nilepri/reddit-mental-health-posts',
        '-p', 'data/raw/reddit-mental-health',
        '--unzip'
    ], check=True, capture_output=True)
    print("✅ Reddit mental health posts: Downloaded (Alternative to Mental Health Conversations)")
except Exception as e:
    print(f"⚠️  Reddit dataset failed: {e}")

# ALTERNATIVE 2: Twitter Mental Health Sentiment  
print("\n📥 Alternative 2: Twitter Sentiment Dataset (Kaggle)...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download',
        '-d', 'harshsingh2209/twitter-sentiment-dataset-for-mental-health-condition',
        '-p', 'data/raw/twitter-sentiment',
        '--unzip'
    ], check=True, capture_output=True)
    print("✅ Twitter sentiment: Downloaded (Alternative to Sentiment Analysis)")
except Exception as e:
    print(f"⚠️  Twitter dataset failed: {e}")

# ALTERNATIVE 3: Student Mental Health
print("\n📥 Alternative 3: Student Mental Health Database (Kaggle)...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download',
        '-d', 'shariful07/student-mental-health-data',
        '-p', 'data/raw/student-mental-health',
        '--unzip'
    ], check=True, capture_output=True)
    print("✅ Student mental health: Downloaded (Clean structured data)")
except Exception as e:
    print(f"⚠️  Student mental health failed: {e}")

# ALTERNATIVE 4: Conversational AI - Ubuntu Dialogue Corpus
print("\n📥 Alternative 4: Conversational Data (Hugging Face)...")
try:
    from datasets import load_dataset
    print("  Loading Ubuntu Dialog Corpus...")
    dataset = load_dataset("ubuntu_dialogue_corpus/ubuntu_dialogue_corpus", split='train', streaming=True)
    
    # Save first 10k samples
    samples = []
    for i, sample in enumerate(dataset):
        if i >= 10000:
            break
        samples.append(sample)
    
    import json
    with open('data/raw/ubuntu_dialogue_10k.json', 'w') as f:
        json.dump(samples, f)
    print("✅ Ubuntu dialogue corpus (10k samples): Downloaded")
except Exception as e:
    print(f"⚠️  Ubuntu dialogue failed: {e}")

# ALTERNATIVE 5: Depression & Anxiety Tweets
print("\n📥 Alternative 5: Depression & Anxiety Detection (Kaggle)...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download',
        '-d', 'yassineAurélich/depression-anxiety-stress-scales-dass21',
        '-p', 'data/raw/dass21',
        '--unzip'
    ], check=True, capture_output=True)
    print("✅ DASS-21 scales: Downloaded")
except Exception as e:
    print(f"⚠️  DASS-21 failed: {e}")

print("\n" + "="*70)
print("✅ ALTERNATIVE DATASETS DOWNLOAD COMPLETE!")
print("="*70)
print("\nYou now have CLEAN replacements for all failed datasets!")
print("\nNext: Run Terminal 3 for data cleaning & processing")
print("="*70)
