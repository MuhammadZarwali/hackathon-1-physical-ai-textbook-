# Implementation Plan: Frontend-Backend Integration for RAG Chatbot

**Branch**: `006-frontend-backend-integration` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-frontend-backend-integration/spec.md`

## Summary

**Objective**: Enable secure HTTP communication between a Docusaurus static site frontend and a FastAPI RAG backend to deliver book-grounded chatbot responses with source attribution.

**Technical Approach**: The frontend ChatWidget component sends user queries to a stateless FastAPI backend via POST requests. The backend processes queries through the existing RAG pipeline (Cohere embeddings → Qdrant retrieval → Cohere generation) and returns JSON responses with answers and source citations. CORS middleware enables cross-origin requests. No API keys are exposed to the frontend.

**Integration Model**: Decoupled architecture with clear separation of concerns. Frontend handles UI state and session management in the browser. Backend handles RAG orchestration, vector search, and response generation. Communication occurs via a single `/query` endpoint with a stable JSON contract.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 4.9+ (React 18+, Docusaurus 3.x)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: React, Docusaurus, fetch API (native)
- Backend: FastAPI, Cohere SDK, Qdrant Client, python-dotenv, uvicorn

**Storage**:
- Qdrant Cloud (vector database for textbook chunks)
- Browser sessionStorage (conversation history)
- No persistent user data storage

**Testing**:
- Frontend: Manual testing in browser (dev & production URLs)
- Backend: pytest for endpoint tests, manual API testing with curl/Postman
- Integration: End-to-end manual testing (user query → backend → response display)

**Target Platform**:
- Frontend: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions), deployed to Vercel as static site
- Backend: Linux server (deployment TBD - Railway/Render/Heroku), development on Windows with uvicorn

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- Query response within 5 seconds for 95% of requests
- Frontend bundle size increase <100KB
- Page load time increase <500ms with ChatWidget
- Backend handles 50 concurrent users without degradation

**Constraints**:
- Frontend must remain stateless (no backend server for frontend)
- Backend must remain stateless (no session storage)
- API responses must be JSON only
- No API keys visible in frontend code or network requests
- CORS must whitelist only known frontend domains

**Scale/Scope**:
- Single backend endpoint (`/query`) with request/response models
- Single ChatWidget component in frontend
- 106 indexed textbook chunks in Qdrant
- 4 supported personas (beginner, software_engineer, robotics_student, ai_researcher)
- 2 query modes (global, selected-text)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Applicable Constitution Principles

**✅ Principle III: AI-Native Design Principles**
- RAG retrieval returns semantically coherent chunks
- Each chunk is independently meaningful with metadata (chapter, section, URL)
- Consistent terminology maintained across responses

**✅ Principle IV: RAG Chatbot Compatibility**
- Supports full-book queries (global mode)
- Supports selected-text queries (context-aware retrieval)
- Responses include "What is this?" "Why does it matter?" "How does it work?" patterns

**✅ Principle V: Personalization Support**
- Backend accepts optional `persona` field in requests
- Responses adapt to 4 user personas: beginner, software_engineer, robotics_student, ai_researcher
- Dynamic explanation depth based on persona

**✅ Principle VIII: Documentation & Structure Standards**
- API contract follows REST conventions
- JSON responses use consistent schema
- Clear error messages for all failure modes

**✅ Principle X: Scope Control**
- Integration focused strictly on connecting existing frontend and backend
- No tangential features (analytics, A/B testing, admin dashboard)
- Depth over breadth: single `/query` endpoint done well

### Constitution Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Educational Clarity | ✅ PASS | Not directly applicable - integration layer, not content |
| II. Technical Accuracy | ✅ PASS | API contract follows REST standards, uses real Cohere/Qdrant APIs |
| III. AI-Native Design | ✅ PASS | RAG pipeline preserves semantic chunk retrieval |
| IV. RAG Compatibility | ✅ PASS | Dual-mode query support (global + selected-text) |
| V. Personalization | ✅ PASS | Persona-aware response generation |
| VI. Multi-Language | ✅ PASS | Not applicable to API layer - content translation is separate |
| VII. Reusable AI Intelligence | ✅ PASS | Stateless backend enables future subagent extensions |
| VIII. Documentation Standards | ✅ PASS | OpenAPI-compatible schema (FastAPI auto-generates) |
| IX. Ethics & Integrity | ✅ PASS | No exposed secrets, proper error handling, honest error messages |
| X. Scope Control | ✅ PASS | Strictly focused on frontend-backend integration |

**GATE STATUS: ✅ PASS** - All applicable principles satisfied. No violations require justification.

## Project Structure

### Documentation (this feature)

```text
specs/006-frontend-backend-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (environment config patterns)
├── data-model.md        # Phase 1 output (request/response schemas)
├── quickstart.md        # Phase 1 output (local testing guide)
├── contracts/           # Phase 1 output (API contract OpenAPI spec)
│   └── query-api.yaml   # /query endpoint contract
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
physical-ai-textbook/
├── rag-backend/                           # Backend (Python/FastAPI)
│   ├── main_cohere.py                     # [EXISTING] FastAPI app with /query endpoint
│   ├── chat_cohere.py                     # [EXISTING] Cohere chat service
│   ├── embedding_cohere.py                # [EXISTING] Cohere embedding service
│   ├── qdrant_service.py                  # [EXISTING] Qdrant vector search
│   ├── personas.py                        # [EXISTING] Persona definitions
│   ├── .env                               # [EXISTING] Backend config (API keys)
│   ├── .env.example                       # [MODIFY] Add CORS_ORIGINS example
│   ├── requirements.txt                   # [EXISTING] Dependencies (Cohere, FastAPI, Qdrant)
│   └── tests/                             # [CREATE] Backend tests
│       ├── test_query_endpoint.py         # /query endpoint tests
│       ├── test_cors.py                   # CORS configuration tests
│       └── test_validation.py             # Input validation tests
│
└── docs/                                  # Frontend (Docusaurus/React)
    ├── src/
    │   ├── components/
    │   │   └── ChatWidget/                # [EXISTING] Chat UI component
    │   │       ├── index.tsx              # [MODIFY] Add API integration
    │   │       └── styles.css             # [EXISTING] Teal & Navy theme
    │   └── theme/
    │       └── Root.tsx                   # [EXISTING] Global widget injection
    ├── .env.development                   # [CREATE] Dev API URL (localhost:8001)
    ├── .env.production                    # [CREATE] Prod API URL (deployed backend)
    ├── docusaurus.config.js               # [MODIFY] Add customFields for API_URL
    └── package.json                       # [EXISTING] Dependencies
