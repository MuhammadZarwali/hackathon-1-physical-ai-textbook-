# Research: Frontend-Backend Integration

**Feature**: Frontend-Backend Integration for RAG Chatbot
**Date**: 2025-12-30
**Status**: Complete

## R1: Environment Variable Configuration in Docusaurus

**Decision**: Use Docusaurus `customFields` in `docusaurus.config.js` to expose build-time environment variables to React components.

**Rationale**:
- Docusaurus is a static site generator - all configuration is baked into the build at build time
- `customFields` is the official Docusaurus pattern for exposing custom configuration to React components
- Environment variables can be set differently for development (`npm start`) vs production (`npm build`)
- Pattern is simple, well-documented, and requires no additional dependencies

**Alternatives Considered**:
1. **Runtime environment variable injection** (e.g., `window.__ENV__`):
   - Rejected: Requires server-side rendering or custom build scripts
   - Docusaurus is statically hosted on Vercel - no server to inject runtime values

2. **Separate config files** (e.g., `config.dev.js`, `config.prod.js`):
   - Rejected: Requires manual switching or build script complexity
   - Environment variables are simpler and more portable

3. **Hardcode different URLs per deployment**:
   - Rejected: Violates portability and requires code changes per environment
   - Not maintainable for multiple environments (dev, staging, prod)

**Implementation Notes**:
```js
// docusaurus.config.js
module.exports = {
  // ... other config
  customFields: {
    API_URL: process.env.API_URL || 'http://localhost:8001'
  }
};
```

```tsx
// React component
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const { siteConfig } = useDocusaurusContext();
const API_URL = siteConfig.customFields.API_URL as string;
```

**Environment Variables**:
- Development: Set `API_URL=http://localhost:8001` via `.env.development` or command line
- Production: Set `API_URL=https://backend.railway.app` in Vercel dashboard environment variables
- Fallback: Defaults to `http://localhost:8001` if not set

**Sources**:
- Docusaurus docs: https://docusaurus.io/docs/deployment#using-environment-variables
- Vercel environment variables: https://vercel.com/docs/projects/environment-variables

---

## R2: CORS Configuration for Vercel + Cloud Backend

**Decision**: Use environment-variable-driven CORS origin whitelist in FastAPI middleware, supporting both localhost (dev) and Vercel domains (prod).

**Rationale**:
- CORS is necessary because frontend (vercel.app) and backend (railway.app) are on different origins
- Environment variable pattern allows different CORS policies per deployment without code changes
- FastAPI's `CORSMiddleware` handles preflight OPTIONS requests automatically
- Wildcard `*.vercel.app` is not secure - explicit domain whitelist is better

**Alternatives Considered**:
1. **Allow all origins (`allow_origins=["*"]`)**:
   - Rejected: Security risk - any website could call our backend
   - CORS exists to prevent unauthorized frontend domains from accessing APIs

2. **Wildcard subdomain matching (`*.vercel.app`)**:
   - Rejected: FastAPI CORS doesn't support wildcard subdomains natively
   - Would require custom middleware or regex matching

3. **Dynamic CORS based on request headers**:
   - Rejected: Adds complexity and potential security vulnerabilities
   - Static whitelist is simpler and safer

**Implementation Notes**:

```python
# main_cohere.py (already implemented)
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Whitelist from env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**CORS Origins by Environment**:
- Development: `CORS_ORIGINS=http://localhost:3000,http://localhost:3001`
- Production: `CORS_ORIGINS=https://hackathon-1-physical-ai-textbook-phi.vercel.app`
- Custom domain: Add to comma-separated list if custom domain is configured

**Preflight Handling**:
- FastAPI automatically responds to OPTIONS requests with appropriate CORS headers
- No additional configuration needed beyond `CORSMiddleware` setup

**Security Notes**:
- Only whitelist known frontend domains
- Use HTTPS in production (enforced by deployment platforms)
- Credentials allowed (`allow_credentials=True`) for potential future auth features
- No sensitive data exposed even if CORS misconfigured - backend validates all requests

**Sources**:
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- MDN CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

---

## R3: Error Handling & Retry Patterns for Frontend API Calls

**Decision**: Implement single retry on failure with 10-second timeout and user-friendly error messages categorized by failure type.

**Rationale**:
- Transient network errors (connection hiccups, DNS delays) are common - single retry often succeeds
- 10-second timeout balances user patience (spec requires 5s for 95% of queries) with Cohere API latency
- Multiple retries increase wait time and frustrate users - fail fast with clear messaging
- Categorized error messages help users understand what went wrong and what to do

**Alternatives Considered**:
1. **No retry logic - fail immediately**:
   - Rejected: Transient network errors would force users to manually retry
   - Poor UX for common recoverable failures

2. **Exponential backoff with multiple retries**:
   - Rejected: Adds complexity and increases latency
   - RAG queries are not critical enough to warrant aggressive retry logic
   - Users can manually retry if needed

3. **Infinite timeout (wait forever)**:
   - Rejected: Users would be stuck waiting with no feedback
   - 10 seconds is reasonable upper bound for user patience

**Implementation Notes**:

**Timeout with AbortController**:
```tsx
const abortController = new AbortController();
const timeoutId = setTimeout(() => abortController.abort(), 10000); // 10s

try {
  const response = await fetch(API_URL, {
    signal: abortController.signal,
    // ... other options
  });
  clearTimeout(timeoutId);
} catch (error) {
  clearTimeout(timeoutId);
  if (error.name === 'AbortError') {
    // Timeout occurred
  }
}
```

