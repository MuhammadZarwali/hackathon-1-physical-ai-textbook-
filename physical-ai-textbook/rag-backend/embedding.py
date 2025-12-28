"""
OpenAI embedding integration for RAG system.
Uses text-embedding-3-large for high-quality 3072-dimensional embeddings.
"""

import os
from typing import List
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating embeddings using OpenAI API."""

    def __init__(self):
        """Initialize OpenAI client with API key from environment."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-3-large"
        self.dimensions = 3072

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed (max ~8000 tokens)

        Returns:
            List of 3072 float values representing the embedding
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        More efficient than calling embed_text multiple times.

        Args:
            texts: List of texts to embed (max 2048 texts per batch)

        Returns:
            List of embeddings, one per input text
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts,
                encoding_format="float"
            )
            # Sort by index to maintain order
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return [item.embedding for item in sorted_data]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise
