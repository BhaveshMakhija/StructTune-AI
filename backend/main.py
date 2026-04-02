import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from training.inference import generate_response
import torch

class InferenceRequest(BaseModel):
    instruction: str
    input_text: str
    model_name: str = "sft"

# Shared model state
model = None
tokenizer = None

def create_app():
    app = FastAPI(title="StructTune AI API")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {"status": "ok", "message": "StructTune AI Backend is running"}
    
    @app.post("/infer")
    async def infer(request: InferenceRequest):
        """
        Main inference endpoint for extraction tasks.
        """
        global model, tokenizer
        try:
            if model is None:
                return {
                    "result": f"{request.instruction}: {request.input_text}",
                    "info": "Model loading deferred for RAM efficiency."
                }
            
            response = generate_response(model, tokenizer, request.instruction, request.input_text)
            return {"result": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/metrics")
    async def get_metrics():
        """
        Get the latest evaluation metrics from storage.
        """
        try:
            results_dir = "evaluation/results"
            if not os.path.exists(results_dir):
                return {"error": "No evaluation results found."}
            
            files = [f for f in os.listdir(results_dir) if f.endswith(".json")]
            if not files:
                return {"error": "No metrics available."}
            
            latest_file = sorted(files)[-1]
            with open(os.path.join(results_dir, latest_file), "r") as f:
                content = json.load(f)
            
            return {"latest": content, "filename": latest_file}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
