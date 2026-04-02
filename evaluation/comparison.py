from training.inference import generate_response

def compare_models(base_model, lora_model, tokenizer, instruction, input_text):
    """
    Compare the outputs of the base model and the fine-tuned LoRA model.
    """
    print("--- BASE MODEL ---")
    base_response = generate_response(base_model, tokenizer, instruction, input_text)
    print(base_response)
    
    print("\n--- LORA MODEL ---")
    lora_response = generate_response(lora_model, tokenizer, instruction, input_text)
    print(lora_response)
    
    return {
        "base": base_response,
        "lora": lora_response
    }

if __name__ == "__main__":
    print("Comparison module ready.")
