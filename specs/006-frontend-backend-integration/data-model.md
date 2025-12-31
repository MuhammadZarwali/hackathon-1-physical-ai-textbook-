# Data Model: Frontend-Backend Integration

**Feature**: Frontend-Backend Integration for RAG Chatbot
**Date**: 2025-12-30
**Status**: Complete

## Overview

This document defines the data models for HTTP communication between the Docusaurus frontend and FastAPI RAG backend. All communication uses JSON format via the `/query` endpoint.

---

## Entities

### 1. QueryRequest

**Direction**: Frontend → Backend (POST /query)

**Purpose**: User's question with optional context and personalization settings.

**Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `question` | string | Yes | 1-1000 chars, non-empty | User's question about the textbook |
| `mode` | enum | Yes | "global" \| "selected" | Query mode: full-book or context-specific |
| `selected_text` | string | Conditional | 10-5000 chars | Selected text for context (required if mode="selected") |
| `persona` | string | No | "beginner" \| "software_engineer" \| "robotics_student" \| "ai_researcher" | User expertise level for response adaptation |

**Validation Rules**:
- `question`:
  - Must not be empty or whitespace-only
  - Maximum 1000 characters
  - Trimmed before validation
- `mode`:
  - Must be exactly "global" or "selected"
  - Case-sensitive
  - Defaults to "global" if omitted (handled by Pydantic default)
- `selected_text`:
  - Required if `mode` is "selected", otherwise ignored
  - Minimum 10 characters to ensure meaningful context
  - Maximum 5000 characters to prevent excessive embedding costs
- `persona`:
  - Optional - if invalid or omitted, backend uses default (no persona-specific adaptation)
  - Valid values: "beginner", "software_engineer", "robotics_student", "ai_researcher"

**Example - Global Query**:
```json
{
  "question": "What is ROS 2 and why is it used in robotics?",
  "mode": "global",
  "persona": "beginner"
}
```

**Example - Selected-Text Query**:
```json
{
  "question": "How does this relate to real-time control?",
  "mode": "selected",
  "selected_text": "ROS 2 uses DDS (Data Distribution Service) for communication between nodes. DDS provides real-time publish-subscribe messaging with quality-of-service controls.",
  "persona": "software_engineer"
}
```

**Example - Minimal Query**:
```json
{
  "question": "What is Gazebo?",
  "mode": "global"
}
```

---

### 2. QueryResponse

**Direction**: Backend → Frontend (200 OK)

**Purpose**: Generated answer with source citations and metadata.

**Schema**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `answer` | string | Yes | Generated answer text (book-grounded or greeting response) |
| `sources` | array of SourceReference | Yes | Retrieved textbook chunks (empty for greetings) |
| `confidence` | enum | Yes | "high" \| "medium" \| "low" \| "none" - retrieval confidence level |
| `mode_used` | string | Yes | "global" \| "selected" \| "direct" - actual mode used (direct = greeting) |
| `chunks_retrieved` | integer | Yes | Number of chunks used for generation (0 for greetings) |

**Confidence Levels**:

| Level | Criteria | Interpretation |
|-------|----------|----------------|
| `high` | Max relevance score ≥ 0.85 AND ≥2 chunks retrieved | Strong textbook match, answer highly reliable |
| `medium` | Max relevance score ≥ 0.70 | Moderate textbook match, answer reliable with some uncertainty |
| `low` | Max relevance score ≥ 0.50 | Weak textbook match, answer may be incomplete or tangential |
| `none` | No chunks retrieved or score < 0.50 | No textbook content found, "not covered" message returned |

**Mode Values**:
- `global`: Full-book search performed
- `selected`: Context-specific search performed (may fall back to global if no results)
- `direct`: No retrieval performed (greeting or simple acknowledgment)

**Example - High Confidence Response**:
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is the next generation of ROS, designed for production robotics systems. It provides a framework for developing robot software with improved real-time capabilities, security features, and multi-robot support. Unlike ROS 1, ROS 2 uses DDS for communication, enabling better scalability and reliability in complex robotic systems.",
  "sources": [
    {
      "chapter_title": "Module 1: Introduction to ROS 2",
      "section_title": "What is ROS 2?",
      "module": "module-1",
      "url": "/docs/module-1/intro#what-is-ros2",
      "relevance_score": 0.92
    },
    {
      "chapter_title": "Module 1: Introduction to ROS 2",
      "section_title": "ROS 2 Architecture",
      "module": "module-1",
      "url": "/docs/module-1/architecture",
      "relevance_score": 0.87
    }
  ],
  "confidence": "high",
  "mode_used": "global",
  "chunks_retrieved": 3
}
```

**Example - Greeting Response**:
```json
{
  "answer": "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant. How can I help you today?",
  "sources": [],
  "confidence": "high",
  "mode_used": "direct",
  "chunks_retrieved": 0
}
```

**Example - Low Confidence Response**:
```json
{
  "answer": "**Note: The textbook has limited coverage of this specific topic.**\n\nThe textbook briefly mentions neural networks in the context of Vision-Language-Action models, which use transformer architectures for robotic control. However, detailed neural network architectures are not the primary focus of this textbook.",
  "sources": [
    {
      "chapter_title": "Module 4: Vision-Language-Action Models",
      "section_title": "VLA Architecture Overview",
      "module": "module-4",
      "url": "/docs/module-4/vla-architecture",
      "relevance_score": 0.62
    }
  ],
  "confidence": "low",
  "mode_used": "global",
  "chunks_retrieved": 1
}
```

**Example - No Results Response**:
```json
{
  "answer": "I couldn't find information about this topic in the textbook. The textbook covers ROS 2, simulation with Gazebo, NVIDIA Isaac, and Vision-Language-Action models. Try rephrasing your question or asking about one of these topics.",
  "sources": [],
  "confidence": "none",
  "mode_used": "global",
  "chunks_retrieved": 0
}
```

---

### 3. SourceReference

**Direction**: Backend → Frontend (nested in QueryResponse)

**Purpose**: Citation for a retrieved textbook chunk.

**Schema**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chapter_title` | string | Yes | Chapter name (e.g., "Module 1: Introduction to ROS 2") |
| `section_title` | string | Yes | Section name (e.g., "What is ROS 2?") |
| `module` | string | Yes | Module identifier (e.g., "module-1") |
| `url` | string | Yes | Clickable link to textbook section (e.g., "/docs/module-1/intro") |
| `relevance_score` | float | Yes | Vector search similarity score (0.0-1.0, rounded to 3 decimals) |

