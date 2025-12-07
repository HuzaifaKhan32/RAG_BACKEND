import os
import re
from qdrant_client import models
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client import QdrantClient
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict
import hashlib

load_dotenv()

# --- Environment Variables ---
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_chatbot_collection")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_PATH = os.path.join(PROJECT_ROOT, "docusaurus", "docs")

# Debug
print(f"[DEBUG] Project root: {PROJECT_ROOT}")
print(f"[DEBUG] Docs path: {DOCS_PATH}")
print(f"[DEBUG] Path exists: {os.path.exists(DOCS_PATH)}")

if not os.path.exists(DOCS_PATH):
    raise FileNotFoundError(f"Docs path not found: {DOCS_PATH}")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# FIX: Use correct Gemini embedding model
EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_SIZE = 768

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def get_embedding(text: str) -> List[float]:
    """Generate embedding using Gemini."""
    response = genai.embed_content(model=EMBEDDING_MODEL, content=text)
    return response['embedding']

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
    """
    Splits text into chunks of specified size with overlap.
    
    Args:
        text: Input text to chunk
        chunk_size: Target chunk size in words
        overlap: Number of words to overlap between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    if not sentences:
        return [text]

    for sentence in sentences:
        sentence_length = len(sentence.split())
        
        if current_length + sentence_length <= chunk_size:
            # Sentence fits in current chunk
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            # Current chunk is full, save it
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            
            # Create new chunk with overlap
            if overlap > 0 and current_chunk:
                # Take last N words as overlap
                chunk_text_str = " ".join(current_chunk)
                words = chunk_text_str.split()
                overlap_words = words[-overlap:] if len(words) > overlap else words
                overlap_text = " ".join(overlap_words)
                
                current_chunk = [overlap_text, sentence]
                current_length = len(overlap_text.split()) + sentence_length
            else:
                current_chunk = [sentence]
                current_length = sentence_length
    
    # Add final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks if chunks else [text]

def extract_markdown_content(filepath: str) -> Dict:
    """Extract content from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter_match = re.match(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if frontmatter_match:
        frontmatter_str = frontmatter_match.group(1)
        markdown_text = frontmatter_match.group(2).strip()
        
        # FIX: Correct regex pattern
        doc_id_match = re.search(r'id:\s*(.*)', frontmatter_str)
        title_match = re.search(r"title:\s*['\"]?(.*?)['\"]?", frontmatter_str)
        
        doc_id = doc_id_match.group(1).strip() if doc_id_match else os.path.splitext(os.path.basename(filepath))[0]
        title = title_match.group(1).strip() if title_match else "No Title"

        # FIX: Correct regex patterns (remove extra backslashes)
        markdown_text = re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)
        markdown_text = re.sub(r'\[.*?\]\(.*?\)', '', markdown_text)

        return {"id": doc_id, "title": title, "text": markdown_text, "filepath": filepath}
    
    return {"id": os.path.splitext(os.path.basename(filepath))[0], "title": "No Title", "text": content.strip(), "filepath": filepath}

def ingest_documents(docs_path: str):
    """Ingest documents into Qdrant."""
    
    # FIX: Check if collection exists instead of recreating
    try:
        qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' exists. Appending documents...")
    except:
        qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
        )
        print(f"Collection '{QDRANT_COLLECTION_NAME}' created.")

    points = []
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                filepath = os.path.join(root, file)
                doc_info = extract_markdown_content(filepath)
                
                relative_path = os.path.relpath(filepath, DOCS_PATH)
                display_path = re.sub(r'^\d{2}-', '', os.path.splitext(relative_path)[0])

                doc_chunks = chunk_text(doc_info["text"])
                print(f"Processing '{filepath}': {len(doc_chunks)} chunks.")

                for i, chunk in enumerate(doc_chunks):
                    chunk_id_str = f"{doc_info['id']}-{i}-{hashlib.md5(chunk.encode()).hexdigest()[:8]}"
                    point_id = int(hashlib.sha256(chunk_id_str.encode()).hexdigest(), 16) % (10**9)

                    embedding = get_embedding(chunk)
                    if embedding:
                        points.append(
                            models.PointStruct(
                                id=point_id,
                                vector=embedding,
                                payload={
                                    "text": chunk,
                                    "doc_id": doc_info["id"],
                                    "title": doc_info["title"],
                                    "chapter_path": display_path,
                                    "chunk_number": i,
                                }
                            )
                        )
    
    if points:
        print(f"Upserting {len(points)} points to Qdrant...")
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            wait=True,
            points=points
        )
        print("Document ingestion complete.")
    else:
        print("No documents found for ingestion.")

if __name__ == "__main__":
    if not QDRANT_URL or not QDRANT_API_KEY or not GEMINI_API_KEY:
        print("Error: Missing environment variables")
        print("Set QDRANT_URL, QDRANT_API_KEY, GEMINI_API_KEY in .env")
    else:
        ingest_documents(docs_path=DOCS_PATH)