```

**Structure Decision**: Web application architecture (Option 2 from template). Frontend and backend are separate deployable units:
- **Frontend**: Deployed to Vercel as static site, served via CDN
- **Backend**: Deployed to cloud service (Railway/Render/Heroku), runs as persistent HTTP server
- **Communication**: Frontend makes cross-origin HTTP requests to backend API URL

This structure is already in place from previous features. This integration feature adds:
1. Environment variable configuration for API URL in frontend
2. CORS configuration in backend
3. Error handling and retry logic in frontend API client
4. Backend endpoint tests

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution principles are satisfied by the proposed architecture.

---

## Phase 0: Research & Unknowns Resolution

**Objective**: Resolve all "NEEDS CLARIFICATION" items from Technical Context and research best practices for integration patterns.

### Research Tasks

#### R1: Environment Variable Configuration in Docusaurus

**Question**: How do we securely configure backend API URLs for different environments (development vs production) in Docusaurus static sites?

**Research Focus**:
- Docusaurus `customFields` in docusaurus.config.js
- `.env.development` and `.env.production` patterns
- Build-time vs runtime environment variable injection
- Best practices for API URL configuration in static sites

**Expected Output**: Documented pattern for configuring `API_URL` in frontend with fallback to localhost for development.

#### R2: CORS Configuration for Vercel + Cloud Backend

**Question**: What CORS origins should be whitelisted for a Vercel-deployed frontend communicating with a Railway/Render backend?

**Research Focus**:
- CORS policy for `*.vercel.app` domains
- Custom domain CORS (if applicable)
- Localhost CORS for development (http://localhost:3000)
- CORS preflight handling in FastAPI
- Environment-based CORS origin lists

**Expected Output**: CORS configuration pattern with environment-variable-driven origin whitelist.

#### R3: Error Handling & Retry Patterns for Frontend API Calls

**Question**: What error handling and retry strategies should the frontend implement for backend API failures?

**Research Focus**:
- Network timeout values (10 seconds recommended)
- Retry logic (retry once on failure)
- User-facing error messages for different failure types (network error, 400, 500, timeout)
- Loading state management during API calls

**Expected Output**: Error handling decision tree for frontend API client.

#### R4: Backend Deployment Platform Selection

**Question**: Which cloud platform should host the FastAPI backend (Railway, Render, Heroku, others)?

**Research Focus**:
- Free tier availability and limits
- Python/FastAPI support
- Environment variable configuration
- HTTPS support
- Deployment simplicity (GitHub integration preferred)

**Expected Output**: Recommended platform with deployment configuration guide.

### Research Deliverable: `research.md`

**Format**:
```markdown
# Research: Frontend-Backend Integration

