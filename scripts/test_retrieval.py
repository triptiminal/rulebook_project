import json
import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b))

def main():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    embeddings = np.load("data/embeddings.npy")
    
    queries = [
        "What attendance is required for a student with a medical certificate to sit for the final examination?",
        "Can a student facing financial hardship retain university services after the normal tuition payment deadline?",
        "Can a student return to the hostel after 10 PM during examination periods?"
    ]
    
    for i, q in enumerate(queries, 1):
        print(f"\nTest Question {i}: {q}")
        
        q_emb = model.encode(q)
        scores = cosine_similarity(embeddings, q_emb)
        
        # Get top 10 results
        top_k_indices = np.argsort(scores)[::-1][:10]
        
        for rank, idx in enumerate(top_k_indices, 1):
            chunk = chunks[idx]
            print(f"  [{rank}] {chunk['file']} — {chunk['section']} (Score: {scores[idx]:.4f})")

if __name__ == "__main__":
    main()
