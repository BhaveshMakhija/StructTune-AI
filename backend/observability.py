import json
import os
from datetime import datetime

class MedAuditObserver:
    def __init__(self, log_dir="logs/audit"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"session_{self.session_id}.jsonl")
        
        # Session Metrics Tracking
        self.total_extractions = 0
        self.total_hallucinations = 0
        self.successful_schemas = 0
        self.total_latency = 0.0

    def log_inference(self, input_text, extracted_json, validation_result, latency_sec=0.0):
        self.total_extractions += 1
        self.total_latency += latency_sec
        
        if validation_result.get("verdict") == "PASS":
            self.successful_schemas += 1
        
        # Count hallucinations from issues list
        issues = validation_result.get("issues", [])
        if any("hallucination" in iss.lower() for iss in issues):
            self.total_hallucinations += 1

        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "output": extracted_json,
            "validation": validation_result
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
    def reset_session(self):
        self.logs = []
        self.metrics = {
            "total_audits": 0,
            "schema_valid": 0,
            "hallucinations": 0,
            "avg_latency": 0.0
        }
        # Clear the physical log file too
        if os.path.exists(self.log_file):
            open(self.log_file, 'w').close()

    def get_session_metrics(self):
        if self.total_extractions == 0:
            return {
                "extraction_accuracy": 0.0,
                "hallucination_rate": 0.0,
                "schema_validity": 0.0,
                "avg_latency": 0.0,
                "total_audits": 0
            }
        
        return {
            "extraction_accuracy": (self.successful_schemas / self.total_extractions) * 100,
            "hallucination_rate": (self.total_hallucinations / self.total_extractions) * 100,
            "schema_validity": (self.successful_schemas / self.total_extractions) * 100,
            "avg_latency": self.total_latency / self.total_extractions,
            "total_audits": self.total_extractions
        }

observer = MedAuditObserver()
