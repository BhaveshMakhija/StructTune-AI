from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI(title="StructTune AI API")
    
    # 1. Setup CORS for React Frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allow all for local lab
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 2. Endpoints
    @app.get("/")
    async def root():
        return {"status": "ok", "message": "StructTune AI Backend is running"}
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
