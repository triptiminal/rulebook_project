# Rulebook QA Assistant

An intelligent, Retrieval-Augmented Generation (RAG) system designed to answer university policy questions using local dense vector search and the Google Gemini API for reasoning and conflict resolution.

This system is specifically built to:
1. Provide accurate answers based strictly on the provided rulebook corpus.
2. Cite the exact clauses used to generate the answer.
3. Automatically flag internal contradictions in the policies (e.g., when a general rule is overridden by a specific exemption).
4. Safely reject out-of-scope questions with a "Not Covered" tag, without hallucinating.

## Features
- **Local Embedding Search:** Uses `all-MiniLM-L6-v2` via `sentence-transformers` to locally embed and search Markdown, PDF, and CSV files efficiently.
- **Decision Engine:** Uses Gemini to act as a strict logic gate, evaluating the retrieved chunks for answers, contradictions, or lack thereof.
- **Glassmorphic UI:** A beautiful, responsive vanilla HTML/CSS/JS frontend.
- **Evaluation Harness:** A built-in batch testing tool to evaluate the system's ability to reject tricky, unanswerable questions.

## Prerequisites
- Python 3.10 or higher
- A Google Gemini API Key

## Installation & Setup

1. **Clone the repository and enter the directory**
   ```bash
   cd rulebook_project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

### 1. Ingest the Data
Before starting the server, you need to parse the rulebook documents (Markdown, PDF, CSV) and generate the vector embeddings.

**Windows (Command Prompt / PowerShell):**
```bash
set PYTHONPATH=.
python scripts/ingest.py
```

**macOS / Linux:**
```bash
export PYTHONPATH=.
python scripts/ingest.py
```
*Note: This will download the `all-MiniLM-L6-v2` model weights on the first run and create a `data/` folder containing your embedded chunks.*

### 2. Start the Server
Run the FastAPI backend using uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
*(Optionally add `--reload` for development)*

### 3. Open the UI
Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

## How to Test

**Answered (Clear, unambiguous rules):**
- *"What is the minimum CGPA required to retain a merit scholarship?"*
- *"Are students allowed to have guests stay overnight in the hostel?"*
- *"What is the penalty for academic plagiarism on a final assignment?"*

**Conflict Detected (Injected contradictions):**
- *"When are my tuition fees due?"* (The Markdown says End of the Second Week, but the CSV says End of the First Week).
- *"What attendance is required for a student with a medical certificate to sit for the final examination?"* (attendance.md says strict 65% minimum, but examinations.md says 60% with a certificate).
- *"Can a student facing financial hardship retain university services after the normal tuition payment deadline?"* (fees.md says services are immediately suspended, but appeals.md says they retain privileges up to the 4th week).

**Not Covered (Out-of-scope questions):**
- *"Where is the nearest campus ATM located?"*
- *"Can I join the undergraduate debate club as a freshman?"*
- *"What time does the university gym close on Sundays?"*

**Evaluation Harness:**
Click the **"Evaluate System"** button in the top left of the UI. This triggers a batch test using 25 highly plausible but totally unanswerable university questions located in `test/25_unanswered_questions.txt`. You can watch the system systematically reject them as "Not Covered" in real-time, verifying that the fast-path semantic threshold is working perfectly!
