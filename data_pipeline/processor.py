import json
import random
import os
from datasets import load_dataset
from tqdm import tqdm

class MedicalDataProcessor:
    def __init__(self):
        self.names = ["James Moore", "Maria Garcia", "Robert Smith", "Linda Taylor", "Michael Brown", "Elizabeth Wilson", "David Jones", "Jennifer Miller"]
        self.symptoms_pool = ["fever", "cough", "fatigue", "shortness of breath", "nausea", "dizziness", "joint pain", "headache"]
        
    def load_hf_datasets(self):
        print("📥 Loading BC5CDR (Chemicals & Diseases)...")
        try:
            bc5cdr = load_dataset("bc5cdr", "bc5cdr", split="train", trust_remote_code=True)
        except:
            bc5cdr = [] # Fallback for local testing if needed
        
        print("📥 Loading NCBI Disease...")
        try:
            ncbi = load_dataset("ncbi_disease", split="train", trust_remote_code=True)
        except:
            ncbi = []
        
        print("📥 Loading MedQuad (QA Corpus)...")
        try:
            medquad = load_dataset("keivalya/MedQuad-MedicalQnADataset", split="train", trust_remote_code=True)
        except:
            try:
                medquad = load_dataset("BIOMEDNLP/MedQuAD", split="train", trust_remote_code=True)
            except:
                medquad = []
        
        return bc5cdr, ncbi, medquad

    def extract_entities(self, bc5cdr, ncbi):
        diseases = set()
        medications = set()
        
        # BC5CDR Label 1 is Chemical, Label 2 is Disease usually? 
        # Actually BC5CDR has 'tokens' and 'ner_tags'
        # 0: O, 1: B-Chemical, 2: I-Chemical, 3: B-Disease, 4: I-Disease
        
        for sample in bc5cdr:
            tokens = sample['tokens']
            tags = sample['ner_tags']
            current_chem = []
            current_dis = []
            for t, tag in zip(tokens, tags):
                if tag in [1, 2]:
                    current_chem.append(t)
                elif tag in [3, 4]:
                    current_dis.append(t)
                else:
                    if current_chem: medications.add(" ".join(current_chem)); current_chem = []
                    if current_dis: diseases.add(" ".join(current_dis)); current_dis = []
        
        for sample in ncbi:
            tokens = sample['tokens']
            tags = sample['ner_tags']
            current_dis = []
            for t, tag in zip(tokens, tags):
                if tag in [1, 2]: # B-Disease, I-Disease
                    current_dis.append(t)
                else:
                    if current_dis: diseases.add(" ".join(current_dis)); current_dis = []
                    
        return list(diseases), list(medications)

    def synthesize_sample(self, diseases, medications):
        name = random.choice(self.names)
        age = random.randint(20, 80)
        diagnosis = random.choice(diseases) if diseases else "Hypertension"
        meds = random.sample(medications, random.randint(1, 2)) if medications else ["Aspirin"]
        symptoms = random.sample(self.symptoms_pool, random.randint(1, 3))
        
        templates = [
            "Patient {name}, {age} years old, presents with {symptoms}. After examination, the patient was diagnosed with {diagnosis} and prescribed {medications}.",
            "Clinical Note: {name} ({age}y/o) reporting {symptoms}. Primary diagnosis is {diagnosis}. Current treatment plan includes {medications}.",
            "Subject: {name}, Age: {age}. Symptoms observed: {symptoms}. Confirmed {diagnosis}. Starting on {medications} immediately."
        ]
        
        template = random.choice(templates)
        input_text = template.format(
            name=name, 
            age=age, 
            symptoms=", ".join(symptoms), 
            diagnosis=diagnosis, 
            medications=" and ".join(meds)
        )
        
        output = {
            "patient_name": name,
            "age": str(age),
            "diagnosis": diagnosis,
            "medications": meds,
            "symptoms": symptoms
        }
        
        return {
            "input": input_text,
            "output": output
        }

    def run(self, num_samples=300):
        bc5cdr, ncbi, medquad = self.load_hf_datasets()
        diseases, medications = self.extract_entities(bc5cdr, ncbi)
        
        samples = []
        for _ in range(num_samples):
            samples.append(self.synthesize_sample(diseases, medications))
            
        return samples

if __name__ == "__main__":
    processor = MedicalDataProcessor()
    # This will be called in Step 3
    pass
