import os
import traceback
from typing import List, Dict

from .llm_client import GeminiAgentClient
from .vector_db import VectorDBClient

# Comprehensive system prompt for the Physical AI & Humanoid Robotics domain
SYSTEM_PROMPT = """You are a Physical AI & Humanoid Robotics expert.

**ON FIRST MESSAGE: Ask user level**
"What's your background? (Beginner/Intermediate/Advanced)"

**THEN ADAPT:**

**Beginner**: Use simple language, 1-2 sentences per point, emojis, no jargon
**Intermediate**: Technical terms ok, 3-4 paragraphs, include examples
**Advanced**: Deep technical detail, math, research concepts ok

**RULES:**
- Beginner max 150 words, Intermediate max 300 words
- Simple questions = short answers (1-2 sentences)
- Complex questions = adapt by user level
- Always cite textbook context: "(Chapter X: Topic)"
- Remember user level in conversation

**RESPONSE FORMAT:**
Beginner: "X is like... 🤖 Questions?"
Intermediate: "X involves... More details on [topic]?"
Advanced: "[Technical explanation] Dive deeper?"
"""


class RAGEngine:
    """
    Orchestrates the Retrieval-Augmented Generation pipeline.
    """

    def __init__(self):
        """Initializes the RAG engine."""
        print("[INFO] Initializing RAGEngine...")
        self.vector_db_client = VectorDBClient()
        self.gemini_agent_client = GeminiAgentClient()
        print("[INFO] RAGEngine initialized.")

    def _build_rag_prompt(
        self,
        query: str,
        context: List[str],
        chat_history: List[Dict]
    ) -> str:
        """Builds the full prompt for the RAG model."""
        history_str = "\n".join(
            [f"User: {msg['user']}\nAI: {msg['ai']}" for msg in chat_history]
        )
        context_str = "\n---\n".join(context)

        # The final prompt structure includes system instructions, context, history, and the user's query.
        return f"""
{SYSTEM_PROMPT}

## Previous Conversation:
{history_str if history_str else "No previous conversation."} 

## Relevant Textbook Content:
{context_str if context_str else "No relevant content found."} 

## User's Current Question:
{query}
"""

    async def chat_with_rag(self, query: str, chat_history: List[Dict]) -> Dict:
        """
        Executes the full RAG pipeline asynchronously.
        
        Args:
            query: The user's question.
            chat_history: The conversation history.
            
        Returns:
            A dictionary with the response and citations, or an error message.
        """
        print(f"[INFO] RAGEngine received query: '{query}'")

        try:
            # 1. Embed the query
            print("[INFO] Step 1: Generating query embedding...")
            query_embedding = await self.gemini_agent_client.get_embedding(query)
            if not query_embedding:
                print("[ERROR] Failed to generate query embedding.")
                return {
                    "response": "Error: Could not generate an embedding for the query.",
                    "citations": [],
                }

            # 2. Retrieve context from the vector database
            print("[INFO] Step 2: Retrieving context from vector database...")
            search_results = await self.vector_db_client.search_vectors(
                query_embedding, limit=5
            )

            context_texts = [
                hit.payload.get("text", "")
                for hit in search_results
                if hit.payload
            ]
            citations = [
                {
                    "title": hit.payload.get("title", "Unknown Title"),
                    "chapter_path": hit.payload.get("chapter_path", "Unknown Path"),
                    "score": hit.score,
                }
                for hit in search_results
                if hit.payload
            ]
            print(f"[INFO] Retrieved {len(context_texts)} context chunks.")

            # 3. Augment the prompt
            print("[INFO] Step 3: Augmenting prompt with context...")
            augmented_prompt = self._build_rag_prompt(
                query, context_texts, chat_history
            )

            # 4. Generate the response
            print("[INFO] Step 4: Generating response with LLM...")
            response_text = await self.gemini_agent_client.generate_content(
                augmented_prompt
            )
            print("[INFO] Response generated successfully.")

            return {"response": response_text, "citations": citations}

        except Exception as e:
            print(f"[ERROR] An unexpected error occurred in RAGEngine: {e}")
            traceback.print_exc()
            return {
                "response": "An unexpected error occurred. Please try again later.",
                "citations": [],
            }
