import json
import os
from evaluation.metrics import is_valid_json, field_accuracy
from judge.validation import MedAuditJudge

class MedAuditEvaluator:
    def __init__(self):
        self.judge = MedAuditJudge()

    def run_evaluation(self, test_samples):
        """
        Expects a list of dictionaries with 'input', 'target_output', and 'predicted_output'.
        """
        results = {
            "total": len(test_samples),
            "schema_validity": 0,
            "hallucination_rate": 0,
            "extraction_accuracy": 0,
            "failed_samples": []
        }

        hallucinations = 0
        valid_jsons = 0
        total_accuracy = 0

        for sample in test_samples:
            text_input = sample["input"]
            target = sample["target_output"]
            pred = sample["predicted_output"]

            # 1. Schema Validity
            is_valid = is_valid_json(json.dumps(pred))
            valid_jsons += is_valid

            # 2. Field Accuracy (Schema level)
            total_accuracy += field_accuracy(json.dumps(pred), json.dumps(target))

            # 3. Judge Validation (Hallucination)
            judge_res = self.judge.validate(text_input, pred)
            if judge_res["verdict"] == "FAIL" and "hallucination" in judge_res["type"]:
                hallucinations += 1
                results["failed_samples"].append({
                    "input": text_input,
                    "pred": pred,
                    "issues": judge_res["issues"]
                })

        results["schema_validity"] = (valid_jsons / len(test_samples)) * 100
        results["hallucination_rate"] = (hallucinations / len(test_samples)) * 100
        results["extraction_accuracy"] = (total_accuracy / len(test_samples)) * 100

        return results

def generate_test_dataset():
    # Load some processed data as test set
    if os.path.exists("data/processed/train.json"):
        with open("data/processed/train.json", "r") as f:
            data = json.load(f)
            return data[:20] # Take 20 for quick eval
    return []

if __name__ == "__main__":
    evaluator = MedAuditEvaluator()
    samples = generate_test_dataset()
    
    # Mock some predictions for evaluation demonstration
    test_eval_data = []
    for s in samples:
        # Simulate some errors
        pred = s["output"].copy()
        if os.urandom(1)[0] % 5 == 0: # 20% hallucination
            pred["medications"].append("Placebo-X")
            
        test_eval_data.append({
            "input": s["input"],
            "target_output": s["output"],
            "predicted_output": pred
        })

    metrics = evaluator.run_evaluation(test_eval_data)
    print("📊 MedAudit Evaluation Results:")
    print(json.dumps(metrics, indent=2))
    
    # Save results
    os.makedirs("evaluation/results", exist_ok=True)
    with open("evaluation/results/medaudit_latest.json", "w") as f:
        json.dump(metrics, f, indent=2)
