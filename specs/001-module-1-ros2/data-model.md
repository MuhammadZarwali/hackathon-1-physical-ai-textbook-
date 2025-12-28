# Data Model: Module 1 - The Robotic Nervous System (ROS 2)

**Feature**: Module 1 - ROS 2 Educational Content
**Date**: 2025-12-24
**Phase**: Phase 1 - Design

## Overview

This document defines the data structures and schemas for Module 1 content, RAG system, and user personalization. Since this is an educational textbook module (not a traditional application), the "data model" focuses on content metadata, embedding schemas, and user preferences rather than database entities.

---

## 1. Chapter Metadata Schema

**Purpose**: Frontmatter for each chapter Markdown file to support navigation, RAG indexing, and personalization

**Schema** (YAML frontmatter):

```yaml
---
# Required fields
sidebar_position: number          # Order in sidebar (1, 2, 3)
title: string                     # "Chapter N: [Title]"
description: string               # One-sentence summary (max 160 chars)

# SEO and RAG metadata
keywords: array<string>           # ["ros2", "middleware", "nodes"]
module: string                    # "module-1-ros2"
chapter_id: string                # "chapter-1-introduction-to-ros2"

# Educational metadata
learning_objectives: array<string>  # List of measurable objectives
prerequisites: array<string>        # ["basic programming", "understanding of software architecture"]
difficulty: enum                    # "beginner" | "intermediate" | "advanced"
estimated_reading_time: number      # Minutes (e.g., 25)

# Persona relevance (1-5 scale, helps RAG prioritize content)
persona_relevance:
  beginner: number                  # 5 = highly relevant, 1 = advanced
  software_engineer: number
  robotics_student: number
  ai_researcher: number

# Technical accuracy
ros2_concepts: array<string>        # ["node", "topic", "middleware"]
verified_against: string            # "docs.ros.org/en/humble/..."
last_verified: date                 # "2025-12-24"
---
```

**Example** (Chapter 1):

```yaml
---
sidebar_position: 1
title: "Chapter 1: Introduction to ROS 2"
description: "Understand what ROS 2 is, why it exists, and its role in physical AI systems"

keywords: ["ros2", "middleware", "robotics", "physical-ai", "distributed-systems"]
module: "module-1-ros2"
chapter_id: "chapter-1-introduction-to-ros2"

learning_objectives:
  - "Explain what ROS 2 is and the problems it solves for physical AI systems"
  - "Describe ROS 2's role as middleware using the nervous system analogy"
  - "Compare ROS 2 to ROS 1 and articulate why ROS 2 was created"
  - "Identify real-world humanoid robotics use cases for ROS 2"

prerequisites: ["basic programming concepts", "understanding of software components"]
difficulty: "beginner"
estimated_reading_time: 25

persona_relevance:
  beginner: 5
  software_engineer: 4
  robotics_student: 4
  ai_researcher: 3

ros2_concepts: ["middleware", "node", "distributed-architecture", "dds"]
verified_against: "docs.ros.org/en/humble/Concepts.html"
last_verified: "2025-12-24"
---
```

**Validation Rules**:
- `sidebar_position` must be unique within module
- `title` must match pattern "Chapter N: [Title]"
- `description` max 160 characters (for SEO)
- `keywords` must include at least 3 terms
- `learning_objectives` must have 3-5 items
- `persona_relevance` values must be 1-5
- `estimated_reading_time` must be 15-45 minutes

---

## 2. RAG Chunk Schema

**Purpose**: Structure for content chunks stored in Qdrant vector database for semantic search

**Schema** (Qdrant document):

