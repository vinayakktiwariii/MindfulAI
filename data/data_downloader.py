# data/data_downloader.py
"""
MindfulAI Data Acquisition Script
Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
Mission: BUILD HAPPY SMILES
"""

import os
import pandas as pd
import requests
from pathlib import Path

class MindfulAIDataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
    def download_kaggle_datasets(self):
        """Download primary datasets from Kaggle"""
        print("🔄 Downloading Kaggle datasets...")
        
        # Note: Users will need to set up Kaggle API credentials
        kaggle_datasets = [
            "nguyenletruongthien/mental-health",
            "suchintikasarkar/sentiment-analysis-for-mental-health",
            "praveengovi/emotions-dataset-for-nlp",
            "ritresearch/happydb"
        ]
        
        for dataset in kaggle_datasets:
            try:
                os.system(f"kaggle datasets download -d {dataset} -p {self.raw_dir}")
                print(f"✅ Downloaded: {dataset}")
            except Exception as e:
                print(f"❌ Failed to download {dataset}: {str(e)}")
    
    def download_huggingface_datasets(self):
        """Download datasets from Hugging Face"""
        print("🔄 Downloading Hugging Face datasets...")
        
        from datasets import load_dataset
        
        hf_datasets = [
            "heliosbrahma/mental_health_chatbot_dataset",
            "Amod/mental_health_counseling_conversations",
            "ShenLab/MentalChat16K"
        ]
        
        for dataset_name in hf_datasets:
            try:
                dataset = load_dataset(dataset_name)
                # Save as CSV for easy processing
                safe_name = dataset_name.replace("/", "_")
                dataset.save_to_disk(f"{self.raw_dir}/{safe_name}")
                print(f"✅ Downloaded: {dataset_name}")
            except Exception as e:
                print(f"❌ Failed to download {dataset_name}: {str(e)}")
    
    def create_initial_analysis(self):
        """Create initial data analysis notebook"""
        analysis_code = '''
# MindfulAI Data Analysis
# Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY
# Mission: BUILD HAPPY SMILES

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up analysis environment
data_dir = Path("data/raw")
results = {}

print("🧠 MindfulAI Data Analysis Report")
print("=" * 50)

# Analyze each dataset
for file_path in data_dir.glob("*.csv"):
    try:
        df = pd.read_csv(file_path)
        results[file_path.name] = {
            "shape": df.shape,
            "columns": list(df.columns),
            "sample": df.head(3).to_dict()
        }
        print(f"✅ {file_path.name}: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Error analyzing {file_path.name}: {str(e)}")

print("\\n🎯 Next Steps:")
print("1. Review dataset structures")
print("2. Identify conversation patterns") 
print("3. Design preprocessing pipeline")
print("4. Create training/validation splits")
'''
        
        with open(self.data_dir / "initial_analysis.py", "w") as f:
            f.write(analysis_code)
        
        print("📊 Created initial_analysis.py")

if __name__ == "__main__":
    print("🚀 MindfulAI Data Acquisition")
    print("Author: VINAYAK TIWARI | ARQONX-AI TECHNOLOGY")
    print("Mission: BUILD HAPPY SMILES")
    print("=" * 50)
    
    manager = MindfulAIDataManager()
    
    # Note: Users need to install and configure kaggle API
    print("📝 Please ensure you have:")
    print("1. Kaggle API configured (kaggle.json in ~/.kaggle/)")
    print("2. Hugging Face datasets library installed")
    print("3. Internet connection")
    
    choice = input("\\nProceed with data download? (y/n): ")
    if choice.lower() == 'y':
        manager.download_kaggle_datasets()
        manager.download_huggingface_datasets()
        manager.create_initial_analysis()
        print("\\n✅ Data acquisition complete!")
        print("🎯 Next: Run 'python data/initial_analysis.py' to explore the data")
    else:
        print("⏸️  Data download skipped. Run this script again when ready.")
