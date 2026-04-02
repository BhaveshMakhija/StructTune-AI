from peft import LoraConfig, get_peft_model, TaskType

def get_lora_config():
    """
    Standard LoRA configuration for causal language modeling.
    """
    config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    return config

def prepare_peft_model(model, config):
    """
    Wraps the base model with the LoRA adapter.
    """
    return get_peft_model(model, config)

if __name__ == "__main__":
    # Test config setup
    config = get_lora_config()
    print(f"✅ LoRA Config: r={config.r}, alpha={config.lora_alpha}")
    print(f"✅ Target Modules: {config.target_modules}")
