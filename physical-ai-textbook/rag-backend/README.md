# Physical AI Textbook RAG Backend

FastAPI backend providing RAG (Retrieval-Augmented Generation) chatbot functionality for the Physical AI textbook.

## Features

- ✅ Vector search with Qdrant
- ✅ OpenAI GPT-4 for question answering
- ✅ Persona-adapted responses (4 personas)
- ✅ Semantic chunking (200-500 words)
- ✅ Source citations with relevance scores

## Prerequisites

1. **Python 3.11+**
2. **Qdrant** (vector database)
3. **OpenAI API Key**

## Setup

### 1. Install Dependencies

```bash
cd rag-backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=http://localhost:6333
```

### 3. Start Qdrant

**Option A: Docker (Recommended)**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option B: Qdrant Cloud**
- Sign up at https://cloud.qdrant.io
- Create a cluster
- Set `QDRANT_URL` and `QDRANT_API_KEY` in `.env`

### 4. Initialize Qdrant Collection

```bash
cd ../scripts
python setup_qdrant.py
```

### 5. Embed Chapter Content

```bash
python embed_chapters.py
```

This will:
- Parse all chapters in `docs/docs/module-1-ros2/`
- Chunk them semantically (200-500 words)
- Generate embeddings using OpenAI
- Store in Qdrant

### 6. Start the API Server

```bash
cd ../rag-backend
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## API Endpoints

### `POST /query`

Ask a question about the textbook content.

**Request**:
```json
{
  "query": "What is ROS 2?",
  "persona": "beginner",
  "max_chunks": 5
}
```

**Response**:
```json
{
  "answer": "ROS 2 is a middleware framework...",
  "sources": [
    {
      "chapter_title": "Chapter 1: Introduction to ROS 2",
      "section_title": "What is ROS 2?",
      "url": "/module-1-ros2/chapter-1#what-is-ros2",
      "relevance_score": 0.92
    }
  ],
  "chunks_retrieved": 3,
  "persona_used": "beginner"
}
```

### Personas

- `beginner` - No robotics background, simple analogies
- `software_engineer` - Parallels to web/distributed systems
- `robotics_student` - Control theory and kinematics focus
- `ai_researcher` - ML systems and embodiment challenges

### `POST /embed`

Embed new content (used by embedding pipeline).

### `GET /health`

Health check endpoint.

### `GET /collection/info`

Get Qdrant collection statistics.

## Testing

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are ROS 2 topics?",
    "persona": "software_engineer",
    "max_chunks": 5
  }'
```

### Test with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "How do AI agents connect to ROS 2?",
        "persona": "ai_researcher",
        "max_chunks": 5
    }
)

print(response.json()["answer"])
```

## Docker Deployment

```bash
# Build
docker build -t physical-ai-rag .

# Run (make sure to set environment variables)
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e QDRANT_URL=http://qdrant:6333 \
  physical-ai-rag
```

## Architecture

```
User Query
    ↓
[FastAPI /query endpoint]
    ↓
[Embedding Service] → OpenAI text-embedding-3-large
    ↓
[Qdrant Search] → Find top 5 similar chunks
    ↓
[Persona Prompts] → Adapt system prompt
    ↓
[OpenAI GPT-4] → Generate answer with context
    ↓
Response with sources
```

## Files

- `main.py` - FastAPI app with endpoints
- `models.py` - Pydantic request/response models
- `embedding.py` - OpenAI embedding integration
- `qdrant_client.py` - Qdrant vector database client
- `personas.py` - Persona-based system prompts
- `qdrant_config.py` - Qdrant collection setup (legacy)
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition

## Troubleshooting

### "OPENAI_API_KEY environment variable not set"

Make sure `.env` file exists and contains your API key.

### "Connection refused" to Qdrant

Make sure Qdrant is running:
```bash
docker ps | grep qdrant
```

### "No relevant content found"

Make sure you've run the embedding pipeline:
```bash
cd scripts
python embed_chapters.py
```

Check collection has content:
```bash
curl http://localhost:8000/collection/info
```

## License

Part of the Physical AI & Humanoid Robotics textbook project.
