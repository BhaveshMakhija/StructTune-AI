import os
from data.loader import get_dataloader

def test_loader():
    dataset = get_dataloader("data/dataset.jsonl")
    assert len(dataset) > 0, "Dataset should not be empty"
    print(f"✅ Loader Sanity Check: SUCCESS")
    print(f"✅ Samples Loaded: {len(dataset)}")

if __name__ == "__main__":
    test_loader()
