# StructTune MedAudit — Clinical Document Extraction + Validation System

## Architecture
- **Extractor**: LoRA fine-tuned TinyLlama for medical entity extraction.
- **RAG**: FAISS-based grounding using MedQuad.
- **Judge**: Rule-based validation for hallucination and consistency.
- **Data Pipeline**: Unified processing of MedQuad, BC5CDR, and NCBI datasets.

## Structure
- `/backend`: FastAPI service.
- `/frontend`: React dashboard.
- `/rag`: FAISS indexing and retrieval.
- `/judge`: Clinical validation logic.
- `/data_pipeline`: Dataset ingestion and processing.
- `/evaluation`: Model and system metrics.
- `/training`: LoRA fine-tuning scripts.
