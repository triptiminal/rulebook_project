import os
import json
import re
import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

CORPUS_DIR = "corpus"
DATA_DIR = "data"

def process_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    sections = content.split('\n## ')
    
    chunks = []
    main_title = sections[0].strip().replace('# ', '')
    if len(sections) > 0:
        for idx, sec in enumerate(sections):
            if idx == 0:
                if len(main_title.split('\n')) > 1:
                    preamble = main_title.split('\n', 1)[1].strip()
                    if preamble:
                        chunks.append({
                            "file": filename,
                            "section": "Preamble/Introduction",
                            "text": f"{main_title.split('\n')[0]}\n{preamble}"
                        })
                continue
            
            lines = sec.split('\n', 1)
            section_title = lines[0].strip()
            section_text = lines[1].strip() if len(lines) > 1 else ""
            
            chunk_text = f"{main_title.split('\n')[0]} - {section_title}\n{section_text}"
            chunks.append({
                "file": filename,
                "section": section_title,
                "text": chunk_text
            })
    return chunks

def process_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    filename = os.path.basename(filepath)
    pattern = r'\n(?=\d+\. )'
    parts = re.split(pattern, text)
    
    chunks = []
    for part in parts:
        part = part.strip()
        if not part: continue
        
        lines = part.split('\n', 1)
        section_title = lines[0].strip()
        
        chunks.append({
            "file": filename,
            "section": section_title,
            "text": part
        })
    return chunks

def process_csv(filepath):
    filename = os.path.basename(filepath)
    chunks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader):
            text = f"Data from {filename} (Row {row_idx + 1}):\n"
            for key, val in row.items():
                text += f"- {key}: {val}\n"
            
            chunks.append({
                "file": filename,
                "section": f"Row {row_idx + 1}",
                "text": text.strip()
            })
    return chunks

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Loading embedding model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    all_chunks = []
    print("Parsing corpus...")
    for filename in sorted(os.listdir(CORPUS_DIR)):
        filepath = os.path.join(CORPUS_DIR, filename)
        if filename.endswith(".md"):
            all_chunks.extend(process_markdown(filepath))
        elif filename.endswith(".pdf"):
            all_chunks.extend(process_pdf(filepath))
        elif filename.endswith(".csv"):
            all_chunks.extend(process_csv(filepath))
            
    print(f"Extracted {len(all_chunks)} chunks. Generating embeddings...")
    texts = [c["text"] for c in all_chunks]
    
    embeddings = model.encode(texts, show_progress_bar=True)
    
    print(f"Saving {len(texts)} chunks and embeddings of shape {embeddings.shape}...")
    with open(os.path.join(DATA_DIR, "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)
        
    np.save(os.path.join(DATA_DIR, "embeddings.npy"), embeddings)
    print("Ingestion complete. Data saved to data/ directory.")

if __name__ == "__main__":
    main()
