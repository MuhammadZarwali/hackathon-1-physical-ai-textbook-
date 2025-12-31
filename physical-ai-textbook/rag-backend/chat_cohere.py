"""Cohere chat service for grounded response generation."""
import os
import cohere
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CohereChatService:
    """Generate grounded responses using Cohere Command."""

    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set in environment")
        self.client = cohere.Client(api_key)

    def generate_response(
        self,
        query: str,
        chunks: List[Dict],
        persona: Optional[str] = None
    ) -> str:
        """
        Generate a grounded response from retrieved chunks.

        Args:
            query: User's question
            chunks: List of retrieved chunks with text and metadata
            persona: Optional persona for response adaptation

        Returns:
            Generated response text
        """
        if not chunks:
            return "I couldn't find relevant information in the textbook to answer your question."

        # Build documents for RAG
        documents = [
            {
                "title": f"{chunk.get('chapter_title', 'Unknown')} - {chunk.get('section_title', 'Unknown')}",
                "text": chunk.get('text', '')
            }
            for chunk in chunks
        ]

        # Build preamble with persona adaptation
        preamble = self._build_preamble(persona)

        try:
            response = self.client.chat(
                message=query,
                documents=documents,
                model="command-r-08-2024",  # Current supported model
                temperature=0.3,
                preamble=preamble
            )
            return response.text
        except Exception as e:
            logger.error(f"Cohere chat error: {e}")
            raise

    def _build_preamble(self, persona: Optional[str] = None) -> str:
        """Build system preamble with optional persona modifier."""
        base = """You are a helpful assistant for the Physical AI & Humanoid Robotics textbook.

CRITICAL GROUNDING RULES:
1. Answer questions ONLY using the provided context from the textbook documents.
2. If the context doesn't contain enough information, say:
   "I couldn't find information about this topic in the textbook."
3. If asked about topics outside robotics, AI, ROS 2, simulation, or Isaac - decline politely.
4. NEVER make up facts, statistics, dates, or specifics not in the context.
5. NEVER use your general knowledge - only the provided documents.
6. Always cite the source chapter/section when providing information.
7. Be accurate and concise - prefer accuracy over verbosity.
8. If only partially covered, say "The textbook partially covers this..." and explain what IS covered."""

        persona_modifiers = {
            "beginner": "\n\nADAPTATION: Explain concepts from first principles. Avoid jargon. Use simple analogies that relate to everyday experiences.",
            "software_engineer": "\n\nADAPTATION: Use programming analogies. Assume familiarity with code, APIs, and software design patterns. Reference relevant programming concepts.",
            "robotics_student": "\n\nADAPTATION: Assume knowledge of kinematics, control theory, and basic robotics. Focus on AI integration aspects and practical applications.",
            "ai_researcher": "\n\nADAPTATION: Assume deep AI/ML knowledge. Focus on robotics-specific applications, architectures, and research challenges. Use technical terminology."
        }

        if persona and persona in persona_modifiers:
            return base + persona_modifiers[persona]
        return base
