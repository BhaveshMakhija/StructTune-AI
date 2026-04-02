import torch

def generate_response(model, tokenizer, instruction, input_text, max_new_tokens=128):
    """
    Inference pipeline for JSON extraction.
    """
    # 1. Format prompt
    prompt = (
        f"### Instruction:\n{instruction}\n\n"
        f"### Input:\n{input_text}\n\n"
        f"### Response:\n"
    )
    
    # 2. Tokenize
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to("cpu") for k, v in inputs.items()}
    
    # 3. Generate
    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False # Determinsitc for JSON extraction
        )
    
    # 4. Decode
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 5. Extract only the response part
    response = full_text.split("### Response:\n")[-1].strip()
    return response

if __name__ == "__main__":
    print("Inference module ready.")
    # test dummy prompt
    # test loop...
