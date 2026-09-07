from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os

from app.retriever import retriever
from app.engine import classify_retrieval, run_reasoning

app = FastAPI(title="Rulebook QA Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    status: str
    answer: str
    citations: List[str]
    retrieved_chunks: List[Dict[str, Any]]

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    # 1. Retrieve raw results from vector store
    raw_results = retriever.search(request.query, top_k=10)
    
    # 2. Classify (Filter based on threshold)
    status, relevant_chunks = classify_retrieval(raw_results)
    
    # 3. Decision Branching
    if status == "not_covered":
        return QueryResponse(
            status="not_covered",
            answer="I'm sorry, but the university rulebook does not contain any information to answer this question.",
            citations=[],
            retrieved_chunks=raw_results
        )
        
    elif status == "needs_reasoning":
        top_chunks = relevant_chunks[:10]
        llm_decision = run_reasoning(request.query, top_chunks)
        
        return QueryResponse(
            status=llm_decision.get("status", "error"),
            answer=llm_decision.get("answer", "An error occurred during reasoning."),
            citations=llm_decision.get("citations", []),
            retrieved_chunks=relevant_chunks
        )

@app.get("/evaluation/questions")
def get_evaluation_questions():
    filepath = "test/25_unanswered_questions.txt"
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]
    return questions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
