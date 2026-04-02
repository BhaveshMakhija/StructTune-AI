import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_base_model(model_id="TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"):
    """
    Load model and tokenizer for CPU.
    """
    print(f"Loading model: {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model on CPU
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32, # CPU standard
        device_map="cpu"
    )
    
    return model, tokenizer

if __name__ == "__main__":
    # Test loading
    model, tokenizer = load_base_model()
    print("✅ Model & Tokenizer loaded successfully!")
    print(f"✅ Vocab size: {len(tokenizer)}")
