import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

def get_qdrant_client():
    """Initialize and return Qdrant client"""
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_api_key:
        # Qdrant Cloud with API key
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
    else:
        # Local Qdrant (Docker or self-hosted)
        client = QdrantClient(url=qdrant_url)

    return client

def initialize_collection(client: QdrantClient, collection_name: str = "textbook_chunks"):
    """Create Qdrant collection if it doesn't exist"""
    try:
        client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists")
    except Exception:
        # Collection doesn't exist, create it
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=3072,  # text-embedding-3-large dimension
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created successfully")

if __name__ == "__main__":
    client = get_qdrant_client()
    initialize_collection(client)
