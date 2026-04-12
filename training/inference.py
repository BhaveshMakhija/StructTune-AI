import torch

# Optimize for CPU speed
torch.set_num_threads(4)
torch.set_num_interop_threads(4)

def generate_response(model, tokenizer, instruction, input_text, max_new_tokens=80, temperature=0.1, do_sample=False):
    """
    Inference pipeline for JSON extraction. Optimized for CPU.
    """
    # 1. Format prompt - If input_text is empty, we assume instruction is the FULL RAW prompt
    if not input_text:
        prompt = instruction
    else:
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
            temperature=temperature if do_sample else None,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=do_sample
        )
    
    # 4. Decode
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 5. Extract response part (handle raw vs templated)
    if "### Response:\n" in full_text:
        response = full_text.split("### Response:\n")[-1].strip()
    else:
        # If raw, we need to strip the input prompt
        response = full_text[len(prompt):].strip()
        # Fallback in case decoding messed with lengths
        if not response and "OUTPUT:\n" in full_text:
            response = full_text.split("OUTPUT:\n")[-1].strip()

    return response

if __name__ == "__main__":
    print("Inference module ready.")
    # test dummy prompt
    # test loop...
