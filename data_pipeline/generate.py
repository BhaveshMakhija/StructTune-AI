from data_pipeline.processor import MedicalDataProcessor
import json
import os

def main():
    print("🪄 Generating MedAudit structured dataset...")
    processor = MedicalDataProcessor()
    
    # Generate samples (target 200-500)
    samples = processor.run(num_samples=400)
    
    # Save as data/processed/train.json
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/train.json", "w") as f:
        json.dump(samples, f, indent=2)
        
    print(f"✅ Successfully generated {len(samples)} samples in data/processed/train.json")

if __name__ == "__main__":
    main()
