from data_pipeline.processor import MedicalDataProcessor
import os

def main():
    print("🚀 Initializing MedAudit Data Pipeline...")
    processor = MedicalDataProcessor()
    # Step 2: Integration check (just load)
    try:
        bc5cdr, ncbi, medquad = processor.load_hf_datasets()
        print("✅ Datasets Integrated Successfully.")
    except Exception as e:
        print(f"❌ Integration Failed: {e}")

if __name__ == "__main__":
    main()
