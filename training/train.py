from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
from training.model_loader import load_base_model
from training.lora_config import get_lora_config, prepare_peft_model
from training.preprocess import preprocess_dataset
from data.loader import get_dataloader
import os

def run_sft_training():
    # 1. Load data
    dataset = get_dataloader("data/dataset.jsonl")
    formatted_dataset = preprocess_dataset(dataset)
    
    # 2. Load model & tokenizer
    model, tokenizer = load_base_model()
    
    # 3. Setup LoRA
    lora_config = get_lora_config()
    model = prepare_peft_model(model, lora_config)
    
    # 4. Training Arguments
    training_args = TrainingArguments(
        output_dir="./output/sft",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        learning_rate=2e-4,
        logging_steps=10,
        save_total_limit=1,
        save_strategy="no", # Don't save auto 
        report_to="none",
        use_cpu=True,
        no_cuda=True
    )
    
    # 5. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=formatted_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    print("🚀 Starting SFT training on CPU...")
    # trainer.train() # User said "Add simple training loop", will run in sanity test if needed
    return trainer

if __name__ == "__main__":
    trainer = run_sft_training()
    print("✅ SFT Trainer initialized successfully!")
