import os
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

CORPUS_DIR = "corpus"
DATA_DIR = "data"

def process_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    # The markdown files have '# Title' and '## Section X: Title'
    # We can split by '## '
    sections = content.split('\n## ')
    
    chunks = []
    # The first element is the main title and preamble
    main_title = sections[0].strip().replace('# ', '')
    if len(sections) > 0:
        for idx, sec in enumerate(sections):
            if idx == 0:
                # The first part is the title, maybe some preamble.
                # If there's substantial preamble, we should capture it.
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
    # The PDF has sections starting with '1. ', '2. ', etc.
    # Split by numbers followed by dot and space at the beginning of a line
    pattern = r'\n(?=\d+\. )'
    parts = re.split(pattern, text)
    
    chunks = []
    for part in parts:
        part = part.strip()
        if not part: continue
        
        # Extract section title (first line)
        lines = part.split('\n', 1)
        section_title = lines[0].strip()
        
        chunks.append({
            "file": filename,
            "section": section_title,
            "text": part
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
            
    print(f"Extracted {len(all_chunks)} chunks. Generating embeddings...")
    texts = [c["text"] for c in all_chunks]
    
    # Generate embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Save chunks and embeddings
    print(f"Saving {len(texts)} chunks and embeddings of shape {embeddings.shape}...")
    with open(os.path.join(DATA_DIR, "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)
        
    np.save(os.path.join(DATA_DIR, "embeddings.npy"), embeddings)
    print("Ingestion complete. Data saved to data/ directory.")

if __name__ == "__main__":
    main()
