# Quickstart Guide: Frontend-Backend Integration

**Feature**: Frontend-Backend Integration for RAG Chatbot
**Date**: 2025-12-30
**Audience**: Developers setting up local environment or testing integration

---

## Prerequisites

### Required Software

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend build tool
- **Git** - Version control
- **Modern web browser** - Chrome, Firefox, Safari, or Edge (last 2 versions)

### Required Credentials

1. **Cohere API Key**: Get from https://dashboard.cohere.ai/api-keys
2. **Qdrant Cloud URL and API Key**: Get from https://cloud.qdrant.io/

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd physical-ai-textbook/rag-backend
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages**:
- fastapi
- uvicorn
- cohere>=5.0.0
- qdrant-client
- python-dotenv
- pydantic

### 3. Configure Environment Variables

Create or edit `.env` file:

```bash
# Cohere API
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud
QDRANT_URL=https://your-cluster.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001

# CORS Configuration (comma-separated list)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**IMPORTANT**: Replace placeholder values with your actual credentials.

### 4. Verify Qdrant Collection

Check that textbook chunks are indexed:

```bash
python -c "from qdrant_service import QdrantService; q = QdrantService(); print(f'Chunks indexed: {q.get_collection_info()}')"
```

**Expected output**: `Chunks indexed: {'points_count': 106, 'status': 'green'}`

If no chunks indexed, run the embedding script:

```bash
python embed_chapters_cohere.py
```

### 5. Start Backend Server

```bash
python main_cohere.py
```

**Expected output**:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### 6. Verify Backend Health

Open in browser or use curl:

```bash
curl http://localhost:8001/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "service": "rag-chatbot",
  "cohere": "available",
  "qdrant": "connected",
  "chunks_indexed": 106
}
```

### 7. Test Query Endpoint

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is ROS 2?",
    "mode": "global",
    "persona": "beginner"
  }'
```

**Expected response** (truncated):
```json
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

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd physical-ai-textbook/docs
```

### 2. Install Node Dependencies

```bash
npm install
```

**Expected packages**:
- docusaurus
- react
- react-dom
- clsx
- prism-react-renderer

### 3. Configure Environment Variables

Create `.env.development` file:

```bash
API_URL=http://localhost:8001
```

For production deployment, create `.env.production`:

```bash
API_URL=https://your-backend-domain.railway.app
```

### 4. Update docusaurus.config.js

Add `customFields` to expose API_URL:

```js
module.exports = {
  // ... other config
  customFields: {
    API_URL: process.env.API_URL || 'http://localhost:8001'
  }
};
```

### 5. Start Development Server

```bash
npm start
```

**Expected output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at http://localhost:3000/
```

### 6. Open in Browser

Navigate to: http://localhost:3000

**Expected UI**:
- Physical AI textbook site loads
- Floating chat button appears in bottom-right corner (teal gradient circle)
- No console errors

---

## Test Integration

### Test 1: Basic Query

1. Click the floating chat button
2. Verify chat panel opens with welcome message
3. Type: "What is ROS 2?"
4. Click send or press Enter
5. **Expected**:
   - Loading indicator appears (typing dots)
   - Response appears within 5 seconds
   - Response includes textbook content
   - Source citations displayed with clickable links

### Test 2: Greeting Handling

1. In chat panel, type: "Hi"
2. Send query
3. **Expected**:
   - Response: "Hello! I'm your Physical AI & Humanoid Robotics textbook assistant. How can I help you today?"
   - No source citations (direct response, no retrieval)

### Test 3: Out-of-Scope Question

1. Type: "What is the best pizza in New York?"
2. Send query
3. **Expected**:
   - Response clearly states topic not covered
   - Suggests textbook topics (ROS 2, Gazebo, Isaac, VLA)
   - No hallucinated content

### Test 4: Source Link Navigation

1. Ask: "What is Gazebo?"
2. Wait for response with sources
3. Click on a source link
4. **Expected**:
   - Browser navigates to the linked textbook section
   - Section matches the cited chapter/section

### Test 5: Persona Adaptation

1. Select "Beginner" from persona dropdown
2. Ask: "What is ROS 2?"
3. Note response style (simple explanations, analogies)
4. Select "AI Researcher" from dropdown
5. Ask same question
6. **Expected**:
   - Response style changes (assumes ML knowledge, more technical)

### Test 6: Page Navigation Persistence

1. On Chapter 1 page, ask a question
2. Navigate to Chapter 3 page
3. Open chat panel
4. **Expected**:
   - Chat history preserved
   - Previous question and answer still visible

### Test 7: Mobile Responsiveness

1. Open browser DevTools
2. Set device to mobile (375px width)
3. Click chat button
4. **Expected**:
   - Chat panel adapts to mobile layout
   - No horizontal scrolling
   - Input and buttons remain usable

---

## Troubleshooting

### Problem: Backend API Not Starting

**Symptoms**:
```
ERROR: Could not import module 'main_cohere'
```

**Solution**:
1. Verify you're in `rag-backend` directory
2. Check Python version: `python --version` (should be 3.11+)
3. Reinstall dependencies: `pip install -r requirements.txt`

---

### Problem: CORS Error in Browser Console

**Symptoms**:
```
Access to fetch at 'http://localhost:8001/query' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution**:
1. Check backend `.env` file has correct CORS_ORIGINS:
   ```
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```
2. Restart backend server after changing .env
3. Verify CORS headers in response (use browser DevTools Network tab)

