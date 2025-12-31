# Quickstart: RAG Chatbot Integration

**Feature**: 005-rag-chatbot-integration
**Date**: 2025-12-29

---

## Overview

This guide provides step-by-step instructions to implement the RAG chatbot for the Physical AI textbook using Cohere embeddings and Qdrant Cloud.

---

## Prerequisites

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Cohere API key (get at https://dashboard.cohere.com/)
- [ ] Qdrant Cloud cluster configured (already set up)
- [ ] Docusaurus site deployed

---

## Step 1: Configure Environment

Create/update `.env` in `physical-ai-textbook/rag-backend/`:

```env
# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud Configuration (already configured)
QDRANT_URL=https://60a00bf7-e8cc-4752-a7c1-c95f9927d4ce.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://hackathon-1-physical-ai-textbook-phi.vercel.app
```

---

## Step 2: Install Dependencies

```bash
cd physical-ai-textbook/rag-backend
pip install cohere qdrant-client fastapi uvicorn python-dotenv
```

Update `requirements.txt`:
```
fastapi>=0.100.0
uvicorn>=0.23.0
python-dotenv>=1.0.0
cohere>=4.0.0
qdrant-client>=1.7.0
pydantic>=2.0.0
```

---

## Step 3: Create Cohere Embedding Service

Create `embedding_cohere.py`:

```python
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
            raise ValueError("COHERE_API_KEY not set")
        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"
        self.vector_size = 1024

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents for storage."""
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document"
        )
        return response.embeddings

    def embed_query(self, query: str) -> List[float]:
        """Embed a search query."""
        response = self.client.embed(
            texts=[query],
            model=self.model,
            input_type="search_query"
        )
        return response.embeddings[0]
```

---

## Step 4: Create Cohere Chat Service

Create `chat_cohere.py`:

```python
"""Cohere chat service for grounded response generation."""
import os
import cohere
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class CohereChatService:
    """Generate grounded responses using Cohere Command."""

    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set")
        self.client = cohere.Client(api_key)

    def generate_response(
        self,
        query: str,
        chunks: List[Dict],
        persona: str = None
    ) -> str:
        """Generate a grounded response from retrieved chunks."""

        # Build documents for RAG
        documents = [
            {
                "title": f"{chunk['chapter_title']} - {chunk['section_title']}",
                "text": chunk['text']
            }
            for chunk in chunks
        ]

        # Build preamble with persona adaptation
        preamble = self._build_preamble(persona)

        response = self.client.chat(
            message=query,
            documents=documents,
            model="command",
            temperature=0.3,
            preamble=preamble
        )

        return response.text

    def _build_preamble(self, persona: str = None) -> str:
        """Build system preamble with optional persona."""
        base = """You are a helpful assistant for the Physical AI & Humanoid Robotics textbook.
Answer questions ONLY using the provided context from the textbook.
If the context doesn't contain enough information to answer, say:
"I couldn't find information about this topic in the textbook."
Always cite the source chapter and section at the end of your response.
Be accurate and concise - prefer accuracy over verbosity."""

        persona_modifiers = {
            "beginner": "\nExplain concepts from first principles. Avoid jargon. Use simple analogies.",
            "software_engineer": "\nUse programming analogies. Assume familiarity with code and APIs.",
            "robotics_student": "\nAssume knowledge of kinematics and control theory. Focus on AI aspects.",
            "ai_researcher": "\nAssume deep AI/ML knowledge. Focus on robotics-specific applications."
        }

        if persona and persona in persona_modifiers:
            return base + persona_modifiers[persona]
        return base
```

---

## Step 5: Create Main API with Cohere

Create `main_cohere.py`:

```python
"""FastAPI RAG backend with Cohere integration."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from embedding_cohere import CohereEmbeddingService
from chat_cohere import CohereChatService
from qdrant_service import QdrantService

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
embedding_service = CohereEmbeddingService()
chat_service = CohereChatService()
qdrant_service = QdrantService()
qdrant_service.vector_size = 1024  # Cohere embed-english-v3.0


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    mode: str = Field(default="global", pattern="^(global|selected)$")
    selected_text: Optional[str] = Field(None, min_length=10, max_length=5000)
    persona: Optional[str] = None


class SourceReference(BaseModel):
    chapter_title: str
    section_title: str
    module: str
    url: str
    relevance_score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceReference]
    confidence: str
    mode_used: str
    chunks_retrieved: int


@app.post("/query", response_model=QueryResponse)
async def query_textbook(request: QueryRequest):
    """Query the textbook using RAG."""

    # Validate selected mode
    if request.mode == "selected" and not request.selected_text:
        raise HTTPException(400, "selected_text required for selected mode")

    # Embed query
    query_vector = embedding_service.embed_query(request.question)

    # Search Qdrant
    if request.mode == "global":
        results = qdrant_service.search(query_vector, limit=5, score_threshold=0.5)
    else:
        # For selected mode, embed the selected text and compare
        # Simplified: search but filter conceptually
        results = qdrant_service.search(query_vector, limit=3, score_threshold=0.5)

    if not results:
        return QueryResponse(
            answer="I couldn't find information about this topic in the textbook. Try rephrasing your question.",
            sources=[],
            confidence="none",
            mode_used=request.mode,
            chunks_retrieved=0
        )

    # Prepare chunks for generation
    chunks = [
        {
            "text": r["payload"]["text"],
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
            relevance_score=c["score"]
        )
        for c in chunks
    ]

    # Determine confidence
    max_score = max(c["score"] for c in chunks)
    if max_score >= 0.85 and len(chunks) >= 2:
        confidence = "high"
    elif max_score >= 0.70:
        confidence = "medium"
    else:
        confidence = "low"

    return QueryResponse(
        answer=answer,
        sources=sources,
        confidence=confidence,
        mode_used=request.mode,
        chunks_retrieved=len(chunks)
    )


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy", "cohere": "available", "qdrant": "connected"}


@app.get("/collection/info")
async def collection_info():
    """Get collection statistics."""
    info = qdrant_service.get_collection_info()
    return {"collection_name": "textbook_chunks", **info}


if __name__ == "__main__":
    import uvicorn
    qdrant_service.initialize_collection()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Step 6: Embed Textbook Content

Create `embed_chapters_cohere.py`:

```python
"""Embed all textbook chapters using Cohere."""
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from embedding_cohere import CohereEmbeddingService
from qdrant_service import QdrantService

def parse_frontmatter(content):
    """Extract YAML frontmatter."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}
    metadata = {}
    for line in match.group(1).split('\n'):
        if ':' in line and not line.strip().startswith('-'):
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip('"\'')
    return metadata

def chunk_by_h2(content, metadata):
    """Chunk by H2 sections."""
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    h2_sections = re.split(r'\n## ', content)

    chunks = []
    chapter_title = metadata.get('title', 'Untitled')
    chapter_id = metadata.get('chapter_id', 'unknown')
    module = metadata.get('module', 'unknown')

    for i, section in enumerate(h2_sections[1:], 1):
        lines = section.split('\n')
        h2_title = lines[0].strip()
        section_content = '\n'.join(lines[1:]).strip()

        if len(section_content) < 100:
            continue

        chunks.append({
            'chunk_id': f"{chapter_id}-section-{i}",
            'text': f"## {h2_title}\n\n{section_content}",
            'chapter_title': chapter_title,
            'section_title': h2_title,
            'module': module,
            'url': f"/docs/{module}/{chapter_id}#{h2_title.lower().replace(' ', '-')}"
        })

    return chunks

def main():
    embedding_service = CohereEmbeddingService()
    qdrant_service = QdrantService()
    qdrant_service.vector_size = 1024
    qdrant_service.initialize_collection()

    base_path = Path("physical-ai-textbook/docs/docs")
    modules = [
        "module-1-ros2",
        "module-2-simulation",
        "module-3-isaac-ai-brain",
        "module-4-vision-language-action"
    ]

    all_chunks = []
    for module in modules:
        module_path = base_path / module
        for chapter_file in module_path.glob("chapter-*.md"):
            print(f"Processing: {chapter_file.name}")
            content = chapter_file.read_text(encoding='utf-8')
            metadata = parse_frontmatter(content)
            chunks = chunk_by_h2(content, metadata)
            all_chunks.extend(chunks)
            print(f"  Created {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print("Generating embeddings...")

    texts = [c['text'] for c in all_chunks]
    embeddings = embedding_service.embed_documents(texts)

    print("Storing in Qdrant...")
    points = [
        {
            "id": chunk['chunk_id'],
            "vector": embeddings[i],
            "payload": chunk
        }
        for i, chunk in enumerate(all_chunks)
    ]

    qdrant_service.upsert_chunks(points)
    print(f"Done! Embedded {len(points)} chunks.")

if __name__ == "__main__":
    main()
```

---

## Step 7: Run and Test

```bash
# 1. Embed content (one-time)
python embed_chapters_cohere.py

# 2. Start API server
python main_cohere.py

# 3. Test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2?", "mode": "global"}'
```

---

## Step 8: Frontend Integration

See frontend implementation in `/sp.tasks` output for:
- React ChatWidget component
- Docusaurus theme integration
- Selected-text mode implementation

---

## Validation Checklist

- [ ] Cohere API key configured
- [ ] Qdrant Cloud connection working
- [ ] All chapters embedded (~100 chunks)
- [ ] `/query` endpoint returns grounded responses
- [ ] Source attribution included in responses
- [ ] Out-of-scope questions handled correctly
- [ ] Response time < 5 seconds

---

## Troubleshooting

### "COHERE_API_KEY not set"
Ensure `.env` file exists with valid Cohere API key.

### "Connection refused" to Qdrant
Verify Qdrant Cloud URL and API key in `.env`.

### Poor retrieval quality
- Lower `score_threshold` (try 0.5)
- Check chunk quality and size
- Verify embeddings are 1024 dimensions

### Slow responses
- Check Cohere API latency
- Reduce `limit` parameter
- Consider caching common queries
