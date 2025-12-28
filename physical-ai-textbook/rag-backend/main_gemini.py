"""
FastAPI backend for Physical AI Textbook RAG chatbot - GEMINI VERSION.
Provides /query endpoint for question answering and /embed endpoint for content ingestion.
Uses Google Gemini API instead of OpenAI.
"""

import os
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import QueryRequest, QueryResponse, Source, EmbedRequest, EmbedResponse
from embedding_gemini import GeminiEmbeddingService
from chat_gemini import GeminiChatService
from qdrant_service import QdrantService
from personas import get_system_prompt, build_rag_prompt

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG API (Gemini)",
    description="RESTful API for RAG chatbot using Google Gemini API",
    version="1.0.0-gemini"
)

# CORS configuration for Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with Gemini
embedding_service = GeminiEmbeddingService()
chat_service = GeminiChatService()
qdrant_service = QdrantService()

# Update Qdrant service to use Gemini's embedding dimension (768)
qdrant_service.vector_size = 768

@app.on_event("startup")
async def startup_event():
    """Initialize Qdrant collection on startup."""
    try:
        qdrant_service.initialize_collection()
        logger.info("RAG backend (Gemini) initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check Qdrant connection
        info = qdrant_service.get_collection_info()
        return {
            "status": "healthy",
            "service": "RAG API (Gemini)",
            "qdrant_status": "connected",
            "vectors_count": info["vectors_count"],
            "ai_provider": "Google Gemini"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "RAG API (Gemini)",
            "error": str(e)
        }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Answer user questions using RAG with Gemini.

    Process:
    1. Embed the user's query using Gemini
    2. Search Qdrant for similar chunks
    3. Build prompt with retrieved context
    4. Generate answer using Gemini 1.5 Flash with persona adaptation
    """
    try:
        logger.info(f"Query: '{request.query}' | Persona: {request.persona}")

        # Step 1: Embed the query using Gemini
        query_vector = embedding_service.embed_query(request.query)

        # Step 2: Search for similar chunks
        search_results = qdrant_service.search(
            query_vector=query_vector,
            limit=request.max_chunks,
            score_threshold=0.7
        )

        if not search_results:
            raise HTTPException(
                status_code=404,
                detail="No relevant content found for this query"
            )

        # Step 3: Extract context and build sources
        context_chunks = [result["payload"]["text"] for result in search_results]
        sources = [
            Source(
                chapter_title=result["payload"]["chapter_title"],
                section_title=result["payload"]["section_title"],
                url=result["payload"]["url"],
                relevance_score=result["score"]
            )
            for result in search_results
        ]

        # Step 4: Build prompt with persona and context
        system_prompt = get_system_prompt(request.persona)
        user_prompt = build_rag_prompt(
            persona=request.persona,
            user_query=request.query,
            context_chunks=context_chunks
        )

        # Step 5: Generate answer with Gemini
        answer = chat_service.generate_answer(system_prompt, user_prompt)

        logger.info(f"Generated answer with {len(search_results)} chunks using Gemini")

        return QueryResponse(
            answer=answer,
            sources=sources,
            chunks_retrieved=len(search_results),
            persona_used=request.persona
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed", response_model=EmbedResponse)
async def embed_content(request: EmbedRequest):
    """
    Embed and store chapter content in Qdrant using Gemini.

    Used by the embedding pipeline to ingest textbook content.
    Accepts pre-chunked content with metadata.
    """
    try:
        logger.info(f"Embedding {len(request.chunks)} chunks with Gemini")

        # Generate embeddings for all chunks
        texts = [chunk.text for chunk in request.chunks]
        embeddings = embedding_service.embed_batch(texts)

        # Prepare data for Qdrant
        qdrant_chunks = []
        for i, (chunk, embedding) in enumerate(zip(request.chunks, embeddings)):
            qdrant_chunks.append({
                "id": chunk.chunk_id,
                "vector": embedding,
                "payload": {
                    "text": chunk.text,
                    "chapter_title": chunk.chapter_title,
                    "section_title": chunk.section_title,
                    "url": chunk.url,
                    "module": chunk.module,
                    "chapter_id": chunk.chapter_id
                }
            })

        # Store in Qdrant
        qdrant_service.upsert_chunks(qdrant_chunks)

        logger.info(f"Successfully embedded and stored {len(qdrant_chunks)} chunks with Gemini")

        return EmbedResponse(
            success=True,
            chunks_embedded=len(qdrant_chunks),
            message=f"Embedded {len(qdrant_chunks)} chunks successfully using Gemini"
        )

    except Exception as e:
        logger.error(f"Error embedding content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collection/info")
async def get_collection_info():
    """Get information about the Qdrant collection."""
    try:
        info = qdrant_service.get_collection_info()
        return info
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_gemini:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
