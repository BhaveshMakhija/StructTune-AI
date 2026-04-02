from datasets import load_dataset
import os
import json

def generate_dummy_dpo_data(file_path="data/dpo_dataset.jsonl"):
    """
    Generate a tiny synthetic DPO dataset for testing.
    """
    samples = [
        {
            "prompt": "Extract name: Alice is here.",
            "chosen": "{\"name\": \"Alice\"}",
            "rejected": "Alice is here."
        },
        {
            "prompt": "Extract city: Bob lives in London.",
            "chosen": "{\"city\": \"London\"}",
            "rejected": "{\"name\": \"Bob\"}"
        }
    ]
    os.makedirs("data", exist_ok=True)
    with open(file_path, "w") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")

def get_dpo_dataloader(file_path="data/dpo_dataset.jsonl"):
    """
    Load a DPO dataset from a local JSONL file.
    """
    if not os.path.exists(file_path):
        generate_dummy_dpo_data(file_path)
        
    dataset = load_dataset("json", data_files=file_path, split="train")
    return dataset

if __name__ == "__main__":
    ds = get_dpo_dataloader()
    print(f"✅ Loaded {len(ds)} DPO samples")
    print(f"✅ DPO Sample: {ds[0]}")
