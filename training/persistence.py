import os
from peft import PeftModel

def save_lora_model(model, output_dir="models/lora_adapter"):
    """
    Saves only the LoRA adapter weights.
    """
    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    print(f"✅ LoRA adapter saved to {output_dir}")

def load_lora_adapter(base_model, adapter_path=os.path.join("models", "lora_adapter").replace(os.path.sep, '/')):
    """
    Loads saved LoRA adapter into a base model.
    """
    if not os.path.exists(adapter_path):
        raise FileNotFoundError(f"Missing adapter at {adapter_path}")
    
    # PEFT paths on Windows must use forward slashes for some internal checks
    normalized_path = adapter_path.replace(os.sep, '/')
    merged_model = PeftModel.from_pretrained(base_model, normalized_path)
    print(f"✅ LoRA adapter loaded from {normalized_path}")
    return merged_model

if __name__ == "__main__":
    # Test path logic
    print("Persistence module ready.")
