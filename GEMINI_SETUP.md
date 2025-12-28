# 🆓 Using Google Gemini API (FREE Alternative to OpenAI)

## ✅ Why Use Gemini?

- **FREE Tier**: 15 requests/minute, 1500 requests/day
- **No Credit Card Required**: Just a Google account
- **Good Quality**: Gemini 1.5 Flash is fast and accurate
- **Perfect for Learning**: Ideal for textbook RAG chatbot

---

## 🔑 Step 1: Get Your Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSy...`)

**That's it!** No payment info needed.

---

## ⚙️ Step 2: Setup (Windows)

### A. Install Dependencies

```bash
cd D:\hackathon-1\physical-ai-textbook\rag-backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies (includes google-generativeai)
pip install -r requirements.txt
```

### B. Configure Environment

```bash
# Copy example file
copy .env.example .env

# Open .env in Notepad
notepad .env
```

**Add your Gemini key to `.env`**:
```
GEMINI_API_KEY=AIzaSy_your_actual_key_here
QDRANT_URL=http://localhost:6333
```

---

## 🐳 Step 3: Start Qdrant (Vector Database)

**Option A: Docker (Easiest)**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Option B: Qdrant Cloud** (Free tier)
1. Sign up at https://cloud.qdrant.io
2. Create cluster
3. Update `.env` with cloud URL

---

## 🚀 Step 4: Initialize & Embed

### A. Setup Qdrant Collection

```bash
cd D:\hackathon-1\physical-ai-textbook\scripts
python setup_qdrant.py
```

### B. Embed All Chapters

```bash
python embed_chapters_gemini.py
```

**What happens:**
- Reads 3 chapters
- Creates ~50 chunks
- Embeds using Gemini `text-embedding-004`
- Stores in Qdrant
- **Time**: 3-5 minutes (FREE!)

---

## ▶️ Step 5: Start RAG Backend (Gemini Version)

```bash
cd D:\hackathon-1\physical-ai-textbook\rag-backend

# Use the Gemini version
python main_gemini.py
```

**Server starts at**: `http://localhost:8000`

---

## 🧪 Step 6: Test It!

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "RAG API (Gemini)",
  "ai_provider": "Google Gemini"
}
```

### Test 2: Ask a Question

```bash
curl -X POST http://localhost:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What is ROS 2?\", \"persona\": \"beginner\", \"max_chunks\": 5}"
```

### Test 3: Interactive API Docs

Open in browser: **http://localhost:8000/docs**

Try queries like:
- "What are ROS 2 topics?"
- "How do AI agents connect to ROS 2?"
- "Explain nodes in ROS 2"

---

## 📊 Differences: Gemini vs OpenAI

| Feature | Gemini | OpenAI |
|---------|--------|--------|
| **Cost** | FREE (1500 req/day) | Paid (~$0.50/day) |
| **Embedding Model** | text-embedding-004 | text-embedding-3-large |
| **Embedding Dimension** | 768 | 3072 |
| **Chat Model** | Gemini 1.5 Flash | GPT-4 |
| **Speed** | Fast | Fast |
| **Quality** | Very Good | Excellent |
| **Setup** | No credit card | Credit card required |

**For this project**: Gemini is **perfect** and **FREE**!

---

## 🔧 Files Used (Gemini Version)

- `main_gemini.py` - FastAPI with Gemini
- `embedding_gemini.py` - Gemini embeddings
- `chat_gemini.py` - Gemini chat
- `embed_chapters_gemini.py` - Embedding script for Gemini

---

## ❓ Troubleshooting

### "GEMINI_API_KEY not set"
- Check `.env` file exists in `rag-backend/`
- Make sure it contains `GEMINI_API_KEY=AIzaSy...`
- Activate venv: `venv\Scripts\activate`

### "Quota exceeded"
- Free tier: 15 requests/minute
- Wait 1 minute and try again
- Or upgrade to paid tier

### Embeddings fail
- Check API key is valid
- Check internet connection
- Try test: `python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('OK')"`

---

## 🎯 Quick Commands Summary

```bash
# Terminal 1: Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2: Setup & Embed
cd D:\hackathon-1\physical-ai-textbook\rag-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Edit .env with GEMINI_API_KEY

cd ..\scripts
python setup_qdrant.py
python embed_chapters_gemini.py

# Terminal 3: Start Server
cd ..\rag-backend
python main_gemini.py

# Terminal 4: Test
curl http://localhost:8000/health
```

---

**✨ With Gemini, you can run the entire RAG chatbot for FREE!**