**Retry Logic**:
```tsx
async function queryWithRetry(url, options, maxRetries = 1) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fetch(url, options);
    } catch (error) {
      if (attempt === maxRetries) throw error;
      // Wait briefly before retry (500ms)
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
}
```

**Error Categorization**:

| Error Type | Detection | User Message |
|-----------|-----------|--------------|
| Network failure | `error.message.includes('Failed to fetch')` | "Unable to connect to the chatbot server. Please check your internet connection." |
| Timeout | `error.name === 'AbortError'` | "The server is taking too long to respond. Please try again." |
| Bad request (400) | `response.status === 400` | "Invalid question format. Please rephrase and try again." |
| Server error (500) | `response.status === 500` | "The server encountered an error. Please try again in a moment." |
| Unknown error | Catch-all | "Something went wrong. Please try again." |

**User Feedback**:
- Show loading indicator immediately on submit
- Display error message if request fails after retry
- Provide "Try Again" button for transient errors
- Allow user to cancel in-flight request by unmounting component

**Performance Considerations**:
- Timeout prevents hanging requests from blocking UI
- Single retry keeps total wait time reasonable (max 20s: 10s + 500ms + 10s)
- Cancel in-flight requests on component unmount to prevent memory leaks

**Sources**:
- MDN AbortController: https://developer.mozilla.org/en-US/docs/Web/API/AbortController
- Fetch API error handling: https://javascript.info/fetch-abort

---

## R4: Backend Deployment Platform Selection

**Decision**: Use **Railway** for FastAPI backend deployment.

**Rationale**:
- **Free tier**: $5/month credit (sufficient for development/demo)
- **Python/FastAPI support**: Native support with automatic runtime detection
- **GitHub integration**: Automatic deploys on git push
- **HTTPS by default**: Automatic SSL certificates
- **Environment variables**: Easy configuration via dashboard or CLI
- **Simple deployment**: No Dockerfile or buildpack config required (auto-detects requirements.txt)
- **Good DX**: Clean UI, fast deploys, excellent documentation

**Alternatives Considered**:

1. **Render**:
   - Pros: Free tier (750 hours/month), Python support, GitHub integration
   - Cons: Free tier instances spin down after 15min inactivity (cold start delays), slower deploys
   - Rejected: Cold starts would break "5 second response" requirement for first query

2. **Heroku**:
   - Pros: Mature platform, extensive documentation
   - Cons: No free tier (minimum $5/month), more complex setup than Railway
   - Rejected: No free option for hackathon demo

3. **Google Cloud Run**:
   - Pros: Serverless, scales to zero, generous free tier
   - Cons: Requires Dockerfile, more complex setup, cold starts
   - Rejected: Complexity not justified for simple FastAPI app

4. **Vercel Serverless Functions**:
   - Pros: Same platform as frontend, serverless
   - Cons: Not optimized for long-running Python apps, 10s timeout limit
   - Rejected: RAG queries may exceed 10s timeout, stateful services (Qdrant connection) don't fit serverless model

**Railway Deployment Steps**:
1. Create Railway account and link GitHub
2. Create new project from `rag-backend` directory
3. Configure environment variables (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, CORS_ORIGINS)
4. Deploy automatically detects `requirements.txt` and installs dependencies
5. Railway assigns public URL (e.g., `https://rag-backend-production-XXXX.up.railway.app`)
6. Update frontend `API_URL` environment variable with Railway URL

**Configuration Requirements**:
- **Start command**: `python main_cohere.py` (or `uvicorn main_cohere:app --host 0.0.0.0 --port $PORT`)
- **Port**: Railway provides `$PORT` environment variable (default 8001 in our case)
- **Environment variables**:
  ```
  COHERE_API_KEY=XZINLeLEgolaXp1ekH0QIae7lpDwvuXA5Chqes62
  QDRANT_URL=https://60a00bf7-e8cc-4752-a7c1-c95f9927d4ce.us-east4-0.gcp.cloud.qdrant.io:6333
  QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  CORS_ORIGINS=https://hackathon-1-physical-ai-textbook-phi.vercel.app
  API_HOST=0.0.0.0
  API_PORT=$PORT
  ```

**Health Check**:
- Railway can ping `/health` endpoint to verify service is running
- Configure in Railway dashboard under "Healthcheck Path"

**Cost Estimate**:
- Free tier: $5 credit/month
- Small FastAPI app: ~$0.10-0.20/day ($3-6/month) with minimal traffic
- Qdrant Cloud: Already on free tier (1GB)
- Cohere API: Pay-per-use (minimal cost for demo traffic)

**Sources**:
- Railway docs: https://docs.railway.app/guides/python
- Railway vs alternatives: https://railway.app/pricing

---

## Research Summary

**All research questions resolved**. Ready to proceed with Phase 1 (Design & Contracts).

**Key Decisions**:
1. **Frontend config**: Docusaurus customFields with environment variables
2. **CORS**: Environment-variable-driven whitelist in FastAPI
3. **Error handling**: Single retry, 10s timeout, categorized error messages
4. **Deployment**: Railway for backend, Vercel for frontend (already deployed)

**No blockers identified**. Implementation can proceed.