## R1: Environment Variable Configuration in Docusaurus
**Decision**: [chosen approach]
**Rationale**: [why chosen]
**Alternatives Considered**: [what else evaluated]
**Implementation Notes**: [specific config needed]

## R2: CORS Configuration
[same structure]

## R3: Error Handling
[same structure]

## R4: Backend Deployment
[same structure]
```

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete (Phase 0 done)

**Objective**: Define data models, API contracts, and integration quickstart guide.

### 1.1 Data Model Definition

**Output**: `data-model.md`

**Entities** (extracted from spec.md):

1. **QueryRequest** (Frontend → Backend)
   - `question` (string, required, 1-1000 chars): User's question
   - `mode` (enum, required): "global" | "selected"
   - `selected_text` (string, optional, 10-5000 chars): Selected text for context (required if mode="selected")
   - `persona` (string, optional): "beginner" | "software_engineer" | "robotics_student" | "ai_researcher"

2. **QueryResponse** (Backend → Frontend)
   - `answer` (string, required): Generated answer text
   - `sources` (array of SourceReference, required): Retrieved chunks with citations
   - `confidence` (enum, required): "high" | "medium" | "low" | "none"
   - `mode_used` (string, required): "global" | "selected" | "direct" (for greetings)
   - `chunks_retrieved` (integer, required): Number of chunks used

3. **SourceReference** (nested in QueryResponse)
   - `chapter_title` (string, required): Chapter name
   - `section_title` (string, required): Section name
   - `module` (string, required): Module identifier
   - `url` (string, required): Clickable link to textbook section
   - `relevance_score` (float, required): 0.0-1.0 retrieval score

4. **ErrorResponse** (Backend → Frontend on failure)
   - `detail` (string, required): Human-readable error message
   - HTTP status codes: 400 (bad request), 500 (server error)

**Validation Rules**:
- Empty or whitespace-only questions rejected (400)
- Questions >1000 chars rejected (400)
- Mode="selected" without `selected_text` rejected (400)
- Invalid persona values ignored (falls back to default)

### 1.2 API Contract Generation

**Output**: `contracts/query-api.yaml` (OpenAPI 3.0 spec)

**Endpoint**: `POST /query`

**Request Body**:
```json
{
  "question": "What is ROS 2?",
  "mode": "global",
  "selected_text": null,
  "persona": "beginner"
}
```

**Success Response (200)**:
```json
{
  "answer": "ROS 2 is the second generation of the Robot Operating System...",
  "sources": [
    {
      "chapter_title": "Module 1: Introduction to ROS 2",
      "section_title": "What is ROS 2?",
      "module": "module-1",
      "url": "/docs/module-1/ros2-intro#what-is-ros2",
      "relevance_score": 0.89
    }
  ],
  "confidence": "high",
  "mode_used": "global",
  "chunks_retrieved": 3
}
```

**Error Response (400)**:
```json
{
  "detail": "selected_text is required when mode is 'selected'"
}
```

**Error Response (500)**:
```json
{
  "detail": "An error occurred while processing your query: connection timeout"
}
```

**Additional Endpoints** (existing, documented for completeness):
- `GET /health`: Health check (returns service status)
- `GET /collection/info`: Qdrant collection stats

### 1.3 Integration Quickstart Guide

**Output**: `quickstart.md`

**Content**:
1. **Prerequisites**: Python 3.11+, Node.js 18+, Cohere API key, Qdrant Cloud credentials
2. **Backend Setup**: Install dependencies, configure .env, start server on port 8001
3. **Frontend Setup**: Install dependencies, configure API_URL, start dev server
4. **Test Integration**: Open browser, click chat button, send test query
5. **Verify Response**: Check console for API calls, verify sources display correctly
6. **Troubleshooting**: CORS errors, connection refused, timeout issues

### 1.4 Agent Context Update

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Purpose**: Add integration-specific technologies to agent context file for future reference.

**Technologies to Add**:
- Frontend: Docusaurus customFields pattern for API URL configuration
- Backend: FastAPI CORS middleware configuration
- Integration: HTTP client error handling and retry patterns

---

## Phase 2: Implementation Readiness

**Output**: This phase is completed by the `/sp.tasks` command, NOT by `/sp.plan`.

**What `/sp.tasks` Will Generate**:
- `tasks.md` with implementation tasks broken down by phase
- Test cases for each task
- Acceptance criteria for integration validation

**Expected Task Phases** (preview for `/sp.tasks`):
1. **Phase 1: Backend Configuration** - CORS setup, .env.example update
2. **Phase 2: Frontend Configuration** - Environment variables, API URL config
3. **Phase 3: API Integration** - Implement fetch calls, error handling, retry logic
4. **Phase 4: Error Handling** - User-facing error messages, timeout handling
5. **Phase 5: Testing** - Manual end-to-end tests, edge case validation
6. **Phase 6: Deployment** - Backend deployment, frontend API URL update

---

## Implementation Steps (Execution Plan)

### Step 1: Backend Readiness

**Status**: ✅ COMPLETE (from previous feature 005-rag-chatbot-integration)

**What Exists**:
- FastAPI application in `rag-backend/main_cohere.py`
- `/query` endpoint with QueryRequest/QueryResponse models
- Greeting detection (responds to "hi" without retrieval)
- Cohere RAG pipeline (embedding → Qdrant → generation)
- Health check and collection info endpoints
- Running on port 8001 (to avoid conflict with legacy port 8000)

**Verification**:
- Server starts with `python main_cohere.py`
- `/query` endpoint accepts POST requests with JSON body
- Responses include answer, sources, confidence, mode_used, chunks_retrieved
- 106 textbook chunks indexed in Qdrant Cloud

**Remaining Work**: CORS configuration for Vercel frontend

### Step 2: CORS Configuration

**Objective**: Enable cross-origin requests from Docusaurus frontend to FastAPI backend.

**Current State**:
- CORS middleware already added in `main_cohere.py` (lines 29-37)
- Reads `CORS_ORIGINS` from environment variable
- Defaults to `http://localhost:3000` if not set
- Allows all methods and headers

