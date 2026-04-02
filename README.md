# 🔬 StructTune AI: Continuous Learning Laboratory v4.0

StructTune AI is a production-grade, CPU-optimized fine-tuning laboratory designed to demonstrate the complete lifecycle of Small Language Model (SLM) alignment. Using the **TinyLlama-1.1B** architecture, this project provides a dynamic research environment for Supervised Fine-Tuning (SFT), Direct Preference Optimization (DPO), and **Iterative Learning Reinforcement**.

---

## 🎨 Advanced Research Hub
StructTune features a modular **React + Vite** dashboard designed for real-time model auditing and iterative training cycles:
*   **3-Phase Calibration**: Compare **Base**, **SFT**, and **DPO-Aligned** checkpoints side-by-side in real-time.
*   **Neural Memory Bank**: A continuous learning layer that allows the model to "memorize" and improve from every user extraction via the **"Refine Model Weights"** feature.
*   **Agnostic Extraction Engine**: A universal semantic parser that handles noisy text (e.g., "it's been a long day") by distinguishing between descriptors and actual entity roles.
*   **Live Laboratory Telemetry**: Dynamic tracking of **Grounding Accuracy** (minimizing hallucination) and **Calibration Integrity** (strict JSON schema compliance).

---

## 🏗️ Technical Architecture

### 1. Model Pipeline (`training/`)
*   **Base Engine**: `TinyLlama-1.1B-Chat-v1.0` optimized for 8GB RAM local execution.
*   **SFT (LoRA)**: Parameter-efficient fine-tuning using `peft` and `trl` to enforce structured JSON extraction.
*   **DPO Alignment**: Preference optimization phase specifically tuned to minimize model "creativity" and maximize context grounding.

### 2. Backend Logic (`backend/`)
*   **Universal Semantic Parser**: Uses structural triggers (`is a`, `being a`, `works as`) and adaptive noise filtering to find entities in messy, high-entropy paragraphs.
*   **Continuous Feedback Loop**: Every successful refinement is stored in a persistent **Experience Cache** (`memory_bank.json`), simulating a production model that learns from its own interaction logs.

### 3. Frontend Dashboard (`frontend/`)
*   **Modular Playground**: A spacious workstation designed to handle long raw-text inputs without UI breakages.
*   **Historical Audit Logs**: Track current session experiments with the ability to "Deep Replay" any past prompt.
*   **Live Metrics Hub**: Visual analytics for Data Shards, Hallucination Filtering, and Model Precision.

---

## 📈 Metric Intelligence
*   **Calibration Integrity**: Measures "Structural Honesty" (Does the model output valid, correctly keyed JSON?).
*   **Grounding Accuracy**: Measures "Data Integrity" (Does the model stick strictly to the input, or is it hallucinating extra fields?).

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   8GB RAM (Optimized for Local CPU)

### 1. Environment Setup
```bash
python -m venv .venv
# Activate and install
.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux
pip install -r requirements.txt
```

### 2. Launch Universal Engine
```bash
# Ensure project root is in path
$env:PYTHONPATH="." 
python backend/main.py
```

### 3. Launch Research Dashboard
```bash
cd frontend
npm install
npm run dev
```
Navigate to **localhost:3000** to begin your fine-tuning experiments.

---

## 🧠 Core Philosophy
StructTune is built on the principle of **Zero-Chat Alignment**: transforming conversational models into reliable, high-precision structured data engines. By combining **Agnostic Parsing** with **Continuous Learning**, we demonstrate that SLMs can achieve enterprise-grade reliability even in memory-constrained environments.

📄 **Disclaimer**: This is a production simulation environment designed for professional demonstration and research.
