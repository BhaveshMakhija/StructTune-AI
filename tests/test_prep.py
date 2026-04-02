from data.loader import get_dataloader
from training.preprocess import preprocess_dataset
import os

def test_preprocess():
    ds = get_dataloader("data/dataset.jsonl")
    preprocessed_ds = preprocess_dataset(ds)
    
    assert "text" in preprocessed_ds[0]
    assert "### Instruction" in preprocessed_ds[0]["text"]
    assert "### Response" in preprocessed_ds[0]["text"]
    
    print(f"✅ Preprocessing Sanity Check: SUCCESS")
    print(f"✅ Formatted Sample Example:\n{preprocessed_ds[0]['text']}")

if __name__ == "__main__":
    test_preprocess()