**Required Changes**:
1. Update `.env` with production CORS origins:
   ```
   CORS_ORIGINS=http://localhost:3000,https://hackathon-1-physical-ai-textbook-phi.vercel.app
   ```
2. Update `.env.example` to document CORS_ORIGINS variable
3. Add custom domain to CORS_ORIGINS after deployment (if applicable)

**Testing**:
- Verify CORS headers in response (Access-Control-Allow-Origin)
- Test preflight OPTIONS request handling
- Confirm both localhost and Vercel origins are accepted

### Step 3: API Contract Validation

**Objective**: Ensure `/query` endpoint matches documented contract.

**Verification Checklist**:
- [x] Request schema matches QueryRequest model (question, mode, selected_text, persona)
- [x] Response schema matches QueryResponse model (answer, sources, confidence, mode_used, chunks_retrieved)
- [x] SourceReference schema matches (chapter_title, section_title, module, url, relevance_score)
- [x] Error responses use standard HTTP status codes (400, 500)
- [x] Greeting detection works (responds without retrieval for "hi", "hello", "thanks")
- [x] Selected-text mode works with fallback to global search
- [x] Persona handling works (adapts response to beginner/engineer/student/researcher)

**Current Status**: Contract already implemented correctly in `main_cohere.py`

**Documentation Needed**: Generate OpenAPI spec from FastAPI (auto-generated at `/docs` endpoint)

