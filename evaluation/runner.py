from training.inference import generate_response
from evaluation.metrics import is_valid_json, exact_match, field_accuracy
import pandas as pd

def run_evaluation(model, tokenizer, dataset, num_samples=10):
    """
    Run metrics on a small subset of the dataset.
    """
    results = []
    
    # 1. Take subset
    # dataset is a HuggingFace dataset
    subset = dataset.select(range(min(num_samples, len(dataset))))
    
    print(f"📊 Running evaluation on {len(subset)} samples...")
    
    for i, example in enumerate(subset):
        instruction = example.get("instruction", "")
        input_text = example.get("input", "")
        target = example.get("output", "")
        
        # Inference
        prediction = generate_response(model, tokenizer, instruction, input_text)
        
        # Metrics
        valid = is_valid_json(prediction)
        em = exact_match(prediction, target)
        fa = field_accuracy(prediction, target)
        
        results.append({
            "id": i,
            "valid_json": valid,
            "exact_match": em,
            "field_accuracy": fa
        })
        
    # 2. Aggregate
    df = pd.DataFrame(results)
    summary = {
        "avg_valid_json": df["valid_json"].mean(),
        "avg_exact_match": df["exact_match"].mean(),
        "avg_field_accuracy": df["field_accuracy"].mean()
    }
    
    print("--- EVALUATION SUMMARY ---")
    for k, v in summary.items():
        print(f"{k}: {v:.4f}")
        
    return summary, df

if __name__ == "__main__":
    print("Evaluation runner ready.")
