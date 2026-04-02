from trl import DPOConfig, DPOTrainer
from training.model_loader import load_base_model
from training.lora_config import get_lora_config, prepare_peft_model
from data.dpo_loader import get_dpo_dataloader

def run_dpo_training():
    # 1. Load DPO data
    dataset = get_dpo_dataloader("data/dpo_dataset.jsonl")
    
    # 2. Load model & tokenizer
    model, tokenizer = load_base_model()
    
    # 3. Setup LoRA
    lora_config = get_lora_config()
    model = prepare_peft_model(model, lora_config)
    
    # 4. DPO Config
    dpo_args = DPOConfig(
        output_dir="./output/dpo",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        max_prompt_length=128,
        max_length=256,
        learning_rate=5e-7,
        num_train_epochs=1,
        use_cpu=True,
        no_cuda=True,
        report_to="none"
    )
    
    # 5. Trainer
    trainer = DPOTrainer(
        model=model,
        ref_model=None, # TRL will handle it via the adapter internally
        args=dpo_args,
        train_dataset=dataset,
        tokenizer=tokenizer
    )
    
    print("🚀 DPO Trainer initialized on CPU...")
    return trainer

if __name__ == "__main__":
    run_dpo_training()