### Step 4: Frontend Integration

**Objective**: Connect ChatWidget to backend API with error handling and retry logic.

**Current State**:
- ChatWidget component exists in `docs/src/components/ChatWidget/index.tsx`
- Component UI complete with Teal & Navy theme
- Message display, source links, persona selection implemented
- API_URL hardcoded with TODO comment (line 9-11)

**Required Changes**:

1. **Environment Configuration**:
   - Create `docs/.env.development`:
     ```
     API_URL=http://localhost:8001
     ```
   - Create `docs/.env.production`:
     ```
     API_URL=https://your-backend-domain.railway.app
     ```
   - Update `docusaurus.config.js` to expose `API_URL` via `customFields`
   - Update `ChatWidget/index.tsx` to read API URL from config

2. **API Client Implementation**:
   - Replace TODO with actual fetch implementation
   - Add 10-second timeout using AbortController
   - Implement retry logic (retry once on failure)
   - Add error handling for network failures, 400, 500, timeout

3. **Error State UI**:
   - Display user-friendly error messages for different failure types
   - Show retry button for transient failures
   - Indicate when backend is unreachable

4. **Loading State**:
   - Show typing indicator while awaiting response
   - Disable input during API call
   - Cancel in-flight requests on unmount

**Testing**:
- Test with localhost backend (development)
- Test with deployed backend (production)
- Test error scenarios (backend down, timeout, invalid request)
- Test on mobile devices (responsive layout)

### Step 5: Environment Configuration

**Objective**: Make backend API URL configurable via environment variables for different deployment environments.

**Why This Step Matters**:
- Development uses `http://localhost:8001` (local backend)
- Production uses deployed backend URL (e.g., `https://rag-backend.railway.app`)
- Staging/preview deployments may use different URLs
- Hardcoding URLs breaks portability and requires code changes per environment

**Implementation Pattern**:

**Frontend (Docusaurus)**:
1. Create environment-specific files:
   - `docs/.env.development` → localhost URL
   - `docs/.env.production` → deployed backend URL
2. Expose API_URL in `docusaurus.config.js`:
   ```js
   customFields: {
     API_URL: process.env.API_URL || 'http://localhost:8001'
   }
   ```
3. Access in React component:
   ```tsx
   import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
   const { siteConfig } = useDocusaurusContext();
   const API_URL = siteConfig.customFields.API_URL;
   ```

**Backend (FastAPI)**:
1. CORS origins already configurable via `CORS_ORIGINS` env var
2. API host/port already configurable via `API_HOST` and `API_PORT` env vars
3. Update `.env.example` to document all configurable values

**Configuration Sources**:
- Local development: `.env` files (gitignored)
- Vercel deployment: Environment variables in Vercel dashboard
- Backend deployment: Environment variables in Railway/Render dashboard

**Security Considerations**:
- No API keys in frontend code (already satisfied - keys only in backend .env)
- Environment files excluded from version control (.gitignore)
- Production URLs use HTTPS only

**Testing**:
- Verify localhost connection in development mode
- Verify production connection after deployment
- Confirm fallback to localhost if env var missing
- Test that changing env var updates API URL without code changes

### Step 6: Validation

**Objective**: Test complete end-to-end integration flow.

**Test Scenarios** (from spec.md User Stories):

**US1: Ask Question and Receive Grounded Answer (P1)**
1. Open textbook site (dev: localhost:3000, prod: Vercel URL)
2. Click floating chat button
3. Verify chat panel opens with welcome message
4. Type "What is ROS 2?" and submit
5. Verify loading indicator appears
6. Verify response displays within 5 seconds
7. Verify response includes textbook-grounded content
8. Verify source citations are clickable links
9. Click a source link
10. Verify browser navigates to correct chapter/section

