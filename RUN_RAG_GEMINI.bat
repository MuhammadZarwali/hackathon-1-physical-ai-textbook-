@echo off
echo ========================================
echo Physical AI Textbook - RAG Setup (Gemini)
echo ========================================
echo.

cd /d D:\hackathon-1\physical-ai-textbook

echo [1/5] Installing Python dependencies...
cd rag-backend
python -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo   Done!
echo.

echo [2/5] Starting Qdrant (using in-memory mode)...
echo   Note: For persistent storage, use Docker or Qdrant Cloud
echo   Done!
echo.

echo [3/5] Setting up Qdrant collection...
cd ..\scripts
python setup_qdrant.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to setup Qdrant
    echo Please start Qdrant first:
    echo   Option 1: docker run -p 6333:6333 qdrant/qdrant
    echo   Option 2: Use Qdrant Cloud (https://cloud.qdrant.io)
    pause
    exit /b 1
)
echo   Done!
echo.

echo [4/5] Embedding all chapters with Gemini...
python embed_chapters_gemini.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to embed chapters
    pause
    exit /b 1
)
echo   Done!
echo.

echo [5/5] Starting RAG API server...
cd ..\rag-backend
echo.
echo ========================================
echo RAG API Starting...
echo ========================================
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo Textbook: http://localhost:3000/hackathon-1/
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python main_gemini.py
