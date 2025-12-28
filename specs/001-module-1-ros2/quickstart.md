# Quickstart Guide: Module 1 Development

**Feature**: Module 1 - The Robotic Nervous System (ROS 2)
**Date**: 2025-12-24
**Phase**: Phase 1 - Design

## Overview

This guide provides step-by-step instructions for setting up the development environment, creating Module 1 content, and testing the RAG chatbot integration.

---

## Prerequisites

- **Git**: For version control
- **Node.js**: v18+ (for Docusaurus)
- **Python**: 3.11+ (for RAG backend)
- **Docker**: (optional, for Qdrant local development)
- **OpenAI API Key**: For embeddings and GPT-4
- **Code Editor**: VS Code recommended

---

## Phase 1: Docusaurus Setup

### 1.1 Initialize Docusaurus Project

```bash
# Navigate to project root
cd hackathon-1

# Install Docusaurus
npx create-docusaurus@latest docs classic

# Move into docs directory
cd docs

# Install dependencies
npm install
```

### 1.2 Configure Docusaurus for Educational Content

Edit `docusaurus.config.js`:

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From Digital Intelligence to Embodied Systems',
  url: 'https://[your-username].github.io',
  baseUrl: '/hackathon-1/',
  organizationName: '[your-username]',
  projectName: 'hackathon-1',

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',  // Docs-only mode
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/[your-username]/hackathon-1/edit/main/docs/',
        },
        blog: false,  // Disable blog
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      items: [
        {
          type: 'localeDropdown',  // For future Urdu support
          position: 'right',
        },
        {
          href: 'https://github.com/[your-username]/hackathon-1',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
      additionalLanguages: ['python', 'bash'],
    },
  },
};
```

### 1.3 Create Module Structure

```bash
# Create docs directory structure
mkdir -p docs/module-1-ros2
mkdir -p docs/module-2-digital-twin
mkdir -p docs/module-3-isaac-ai-brain
mkdir -p docs/module-4-vision-language-action

# Create module metadata for Module 1
cat > docs/module-1-ros2/_category_.json << EOF
{
  "label": "Module 1: The Robotic Nervous System (ROS 2)",
  "position": 1,
  "link": {
    "type": "generated-index",
    "description": "Learn ROS 2 as the nervous system of physical AI systems."
  }
}
EOF
```

### 1.4 Create Chapter Template

Create `docs/module-1-ros2/chapter-1-introduction-to-ros2.md`:

```markdown
---
sidebar_position: 1
title: "Chapter 1: Introduction to ROS 2"
description: "Understand what ROS 2 is, why it exists, and its role in physical AI systems"
keywords: ["ros2", "middleware", "robotics", "physical-ai"]
module: "module-1-ros2"
chapter_id: "chapter-1-introduction-to-ros2"
learning_objectives:
  - "Explain what ROS 2 is and the problems it solves"
  - "Describe ROS 2's role as middleware"
  - "Compare ROS 2 to ROS 1"
prerequisites: ["basic programming"]
difficulty: "beginner"
estimated_reading_time: 25
persona_relevance:
  beginner: 5
  software_engineer: 4
  robotics_student: 4
  ai_researcher: 3
---

# Chapter 1: Introduction to ROS 2

## Learning Objectives

By the end of this chapter, you will:
- Explain what ROS 2 is and the problems it solves for physical AI systems
- Describe ROS 2's role as middleware using the nervous system analogy
- Compare ROS 2 to ROS 1 and articulate why ROS 2 was created

## What is ROS 2?

ROS 2 (Robot Operating System 2) is a middleware framework for robot software development. It provides communication infrastructure, tools, and libraries that enable developers to build robot applications.

**Definition**: Middleware is software that connects different applications and components, allowing them to communicate and share data.

**Why it matters**: Robots are complex systems with many sensors, actuators, and computational components. ROS 2 provides the "nervous system" that allows these components to work together seamlessly.

:::note For Beginners
Think of ROS 2 as the phone network that lets different apps on your phone communicate. Just as apps can send messages to each other through the operating system, robot components send data through ROS 2.
:::

