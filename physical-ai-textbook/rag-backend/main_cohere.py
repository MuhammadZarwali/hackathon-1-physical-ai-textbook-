"""FastAPI RAG backend with Cohere integration."""
import os
import logging
import hashlib
import json
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import services
from embedding_cohere import CohereEmbeddingService
from chat_cohere import CohereChatService
from qdrant_service import QdrantService

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Physical AI Textbook RAG Chatbot with Cohere",
    version="1.0.0"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
embedding_service = CohereEmbeddingService()
chat_service = CohereChatService()
qdrant_service = QdrantService()
qdrant_service.vector_size = 1024  # Cohere embed-english-v3.0

# Response cache (in-memory, LRU)
# Stores up to 100 most recent query responses
response_cache: Dict[str, Dict[str, Any]] = {}
CACHE_MAX_SIZE = 100

def get_cache_key(question: str, mode: str, persona: Optional[str]) -> str:
    """Generate a cache key from query parameters."""
    # Normalize question (lowercase, strip whitespace)
    normalized = question.lower().strip()
    # Create cache key: hash of (question, mode, persona)
    cache_data = f"{normalized}|{mode}|{persona or 'none'}"
    return hashlib.md5(cache_data.encode()).hexdigest()

def get_from_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    """Retrieve response from cache if it exists."""
    return response_cache.get(cache_key)