**US2: Handle Out-of-Scope Questions Gracefully (P1)**
1. Open chat panel
2. Type "What is the best pizza in New York?"
3. Submit query
4. Verify response clearly states topic not covered
5. Verify no hallucinated content
6. Verify suggestions provided (if applicable)

**US3: Resume Conversation Across Page Navigation (P2)**
1. Open chat panel on Chapter 1 page
2. Ask "What is ROS 2?"
3. Navigate to Chapter 3 page
4. Verify chat panel retains message history
5. Ask follow-up question "How does this relate to Gazebo?"
6. Verify conversation context preserved

**US4: Receive Persona-Adapted Responses (P3)**
1. Open chat panel
2. Select "Beginner" persona from dropdown
3. Ask "What is ROS 2?"
4. Verify response uses simple analogies
5. Close and reopen chat
6. Select "AI Researcher" persona
7. Ask same question
8. Verify response assumes deep ML knowledge

**Edge Cases** (from spec.md):
- Backend API unreachable → displays "connection lost" message
- Very long question (>1000 chars) → frontend prevents submission
- Empty query → frontend prevents submission
- Mobile device (375px width) → chat widget adapts layout
- Rapid-fire queries → sequential processing, no race conditions
- Malformed backend response → graceful error handling

**Performance Validation**:
- 95% of queries return within 5 seconds (measure with browser DevTools)
- Chat widget loads without breaking page layout
- Frontend bundle size increase <100KB (check build output)
- Page load time increase <500ms (measure with Lighthouse)

**Security Validation**:
- No API keys visible in browser DevTools Network tab
- CORS headers present in response
- HTTPS enforced in production
- Input validation prevents injection attacks

---

## Quality Control

**Grounding Verification**:
- All responses must cite textbook sources
- Zero hallucinated content not present in textbook
- Out-of-scope questions handled honestly

**Error Handling**:
- Missing answers communicated clearly ("not covered in textbook")
- Network failures show user-friendly messages
- Backend errors don't expose internal details

**Security**:
- No API keys, database credentials, or internal config exposed to frontend
- CORS whitelist prevents unauthorized origins
- Input validation on both frontend and backend

---

## Frontend–Backend Integration Plan Completion Criteria

This implementation plan is complete when:

**Documentation**:
- [x] `plan.md` written with all sections filled (Technical Context, Constitution Check, Project Structure, Phases 0-1)
- [ ] `research.md` created with decisions on environment config, CORS, error handling, deployment platform
- [ ] `data-model.md` created with QueryRequest, QueryResponse, SourceReference, ErrorResponse schemas
- [ ] `contracts/query-api.yaml` created with OpenAPI spec for /query endpoint
- [ ] `quickstart.md` created with local setup and testing instructions

**Design Decisions**:
- [x] Backend API contract validated (already implemented in main_cohere.py)
- [x] CORS configuration approach decided (environment-variable-driven origin whitelist)
- [x] Frontend environment variable pattern decided (customFields in docusaurus.config.js)
- [x] Error handling strategy decided (retry once, 10s timeout, user-friendly messages)
- [ ] Backend deployment platform selected (Railway/Render/Heroku)

**Readiness Gates**:
- [x] All NEEDS CLARIFICATION items resolved
- [x] Constitution Check passed (no violations)
- [x] Project structure documented with real paths
- [x] Integration steps defined (6 steps with clear objectives)
- [x] Test scenarios extracted from spec.md user stories

**Next Step**:
- Run `/sp.tasks` to generate task breakdown with acceptance criteria for implementation
- `/sp.tasks` will create `tasks.md` with 6 phases matching the integration steps above

**Not Included in This Plan** (by design):
- Implementation code or commands (those belong in `/sp.tasks` and `/sp.implement`)
- Deployment automation or CI/CD pipelines (out of scope per spec.md)
- Analytics, A/B testing, or monitoring (out of scope per spec.md)
- Backend deployment scripts (deployment platform selection in research.md only)

---

**Plan Status**: ✅ READY FOR TASK GENERATION (`/sp.tasks`)
