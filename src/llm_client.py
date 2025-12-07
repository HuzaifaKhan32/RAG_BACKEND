import os
import traceback
from dotenv import load_dotenv
from openai import AsyncOpenAI, APIError

# Load environment variables
load_dotenv()

# --- Gemini Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found in environment.")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/"
GEMINI_MODEL_NAME = "models/gemini-2.5-flash" 
EMBEDDING_MODEL_NAME = "models/text-embedding-004"
EXPECTED_EMBEDDING_DIM = 768


class GeminiAgentClient:
    """A client for interacting with Google Gemini models via an OpenAI-compatible interface."""

    def __init__(self, timeout=60):
        """Initializes the asynchronous OpenAI client to point to Gemini's endpoint."""
        print("[INFO] Initializing GeminiAgentClient...")
        self.client = AsyncOpenAI(
            api_key=GEMINI_API_KEY,
            base_url=GEMINI_BASE_URL,
            timeout=timeout,
        )
        print(f"[INFO] GeminiAgentClient initialized for model: {GEMINI_MODEL_NAME}")

    async def get_embedding(self, text: str) -> list[float]:
        """
        Generates an embedding for the given text.

        Args:
            text: The text to embed.
        
        Returns:
            A list of floats representing the embedding, or an empty list on error.
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
            print(f"[ERROR] An unexpected error occurred during content generation: {e}")
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