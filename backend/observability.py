import json
import os
from datetime import datetime

class MedAuditObserver:
    def __init__(self, log_dir="logs/audit"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"session_{self.session_id}.jsonl")

    def log_inference(self, input_text, extracted_json, validation_result):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "output": extracted_json,
            "validation": validation_result
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        # Also maintain a global latest for simple dashboarding
        with open(os.path.join(self.log_dir, "latest.json"), "w") as f:
            json.dump(entry, f, indent=2)

observer = MedAuditObserver()
