"""
Google Gemini chat integration for RAG system.
Uses Gemini 1.5 Flash for generating answers.
"""

import os
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class GeminiChatService:
    """Service for generating chat responses using Google Gemini."""

    def __init__(self):
        """Initialize Gemini client with API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_answer(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate an answer using Gemini.

        Args:
            system_prompt: System instructions (persona-based)
            user_prompt: User query with context

        Returns:
            Generated answer text
        """
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=800,
                )
            )

            return response.text

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
