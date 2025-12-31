"""Cohere embedding service for RAG system."""
import os
import cohere
from typing import List
import logging

logger = logging.getLogger(__name__)

class CohereEmbeddingService:
    """Generate embeddings using Cohere embed-english-v3.0."""

    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set in environment")
        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"
        self.vector_size = 1024

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed documents for storage in vector database.

        Args:
            texts: List of document texts to embed

        Returns:
            List of embedding vectors (1024 dimensions each)
        """
        if not texts:
            return []

        # Cohere API has batch limits, process in chunks of 96
        batch_size = 96
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embed(
                texts=batch,
                model=self.model,
                input_type="search_document"
            )
            all_embeddings.extend(response.embeddings)

        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query.

        Args:
            query: User's search query

        Returns:
            Embedding vector (1024 dimensions)
        """
        response = self.client.embed(
            texts=[query],
            model=self.model,
            input_type="search_query"
        )
        return response.embeddings[0]