```python
{
    "id": str,                    # UUID for chunk
    "content": str,               # 200-500 word text chunk
    "embedding": list[float],     # 3072-dim vector (text-embedding-3-large)
    "metadata": {
        # Source identification
        "module": str,            # "module-1-ros2"
        "chapter": str,           # "chapter-1-introduction-to-ros2"
        "chapter_title": str,     # "Chapter 1: Introduction to ROS 2"
        "section_title": str,     # "What Problem ROS 2 Solves"
        "heading_level": int,     # 2 or 3 (H2, H3)

        # Content classification
        "content_type": enum,     # "definition" | "explanation" | "example" | "summary"
        "ros2_concepts": list[str],  # ["middleware", "node"]
        "keywords": list[str],       # ["distributed", "communication"]

        # Persona targeting
        "persona_relevance": {
            "beginner": int,      # 1-5
            "software_engineer": int,
            "robotics_student": int,
            "ai_researcher": int
        },

        # Navigation
        "url": str,               # "/module-1-ros2/chapter-1-introduction-to-ros2#what-problem-ros2-solves"
        "sequence": int,          # Position in chapter (1, 2, 3...)

        # Quality metadata
        "word_count": int,
        "has_code": bool,
        "has_diagram_description": bool,
        "verified": bool          # Technical accuracy checked
    }
}
```

**Chunking Logic**:
1. Split chapter Markdown on H2 and H3 headings
2. Each heading + content = one chunk (target 200-500 words)
3. If section >500 words, split on paragraphs (preserve semantic boundaries)
4. Extract metadata from chapter frontmatter + section analysis
5. Generate embedding via OpenAI API
6. Store in Qdrant with metadata filters

**Qdrant Collection Configuration**:
```python
collection_config = {
    "vector_size": 3072,  # text-embedding-3-large
    "distance": "Cosine",
    "on_disk_payload": True,  # Store metadata on disk for large collections
}
```

---

## 3. User Persona Schema

**Purpose**: Capture user preferences to personalize RAG responses and recommend content

**Schema** (JSON, stored client-side or in session):

