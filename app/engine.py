import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

RELEVANCE_THRESHOLD = 0.45
MIN_EVIDENCE = 1

try:
    client = genai.Client()
except Exception:
    client = None

def classify_retrieval(results):
    relevant = [
        result
        for result in results
        if result["score"] >= RELEVANCE_THRESHOLD
    ]

    if len(relevant) < MIN_EVIDENCE:
        return "not_covered", relevant

    return "needs_reasoning", relevant

def run_reasoning(query, relevant_chunks):
    if not client:
        return {
            "status": "error",
            "answer": "Google GenAI Client could not be initialized. Please check your GEMINI_API_KEY in the .env file.",
            "citations": []
        }
        
    context_text = ""
    for idx, chunk in enumerate(relevant_chunks):
        context_text += f"\n--- Source: {chunk['file']} - {chunk['section']} ---\n"
        context_text += chunk['text'] + "\n"

    prompt = f"""
You are an expert University Policy Assistant. You must answer the user's question based strictly on the provided policy documents.

User Query: "{query}"

Context Documents:
{context_text}

Instructions:
1. Carefully read the context documents.
2. Determine if the documents provide a clear answer to the query.
   - If the documents do not contain enough information to answer the query, flag it as "not_covered".
3. CRITICAL: Check if any of the provided rules CONTRADICT each other regarding the query. 
   - Note: In this system, any time one section states a strict general rule, but another section provides an EXEMPTION, WAIVER, or DIFFERENT THRESHOLD for that exact rule, YOU MUST FLAG THIS AS A "conflict". 
   - Why? Because the rulebook is technically giving two different answers depending on which section the student reads. For example, if Section A says "Curfew is strictly 10 PM" and Section B says "Students studying in the library are exempt from curfew", this is a CONFLICT for our purposes.
   - If the rules are completely consistent without any such exceptions overriding another rule, flag it as "answered".
4. Provide a clear, helpful response explaining the answer or the contradiction. If it's a conflict, explain exactly what the conflicting clauses state. If not covered, state that the rulebook is silent on this issue.
5. List the citations you used (using exactly "filename.md - Section Name"). Leave empty if not covered.

Respond in JSON format exactly matching this schema:
{{
  "status": "answered" | "conflict" | "not_covered",
  "answer": "Your detailed explanation here...",
  "citations": ["filename.md - Section Name", ...]
}}
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "status": "error",
            "answer": f"Error calling LLM: {str(e)}",
            "citations": []
        }
