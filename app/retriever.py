import json
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Retriever, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        print("Initializing Retriever: Loading model and embeddings...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        with open("data/chunks.json", "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        self.embeddings = np.load("data/embeddings.npy")

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b))

    def search(self, query, top_k=10):
        q_emb = self.model.encode(query)
        scores = self.cosine_similarity(self.embeddings, q_emb)
        
        top_k_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_k_indices:
            chunk = self.chunks[idx].copy()
            chunk["score"] = float(scores[idx])
            results.append(chunk)
            
        return results

# Singleton instance to be imported by the FastAPI app
retriever = Retriever()
