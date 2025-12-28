# 🚀 Complete Setup Guide - Physical AI Textbook with Gemini

## ✅ What's Already Done:

1. ✅ **Gemini API Key Configured** (in `.env` file)
2. ✅ **All Code Ready** (Gemini-powered RAG backend)
3. ✅ **Dependencies Installing** (Python packages)
4. ✅ **3 Chapters Complete** (~12,000 words)

---

## 🎯 What You Need to Do:

### **Option A: Use Qdrant Cloud (EASIEST - No Docker needed)**

#### Step 1: Sign up for Qdrant Cloud (FREE)
1. Go to: https://cloud.qdrant.io
2. Sign up (free tier available)
3. Create a cluster (choose free tier)
4. Get your cluster URL and API key

#### Step 2: Update .env file
```bash
cd D:\hackathon-1\physical-ai-textbook\rag-backend
notepad .env
```

**Add these lines:**
```
QDRANT_URL=https://your-cluster-url.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

#### Step 3: Run the complete setup
```bash
D:\hackathon-1\RUN_RAG_GEMINI.bat
```

---

### **Option B: Use Docker (if you have Docker installed)**

#### Step 1: Start Qdrant
```bash
docker run -d -p 6333:6333 --name qdrant-textbook qdrant/qdrant
```

#### Step 2: Run the complete setup
```bash
D:\hackathon-1\RUN_RAG_GEMINI.bat
```

---

### **Option C: Manual Step-by-Step (if batch file doesn't work)**

#### Step 1: Install Dependencies
```bash
cd D:\hackathon-1\physical-ai-textbook\rag-backend
python -m pip install -r requirements.txt
```

#### Step 2: Setup Qdrant Collection
```bash
cd D:\hackathon-1\physical-ai-textbook\scripts
python setup_qdrant.py
```

Expected output:
```
✓ Connected to Qdrant
✓ Collection 'textbook_chunks' ready
```

#### Step 3: Embed All Chapters (Using Gemini - FREE!)
```bash
python embed_chapters_gemini.py
```

Expected output:
```
Processing: chapter-1-introduction-to-ros2.md
  Created 15 chunks
  ✓ Embedded successfully with Gemini

Processing: chapter-2-ros2-communication-model.md
  Created 18 chunks
  ✓ Embedded successfully with Gemini

Processing: chapter-3-bridging-ai-agents-with-ros2.md
  Created 17 chunks
  ✓ Embedded successfully with Gemini

✓ Embedding pipeline complete with Gemini!
```

**Time**: 3-5 minutes
**Cost**: $0 (FREE with Gemini!)

#### Step 4: Start RAG Backend
```bash
cd D:\hackathon-1\physical-ai-textbook\rag-backend
python main_gemini.py
```

Expected output:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     RAG backend (Gemini) initialized successfully
```

---

## 🧪 Testing the RAG System

### Test 1: Health Check
**Open in browser:** http://localhost:8000/health

Expected response:
```json
{
  "status": "healthy",
  "service": "RAG API (Gemini)",
  "qdrant_status": "connected",
  "vectors_count": 50,
  "ai_provider": "Google Gemini"
}
```

### Test 2: Interactive API Docs
**Open in browser:** http://localhost:8000/docs

Click on `/query` → Try it out

**Example query:**
```json
{
  "query": "What is ROS 2?",
  "persona": "beginner",
  "max_chunks": 5
}
```

### Test 3: Command Line Test
```bash
curl -X POST http://localhost:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What are ROS 2 topics?\", \"persona\": \"software_engineer\", \"max_chunks\": 5}"
```

### Test 4: Different Personas
Try the same question with different personas:

**Beginner:**
```json
{"query": "What are nodes in ROS 2?", "persona": "beginner"}
```
→ Gets simple analogies

**Software Engineer:**
```json
{"query": "What are nodes in ROS 2?", "persona": "software_engineer"}
```
→ Gets comparisons to microservices

**AI Researcher:**
```json
{"query": "What are nodes in ROS 2?", "persona": "ai_researcher"}
```
→ Gets ML systems parallels

---

## 📊 What You Have Now:

### **3 Running Services:**

1. **Docusaurus (Textbook)**
   - URL: http://localhost:3000/hackathon-1/
   - 3 complete chapters browsable

2. **Qdrant (Vector Database)**
   - URL: http://localhost:6333
   - Stores ~50 embedded chunks

3. **RAG Backend (Gemini)**
   - URL: http://localhost:8000
   - Answers questions about chapters
   - 4 persona modes
   - FREE with Gemini!

---

## ❓ Troubleshooting

### "GEMINI_API_KEY not set"
✅ **Already fixed** - Key is in `.env` file

### "Connection refused" to Qdrant
**Solution**: Start Qdrant first
- Docker: `docker run -p 6333:6333 qdrant/qdrant`
- Or use Qdrant Cloud (https://cloud.qdrant.io)

### "No such file or directory"
**Solution**: Make sure you're in the correct directory
```bash
cd D:\hackathon-1\physical-ai-textbook
```

### Embedding fails
**Check API key works:**
```bash
python -c "import google.generativeai as genai; genai.configure(api_key='AIzaSyDQdx3KjwDWQ_OuiVfuVucZA7vm6glpzrQ'); print('✓ API key works!')"
```

---

## 🎉 Success Indicators

You'll know everything works when:

✅ **Health check** returns `"status": "healthy"`
✅ **Collection info** shows ~50 vectors
✅ **Query test** returns a relevant answer with sources
✅ **Different personas** give different explanation styles

---

## 📈 Progress Update

**Completed**: 80/132 tasks (61%)

**What's left**:
- Phase 8: Chat UI Integration (10 tasks)
- Phase 9: Deployment (11 tasks)
- Phase 10: Polish (10 tasks)
- Phase 11: Bonus (11 tasks)

---

## 🔥 Quick Start (Choose ONE)

### If you have Docker:
```bash
# Terminal 1
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2
D:\hackathon-1\RUN_RAG_GEMINI.bat
```

### If you don't have Docker:
1. Sign up for Qdrant Cloud (https://cloud.qdrant.io)
2. Update `.env` with Qdrant Cloud URL
3. Run: `D:\hackathon-1\RUN_RAG_GEMINI.bat`

---

**Your Gemini API Key is ready, Python packages are installing!** 🎊

**Next**: Choose Option A (Qdrant Cloud) or Option B (Docker) and follow the steps!
