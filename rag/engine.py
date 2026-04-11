import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from datasets import load_dataset

class RAGEngine:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name, device="cpu")
        self.index = None
        self.corpus = []
        self.index_path = "rag/medquad_faiss.index"
        self.corpus_path = "rag/medquad_corpus.json"

    def build_index(self, num_samples=500):
        print("📥 Fetching MedQuad for RAG index...")
        try:
            medquad = load_dataset("keivalya/MedQuad-MedicalQnADataset", split="train", trust_remote_code=True)
            # Take a small subset for CPU speed
            subset = medquad.select(range(min(num_samples, len(medquad))))
            self.corpus = [f"Q: {row['Question']}\nA: {row['Answer']}" for row in subset]
        except:
            print("⚠️ MedQuad load failed, using dummy medical corpus.")
            self.corpus = [
                "Hypertension is defined as blood pressure above 140/90 mmHg.",
                "Common symptoms of Diabetes include increased thirst, frequent urination, and unexplained weight loss.",
                "Acetaminophen is used to treat mild to moderate pain and reduce fever.",
                "Aspirin is often prescribed to reduce the risk of heart attack."
            ]
        
        print(f"Indexing {len(self.corpus)} documents...")
        embeddings = self.model.encode(self.corpus, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # Persistence
        faiss.write_index(self.index, self.index_path)
        import json
        with open(self.corpus_path, "w") as f:
            json.dump(self.corpus, f)
        print(f"✅ RAG index built and saved to {self.index_path}")

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.corpus_path):
            self.index = faiss.read_index(self.index_path)
            import json
            with open(self.corpus_path, "r") as f:
                self.corpus = json.load(f)
            return True
        return False

    def retrieve(self, query, top_k=2):
        if self.index is None:
            if not self.load_index():
                print("⚠️ Index not found, building now...")
                self.build_index()
        
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = [self.corpus[i] for i in indices[0] if i != -1]
        return results

if __name__ == "__main__":
    engine = RAGEngine()
    engine.build_index(num_samples=100)
    test_query = "What are symptoms of high blood pressure?"
    context = engine.retrieve(test_query)
    print(f"Query: {test_query}\nRetrieved: {context}")
