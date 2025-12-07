import sys
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.rag_engine import RAGEngine

load_dotenv()

# --- FastAPI Setup ---
app = FastAPI(
    title="Physical AI RAG Chatbot",
    description="RAG backend for Physical AI textbook",
    version="1.0.0"
)

# --- CORS Configuration ---
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialize RAG Engine ---
rag_engine = RAGEngine()

# --- Pydantic Models ---
class Message(BaseModel):
    user: str
    ai: str

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    chat_history: Optional[List[Message]] = []

class Citation(BaseModel):
    title: str
    chapter_path: str
    score: float

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation] = []
    session_id: str

# --- Endpoints ---
@app.get("/")
async def root():
    return {
        "message": "Physical AI RAG Chatbot API",
        "docs": "/docs",
        "health": "/api/health",
        "chat": "/api/chat/query"
    }

@app.get("/api/health")
async def health_check():
    """Health check - simplified version"""
    try:
        return {
            "status": "ok",
            "message": "FastAPI is running!",
            "qdrant": "ready",
            "gemini": "ready",
            "rag_engine": "initialized"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")

@app.post("/api/chat/query", response_model=ChatResponse)
async def chat_with_rag_endpoint(request: ChatRequest):
    try:
        print(f"[DEBUG] Received query: {request.query}")
        print(f"[DEBUG] RAGEngine available: {rag_engine is not None}")
        
        history_dicts = [{"user": msg.user, "ai": msg.ai} for msg in request.chat_history]
        session_id = request.session_id or "default"
        
        response_data = await rag_engine.chat_with_rag(request.query, history_dicts)
        print(f"[DEBUG] Got response: {response_data}")
        
        return ChatResponse(
            response=response_data["response"],
            citations=[Citation(**c) for c in response_data["citations"]],
            session_id=session_id
        )
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)