---

### Problem: Frontend Can't Connect to Backend

**Symptoms**:
- Chat shows "Unable to connect to the chatbot server"
- Network tab shows "Failed to fetch" or "ERR_CONNECTION_REFUSED"

**Solution**:
1. Verify backend is running: `curl http://localhost:8001/health`
2. Check frontend API_URL is correct in `docusaurus.config.js`
3. Verify no firewall blocking port 8001
4. Check backend console for errors

---

### Problem: "No Chunks Indexed" in Health Check

**Symptoms**:
```json
{
  "chunks_indexed": 0,
  "qdrant": "disconnected"
}
```

**Solution**:
1. Verify Qdrant credentials in `.env` are correct
2. Test Qdrant connection:
   ```bash
   python -c "from qdrant_service import QdrantService; QdrantService().get_collection_info()"
   ```
3. Run embedding script to index textbook:
   ```bash
   python embed_chapters_cohere.py
   ```

---

### Problem: Slow Response Times (>10 seconds)

**Symptoms**:
- Queries timeout or take very long
- User sees loading indicator for extended period

**Solution**:
1. Check Cohere API status: https://status.cohere.ai/
2. Verify Qdrant Cloud status: https://status.qdrant.io/
3. Check network latency to Qdrant Cloud
4. Consider increasing timeout in frontend (currently 10s)
5. Reduce `limit` in Qdrant search (currently 5 chunks)

---

### Problem: Empty Response or Hallucinated Content

**Symptoms**:
- Response doesn't match textbook content
- Sources list is empty when it shouldn't be

**Solution**:
1. Verify chunks are indexed: `curl http://localhost:8001/collection/info`
2. Check Cohere embedding service is using correct model (embed-english-v3.0)
3. Test query directly with backend:
   ```bash
   curl -X POST http://localhost:8001/query \
     -H "Content-Type: application/json" \
     -d '{"question": "What is ROS 2?", "mode": "global"}'
   ```
4. Check backend console for RAG pipeline errors

---

## Testing Checklist

Before marking integration complete, verify:

- [ ] Backend starts without errors
- [ ] Health check returns "healthy" status
- [ ] 106 chunks indexed in Qdrant
- [ ] Frontend builds without errors
- [ ] Chat widget renders on all pages
- [ ] Basic query returns grounded answer with sources
- [ ] Greeting handled without retrieval
- [ ] Out-of-scope question handled gracefully
- [ ] Source links navigate to correct sections
- [ ] Persona adaptation works
- [ ] Chat history persists across page navigation
- [ ] Mobile layout responsive (375px+ width)
- [ ] No CORS errors in console
- [ ] No exposed API keys in browser DevTools
- [ ] Response time <5 seconds for 95% of queries

---

## Next Steps

Once local integration is working:

1. **Deploy Backend**: Choose Railway, Render, or Heroku (see [research.md](./research.md#r4-backend-deployment-platform-selection))
2. **Update Frontend API_URL**: Set production URL in Vercel environment variables
3. **Update CORS_ORIGINS**: Add production frontend URL to backend CORS whitelist
4. **Test Production**: Verify end-to-end flow on deployed site
5. **Monitor Performance**: Check response times and error rates

---

## Resources

- **API Contract**: See [contracts/query-api.yaml](./contracts/query-api.yaml)
- **Data Models**: See [data-model.md](./data-model.md)
- **Implementation Plan**: See [plan.md](./plan.md)
- **FastAPI Docs**: http://localhost:8001/docs (auto-generated OpenAPI UI)
- **Cohere Docs**: https://docs.cohere.com/
- **Qdrant Docs**: https://qdrant.tech/documentation/

---

**Quickstart Status**: ✅ COMPLETE - Ready for implementation phase
