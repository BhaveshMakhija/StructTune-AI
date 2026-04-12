from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    import time
    start_time = time.time()
    
    logger.info(f"--- CLINICAL EXTRACTION ---")
    if not request.text.strip():
        return {"error": "Empty input"}

    try:
        # SUPER MINIMAL PROMPT - Optimized for 1.1B stability
        prompt = f"""
Extract medical information from input text into valid JSON format.
Output ONLY JSON. No explanation.

Rules:
- Format: "patient_name", "age", "diagnosis", "medications", "symptoms"
- If missing, use "" or []

INPUT:
{request.text}

OUTPUT:
"""

        # INFERENCE - Deterministic
        response_text = generate_response(
            model, 
            tokenizer, 
            prompt, 
            "", 
            max_new_tokens=80, 
            temperature=0.1, 
            do_sample=False
        )
        
        logger.info(f"RAW OUTPUT: {response_text}")

        # STABILIZED PARSING
        import re
        # Isolate the main JSON object
        json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        clean_json = json_match.group(1) if json_match else "{}"

        # Sanitize common model mess-ups
        clean_json = re.sub(r'//.*', '', clean_json) # strip // comments
        clean_json = re.sub(r',\s*([\]\}])', r'\1', clean_json) # fix trailing commas
        
        try:
            extracted = json.loads(clean_json)
            # Schema normalization
            keys = {"patient_name": "", "age": "", "diagnosis": "", "medications": [], "symptoms": []}
            for k, default in keys.items():
                if k not in extracted: extracted[k] = default
            
            val_res = judge.validate(request.text, extracted)
            result = {
                "extracted": extracted,
                "validation": val_res,
                "latency": time.time() - start_time,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Stabilization failed: {e}")
            result = {
                "extracted": {"patient_name": "Structure Error", "age": "", "diagnosis": "Malformed output", "medications": [], "symptoms": []},
                "validation": {"verdict": "FAIL", "issues": ["Model structural failure"]},
                "latency": time.time() - start_time
            }

        observer.log_inference(request.text, result.get("extracted", {}), result.get("validation", {}), latency_sec=result["latency"])
        return result

    except Exception as e:
        logger.error(f"Backend Error: {e}")
        raise HTTPException(status_code=500, detail="Inference Failed")

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
    logger.info("Fetching live session metrics.")
    try:
        # Return dynamic session metrics instead of static file
        return observer.get_session_metrics()
    except Exception as e:
        logger.error(f"Metrics fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_session():
    try:
        observer.reset_session()
        logger.info("Session metrics and logs cleared by user.")
        return {"status": "success", "message": "Global session metrics reset."}
    except Exception as e:
        logger.error(f"Reset failed: {e}")
        raise HTTPException(status_code=500, detail="Reset failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
