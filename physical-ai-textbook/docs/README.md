# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

### Prerequisites

This project consists of two parts that need to be deployed separately:
1. **Backend API** (FastAPI RAG chatbot) - deploy to Railway or similar platform
2. **Frontend Website** (Docusaurus) - deploy to Vercel or similar static hosting

### Backend Deployment (Railway)

1. **Create Railway Account** and create a new project

2. **Set Environment Variables** in Railway dashboard:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   API_HOST=0.0.0.0
   API_PORT=8001
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-vercel-domain.vercel.app
   ```

3. **Deploy Backend**:
   - Connect Railway to your GitHub repository
   - Set root directory to `physical-ai-textbook/rag-backend`
   - Railway will automatically detect requirements.txt and deploy
   - Note the deployed backend URL (e.g., `https://your-backend.railway.app`)

4. **Verify Backend Health**:
   ```bash
   curl https://your-backend.railway.app/health
   ```

### Frontend Deployment (Vercel)

1. **Update Production Environment**:
   - Edit `physical-ai-textbook/docs/.env.production`
   - Set `API_URL=https://your-backend.railway.app` (from backend deployment)

2. **Configure Vercel**:
   - Create Vercel account and import your GitHub repository
   - Set root directory to `physical-ai-textbook/docs`
   - Set environment variable in Vercel dashboard:
     - Key: `API_URL`
     - Value: `https://your-backend.railway.app`

3. **Deploy Frontend**:
   - Vercel will automatically build and deploy on push to main branch
   - Or manually trigger deployment from Vercel dashboard

4. **Update Backend CORS**:
   - After frontend deploys, note your Vercel URL (e.g., `https://your-project.vercel.app`)
   - Update Railway environment variable `CORS_ORIGINS` to include this URL
   - Redeploy backend

### Manual Deployment (GitHub Pages)

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

### Testing Production Deployment

1. **Test Backend Health**:
   ```bash
   curl https://your-backend.railway.app/health
   ```

2. **Test Frontend Chatbot**:
   - Open `https://your-project.vercel.app`
   - Click chat button in bottom-right corner
   - Ask: "What is ROS 2?"
   - Verify response includes textbook content with clickable source links

3. **Verify CORS**:
   - Open browser DevTools → Network tab
   - Submit a chat query
   - Verify no CORS errors in console
   - Verify API request to `/query` endpoint succeeds

### Troubleshooting

**"Failed to fetch" error in chat**:
- Check backend is running: `curl https://your-backend.railway.app/health`
- Verify API_URL in Vercel environment variables matches backend URL
- Redeploy frontend after changing API_URL

**CORS errors in browser console**:
- Verify backend CORS_ORIGINS includes your Vercel URL
- Ensure no trailing slashes in URLs
- Redeploy backend after changing CORS_ORIGINS

**Empty responses or 500 errors**:
- Check Railway logs for backend errors
- Verify all API keys (COHERE_API_KEY, QDRANT_API_KEY, etc.) are set correctly
- Ensure Qdrant collection exists and has data
