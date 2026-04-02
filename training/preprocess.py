def formatting_func(example):
    """
    Format the sample for instruction fine-tuning.
    """
    instruction = example.get("instruction", "")
    input_text = example.get("input", "")
    output = example.get("output", "")
    
    text = (
        f"### Instruction:\n{instruction}\n\n"
        f"### Input:\n{input_text}\n\n"
        f"### Response:\n{output}"
    )
    return {"text": text}

def preprocess_dataset(dataset):
    """
    Map the formatting function over the dataset.
    """
    return dataset.map(formatting_func, remove_columns=dataset.column_names)

if __name__ == "__main__":
    # Test with dummy data
    sample = {"instruction": "Extract name", "input": "John is here", "output": '{"name": "John"}'}
    formatted = formatting_func(sample)
    print(f"✅ Formatted Sample:\n{formatted['text']}")
