import os
import traceback
from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.exceptions import ApiException
from dotenv import load_dotenv

load_dotenv()


class VectorDBClient:
    """Asynchronous client for interacting with Qdrant vector database."""

    def __init__(self, timeout=30):
        """Initialize Qdrant client."""
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv(
            "QDRANT_COLLECTION_NAME", "rag_chatbot_collection"
        )

        if not self.url:
            raise ValueError("QDRANT_URL must be set in environment")

        self.client = AsyncQdrantClient(
            url=self.url, api_key=self.api_key, timeout=timeout
        )
        print(f"[INFO] AsyncQdrantClient initialized for URL: {self.url}")
        print(f"[INFO] Using collection: {self.collection_name}")

    async def search_vectors(self, query_vector: list, limit: int = 5):
        """
        Search Qdrant for similar vectors asynchronously.
        
        Args:
            query_vector: The embedding vector to search for.
            limit: Number of results to return.
        
        Returns:
            A list of ScoredPoint objects, or an empty list on error.
        """
        if not query_vector:
            print("[ERROR] Query vector is empty.")
            return []

        try:
            print(
                f"[INFO] Searching Qdrant with {len(query_vector)}-dim vector..."
            )
            
            # The 'search' method is the correct one for vector similarity search.
            # It returns a list of ScoredPoint objects.
            search_results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,  # Ensure payload is returned for citations
            )
            
            print(f"[INFO] Found {len(search_results)} results from Qdrant.")
            return search_results

        except ApiException as e:
            print(f"[ERROR] Qdrant search failed due to a client-side error: {e}")
            traceback.print_exc()
            return []
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred during Qdrant search: {e}")
            traceback.print_exc()
            return []

    async def get_collection_info(self):
        """Get information about the collection asynchronously."""
        try:
            info = await self.client.get_collection(
                collection_name=self.collection_name
            )
            return info
        except Exception as e:
            print(f"[ERROR] Failed to get collection info: {e}")
            return None

async def main():
    """Test the VectorDBClient."""
    try:
        client = VectorDBClient()
        print("✓ AsyncQdrantClient initialized successfully")

        info = await client.get_collection_info()
        if info:
            print(f"✓ Collection info: {info.vectors_config}")
        else:
            print("✗ Could not get collection info")

    except Exception as e:
        print(f"✗ Error during client test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())