# Research: RAG Chatbot Integration

**Feature**: 005-rag-chatbot-integration
**Date**: 2025-12-29
**Purpose**: Document technology decisions and best practices for RAG implementation

---

## 1. Cohere Embeddings

### Decision
Use Cohere `embed-english-v3.0` model for generating text embeddings.

### Rationale
- User explicitly specified Cohere as the embedding provider
- embed-english-v3.0 produces 1024-dimensional vectors optimized for semantic search
- High-quality retrieval performance for English technical content
- Supports both document and query embedding with input_type parameter

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| OpenAI ada-002 | User specified Cohere |
| Gemini text-embedding-004 | User specified Cohere; would require migration from existing setup |
| Local models (sentence-transformers) | Lower quality for technical content, requires GPU |

### Implementation Notes
```python
import cohere
co = cohere.Client(api_key)

# For documents
doc_embeddings = co.embed(
    texts=chunks,
    model="embed-english-v3.0",
    input_type="search_document"
).embeddings

# For queries
query_embedding = co.embed(
    texts=[query],
    model="embed-english-v3.0",
    input_type="search_query"
).embeddings[0]
```

---

## 2. Qdrant Cloud Vector Storage

### Decision
Use Qdrant Cloud (free tier) for vector storage and similarity search.

### Rationale
- User explicitly specified Qdrant Cloud
- Free tier supports up to 1GB storage (sufficient for ~100 chunks)
- Native Python client with async support
- Efficient cosine similarity search
- Metadata filtering capabilities

### Configuration
- **Cluster URL**: `https://60a00bf7-e8cc-4752-a7c1-c95f9927d4ce.us-east4-0.gcp.cloud.qdrant.io:6333`
- **Collection**: `textbook_chunks`
- **Vector Size**: 1024 (Cohere embed-english-v3.0)
- **Distance Metric**: Cosine

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Pinecone | User specified Qdrant |
| ChromaDB | Cloud deployment complexity |
| Weaviate | User specified Qdrant |

---

## 3. Response Generation

### Decision
Use Cohere Command model for grounded response generation.

### Rationale
- Consistent provider (same as embeddings)
- Command model supports RAG-style prompting
- Built-in citation support
- No need to manage multiple API keys

### Grounding Strategy
```python
system_prompt = """You are a helpful assistant for the Physical AI textbook.
Answer questions ONLY using the provided context from the textbook.
If the context doesn't contain enough information to answer, say:
"I couldn't find information about this topic in the textbook."
Always cite the source chapter and section at the end of your response.
Be accurate and concise - prefer accuracy over verbosity."""

response = co.chat(
    message=user_query,
    documents=[{"text": chunk.text, "title": chunk.chapter_title} for chunk in retrieved_chunks],
    model="command",
    temperature=0.3  # Low temperature for factual responses
)
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| GPT-4 | Additional API key, higher cost |
| Gemini | Already have Cohere for embeddings |
| Claude | Additional API key management |

---

## 4. Semantic Chunking Strategy

### Decision
Chunk by H2 sections with 200-500 word targets, preserving metadata.

### Rationale
- Aligns with Constitution AI-Native Design requirements
- H2 sections typically represent complete semantic units
- 200-500 words provides sufficient context for retrieval
- Metadata enables source attribution

### Chunk Structure
```python
{
    "chunk_id": "chapter-1-ros2-section-3",
    "text": "## Section Title\n\nContent...",
    "chapter_title": "Introduction to ROS 2",
    "section_title": "ROS 2 Architecture",
    "module": "module-1-ros2",
    "url": "/docs/module-1-ros2/chapter-1-introduction-to-ros2#ros-2-architecture"
}
```

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Fixed-size (500 tokens) | Breaks semantic boundaries |
| Paragraph-level | Too small, loses context |
| Chapter-level | Too large, poor retrieval precision |

---

## 5. Query Mode Implementation

### Decision
Support Global Mode and Selected-Text Mode via single endpoint with mode parameter.

### Rationale
- Unified API simplifies frontend integration
- Mode parameter clearly indicates intent
- Selected-Text mode doesn't require separate embedding - uses inline search

### Implementation Pattern
```python
@app.post("/query")
async def query(request: QueryRequest):
    if request.mode == "global":
        # Search entire Qdrant collection
        results = qdrant.search(embed(request.question), limit=5)
    elif request.mode == "selected":
        # Embed selected text, search against it directly
        # Or: filter Qdrant by text similarity to selection
        results = search_in_text(request.question, request.selected_text)

    return generate_response(request.question, results)
```

---

## 6. Frontend Integration Pattern

### Decision
React component embedded via Docusaurus theme customization.

### Rationale
- Docusaurus supports custom React components
- Theme Root wrapper enables global injection
- Minimal bundle impact with lazy loading
- Preserves reading experience with collapsible panel

### Integration Point
```tsx
// src/theme/Root.tsx
import ChatWidget from '@site/src/components/ChatWidget';

export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
```

### Bundle Optimization
- Lazy load chat panel on first interaction
- Minimize dependencies (no heavy UI libraries)
- Use CSS modules for styling
- Target < 100KB addition

---

## 7. Security Considerations

### Decision
All API keys server-side only; CORS restricted to known origins.

### Implementation
- Cohere API key in backend `.env` only
- Qdrant API key in backend `.env` only
- Frontend calls backend API (no direct Cohere/Qdrant calls)
- CORS allows: localhost:3000, vercel.app domain

### Rate Limiting
- Consider implementing rate limiting if abuse detected
- Start without, monitor usage patterns

---

## 8. Error Handling Strategy

### Decision
Graceful degradation with user-friendly messages.

### Error Categories
| Error | User Message |
|-------|--------------|
| Cohere API failure | "The chatbot is temporarily unavailable. Please try again." |
| Qdrant connection error | "Unable to search the textbook. Please try again." |
| No results found | "I couldn't find information about this topic in the textbook." |
| Low confidence | "I found some related content, but I'm not confident it answers your question." |
| Input validation | "Please enter a valid question." |

---

## Summary of Decisions

| Component | Choice | Key Reason |
|-----------|--------|------------|
| Embeddings | Cohere embed-english-v3.0 | User requirement |
| Vector DB | Qdrant Cloud | User requirement |
| Response Gen | Cohere Command | Provider consistency |
| Chunking | H2 sections (200-500 words) | Constitution alignment |
| Query Modes | Single endpoint + mode param | API simplicity |
| Frontend | React widget in Root | Docusaurus pattern |
| Security | Server-side keys only | Best practice |