## [Continue with content per spec.md requirements...]

## Summary

This chapter covered:
- ROS 2 is a middleware framework for robot software development
- It solves problems of modularity, communication, and distributed computation
- ROS 2 improves on ROS 1 with real-time support, security, and cross-platform compatibility
- In humanoid robotics, ROS 2 enables coordination between perception, planning, and actuation

**Next**: Chapter 2 explores the communication primitives (nodes, topics, services, actions) that make ROS 2 powerful.

## Further Reading

- [Official ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Design Decisions](https://design.ros2.org/articles/why_ros2.html)
```

### 1.5 Test Docusaurus Locally

```bash
# Start development server
npm start

# Build for production
npm run build

# Serve production build
npm run serve
```

Visit `http://localhost:3000` to see the site.

---

## Phase 2: RAG Backend Setup

### 2.1 Create FastAPI Project

```bash
# Navigate to project root
cd hackathon-1

# Create RAG backend directory
mkdir -p rag-backend
cd rag-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn qdrant-client openai python-dotenv pydantic
pip freeze > requirements.txt
```

### 2.2 Create FastAPI Application

Create `rag-backend/main.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Physical AI Textbook RAG API")

# CORS for Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://[your-username].github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
openai.api_key = os.getenv("OPENAI_API_KEY")
qdrant = QdrantClient(host="localhost", port=6333)  # Or Qdrant Cloud URL

# Request/Response models
class QueryRequest(BaseModel):
    query: str
    selected_text: str | None = None
    persona: str = "software_engineer"
    context_mode: str = "full_book"
    current_chapter: str | None = None
    max_chunks: int = 5

class Source(BaseModel):
    chapter_title: str
    section_title: str
    url: str
    relevance_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    chunks_retrieved: int
    persona_used: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "RAG API"}

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    # 1. Generate query embedding
    embedding_response = openai.Embedding.create(
        model="text-embedding-3-large",
        input=request.query
    )
    query_embedding = embedding_response["data"][0]["embedding"]

    # 2. Search Qdrant
    search_result = qdrant.search(
        collection_name="textbook_chunks",
        query_vector=query_embedding,
        limit=request.max_chunks,
        query_filter={
            "must": [
                {"key": f"metadata.persona_relevance.{request.persona}", "range": {"gte": 3}}
            ]
        } if request.persona else None
    )

    # 3. Construct context
    context_chunks = [hit.payload["content"] for hit in search_result]
    if request.selected_text:
        context_chunks.insert(0, f"User-selected text: {request.selected_text}")

    # 4. Generate response with GPT-4
    persona_prompts = {
        "beginner": "You are a patient educator explaining robotics to beginners. Use simple language and analogies.",
        "software_engineer": "You are explaining robotics to an experienced software engineer. Draw parallels to web development and distributed systems.",
        "robotics_student": "You are explaining AI integration to a robotics student familiar with control theory.",
        "ai_researcher": "You are explaining embodied systems to an AI researcher familiar with ML models."
    }

    system_prompt = persona_prompts.get(request.persona, persona_prompts["software_engineer"])

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"{system_prompt}\n\nAnswer based on this textbook content:\n\n" + "\n\n".join(context_chunks)},
            {"role": "user", "content": request.query}
        ]
    )

    answer = completion.choices[0].message.content

    # 5. Format sources
    sources = [
        Source(
            chapter_title=hit.payload["metadata"]["chapter_title"],
            section_title=hit.payload["metadata"]["section_title"],
            url=hit.payload["metadata"]["url"],
            relevance_score=hit.score
        )
        for hit in search_result
    ]

    return QueryResponse(
        answer=answer,
        sources=sources,
        chunks_retrieved=len(search_result),
        persona_used=request.persona
    )

@app.post("/embed")
async def embed_content(content: dict):
    """Endpoint to embed chapter content into Qdrant"""
    # Implementation for content ingestion
    # This would be called during build to index all chapters
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2.3 Setup Qdrant

**Option A: Docker (Local Development)**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option B: Qdrant Cloud (Free Tier)**
1. Sign up at https://cloud.qdrant.io
2. Create cluster
3. Update `QdrantClient` with cloud URL and API key

### 2.4 Create Collection in Qdrant

```python
# scripts/setup_qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="textbook_chunks",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)

print("Collection 'textbook_chunks' created successfully!")
```

Run: `python scripts/setup_qdrant.py`

### 2.5 Test FastAPI Locally

```bash
# Start server
uvicorn main:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test query (after embedding content)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?", "persona": "beginner"}'
```

---

## Phase 3: Content Embedding Pipeline

### 3.1 Create Embedding Script

Create `scripts/embed_chapters.py`:

```python
import os
import openai
import frontmatter
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from pathlib import Path
import uuid
import re

openai.api_key = os.getenv("OPENAI_API_KEY")
qdrant = QdrantClient(host="localhost", port=6333)

def chunk_chapter(md_file):
    """Split chapter into semantic chunks (200-500 words on H2/H3 boundaries)"""
    post = frontmatter.load(md_file)
    content = post.content
    metadata = post.metadata

    # Split on H2/H3 headings
    chunks = []
    sections = re.split(r'(^##\s+.+$)', content, flags=re.MULTILINE)

    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        body = sections[i+1].strip() if i+1 < len(sections) else ""

        # Combine heading + body
        chunk_text = f"{heading}\n\n{body}"
        word_count = len(chunk_text.split())

        if 200 <= word_count <= 500:
            chunks.append({
                "text": chunk_text,
                "section_title": heading.replace("## ", "").replace("### ", ""),
                "heading_level": heading.count("#"),
                "word_count": word_count
            })

    return chunks, metadata

def embed_and_store(chapter_file):
    """Embed chapter and store in Qdrant"""
    chunks, metadata = chunk_chapter(chapter_file)

    for idx, chunk in enumerate(chunks):
        # Generate embedding
        response = openai.Embedding.create(
            model="text-embedding-3-large",
            input=chunk["text"]
        )
        embedding = response["data"][0]["embedding"]

        # Create Qdrant point
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": chunk["text"],
                "metadata": {
                    "module": metadata.get("module"),
                    "chapter": metadata.get("chapter_id"),
                    "chapter_title": metadata.get("title"),
                    "section_title": chunk["section_title"],
                    "heading_level": chunk["heading_level"],
                    "url": f"/{metadata.get('module')}/{metadata.get('chapter_id')}",
                    "sequence": idx + 1,
                    "word_count": chunk["word_count"],
                    "persona_relevance": metadata.get("persona_relevance", {}),
                    "keywords": metadata.get("keywords", []),
                    "ros2_concepts": metadata.get("ros2_concepts", []),
                }
            }
        )

        # Upload to Qdrant
        qdrant.upsert(
            collection_name="textbook_chunks",
            points=[point]
        )

    print(f"Embedded {len(chunks)} chunks from {chapter_file.name}")

# Embed all chapters
docs_dir = Path("docs/module-1-ros2")
for chapter in docs_dir.glob("chapter-*.md"):
    embed_and_store(chapter)

print("All chapters embedded successfully!")
```

Run: `python scripts/embed_chapters.py`

---

## Phase 4: GitHub Pages Deployment

### 4.1 Configure GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        working-directory: ./docs
        run: npm ci
      - name: Build
        working-directory: ./docs
        run: npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./docs/build
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

### 4.2 Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: GitHub Actions
3. Push to `main` branch to trigger deployment

---

## Summary

You now have:
- ✅ Docusaurus configured for educational content
- ✅ Module 1 structure with chapter template
- ✅ FastAPI RAG backend with Qdrant and OpenAI
- ✅ Content embedding pipeline
- ✅ GitHub Pages deployment

**Next Steps**:
1. Write Module 1 chapters following spec.md requirements
2. Run embedding script to index content
3. Integrate chat UI into Docusaurus (React component)
4. Deploy RAG backend to Railway/Render
5. Test end-to-end RAG functionality
