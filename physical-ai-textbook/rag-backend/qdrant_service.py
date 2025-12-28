"""
Qdrant vector database client for RAG system.
Handles storing and searching chapter embeddings.
"""

import os
import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
import logging

logger = logging.getLogger(__name__)

class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        """Initialize Qdrant client from environment configuration."""
        qdrant_url = os.getenv("QDRANT_URL", ":memory:")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        # Support in-memory mode for local testing without Docker
        if qdrant_url == ":memory:" or qdrant_url == "memory":
            logger.info("Using Qdrant in-memory mode (data will not persist)")
            self.client = QdrantClient(":memory:")
        elif qdrant_api_key:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            self.client = QdrantClient(url=qdrant_url)

        self.collection_name = "textbook_chunks"
        self.vector_size = 768  # Default for Gemini text-embedding-004

    def initialize_collection(self):
        """
        Create the collection if it doesn't exist.
        Safe to call multiple times - won't recreate if exists.
        """
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise

    def upsert_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Insert or update chapter chunks with embeddings.

        Args:
            chunks: List of dicts with keys:
                - id: unique chunk identifier (string, will be converted to UUID)
                - vector: embedding vector (768 dimensions for Gemini)
                - payload: metadata (chapter, section, text, etc.)
        """
        try:
            points = []
            for chunk in chunks:
                # Convert string ID to UUID using namespace UUID5
                # This ensures deterministic UUIDs from the same string ID
                chunk_id = chunk["id"]
                if isinstance(chunk_id, str):
                    # Use UUID5 with a namespace to create deterministic UUIDs
                    chunk_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))
                else:
                    chunk_uuid = str(chunk_id)

                points.append(PointStruct(
                    id=chunk_uuid,
                    vector=chunk["vector"],
                    payload=chunk["payload"]
                ))

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Upserted {len(points)} chunks")
        except Exception as e:
            logger.error(f"Error upserting chunks: {e}")
            raise

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.7,
        filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.

        Args:
            query_vector: Embedding of the user query
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1)
            filter_dict: Optional metadata filters (e.g., {"chapter": "chapter-1"})

        Returns:
            List of matching chunks with scores and metadata
        """
        try:
            search_filter = None
            if filter_dict:
                conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                    for key, value in filter_dict.items()
                ]
                search_filter = Filter(must=conditions)

            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=search_filter
            ).points

            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise

    def delete_collection(self):
        """Delete the entire collection. Use with caution!"""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection (size, vectors, etc.)"""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise
