# data/process_remaining_folders.py
# Process ALL remaining folders regardless of name

import pandas as pd
from pathlib import Path
import os

raw_dir = Path('data/raw')
processed_dir = Path('data/processed')
processed_dir.mkdir(parents=True, exist_ok=True)

print("="*80)
print("🔄 PROCESSING ALL REMAINING FOLDERS")
print("="*80)

# Get all directories in raw/
all_dirs = [d for d in raw_dir.iterdir() if d.is_dir()]
print(f"\nFound {len(all_dirs)} folders to process:")
for d in all_dirs:
    print(f"  📁 {d.name}")

processed_count = 0

# Process each folder
for folder in all_dirs:
    folder_name = folder.name
    print(f"\n📊 Processing: {folder_name}...")
    
    try:
        # Find all CSV files in this folder
        csv_files = list(folder.glob('*.csv'))
        
        if not csv_files:
            print(f"   ⚠️  No CSV files found")
            continue
        
        # Load all CSVs from this folder
        dfs = []
        for csv_file in csv_files:
            try:
                # Try different encodings
                try:
                    df = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip', nrows=10000)
                except:
                    df = pd.read_csv(csv_file, encoding='latin-1', on_bad_lines='skip', nrows=10000)
                
                dfs.append(df)
            except Exception as e:
                print(f"      ⚠️  Could not read {csv_file.name}: {e}")
                continue
        
        if not dfs:
            print(f"   ⚠️  No valid CSV data found")
            continue
        
        # Combine all CSVs from this folder
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"   ✅ Loaded {len(combined_df)} rows")
        
        # Extract text columns
        text_columns = []
        for col in combined_df.columns:
            if combined_df[col].dtype == 'object':  # String columns
                text_columns.append(col)
        
        if text_columns:
            # Combine all text columns
            all_text = []
            for col in text_columns:
                texts = combined_df[col].astype(str).str.strip()
                all_text.extend(texts.tolist())
            
            # Clean and deduplicate
            text_df = pd.DataFrame({'text': all_text})
            text_df['text'] = text_df['text'].str.strip()
            text_df = text_df[text_df['text'].str.len() > 5]  # Remove short
            text_df.drop_duplicates(inplace=True)
            text_df.dropna(inplace=True)
            
            # Save
            safe_folder_name = folder_name.replace('-', '_').replace(' ', '_').lower()
            output_file = processed_dir / f'{safe_folder_name}_clean.csv'
            text_df.to_csv(output_file, index=False)
            
            print(f"   ✅ Saved: {output_file.name} ({len(text_df)} rows)")
            processed_count += 1
        else:
            print(f"   ⚠️  No text columns found")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "="*80)
print(f"✅ PROCESSING COMPLETE - {processed_count} folders processed")
print("="*80)

# Create final MEGA MASTER
print("\n📊 Creating final MEGA MASTER DATASET...")
try:
    all_texts = []
    
    for csv_file in processed_dir.glob('*_clean.csv'):
        df = pd.read_csv(csv_file)
        all_texts.extend(df.iloc[:, 0].astype(str).tolist())
    
    mega_df = pd.DataFrame({'text': all_texts})
    mega_df.drop_duplicates(inplace=True)
    mega_df = mega_df[mega_df['text'].str.len() > 5]
    
    mega_file = processed_dir / 'FINAL_MEGA_MASTER_DATASET.csv'
    mega_df.to_csv(mega_file, index=False)
    
    print(f"✅ FINAL_MEGA_MASTER_DATASET.csv created: {len(mega_df)} rows")
except Exception as e:
    print(f"❌ Error: {e}")

# List all processed files
print("\n" + "="*80)
print("📁 ALL PROCESSED FILES:")
print("="*80)

processed_files = sorted(processed_dir.glob('*.csv'))
total_rows = 0
for f in processed_files:
    df = pd.read_csv(f)
    rows = len(df)
    size_mb = f.stat().st_size / (1024*1024)
    total_rows += rows
    print(f"✅ {f.name:<50} {rows:>8,} rows ({size_mb:>6.2f} MB)")

print(f"\n📊 TOTAL: {len(processed_files)} files, {total_rows:,} total rows")
print("="*80)
