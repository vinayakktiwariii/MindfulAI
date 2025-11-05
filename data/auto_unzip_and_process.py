# data/auto_unzip_and_process.py
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# AUTO-unzip and process all Kaggle datasets

import os
import zipfile
import pandas as pd
from pathlib import Path
import concurrent.futures

raw_dir = Path('data/raw')
processed_dir = Path('data/processed')

print("="*80)
print("🚀 AUTO-UNZIP & PROCESS KAGGLE DATASETS")
print("="*80)

# STEP 1: Find and extract all ZIP files
print("\n📦 Step 1: Finding and extracting ZIP files...")
zip_count = 0

for zip_file in raw_dir.glob('*.zip'):
    try:
        extract_path = raw_dir / zip_file.stem
        extract_path.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        print(f"✅ Extracted: {zip_file.name} → {extract_path.name}/")
        zip_count += 1
    except Exception as e:
        print(f"❌ Failed to extract {zip_file.name}: {e}")

print(f"\n✅ Total ZIP files extracted: {zip_count}")

# STEP 2: Process Reddit data
def process_reddit():
    try:
        print("\n📊 Processing: Reddit Mental Health Posts...")
        reddit_path = raw_dir / 'reddit-mental-health'
        
        if reddit_path.exists():
            all_files = list(reddit_path.glob('*.csv'))
            if all_files:
                dfs = [pd.read_csv(f) for f in all_files if f.stat().st_size > 0]
                df = pd.concat(dfs, ignore_index=True)
                
                # Clean
                df['text'] = df.get('title', '') + ' ' + df.get('selftext', '')
                df_clean = df[['text']].dropna()
                df_clean.to_csv(processed_dir / 'reddit_mental_health_clean.csv', index=False)
                print(f"✅ Reddit processed: {len(df_clean)} posts")
                return True
        return False
    except Exception as e:
        print(f"❌ Reddit processing failed: {e}")
        return False

# STEP 3: Process Twitter sentiment
def process_twitter():
    try:
        print("\n📊 Processing: Twitter Sentiment Data...")
        twitter_path = raw_dir / 'twitter-sentiment'
        
        if twitter_path.exists():
            csv_files = list(twitter_path.glob('*.csv'))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                df_clean = df[['text']].dropna() if 'text' in df.columns else df.iloc[:, [0]]
                df_clean.to_csv(processed_dir / 'twitter_sentiment_clean.csv', index=False)
                print(f"✅ Twitter processed: {len(df_clean)} tweets")
                return True
        return False
    except Exception as e:
        print(f"❌ Twitter processing failed: {e}")
        return False

# STEP 4: Process Student Mental Health
def process_student():
    try:
        print("\n📊 Processing: Student Mental Health...")
        student_path = raw_dir / 'student-mental-health'
        
        if student_path.exists():
            csv_files = list(student_path.glob('*.csv'))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                df_clean = df.dropna()
                df_clean.to_csv(processed_dir / 'student_mental_health_clean.csv', index=False)
                print(f"✅ Student data processed: {len(df_clean)} records")
                return True
        return False
    except Exception as e:
        print(f"❌ Student processing failed: {e}")
        return False

# STEP 5: Process DASS-21
def process_dass21():
    try:
        print("\n📊 Processing: DASS-21 Scales...")
        dass_path = raw_dir / 'dass21'
        
        if dass_path.exists():
            csv_files = list(dass_path.glob('*.csv'))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                df_clean = df.dropna()
                df_clean.to_csv(processed_dir / 'dass21_clean.csv', index=False)
                print(f"✅ DASS-21 processed: {len(df_clean)} records")
                return True
        return False
    except Exception as e:
        print(f"❌ DASS-21 processing failed: {e}")
        return False

# STEP 6: Run all in parallel
print("\n" + "="*80)
print("⚡ Processing all datasets in parallel...")
print("="*80)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(process_reddit),
        executor.submit(process_twitter),
        executor.submit(process_student),
        executor.submit(process_dass21),
    ]
    
    for future in concurrent.futures.as_completed(futures):
        future.result()

# STEP 7: Create final master dataset
print("\n📊 Creating MEGA Master Dataset from ALL sources...")
try:
    all_texts = []
    
    for csv_file in processed_dir.glob('*_clean.csv'):
        try:
            df = pd.read_csv(csv_file)
            for col in df.columns:
                all_texts.extend(df[col].dropna().astype(str).tolist())
        except:
            pass
    
    master_df = pd.DataFrame({'text': all_texts})
    master_df['text'] = master_df['text'].str.strip()
    master_df.drop_duplicates(inplace=True)
    master_df = master_df[master_df['text'].str.len() > 5]  # Remove short text
    
    master_df.to_csv(processed_dir / 'MEGA_MASTER_DATASET.csv', index=False)
    print(f"✅ MEGA Master Dataset created: {len(master_df)} unique samples")
    
except Exception as e:
    print(f"❌ Master dataset creation failed: {e}")

# STEP 8: Summary
print("\n" + "="*80)
print("✅ AUTO-UNZIP & PROCESS COMPLETE!")
print("="*80)

processed_files = list(processed_dir.glob('*.csv'))
print(f"\n📁 Total processed files: {len(processed_files)}")
print("\nProcessed datasets:")
for f in sorted(processed_files):
    size_mb = f.stat().st_size / (1024*1024)
    print(f"  ✅ {f.name} ({size_mb:.2f} MB)")

print("\n" + "="*80)
print("🎯 ALL DATASETS READY FOR TRAINING!")
print("="*80)
