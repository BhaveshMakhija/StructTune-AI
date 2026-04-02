import json
import os
from datetime import datetime

def save_metrics(metrics, base_dir="evaluation/results"):
    """
    Save evaluation metrics to a JSON file.
    """
    os.makedirs(base_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"metrics_{timestamp}.json"
    filepath = os.path.join(base_dir, filename)
    
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"✅ Metrics stored at {filepath}")
    return filepath

if __name__ == "__main__":
    test_metrics = {"valid_json": 1.0, "exact_match": 0.5}
    save_metrics(test_metrics)
