"""OpenAI Agent for RAG Chatbot - uses OpenAI Agents SDK with OpenRouter API.

This agent provides:
- Tool-based retrieval from Qdrant (textbook content)
- Conversation memory for follow-up questions
- Structured responses with source attribution
- Grounding (only answers from textbook)
"""

import os
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# OpenAI Agents SDK
from agents import Agent, Runner
from agents.handoffs import Handoff

# Existing services
from qdrant_service import QdrantService
from embedding_cohere import CohereEmbeddingService

# Load environment
load_dotenv()

# OpenRouter configuration (compatible with OpenAI SDK)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_MODEL = "openai/gpt-4o-mini"  # Use OpenAI via OpenRouter


def search_textbook(query: str, limit: int = 5) -> List[Dict]:
    """
    Search textbook using Qdrant retrieval.

    Args:
        query: User's question
        limit: Max chunks to retrieve

    Returns:
        List of retrieved chunks with metadata
    """
    qdrant = QdrantService()
    embedding = CohereEmbeddingService()

    try:
        # Embed query
        query_vector = embedding.embed_query(query)

        # Search Qdrant
        results = qdrant.search(query_vector, limit=limit, score_threshold=0.5)

        # Format results for agent
        chunks = []
        for r in results:
            payload = r["payload"]
            chunks.append({
                "id": payload.get("chunk_id", ""),
                "content": payload.get("text", ""),
                "chapter_title": payload.get("chapter_title", "Unknown"),
                "section_title": payload.get("section_title", "Unknown"),
                "module": payload.get("module", "Unknown"),
                "url": payload.get("url", "/"),
                "score": r["score"]
            })

        return chunks
    except Exception as e:
        print(f"Search error: {e}")
        return []


def build_retrieved_context(chunks: List[Dict]) -> str:
    """
    Build context string from retrieved chunks.

    Args:
        chunks: List of retrieved chunks

    Returns:
        Formatted context string
    """
    if not chunks:
        return "No relevant information found in the textbook."

    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source {i+1}: {chunk['chapter_title']} - {chunk['section_title']}]\n"
            f"{chunk['content'][:300]}...\n"
        )

    return "\n".join(context_parts)


# Define the search tool for the agent
async def search_textbook_tool(query: str) -> str:
    """
    Tool function for the agent to search textbook.

    Args:
        query: The user's question

    Returns:
        Retrieved textbook content with sources
    """
    print(f"[TOOL] Searching textbook for: {query}")

    # Search Qdrant
    chunks = search_textbook(query)

    if not chunks:
        return "I couldn't find relevant information in the textbook. The textbook covers ROS 2, simulation with Gazebo, NVIDIA Isaac, and Vision-Language-Action models."

    # Build response with sources
    response = build_retrieved_context(chunks)

    # Add source list at the end
    sources = "\n\nSources:\n"
    for i, chunk in enumerate(chunks[:3]):  # Limit to top 3 sources
        sources += f"{i+1}. {chunk['url']} - {chunk['chapter_title']}: {chunk['section_title']}\n"

    return response + sources


# Create the agent with retrieval tool
def create_agent() -> Agent:
    """
    Create an OpenAI Agent equipped with textbook retrieval.
    """
    # Define the search tool
    textbook_search_tool = {
        "type": "function",
        "function": {
            "name": "search_textbook",
            "description": "Search the Physical AI & Humanoid Robotics textbook to answer questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's question about the textbook"
                    }
                },
                "required": ["query"]
            }
        }
    }

    # System instructions
    instructions = """You are a helpful assistant for the Physical AI & Humanoid Robotics textbook.

IMPORTANT RULES:
1. Always use the search_textbook tool to answer questions about the textbook.
2. Only use information retrieved from the textbook. Do NOT use your general knowledge.
3. If the textbook doesn't contain relevant information, say so clearly.
4. Always cite sources (chapter and section) when providing information.
5. Be accurate and concise - prefer accuracy over verbosity.
6. Never make up facts or information not in the retrieved context.
7. For questions about topics outside robotics, AI, ROS 2, simulation, Isaac, or VLA - politely decline and suggest the user check the textbook topics.
8. If you're asked about specific code or implementation details that aren't in the textbook, admit that limitation.

When a user asks a question:
1. Use the search_textbook tool with their exact question.
2. Review the retrieved content.
3. Answer using ONLY the retrieved information.
4. List the sources at the end of your response.
"""

    # Create agent
    agent = Agent(
        name="Textbook Assistant",
        instructions=instructions,
        tools=[textbook_search_tool],
        model=OPENAI_MODEL
    )

    return agent


async def run_agent_with_history() -> None:
    """
    Run the agent with conversation history.
    """
    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set in .env")
        print("Please add: OPENROUTER_API_KEY=your_key_here")
        print("Get key from: https://openrouter.ai/keys")
        return

    print("=" * 60)
    print("OpenAI Agent for RAG Chatbot")
    print("=" * 60)
    print(f"Model: {OPENAI_MODEL}")
    print(f"Base URL: {OPENROUTER_BASE_URL}")
    print()

    # Create agent
    agent = create_agent()

    # Conversation history (simple in-memory)
    conversation_history: List[Dict[str, str]] = []

    # Run with Runner for better control
    print("\n[SYSTEM] Agent initialized with retrieval capability")
    print("[SYSTEM] Type 'quit' or 'exit' to end\n")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Add to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Keep last 5 exchanges for context
        recent_history = conversation_history[-10:]

        # Create Handoff for history
        history_handoff = Handoff(
            target_agent=agent,
            instructions="Use the conversation history for context",
            metadata={"history": recent_history}
        )

        try:
            # Run agent
            result = Runner.run_sync(
                starting_agent=agent,
                input=user_input,
                handoffs=[history_handoff]
            )

            print(f"\n[ASSISTANT] {result.final_output}")
            print("-" * 60)

            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": result.final_output})

            # Show tool usage
            if hasattr(result, 'agents') and result.agents:
                for agent_output in result.agents:
                    if hasattr(agent_output, 'outputs'):
                        for output in agent_output.outputs:
                            if hasattr(output, 'tool_calls'):
                                for tool_call in output.tool_calls:
                                    print(f"[TOOL CALL] {tool_call.tool.name}: {tool_call.function.arguments}")

        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            print("Please try again.")


if __name__ == "__main__":
    asyncio.run(run_agent_with_history())
