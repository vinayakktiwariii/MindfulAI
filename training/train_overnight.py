# training/train_overnight.py - FINAL WORKING VERSION
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from pathlib import Path
import datetime

print("="*80)
print("🧠 NAINA OVERNIGHT TRAINING - WEEK 3")
print("Built by ArqonX AI Technologies | Founder: Vinayak Tiwari")
print("="*80)
print(f"⏰ Start Time: {datetime.datetime.now().strftime('%I:%M %p')}")
print("="*80 + "\n")

# Load data
training_dir = Path('training')

try:
    with open(training_dir / 'augmented_train.json', 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    with open(training_dir / 'augmented_validation.json', 'r', encoding='utf-8') as f:
        val_data = json.load(f)
    
    print(f"✅ Loaded {len(train_data)} training samples")
    print(f"✅ Loaded {len(val_data)} validation samples\n")
except FileNotFoundError:
    print("❌ Training data not found!")
    print("Run: python training/augment_training_data.py first")
    exit(1)

# Model setup
model_name = "distilgpt2"
print(f"📥 Loading model: {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)
print("✅ Model loaded\n")

# Tokenize
print("🔄 Tokenizing datasets...")

def tokenize_texts(texts):
    return tokenizer(
        [item['text'] for item in texts],
        truncation=True,
        max_length=256,
        padding='max_length',
        return_tensors='pt'
    )

train_encodings = tokenize_texts(train_data)
val_encodings = tokenize_texts(val_data)

print("✅ Tokenization complete\n")

# Simple PyTorch dataset
class SimpleDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings
    
    def __len__(self):
        return self.encodings['input_ids'].shape[0]
    
    def __getitem__(self, idx):
        return {
            'input_ids': self.encodings['input_ids'][idx],
            'attention_mask': self.encodings['attention_mask'][idx],
            'labels': self.encodings['input_ids'][idx]
        }

train_dataset = SimpleDataset(train_encodings)
val_dataset = SimpleDataset(val_encodings)

# Training config - FIXED parameter names
output_dir = training_dir / 'naina_model'
output_dir.mkdir(exist_ok=True)

training_args = TrainingArguments(
    output_dir=str(output_dir),
    num_train_epochs=5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    warmup_steps=10,
    weight_decay=0.01,
    logging_dir=str(training_dir / 'logs'),
    logging_steps=5,
    save_steps=20,
    eval_strategy="steps",  # FIXED: was evaluation_strategy
    eval_steps=20,
    save_total_limit=2,
    load_best_model_at_end=True,
    report_to="none",
)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator,
)

print("="*80)
print("🚀 STARTING TRAINING...")
print("="*80)
print("⏰ Estimated time: 2-3 hours")
print("💤 Sleep - it runs automatically!")
print("="*80 + "\n")

# Train
try:
    trainer.train()
    
    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE!")
    print("="*80)
    
    # Save
    final_model_dir = training_dir / 'naina_final_model'
    final_model_dir.mkdir(exist_ok=True)
    
    model.save_pretrained(final_model_dir)
    tokenizer.save_pretrained(final_model_dir)
    
    print(f"💾 Model saved: {final_model_dir}")
    print(f"⏰ End: {datetime.datetime.now().strftime('%I:%M %p')}")
    print("\n🎉 NAINA ready for deployment!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
