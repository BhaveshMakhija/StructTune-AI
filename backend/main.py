from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import logging
import os
import torch

# Internal modules
from rag.engine import RAGEngine
from judge.validation import MedAuditJudge
from training.model_loader import load_base_model
from training.inference import generate_response
from evaluation.metrics import is_valid_json

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MedAudit-API")

app = FastAPI(title="StructTune MedAudit API", version="1.0.0")

# Global State
model = None
tokenizer = None
rag_engine = RAGEngine()
judge = MedAuditJudge()

@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    logger.info("Initializing MedAudit System...")
    try:
        # Check if adapter exists, else load base
        base_model, tokenizer = load_base_model()
        adapter_path = "./models/medaudit-adapter"
        if os.path.exists(adapter_path):
            from peft import PeftModel
            logger.info(f"Loading LoRA adapter from {adapter_path}")
            model = PeftModel.from_pretrained(base_model, adapter_path)
        else:
            logger.warning("No LoRA adapter found. Using base TinyLlama.")
            model = base_model
        
        logger.info("Initializing RAG index...")
        if not rag_engine.load_index():
            logger.info("RAG index not found. Building initial index...")
            rag_engine.build_index(num_samples=100)
            
        logger.info("MedAudit Backend Ready.")
    except Exception as e:
        logger.error(f"Startup failed: {e}")

class ExtractRequest(BaseModel):
    text: str
    use_rag: bool = True

from backend.observability import observer

@app.post("/extract")
async def extract_medical_data(request: ExtractRequest):
    logger.info(f"Received extraction request: {request.text[:50]}...")
    try:
        context = ""
        if request.use_rag:
            logger.info("Retrieving context from MedQuad...")
            retrieved = rag_engine.retrieve(request.text)
            context = "\n".join(retrieved)
            logger.info(f"Retrieved {len(retrieved)} context blocks.")

        instruction = (
            "Extract medical information (patient_name, age, diagnosis, medications, symptoms) "
            "from the input text into JSON format."
        )
        if context:
            instruction += f"\nUse the following context for grounding:\n{context}"

        response_text = generate_response(model, tokenizer, instruction, request.text)
        
        # Parse JSON
        try:
            extracted_json = json.loads(response_text)
        except:
            logger.warning("Model produced invalid JSON. Attempting cleanup.")
            extracted_json = {"error": "Invalid JSON format", "raw": response_text}

        # Run Validation for Logging
        val_res = judge.validate(request.text, extracted_json)
        
        # Log for Observability
        observer.log_inference(request.text, extracted_json, val_res)

        return {
            "input": request.text,
            "context": context,
            "extracted": extracted_json,
            "validation": val_res
        }
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate")
async def validate_extraction(data: dict):
    logger.info("Received validation request.")
    try:
        input_text = data.get("input", "")
        extracted_json = data.get("extracted", {})
        
        validation_result = judge.validate(input_text, extracted_json)
        return validation_result
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_latest_metrics():
    logger.info("Fetching latest evaluation metrics.")
    try:
        metrics_path = "evaluation/results/medaudit_latest.json"
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                return json.load(f)
        else:
            return {"status": "No evaluation data found. Run evaluation script first."}
    except Exception as e:
        logger.error(f"Metrics fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
