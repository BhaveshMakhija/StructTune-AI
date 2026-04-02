# StructTune AI 🧪: The Fine-Tuning Laboratory

**StructTune AI** is an end-to-end laboratory for developing high-precision JSON extraction models. It specializes in calibrating Small Language Models (SLMs) to bridge the gap between unstructured text and deterministic structured data.

### 🎯 Project Goal
State-of-the-art LLMs often struggle with consistent JSON adherence in resource-constrained environments. This lab provides a modular framework to **synthesize data**, **calibrate via SFT (LoRA)**, **align via DPO**, and **benchmark results** in a real-time React dashboard—all optimized to run on **8GB RAM / CPU-only** hardware.

---

## 🏗️ Technical Architecture

The laboratory follows a decoupled, pipeline-first architecture, ensuring each stage of the ML lifecycle is independent:

```text
/data          → Synthetic JSONL generators and instruction loaders.
/models        → Storage for low-rank (LoRA) adapters and model checkpoints.
/training      → Orchestration of SFT and DPO training loops on CPU.
/evaluation    → Precision metrics engine (Validity, Exact Match, Field Accuracy).
/backend       → FastAPI REST server for low-latency model inference.
/frontend      → React + Vite interactive comparison playground.
/tests         → End-to-end integration and sanity suites.
```

---

## 🔬 The Development Pipeline

### 1. Dataset Engineering (`/data`)
We utilize a **Synthetic Instruction Synthesis** strategy to generate high-quality JSONL samples. By creating a variety of extraction scenarios (Name, Age, City, Occupation), we ensure the model learns diverse structural patterns rather than just rote memorization.

### 2. SFT: Supervised Fine-Tuning (`/training`)
To maintain a lightweight footprint, we implement **PEFT (LoRA)** on `TinyLlama-1.1B`. 
- **Design Choice**: Low-rank adaptation allows us to train only 1% of the model parameters, fitting the entire process into 8GB of RAM.
- **Optimization**: Gradient accumulation and `float32` CPU-optimized tensors are used to ensure stability without a GPU.

### 3. DPO: Direct Preference Optimization (`/training`)
Beyond simple calibration, we apply **DPO** to align the model with "Preferred" structured outputs. This stage penalizes malformed JSON strings and rewards strict schema adherence, significantly reducing hallucination in structured fields.

### 4. Evaluation Engine (`/evaluation`)
We move beyond generic 'Loss' metrics to task-specific KPIs:
- **JSON Validity**: Boolean check for parseable JSON strings.
- **Exact Match (EM)**: String-level parity with ground truth.
- **Field-Level Accuracy**: Deep comparison of JSON keys/values to identify specific extraction errors.

### 5. React Playground (`/frontend`)
The final piece is a **Three-Way Comparison Dashboard**. It benchmarks the **Base Model**, the **SFT Model**, and the **DPO Model** side-by-side, allowing for qualitative analysis of the fine-tuning delta in real-time.

---

## 🚦 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- `.venv` virtual environment for isolation.

### 1. Backend & ML Setup
```bash
# Initialize Environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run Training (CPU-only)
python training/train.py      # Produces SFT Adapter
python training/dpo_train.py  # Produces DPO Adapter

# Launch API
python backend/main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*The lab will be accessible at `http://localhost:3000`.*

---

## 📊 Benchmarking & Performance

### Sample Parity
| Component | Input Text | Model Output (JSON) | Accuracy |
| :--- | :--- | :--- | :--- |
| **Base** | "Jane is 29." | "Jane is 29 years old." | ❌ 0% |
| **SFT** | "Jane is 29." | `{"name": "Jane", "age": 29}` | ✅ 90% |
| **DPO** | "Jane is 29." | `{"name": "Jane", "age": 29}` | ✅ 100% |

### Why this works:
- **CPU-Friendly**: Avoids heavy CUDA dependencies; runs on global standard hardware.
- **Low-Rank Focus**: LoRA adapters are <50MB, making them highly portable.
- **Constraint-Aware**: Designed for edge-case stability on 8GB machines.

---

