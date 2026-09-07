from app.retriever import retriever
from app.engine import classify_retrieval, run_reasoning
import json

def test():
    queries = [
        "What happens if I miss an exam because of a family wedding?", # Should be not_covered
        "What attendance is required for a student with a medical certificate to sit for the final examination?", # Should be conflict
        "Can a student return to the hostel after 10 PM during examination periods?" # Should be conflict
    ]
    
    for i, q in enumerate(queries, 1):
        print(f"\n--- Testing Query {i} ---")
        print(f"Q: {q}")
        
        raw_results = retriever.search(q, top_k=10)
        status, relevant_chunks = classify_retrieval(raw_results)
        
        print(f"Retrieval Status: {status}")
        print(f"Relevant Chunks Found: {len(relevant_chunks)}")
        
        if status == "not_covered":
            print("Result: NOT COVERED")
        elif status == "needs_reasoning":
            print("Running LLM Reasoning...")
            decision = run_reasoning(q, relevant_chunks[:5])
            print("LLM Decision:")
            print(json.dumps(decision, indent=2))

if __name__ == "__main__":
    test()
