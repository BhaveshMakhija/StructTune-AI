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

def compare_all_models(base_model, sft_model, dpo_model, tokenizer, instruction, input_text):
    """
    Compare the outputs of the base model, SFT model, and DPO-tuned model.
    """
    print("--- BASE MODEL ---")
    base_res = generate_response(base_model, tokenizer, instruction, input_text)
    print(base_res)
    
    print("\n--- SFT (LoRA) MODEL ---")
    sft_res = generate_response(sft_model, tokenizer, instruction, input_text)
    print(sft_res)
    
    print("\n--- DPO MODEL ---")
    dpo_res = generate_response(dpo_model, tokenizer, instruction, input_text)
    print(dpo_res)
    
    return {
        "base": base_res,
        "sft": sft_res,
        "dpo": dpo_res
    }

if __name__ == "__main__":
    print("Comparison module ready.")
