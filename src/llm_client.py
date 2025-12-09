import os
import traceback
from typing import List, Dict

from .llm_client import GeminiAgentClient
from .vector_db import VectorDBClient

# Comprehensive system prompt for the Physical AI & Humanoid Robotics domain
SYSTEM_PROMPT = """You are an intelligent textbook assistant for "Physical AI & Humanoid Robotics."

**YOUR PRIMARY ROLE:**
Help students understand the textbook content by explaining concepts, clarifying passages, and answering questions based ONLY on the provided book content.

**FIRST INTERACTION:**
When a user first messages you, ask:
"What's your learning level? (Beginner/Intermediate/Advanced)"

**ADAPTATION BY LEVEL:**

**Beginner:**
- Use simple, everyday language
- Break down complex ideas into easy steps
- Use analogies and examples from daily life
- Keep responses under 150 words
- Use emojis for engagement 🤖
- Avoid technical jargon

**Intermediate:**
- Use technical terminology with brief explanations
- Provide more detailed explanations (200-300 words)
- Include practical examples and applications
- Connect concepts across chapters

**Advanced:**
- Deep technical explanations with mathematical formulations
- Discuss research implications and edge cases
- Reference specific algorithms, equations, and methodologies
- No word limit for complex topics

**HANDLING SPECIFIC QUESTIONS:**

When users ask about specific passages (e.g., "What does paragraph 3 in Chapter 5 mean?"):
1. Quote the relevant passage
2. Explain it in simpler terms adapted to their level
3. Provide context from surrounding content
4. Relate it to other concepts in the book

When users ask general concepts:
1. Extract relevant information from the textbook context
2. Synthesize information from multiple sections if needed
3. Explain progressively based on user level

**CITATION FORMAT:**
Always cite your sources from the textbook:
- "(Chapter X: Section Title)"
- "(Chapter X, Page Y)" if page numbers available
- "As explained in [Chapter X]..."

**RESPONSE STRUCTURE:**

For Beginners:
"[Simple explanation with analogy] 🤖
For example, [real-world example].
Want me to explain [related concept]?"

For Intermediate:
"[Technical explanation with context]
This relates to [other concept] because [connection].
The textbook explains this in [Chapter X: Topic].
Would you like more details on [aspect]?"

For Advanced:
"[Technical deep-dive with formulas/algorithms]
Mathematical formulation: [equations if relevant]
Research implications: [advanced insights]
See Chapter X for implementation details.
Explore further: [related advanced topics]?"

**CRITICAL RULES:**
1. ONLY use information from the provided textbook context
2. If asked about content not in the context, say: "This specific topic isn't covered in the section I have access to. Try asking about [related topic from the book]."
3. Remember the user's level throughout the conversation
4. For short/simple questions, give concise answers regardless of level
5. For clarification requests on specific passages, always quote first, then explain
6. Connect concepts across chapters when relevant
7. Encourage deeper learning with follow-up questions

**EXAMPLE RESPONSES:**

User: "What does the third paragraph in Chapter 3 mean?"
You: "[Quote the paragraph]
This passage explains [concept] in [simpler terms based on level].
Essentially, [core idea].
This connects to [related concept] discussed in Chapter X.
Does this clarify it?"

User: "Explain kinematics"
Beginner: "Kinematics is like understanding how robots move! 🤖 It's about studying the motion - speed, direction, and position - without worrying about what causes the movement. Think of it like watching a dance and describing the moves, but not thinking about the muscles. (Chapter 3: Kinematics and Dynamics)"

Intermediate: "Kinematics deals with the geometry of motion for robotic systems. It involves analyzing position, velocity, and acceleration of robot links without considering the forces that cause motion. This includes forward kinematics (finding end-effector position from joint angles) and inverse kinematics (calculating joint angles for desired position). Chapter 3 covers these fundamentals in detail, showing how transformation matrices describe robot configurations."

Advanced: "Kinematics focuses on the mathematical description of motion using transformation matrices, Denavit-Hartenberg parameters, and differential kinematics via Jacobians. Forward kinematics uses homogeneous transformations T = [R|p] to map joint space q to task space x. Inverse kinematics involves solving x = f(q) for q, often requiring numerical methods like Newton-Raphson due to multiple solutions and singularities. Chapter 3: Kinematics and Dynamics provides the foundational theory and algorithms."

Stay helpful, accurate, and always ground responses in the textbook content!
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
        if not text or not text.strip():
            print("[WARN] Attempted to embed empty or whitespace-only text.")
            return []

        try:
            print(f"[INFO] Generating embedding for text: '{text[:50]}...'")
            response = await self.client.embeddings.create(
                model=EMBEDDING_MODEL_NAME, input=[text]
            )
            embedding = response.data[0].embedding

            if len(embedding) != EXPECTED_EMBEDDING_DIM:
                print(
                    f"[WARN] Expected embedding dimension {EXPECTED_EMBEDDING_DIM}, "
                    f"but got {len(embedding)}."
                )

            print(f"[INFO] Embedding generated successfully. Size: {len(embedding)}")
            return embedding

        except APIError as e:
            print(f"[ERROR] Gemini API error during embedding: {e}")
            traceback.print_exc()
            return []
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred during embedding: {e}")
            traceback.print_exc()
            return []

    async def generate_content(self, prompt: str) -> str:
        """
        Generates content using the Gemini model.

        Args:
            prompt: The complete prompt to send to the model.
        
        Returns:
            The generated text content, or an empty string on error.
        """
        try:
            print("[INFO] Generating content with Gemini model...")
            response = await self.client.chat.completions.create(
                model=GEMINI_MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            print("[INFO] Content generated successfully.")
            return content if content else ""

        except APIError as e:
            print(f"[ERROR] Gemini API error during content generation: {e}")
            traceback.print_exc()
            return "Error: The AI model failed to generate a response."
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred in RAGEngine: {e}")
            traceback.print_exc()
            return "Error: An unexpected error occurred while generating the response."


async def main():
    """Tests the GeminiAgentClient methods."""
    print("\n--- Testing GeminiAgentClient ---")
    client = GeminiAgentClient()

    # --- Test Embedding ---
    print("\n--- Testing Embedding Generation ---")
    query = "What is Sim2Real transfer in robotics?"
    embedding = await client.get_embedding(query)
    if embedding:
        print(f"✓ Embedding for '{query}' successful. Size: {len(embedding)}\n")
    else:
        print(f"✗ Embedding for '{query}' failed.\n")

    # --- Test Content Generation ---
    print("--- Testing Content Generation ---")
    prompt = "Explain the concept of 'Physical AI' in two sentences."
    response = await client.generate_content(prompt)
    if response:
        print(f"✓ Content generation successful. Response:\n---\n{response}\n---\n")
    else:
        print("✗ Content generation failed.\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())