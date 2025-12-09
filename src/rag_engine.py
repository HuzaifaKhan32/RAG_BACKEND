# src/rag_engine.py
import os
import traceback
from typing import List, Dict

from .llm_client import GeminiAgentClient
from .vector_db import VectorDBClient

# IMPROVED system prompt - removed learning level, added fallback behavior
SYSTEM_PROMPT = """You are an intelligent assistant specializing in Physical AI & Humanoid Robotics.

**YOUR PRIMARY ROLE:**
Answer questions about robotics, AI, and related topics clearly and accurately.

**WHEN TEXTBOOK CONTEXT IS PROVIDED:**
- Base your answer primarily on the provided textbook content
- Cite specific sections: "(Chapter X: Section Name)"
- Connect concepts across different chapters when relevant
- Provide technical depth with clear explanations

**WHEN NO TEXTBOOK CONTEXT IS AVAILABLE:**
- Answer using your general knowledge about robotics and AI
- Be clear that you're providing general information
- Suggest related topics that might be in the textbook
- Remain accurate and helpful

**RESPONSE STYLE:**
- Be direct and concise
- Use clear technical language
- Include examples when helpful
- Format responses with proper structure (paragraphs, not excessive bullet points)
- Avoid asking about learning levels or user preferences

**CITATION FORMAT:**
When using textbook content:
- "According to Chapter X..."
- "The textbook explains in [Section]..."
- "As covered in Chapter X: [Topic]..."

**CRITICAL RULES:**
1. Prioritize textbook content when available
2. Fall back to general knowledge when textbook content is insufficient
3. Be helpful and informative in all cases
4. Don't refuse to answer if context is missing - use your knowledge
5. Keep responses natural and conversational, not overly structured
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
        chat_history: List[Dict],
        has_context: bool
    ) -> str:
        """Builds the full prompt for the RAG model."""
        history_str = "\n".join(
            [f"User: {msg['user']}\nAI: {msg['ai']}" for msg in chat_history[-3:]]  # Only last 3 messages
        )
        
        if has_context and context:
            context_str = "\n\n---\n\n".join(context)
            context_section = f"""## Relevant Textbook Content:
{context_str}

Use the above textbook content to answer the question. Cite the sources appropriately."""
        else:
            context_section = """## Note:
No specific textbook content was found for this query. Answer using your general knowledge about Physical AI, Robotics, and related topics. Be helpful and accurate."""

        history_section = f"""## Previous Conversation:
{history_str}
""" if history_str else ""

        return f"""{SYSTEM_PROMPT}

{history_section}
{context_section}

## User's Question:
{query}

## Your Response:
Provide a clear, direct answer. If using textbook content, cite it. If using general knowledge, be helpful and suggest related textbook topics if relevant."""

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
            
            # Initialize context and citations
            context_texts = []
            citations = []
            has_relevant_context = False
            
            # 2. Try to retrieve context from the vector database
            if query_embedding:
                print("[INFO] Step 2: Retrieving context from vector database...")
                try:
                    search_results = await self.vector_db_client.search_vectors(
                        query_embedding, limit=5
                    )
                    
                    if search_results:
                        # Filter results by relevance score (threshold: 0.5)
                        relevant_results = [hit for hit in search_results if hit.score > 0.5]
                        
                        if relevant_results:
                            has_relevant_context = True
                            context_texts = [
                                hit.payload.get("text", "")
                                for hit in relevant_results
                                if hit.payload
                            ]
                            citations = [
                                {
                                    "title": hit.payload.get("title", ""),
                                    "chapter_path": hit.payload.get("chapter_path", "Unknown"),
                                    "score": hit.score,
                                }
                                for hit in relevant_results
                                if hit.payload
                            ]
                            print(f"[INFO] Retrieved {len(context_texts)} relevant context chunks (score > 0.5).")
                        else:
                            print("[INFO] No highly relevant results found (all scores < 0.5). Will use general knowledge.")
                    else:
                        print("[INFO] No search results returned. Will use general knowledge.")
                        
                except Exception as search_error:
                    print(f"[WARN] Vector search failed: {search_error}. Falling back to general knowledge.")
            else:
                print("[WARN] Could not generate embedding. Falling back to general knowledge.")

            # 3. Build the prompt (with or without context)
            print(f"[INFO] Step 3: Building prompt (has_context={has_relevant_context})...")
            augmented_prompt = self._build_rag_prompt(
                query, context_texts, chat_history, has_relevant_context
            )

            # 4. Generate the response
            print("[INFO] Step 4: Generating response with LLM...")
            response_text = await self.gemini_agent_client.generate_content(
                augmented_prompt
            )
            
            # Add a note if we're using general knowledge
            if not has_relevant_context and response_text:
                print("[INFO] Response generated using general knowledge (no textbook context).")
            else:
                print("[INFO] Response generated successfully with textbook context.")

            return {
                "response": response_text,
                "citations": citations,
                "has_textbook_context": has_relevant_context
            }

        except Exception as e:
            print(f"[ERROR] An unexpected error occurred in RAGEngine: {e}")
            traceback.print_exc()
            
            # Even on error, try to answer with general knowledge
            try:
                print("[INFO] Attempting fallback response with general knowledge...")
                fallback_prompt = f"""{SYSTEM_PROMPT}

The system encountered an error retrieving textbook content. Please answer the following question using your general knowledge about Physical AI and Robotics:

{query}

Provide a helpful, accurate answer."""
                
                fallback_response = await self.gemini_agent_client.generate_content(fallback_prompt)
                
                return {
                    "response": fallback_response,
                    "citations": [],
                    "has_textbook_context": False
                }
            except:
                return {
                    "response": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                    "citations": [],
                    "has_textbook_context": False
                }
