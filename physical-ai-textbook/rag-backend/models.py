from pydantic import BaseModel, Field
from typing import Optional, List

class QueryRequest(BaseModel):
    """Request model for RAG query endpoint"""
    query: str = Field(..., max_length=500, description="User's question or search query")
    selected_text: Optional[str] = Field(None, description="Optional user-highlighted text passage for context")
    persona: str = Field(default="software_engineer", description="User persona for personalized responses")
    context_mode: str = Field(default="full_book", description="Scope of context for retrieval")
    current_chapter: Optional[str] = Field(None, description="Optional chapter ID for context-aware retrieval")
    max_chunks: int = Field(default=5, ge=1, le=10, description="Maximum number of chunks to retrieve")
    include_citations: bool = Field(default=True, description="Whether to include source citations in response")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is ROS 2?",
                "persona": "beginner",
                "max_chunks": 5
            }
        }


class Source(BaseModel):
    """Source citation for RAG response"""
    chapter_title: str = Field(..., description="Title of the source chapter")
    section_title: str = Field(..., description="Title of the source section")
    url: str = Field(..., description="URL to the source content")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score from vector search")


class QueryResponse(BaseModel):
    """Response model for RAG query endpoint"""
    answer: str = Field(..., description="AI-generated answer based on textbook content")
    sources: List[Source] = Field(default=[], description="List of source chunks used to generate the answer")
    chunks_retrieved: int = Field(..., description="Number of chunks retrieved from vector database")
    persona_used: str = Field(..., description="Persona applied for response generation")
    processing_time_ms: Optional[int] = Field(None, description="Time taken to process the query (milliseconds)")


class ChunkData(BaseModel):
    """Individual chunk to be embedded"""
    chunk_id: str = Field(..., description="Unique identifier for this chunk")
    text: str = Field(..., description="Chunk text content")
    chapter_title: str = Field(..., description="Chapter title")
    section_title: str = Field(..., description="Section title")
    url: str = Field(..., description="URL to this section")
    module: str = Field(..., description="Module identifier")
    chapter_id: str = Field(..., description="Chapter identifier")


class EmbedRequest(BaseModel):
    """Request model for content embedding endpoint"""
    chunks: List[ChunkData] = Field(..., description="List of chunks to embed")

    class Config:
        json_schema_extra = {
            "example": {
                "chunks": [
                    {
                        "chunk_id": "ch1-sec1",
                        "text": "ROS 2 is a middleware framework...",
                        "chapter_title": "Chapter 1: Introduction to ROS 2",
                        "section_title": "What is ROS 2?",
                        "url": "/module-1-ros2/chapter-1#what-is-ros2",
                        "module": "module-1-ros2",
                        "chapter_id": "chapter-1-introduction-to-ros2"
                    }
                ]
            }
        }


class EmbedResponse(BaseModel):
    """Response model for embedding endpoint"""
    success: bool = Field(..., description="Whether embedding was successful")
    chunks_embedded: int = Field(..., description="Number of chunks embedded")
    message: str = Field(..., description="Status message")
