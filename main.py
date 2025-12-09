# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

from src.rag_engine import RAGEngine

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics RAG Backend",
    description="Intelligent textbook assistant powered by RAG",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine (singleton)
rag_engine = RAGEngine()

# Request/Response models
class ChatMessage(BaseModel):
    user: str
    ai: str

class ChatRequest(BaseModel):
    query: str
    chat_history: List[ChatMessage] = []

class Citation(BaseModel):
    title: str
    chapter_path: str
    score: float

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation]
    has_textbook_context: bool = True  # Indicates if response used textbook or general knowledge


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Physical AI RAG Backend",
        "version": "1.0.0"
    }


@app.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"ok": True}


@app.post("/api/chat/query", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for RAG-powered conversations.
    
    Args:
        request: ChatRequest containing query and chat history
        
    Returns:
        ChatResponse with AI response, citations, and context indicator
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        # Convert Pydantic models to dicts for RAG engine
        chat_history_dicts = [
            {"user": msg.user, "ai": msg.ai}
            for msg in request.chat_history
        ]
        
        # Execute RAG pipeline
        result = await rag_engine.chat_with_rag(
            query=request.query,
            chat_history=chat_history_dicts
        )
        
        return ChatResponse(
            response=result["response"],
            citations=result.get("citations", []),
            has_textbook_context=result.get("has_textbook_context", False)
        )
        
    except Exception as e:
        print(f"[ERROR] Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request"
        )


@app.get("/api/health")
async def health_check():
    """
    Comprehensive health check endpoint.
    """
    try:
        # Check Qdrant connection
        collection_info = await rag_engine.vector_db_client.get_collection_info()
        
        if collection_info:
            return {
                "status": "healthy",
                "services": {
                    "qdrant": "connected",
                    "gemini": "available",
                },
                "collection": {
                    "name": rag_engine.vector_db_client.collection_name,
                    "points": collection_info.points_count,
                    "status": collection_info.status
                }
            }
        else:
            return {
                "status": "degraded",
                "services": {
                    "qdrant": "connection_failed",
                    "gemini": "available",
                },
                "message": "Vector database connection failed, but chatbot can still answer with general knowledge"
            }
            
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "message": "Some services unavailable, but chatbot can still function with general knowledge"
        }


@app.get("/api/collection-info")
async def get_collection_info():
    """
    Get information about the Qdrant collection.
    """
    try:
        info = await rag_engine.vector_db_client.get_collection_info()
        if info:
            return {
                "collection_name": rag_engine.vector_db_client.collection_name,
                "points_count": info.points_count,
                "status": info.status,
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="Could not retrieve collection information"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving collection info: {str(e)}"
        )


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
