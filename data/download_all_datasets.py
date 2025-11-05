# data/download_all_datasets.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES
# Downloads all necessary datasets for training future models

import os
import subprocess
import json
from pathlib import Path

# Create data directories
raw_dir = Path('data/raw')
raw_dir.mkdir(parents=True, exist_ok=True)

print("="*60)
print("🔄 MindfulAI Dataset Downloader")
print("="*60)

# Dataset 1: Mental Health Conversations
print("\n📥 Downloading: Mental Health Conversational Dataset...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download', 
        '-d', 'reihaneh7/mental-health-conversations', 
        '-p', 'data/raw/mental-health-conversations',
        '--unzip'
    ], check=True)
    print("✅ Mental health conversations: Downloaded")
except Exception as e:
    print(f"⚠️  Could not download mental health conversations: {e}")

# Dataset 2: Emotion Dataset
print("\n📥 Downloading: Emotion Detection Dataset...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download',
        '-d', 'parulpandey/emotion-dataset',
        '-p', 'data/raw/emotion-dataset',
        '--unzip'
    ], check=True)
    print("✅ Emotion dataset: Downloaded")
except Exception as e:
    print(f"⚠️  Could not download emotion dataset: {e}")

# Dataset 3: Mental Health Dataset
print("\n📥 Downloading: Mental Health Survey Dataset...")
try:
    subprocess.run([
        'kaggle', 'datasets', 'download',
        '-d', 'osmi/mental-health-in-tech-survey',
        '-p', 'data/raw/mental-health-survey',
        '--unzip'
    ], check=True)
    print("✅ Mental health survey: Downloaded")
except Exception as e:
    print(f"⚠️  Could not download mental health survey: {e}")

# Dataset 4: Sentiment Analysis
print("\n📥 Downloading: Sentiment Analysis Dataset...")
try:
    from datasets import load_dataset
    dataset = load_dataset('emotion', split='train')
    dataset.to_csv('data/raw/emotion_train.csv', index=False)
    dataset = load_dataset('emotion', split='validation')
    dataset.to_csv('data/raw/emotion_validation.csv', index=False)
    print("✅ Sentiment analysis: Downloaded")
except Exception as e:
    print(f"⚠️  Could not download sentiment analysis: {e}")

# Dataset 5: Conversational AI Dataset
print("\n📥 Downloading: Conversational AI Dataset (Hugging Face)...")
try:
    from datasets import load_dataset
    dataset = load_dataset('daily_dialog', split='train')
    dataset.save_to_disk('data/raw/daily_dialog_train')
    dataset = load_dataset('daily_dialog', split='validation')
    dataset.save_to_disk('data/raw/daily_dialog_validation')
    print("✅ Conversational AI: Downloaded")
except Exception as e:
    print(f"⚠️  Could not download conversational AI: {e}")

print("\n" + "="*60)
print("✅ Dataset Download Complete!")
print("="*60)
print("\nDatasets saved to: data/raw/")
print("\nYou can now:")
print("1. Use these datasets for training future models")
print("2. Analyze emotion patterns")
print("3. Build conversational training pipelines")
print("\n" + "="*60)