**Validation Rules**:
- `url` must be a valid relative or absolute URL
- `relevance_score` must be between 0.0 and 1.0
- All string fields must be non-empty

**Display Guidelines**:
- Show top 3 sources to avoid overwhelming user
- Display as clickable links with chapter and section titles
- Show relevance score as percentage or badge (optional)
- Sort by relevance_score descending (highest first)

**Example**:
```json
{
  "chapter_title": "Module 2: Simulation with Gazebo",
  "section_title": "Setting Up Gazebo Environment",
  "module": "module-2",
  "url": "/docs/module-2/setup",
  "relevance_score": 0.856
}
```

---

### 4. ErrorResponse

**Direction**: Backend → Frontend (4xx or 5xx status)

**Purpose**: Error information when request fails.

**Schema**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `detail` | string | Yes | Human-readable error message |

**HTTP Status Codes**:

| Code | Scenario | Example Message |
|------|----------|-----------------|
| 400 | Bad Request - validation failed | "selected_text is required when mode is 'selected'" |
| 400 | Bad Request - empty question | "question must not be empty" |
| 400 | Bad Request - question too long | "question must not exceed 1000 characters" |
| 500 | Server Error - unexpected failure | "An error occurred while processing your query: connection timeout" |

**Error Message Guidelines**:
- Must be user-friendly (no stack traces or internal details)
- Should indicate what went wrong and how to fix it
- Must not expose sensitive information (API keys, database details)

**Example - Validation Error (400)**:
```json
{
  "detail": "selected_text is required when mode is 'selected'"
}
```

**Example - Server Error (500)**:
```json
{
  "detail": "An error occurred while processing your query: connection timeout"
}
```

---

## State Transitions

### Query Processing Flow

```
[User submits question]
      ↓
[Frontend validates input]
      ↓ (valid)
[Frontend sends QueryRequest to /query]
      ↓
[Backend validates request]
      ↓ (valid)
[Backend checks for greeting] → [Greeting detected] → [Return direct response]
      ↓ (not greeting)
[Backend embeds query]
      ↓
[Backend searches Qdrant]
      ↓
[Backend generates response with Cohere]
      ↓
[Backend returns QueryResponse with sources and confidence]
      ↓
[Frontend displays answer and sources]
```

### Error Handling Flow

```
[Frontend sends QueryRequest]
      ↓
[Network error / timeout] → [Retry once] → [Still fails] → [Show error message]
      ↓ (success)
[Backend returns 400] → [Show validation error]
      ↓ (success)
[Backend returns 500] → [Show server error]
      ↓ (success)
[Backend returns 200 with QueryResponse]
      ↓
[Frontend parses JSON]
      ↓ (parse error)
[Show "malformed response" error]
      ↓ (success)
[Display answer and sources]
```

---

## Validation Summary

**Frontend Validation** (before sending request):
- Question not empty
- Question ≤ 1000 characters
- If mode="selected", selected_text must be provided
- Persona must be one of valid values (or omitted)

**Backend Validation** (Pydantic models):
- Question: 1-1000 chars, non-empty
- Mode: "global" or "selected"
- Selected_text: 10-5000 chars if mode="selected"
- Persona: Optional, valid enum value

**Response Validation** (frontend should handle):
- HTTP status 200, 400, 500
- Response body is valid JSON
- Required fields present (answer, sources, confidence, mode_used, chunks_retrieved)
- Sources array has valid SourceReference objects

---

## API Contract Reference

**Endpoint**: `POST /query`

**Request Headers**:
```
Content-Type: application/json
```

**Response Headers**:
```
Content-Type: application/json
Access-Control-Allow-Origin: <frontend-origin>
```

**Full Request/Response Example**:

**Request**:
```http
POST http://localhost:8001/query HTTP/1.1
Content-Type: application/json

{
  "question": "What is ROS 2?",
  "mode": "global",
  "persona": "beginner"
}
```

**Response (200 OK)**:
```http
HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: http://localhost:3000

{
  "answer": "ROS 2 is the second generation of the Robot Operating System...",
  "sources": [
    {
      "chapter_title": "Module 1: Introduction to ROS 2",
      "section_title": "What is ROS 2?",
      "module": "module-1",
      "url": "/docs/module-1/intro#what-is-ros2",
      "relevance_score": 0.92
    }
  ],
  "confidence": "high",
  "mode_used": "global",
  "chunks_retrieved": 3
}
```

---

**Data Model Status**: ✅ COMPLETE - Ready for contract generation (Phase 1.2)
