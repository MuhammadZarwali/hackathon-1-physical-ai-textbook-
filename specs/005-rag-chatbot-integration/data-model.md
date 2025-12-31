# Data Model: RAG Chatbot Integration

**Feature**: 005-rag-chatbot-integration
**Date**: 2025-12-29

---

## Core Entities

### 1. Chunk

A semantic unit of textbook content stored in Qdrant with its embedding vector.

```yaml
Chunk:
  chunk_id: string          # Unique identifier (e.g., "chapter-1-ros2-section-3")
  text: string              # Full text content (200-500 words)
  vector: float[1024]       # Cohere embed-english-v3.0 embedding
  metadata:
    chapter_title: string   # "Introduction to ROS 2"
    section_title: string   # "ROS 2 Architecture"
    module: string          # "module-1-ros2"
    chapter_id: string      # "chapter-1-introduction-to-ros2"
    url: string             # "/docs/module-1-ros2/chapter-1-introduction-to-ros2#ros-2-architecture"
    word_count: integer     # Approximate word count
```

**Validation Rules**:
- `chunk_id` must be unique across collection
- `text` must be between 100-2000 characters
- `vector` must be exactly 1024 dimensions
- `url` must be a valid relative path

---

### 2. Query

User's question with mode and optional context.

```yaml
Query:
  question: string          # User's natural language question
  mode: enum                # "global" | "selected"
  selected_text: string?    # Required if mode="selected" (10-5000 chars)
  persona: enum?            # "beginner" | "software_engineer" | "robotics_student" | "ai_researcher"
```

**Validation Rules**:
- `question` must be 1-1000 characters
- `mode` must be one of allowed values
- If `mode="selected"`, `selected_text` is required (10-5000 characters)
- `persona` is optional, defaults to null (general audience)

---

### 3. RetrievedChunk

A chunk returned from similarity search with its relevance score.

```yaml
RetrievedChunk:
  chunk_id: string
  text: string
  score: float              # Cosine similarity (0.0-1.0)
  metadata:
    chapter_title: string
    section_title: string
    module: string
    url: string
```

**Score Interpretation**:
- `>= 0.85`: High confidence match
- `0.70 - 0.84`: Moderate confidence
- `< 0.70`: Low confidence (below threshold)

---

### 4. Response

Generated answer with sources and confidence.

```yaml
Response:
  answer: string            # Generated response text
  sources: SourceReference[]
  confidence: enum          # "high" | "medium" | "low" | "none"
  mode_used: string         # "global" | "selected"
  chunks_retrieved: integer # Number of chunks used
```

---

### 5. SourceReference

Pointer to original textbook location.

```yaml
SourceReference:
  chapter_title: string     # "Introduction to ROS 2"
  section_title: string     # "ROS 2 Architecture"
  module: string            # "Module 1"
  url: string               # Clickable link to section
  relevance_score: float    # How relevant this source was
```

---

### 6. Persona

User expertise profile for response adaptation.

```yaml
Persona:
  id: string                # "beginner" | "software_engineer" | "robotics_student" | "ai_researcher"
  name: string              # Display name
  description: string       # Brief description
  prompt_modifier: string   # Added to system prompt
```

**Defined Personas**:

| ID | Name | Prompt Modifier |
|----|------|-----------------|
| beginner | Beginner | "Explain concepts from first principles. Avoid jargon. Use simple analogies." |
| software_engineer | Software Engineer | "Use programming analogies. Assume familiarity with code, APIs, and software patterns." |
| robotics_student | Robotics Student | "Assume knowledge of kinematics and control theory. Focus on AI integration aspects." |
| ai_researcher | AI Researcher | "Assume deep AI/ML knowledge. Focus on robotics-specific applications and challenges." |

---

## Qdrant Collection Schema

```yaml
Collection: textbook_chunks
  vectors:
    size: 1024
    distance: Cosine

  payload_schema:
    chunk_id: keyword
    text: text
    chapter_title: keyword
    section_title: keyword
    module: keyword
    chapter_id: keyword
    url: keyword
    word_count: integer
```

---

## API Request/Response Schemas

### QueryRequest

```json
{
  "question": "What is ROS 2?",
  "mode": "global",
  "selected_text": null,
  "persona": "software_engineer"
}
```

### QueryResponse

```json
{
  "answer": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software...",
  "sources": [
    {
      "chapter_title": "Introduction to ROS 2",
      "section_title": "What is ROS 2?",
      "module": "Module 1",
      "url": "/docs/module-1-ros2/chapter-1-introduction-to-ros2#what-is-ros-2",
      "relevance_score": 0.92
    }
  ],
  "confidence": "high",
  "mode_used": "global",
  "chunks_retrieved": 3
}
```

### EmbedRequest (Admin)

```json
{
  "chunks": [
    {
      "chunk_id": "chapter-1-ros2-section-1",
      "text": "## What is ROS 2?\n\nROS 2 is...",
      "chapter_title": "Introduction to ROS 2",
      "section_title": "What is ROS 2?",
      "module": "module-1-ros2",
      "url": "/docs/module-1-ros2/chapter-1#what-is-ros-2"
    }
  ]
}
```

### ErrorResponse

```json
{
  "error": true,
  "message": "I couldn't find information about this topic in the textbook.",
  "code": "NO_RESULTS",
  "suggestion": "Try rephrasing your question or asking about a different topic."
}
```

---

## State Transitions

### Query Processing Flow

```
[User Input]
    → Validate Input
    → Embed Query (Cohere)
    → Search Qdrant (mode-aware)
    → Filter by Threshold
    → [Results?]
        → Yes: Generate Response (Cohere Command)
        → No: Return "Not Found" Response
    → Add Source Attribution
    → Return Response
```

### Confidence Determination

```
score >= 0.85 AND chunks >= 2  → HIGH
score >= 0.70 AND chunks >= 1  → MEDIUM
score >= 0.50 AND chunks >= 1  → LOW
else                           → NONE (decline to answer)
```

---

## Relationships

```
Chunk (1) ←→ (N) RetrievedChunk : Search results reference chunks
Query (1) → (N) RetrievedChunk : Query retrieves multiple chunks
Response (1) → (N) SourceReference : Response cites multiple sources
SourceReference (N) → (1) Chunk : Sources point to original chunks
```
