from datasets import load_dataset
import os

def get_dataloader(file_path="data/dataset.jsonl"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing dataset at {file_path}")
    
    # Load dataset from data file
    dataset = load_dataset("json", data_files=file_path, split="train")
    return dataset

if __name__ == "__main__":
    ds = get_dataloader()
    print(f"✅ Loaded {len(ds)} samples")
    print(f"✅ Sample 1: {ds[0]}")