def save_to_cache(cache_key: str, response_data: Dict[str, Any]):
    """Save response to cache with LRU eviction."""
    global response_cache
    # If cache is full, remove oldest entry (simple FIFO for now)
    if len(response_cache) >= CACHE_MAX_SIZE:
        # Remove first (oldest) key
        oldest_key = next(iter(response_cache))
        del response_cache[oldest_key]
        logger.info(f"Cache full, evicted oldest entry")

    response_cache[cache_key] = response_data
    logger.info(f"Cached response for key: {cache_key[:8]}...")


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for RAG queries."""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")
    mode: str = Field(default="global", pattern="^(global|selected)$", description="Query mode")
    selected_text: Optional[str] = Field(None, min_length=10, max_length=5000, description="Selected text for context")
    persona: Optional[str] = Field(None, description="User persona for response adaptation")


class SourceReference(BaseModel):
    """Source reference for a retrieved chunk."""
    chapter_title: str
    section_title: str
    module: str
    url: str
    relevance_score: float


class QueryResponse(BaseModel):
    """Response model for RAG queries."""
    answer: str
    sources: List[SourceReference]
    confidence: str
    mode_used: str
    chunks_retrieved: int


# Endpoints
@app.post("/query", response_model=QueryResponse)
async def query_textbook(request: QueryRequest):
    """
    Query the textbook using RAG.

    - **question**: The user's question about the textbook
    - **mode**: "global" for full book search, "selected" for context-specific
    - **selected_text**: Required if mode is "selected"
    - **persona**: Optional persona (beginner, software_engineer, robotics_student, ai_researcher)
    """
    # Check if it's a greeting - skip retrieval
    greetings = ["hi", "hello", "hey", "thanks", "thank you", "bye", "goodbye"]
    query_lower = request.question.lower().strip()
    is_greeting = any(greeting in query_lower for greeting in greetings)

    if is_greeting:
        # Skip RAG for greetings - respond directly
        logger.info(f"Greeting detected: {request.question}")
        answer = "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant. How can I help you today?"

        return QueryResponse(
            answer=answer,
            sources=[],
            confidence="high",
            mode_used="direct",
            chunks_retrieved=0
        )

    logger.info(f"Query received: {request.question[:50]}... mode={request.mode}")

    # Check cache first
    cache_key = get_cache_key(request.question, request.mode, request.persona)
    cached_response = get_from_cache(cache_key)

    if cached_response:
        logger.info(f"Cache HIT for key: {cache_key[:8]}... (skipping API calls)")
        return QueryResponse(**cached_response)

    logger.info(f"Cache MISS for key: {cache_key[:8]}... (executing RAG pipeline)")

    # Validate selected mode
    if request.mode == "selected" and not request.selected_text:
        raise HTTPException(
            status_code=400,
            detail="selected_text is required when mode is 'selected'"
        )

    try:
        # Embed query
        query_vector = embedding_service.embed_query(request.question)

        # Search Qdrant based on mode
        if request.mode == "global":
            results = qdrant_service.search(
                query_vector,
                limit=5,
                score_threshold=0.5
            )
        else:
            # Selected-text mode: combine query with selected text for embedding
            combined_query = f"{request.question}\n\nContext: {request.selected_text[:500]}"
            combined_vector = embedding_service.embed_query(combined_query)
            results = qdrant_service.search(
                combined_vector,
                limit=3,
                score_threshold=0.6  # Higher threshold for selected mode
            )
            # Fallback to global search if selected mode returns no results
            if not results:
                logger.info("Selected mode fallback to global search")
                results = qdrant_service.search(
                    query_vector,
                    limit=3,
                    score_threshold=0.5
                )

        # Handle no results
        if not results:
            no_results_response = QueryResponse(
                answer="I couldn't find information about this topic in the textbook. The textbook covers ROS 2, simulation with Gazebo, NVIDIA Isaac, and Vision-Language-Action models. Try rephrasing your question or asking about one of these topics.",
                sources=[],
                confidence="none",
                mode_used=request.mode,
                chunks_retrieved=0
            )
            # Cache "not found" responses too
            save_to_cache(cache_key, no_results_response.model_dump())
            return no_results_response

        # Prepare chunks for generation
        chunks = [
            {
                "text": r["payload"].get("text", ""),
                "chapter_title": r["payload"].get("chapter_title", "Unknown"),
                "section_title": r["payload"].get("section_title", "Unknown"),
                "module": r["payload"].get("module", "Unknown"),
                "url": r["payload"].get("url", "/"),
                "score": r["score"]
            }
            for r in results
        ]

        # Generate response
        answer = chat_service.generate_response(
            request.question,
            chunks,
            request.persona
        )

        # Build sources
        sources = [
            SourceReference(
                chapter_title=c["chapter_title"],
                section_title=c["section_title"],
                module=c["module"],
                url=c["url"],
                relevance_score=round(c["score"], 3)
            )
            for c in chunks
        ]

        # Determine confidence
        max_score = max(c["score"] for c in chunks)
        if max_score >= 0.85 and len(chunks) >= 2:
            confidence = "high"
        elif max_score >= 0.70:
            confidence = "medium"
        elif max_score >= 0.50:
            confidence = "low"
        else:
            confidence = "none"

        # Add uncertainty indicator for low confidence responses
        if confidence == "low":
            answer = f"**Note: The textbook has limited coverage of this specific topic.**\n\n{answer}"

        logger.info(f"Response generated: {len(chunks)} chunks, confidence={confidence}")

        # Build response object
        response = QueryResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            mode_used=request.mode,
            chunks_retrieved=len(chunks)
        )

        # Save to cache for future requests
        save_to_cache(cache_key, response.model_dump())

        return response

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your query: {str(e)}"
        )


@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics."""
    return {
        "cache_size": len(response_cache),
        "cache_max_size": CACHE_MAX_SIZE,
        "cache_usage_percent": round((len(response_cache) / CACHE_MAX_SIZE) * 100, 2),
        "cached_queries": list(response_cache.keys())[:10]  # Show first 10 cache keys
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        # Verify Qdrant connection
        info = qdrant_service.get_collection_info()
        qdrant_status = "connected" if info.get("status") == "green" else "degraded"
    except Exception:
        qdrant_status = "disconnected"

    return {
        "status": "healthy" if qdrant_status == "connected" else "degraded",
        "service": "rag-chatbot",
        "cohere": "available",
        "qdrant": qdrant_status,
        "chunks_indexed": info.get("points_count", 0) if qdrant_status == "connected" else 0
    }


@app.get("/collection/info")
async def collection_info():
    """Get collection statistics."""
    try:
        info = qdrant_service.get_collection_info()
        return {
            "collection_name": "textbook_chunks",
            "points_count": info.get("points_count", 0),
            "status": info.get("status", "unknown"),
            "embedding_model": "cohere-embed-english-v3.0",
            "vector_dimensions": 1024
        }
    except Exception as e:
        logger.error(f"Collection info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # Initialize collection if needed
    try:
        qdrant_service.initialize_collection()
    except Exception as e:
        logger.warning(f"Collection initialization: {e}")

    # Start server on port 8001 to avoid conflict with legacy Gemini API
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8001))
    )