```json
{
    "user_id": "string (optional, for registered users)",
    "persona": "enum (beginner | software_engineer | robotics_student | ai_researcher)",
    "preferences": {
        "explanation_depth": "enum (simplified | standard | detailed)",
        "code_examples": "boolean (show small snippets)",
        "analogies": "boolean (use analogies for concepts)",
        "connections_to": "string (distributed_systems | control_theory | ml_systems | none)"
    },
    "learning_history": {
        "completed_chapters": ["array of chapter_ids"],
        "bookmarked_sections": ["array of urls"],
        "recent_queries": ["array of query strings"]
    },
    "language": "enum (en | ur)",  # For future Urdu support
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

**Default Persona Characteristics**:

| Persona | Explanation Depth | Code Examples | Analogies | Connections To |
|---------|-------------------|---------------|-----------|----------------|
| **Beginner** | Simplified | Minimal | Heavy use | None (foundational) |
| **Software Engineer** | Standard | Yes | Moderate | Distributed systems, APIs |
| **Robotics Student** | Standard-Detailed | Yes | Minimal | Control theory, real-time systems |
| **AI Researcher** | Detailed | Minimal | Minimal | ML systems, distributed training |

**Usage in RAG**:
- Persona influences system prompt for GPT-4
- Persona filters Qdrant results by `persona_relevance` score
- Explanation depth adjusts response verbosity
- Learning history prevents redundant explanations ("as you learned in Chapter 1...")

---

## 4. RAG Query Schema

**Purpose**: Structure for user queries sent to FastAPI backend

**Request Schema** (`POST /query`):

```json
{
    "query": "string (required, max 500 chars)",
    "selected_text": "string (optional, user-highlighted passage)",
    "persona": "enum (beginner | software_engineer | robotics_student | ai_researcher)",
    "context_mode": "enum (full_book | selected_text_only | current_chapter)",
    "current_chapter": "string (optional, chapter_id for context)",
    "max_chunks": "number (optional, default 5, max 10)",
    "include_citations": "boolean (default true)"
}
```

**Response Schema**:

```json
{
    "answer": "string (GPT-4 generated response)",
    "sources": [
        {
            "chapter_title": "string",
            "section_title": "string",
            "url": "string",
            "relevance_score": "float (0-1)"
        }
    ],
    "chunks_retrieved": "number",
    "persona_used": "string",
    "processing_time_ms": "number"
}
```

---

## 5. Module Catalog Schema

**Purpose**: Index of all modules in the textbook for navigation and RAG context

**Schema** (JSON, generated at build time):

```json
{
    "modules": [
        {
            "module_id": "module-1-ros2",
            "title": "Module 1: The Robotic Nervous System (ROS 2)",
            "description": "Introduction to ROS 2 architecture, communication model, and AI agent integration",
            "sequence": 1,
            "chapters": [
                {
                    "chapter_id": "chapter-1-introduction-to-ros2",
                    "title": "Chapter 1: Introduction to ROS 2",
                    "url": "/module-1-ros2/chapter-1-introduction-to-ros2",
                    "sequence": 1,
                    "estimated_reading_time": 25,
                    "difficulty": "beginner"
                },
                {
                    "chapter_id": "chapter-2-ros2-communication-model",
                    "title": "Chapter 2: ROS 2 Communication Model",
                    "url": "/module-1-ros2/chapter-2-ros2-communication-model",
                    "sequence": 2,
                    "estimated_reading_time": 30,
                    "difficulty": "intermediate"
                },
                {
                    "chapter_id": "chapter-3-bridging-ai-agents-with-ros2",
                    "title": "Chapter 3: Bridging AI Agents with ROS 2",
                    "url": "/module-1-ros2/chapter-3-bridging-ai-agents-with-ros2",
                    "sequence": 3,
                    "estimated_reading_time": 28,
                    "difficulty": "intermediate"
                }
            ],
            "total_reading_time": 83,
            "prerequisites": [],
            "learning_outcomes": [
                "Understand ROS 2 as middleware for physical AI",
                "Master ROS 2 communication primitives",
                "Design AI-ROS 2 integration architectures"
            ]
        }
    ]
}
```

**Generation**: Auto-generated by a build script that parses all chapter frontmatter.

---

## 6. Glossary Schema

**Purpose**: Maintain consistent terminology across chapters for RAG and learner reference

**Schema** (JSON or Markdown table):

```json
{
    "terms": [
        {
            "term": "ROS 2",
            "definition": "A middleware framework for robot software development providing communication infrastructure, tools, and libraries",
            "category": "framework",
            "related_concepts": ["middleware", "DDS", "node", "graph"],
            "official_source": "https://docs.ros.org/en/humble/",
            "first_introduced": "chapter-1-introduction-to-ros2"
        },
        {
            "term": "Node",
            "definition": "An executable process that performs computation; fundamental unit in the ROS 2 graph",
            "category": "core-concept",
            "related_concepts": ["executor", "graph", "topic", "service"],
            "official_source": "https://docs.ros.org/en/humble/Concepts/Basic/About-Nodes.html",
            "first_introduced": "chapter-1-introduction-to-ros2"
        }
    ]
}
```

**Usage**:
- RAG system can look up definitions for clarification
- Cross-reference validation during content creation
- Generate glossary page in Docusaurus
- Ensure consistent terminology per constitution Principle VIII

---

## Summary

This data model supports:
- ✅ **Educational Clarity**: Chapter metadata with learning objectives, prerequisites, difficulty
- ✅ **Technical Accuracy**: ROS 2 concepts tracked, verified against official docs
- ✅ **AI-Native Design**: Chunk schema optimized for RAG with metadata filters
- ✅ **RAG Compatibility**: Self-contained chunks with explicit metadata for retrieval
- ✅ **Personalization**: Persona schema with relevance scoring and preference tracking
- ✅ **Multi-Language Support**: Language field in user schema for future Urdu translation
- ✅ **Reusable AI Intelligence**: Consistent schemas enable subagent tasks (summarization, quiz generation)

All schemas align with constitution principles and support hackathon bonus criteria (personalization, RAG chatbot, AI intelligence).
