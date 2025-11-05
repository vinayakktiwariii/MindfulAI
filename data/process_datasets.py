# data/process_datasets.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Processes & cleans all downloaded datasets in parallel

import os
import pandas as pd
import json
from pathlib import Path
import concurrent.futures

raw_dir = Path('data/raw')
processed_dir = Path('data/processed')
processed_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("🔄 DATA PROCESSING & CLEANING PIPELINE")
print("="*70)

def process_emotion_dataset():
    """Process emotion dataset"""
    try:
        print("\n📊 Processing: Emotion Dataset...")
        emotion_files = list(raw_dir.glob('emotion-dataset/*.csv'))
        
        all_data = []
        for file in emotion_files:
            df = pd.read_csv(file)
            all_data.append(df)
        
        combined = pd.concat(all_data, ignore_index=True)
        combined.to_csv(processed_dir / 'emotion_dataset_clean.csv', index=False)
        print(f"✅ Emotion dataset cleaned: {len(combined)} rows")
        return True
    except Exception as e:
        print(f"❌ Emotion processing failed: {e}")
        return False

def process_mental_health_survey():
    """Process mental health survey"""
    try:
        print("\n📊 Processing: Mental Health Survey...")
        survey_files = list(raw_dir.glob('mental-health-survey/*.csv'))
        
        if survey_files:
            df = pd.read_csv(survey_files[0])
            # Clean and standardize
            df.dropna(subset=['state', 'treatment'], how='all', inplace=True)
            df.to_csv(processed_dir / 'mental_health_survey_clean.csv', index=False)
            print(f"✅ Mental health survey cleaned: {len(df)} rows")
            return True
        else:
            print("⚠️  No survey files found")
            return False
    except Exception as e:
        print(f"❌ Survey processing failed: {e}")
        return False

def process_reddit_data():
    """Process Reddit mental health posts"""
    try:
        print("\n📊 Processing: Reddit Mental Health Posts...")
        reddit_files = list(raw_dir.glob('reddit-mental-health/*.csv'))
        
        if reddit_files:
            df = pd.read_csv(reddit_files[0])
            # Keep only text and labels
            if 'title' in df.columns and 'selftext' in df.columns:
                df['full_text'] = df['title'] + ' ' + df['selftext']
                df_clean = df[['full_text']].dropna()
                df_clean.to_csv(processed_dir / 'reddit_mental_health_clean.csv', index=False)
                print(f"✅ Reddit posts cleaned: {len(df_clean)} posts")
                return True
        print("⚠️  Reddit data not yet available")
        return False
    except Exception as e:
        print(f"❌ Reddit processing failed: {e}")
        return False

def process_twitter_sentiment():
    """Process Twitter sentiment data"""
    try:
        print("\n📊 Processing: Twitter Sentiment Data...")
        twitter_files = list(raw_dir.glob('twitter-sentiment/*.csv'))
        
        if twitter_files:
            df = pd.read_csv(twitter_files[0])
            # Keep only text and sentiment
            if 'text' in df.columns:
                df_clean = df[['text']].dropna()
                df_clean.to_csv(processed_dir / 'twitter_sentiment_clean.csv', index=False)
                print(f"✅ Twitter data cleaned: {len(df_clean)} tweets")
                return True
        print("⚠️  Twitter data not yet available")
        return False
    except Exception as e:
        print(f"❌ Twitter processing failed: {e}")
        return False

def create_combined_dataset():
    """Combine all cleaned datasets into one master file"""
    try:
        print("\n📊 Creating Master Combined Dataset...")
        all_texts = []
        
        # Load all available cleaned files
        for csv_file in processed_dir.glob('*_clean.csv'):
            try:
                df = pd.read_csv(csv_file)
                if 'full_text' in df.columns:
                    all_texts.extend(df['full_text'].tolist())
                elif 'text' in df.columns:
                    all_texts.extend(df['text'].tolist())
                elif 'selftext' in df.columns:
                    all_texts.extend(df['selftext'].tolist())
            except:
                pass
        
        master_df = pd.DataFrame({'text': all_texts})
        master_df.drop_duplicates(inplace=True)
        master_df.to_csv(processed_dir / 'MASTER_DATASET.csv', index=False)
        print(f"✅ Master dataset created: {len(master_df)} unique samples")
        return True
    except Exception as e:
        print(f"❌ Master dataset creation failed: {e}")
        return False

# Run all processing in parallel
print("\n⚡ Running all processors in parallel...")
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = {
        executor.submit(process_emotion_dataset): 'Emotion',
        executor.submit(process_mental_health_survey): 'Survey',
        executor.submit(process_reddit_data): 'Reddit',
        executor.submit(process_twitter_sentiment): 'Twitter',
    }
    
    for future in concurrent.futures.as_completed(futures):
        result = future.result()

# Create combined master dataset
create_combined_dataset()

print("\n" + "="*70)
print("✅ DATA PROCESSING COMPLETE!")
print("="*70)
print("\n📁 Processed files saved to: data/processed/")
print("\nReady for training:")
print("  - emotion_dataset_clean.csv")
print("  - mental_health_survey_clean.csv")
print("  - reddit_mental_health_clean.csv")
print("  - twitter_sentiment_clean.csv")
print("  - MASTER_DATASET.csv (Combined)")
print("="*70)
