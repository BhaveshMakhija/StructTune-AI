import re
import json

class MedAuditJudge:
    def __init__(self):
        # Sample medical dictionary for simple omission checks
        self.medical_keywords = ["fever", "cough", "pain", "nausea", "dizziness", "hypertension", "diabetes", "aspirin", "insulin"]

    def validate(self, input_text, extracted_json):
        issues = []
        verdict = "PASS"
        issues_type = []

        # 1. Missing Fields Check
        required_fields = ["patient_name", "age", "diagnosis", "medications", "symptoms"]
        for field in required_fields:
            if field not in extracted_json or not extracted_json[field]:
                issues.append(f"Missing or empty field: {field}")
                if "omission" not in issues_type: issues_type.append("omission")

        # 2. Hallucination Check (Strictness: Low for names/ages, High for medical)
        # Check if diagnosis/meds/symptoms are in input
        text_lower = input_text.lower()
        
        # Check Diagnosis
        diag = str(extracted_json.get("diagnosis", "")).lower()
        if diag and diag not in text_lower:
            issues.append(f"Potential hallucination: Diagnosis '{diag}' not found in input.")
            if "hallucination" not in issues_type: issues_type.append("hallucination")

        # Check Medications
        meds = extracted_json.get("medications", [])
        for med in meds:
            if str(med).lower() not in text_lower:
                issues.append(f"Potential hallucination: Medication '{med}' not found in input.")
                if "hallucination" not in issues_type: issues_type.append("hallucination")

        # Check Symptoms
        symptoms = extracted_json.get("symptoms", [])
        for sym in symptoms:
            if str(sym).lower() not in text_lower:
                issues.append(f"Potential hallucination: Symptom '{sym}' not found in input.")
                if "hallucination" not in issues_type: issues_type.append("hallucination")

        # 3. Logic/Consistency Check (Simple)
        # Check if age is a number
        age = str(extracted_json.get("age", ""))
        if age and not re.search(r'\d+', age):
            issues.append(f"Consistency error: Age '{age}' is not a valid number.")
            if "contradiction" not in issues_type: issues_type.append("contradiction")

        if issues:
            verdict = "FAIL"

        return {
            "verdict": verdict,
            "issues": issues,
            "type": "|".join(issues_type) if issues_type else "none"
        }

if __name__ == "__main__":
    judge = MedAuditJudge()
    test_input = "John Doe, 45, has a servere headache. Diagnosed with Migraine. Prescribed Sumatriptan."
    test_output = {
        "patient_name": "John Doe",
        "age": "45",
        "diagnosis": "Migraine",
        "medications": ["Sumatriptan", "Aspirin"], # Aspirin is hallucinated
        "symptoms": ["headache"]
    }
    result = judge.validate(test_input, test_output)
    print(json.dumps(result, indent=2))
