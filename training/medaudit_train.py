import json
import torch
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
from training.model_loader import load_base_model
from training.lora_config import get_lora_config, prepare_peft_model
import os

def formatting_func(example):
    """
    Format the sample for MedAudit clinical extraction.
    """
    input_text = example.get("input", "")
    output = example.get("output", {})
    
    # Prompting for structured extraction
    text = (
        f"### Instruction:\nExtract medical information (patient_name, age, diagnosis, medications, symptoms) from the following text into JSON format.\n\n"
        f"### Input:\n{input_text}\n\n"
        f"### Response:\n{json.dumps(output)}"
    )
    return {"text": text}

def train_medaudit():
    # 1. Load the structured dataset
    dataset_path = "data/processed/train.json"
    if not os.path.exists(dataset_path):
        print(f"❌ Error: {dataset_path} not found. Run generate.py first.")
        return
    
    dataset = load_dataset("json", data_files=dataset_path, split="train")
    formatted_dataset = dataset.map(formatting_func, remove_columns=dataset.column_names)
    
    # 2. Load model (TinyLlama)
    model, tokenizer = load_base_model()
    
    # 3. Apply LoRA
    lora_config = get_lora_config()
    model = prepare_peft_model(model, lora_config)
    
    # 4. CPU-friendly Training Arguments
    training_args = TrainingArguments(
        output_dir="./models/medaudit-lora",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        warmup_steps=5,
        learning_rate=2e-4,
        logging_steps=10,
        save_strategy="no",
        no_cuda=True,  # Force CPU
        report_to="none"
    )
    
    # 5. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=formatted_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    print("🚀 Starting MedAudit Fine-tuning (CPU)...")
    # For the purpose of this task (Step 4 commit), we provide the pipeline.
    # We will run a few steps to ensure it works.
    trainer.train()
    
    # Save the adapter
    model.save_pretrained("./models/medaudit-adapter")
    print("✅ Training complete. Adapter saved to ./models/medaudit-adapter")

if __name__ == "__main__":
    train_medaudit()
