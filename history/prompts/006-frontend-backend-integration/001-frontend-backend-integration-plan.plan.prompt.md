---
id: 001
title: Frontend-Backend Integration Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 006-frontend-backend-integration
branch: 006-frontend-backend-integration
user: MuhammadZarwali
command: /sp.plan
labels: ["integration", "api", "cors", "environment-config", "deployment"]
links:
  spec: specs/006-frontend-backend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/006-frontend-backend-integration/plan.md
  - specs/006-frontend-backend-integration/research.md
  - specs/006-frontend-backend-integration/data-model.md
  - specs/006-frontend-backend-integration/contracts/query-api.yaml
  - specs/006-frontend-backend-integration/quickstart.md
tests:
  - No automated tests (planning phase)
---

## Prompt

You are a senior AI systems architect with 20+ years of experience in API-based AI systems.

Produce an EXECUTION PLAN for integrating a FastAPI RAG backend with a Docusaurus frontend.

This plan must follow the PROJECT CONSTITUTION and the approved RAG CHATBOT SPECIFICATION.

INTEGRATION GOAL
Enable secure communication between the Docusaurus frontend and a FastAPI backend that serves book-grounded RAG responses.

SYSTEM OVERVIEW
Frontend: Docusaurus static site
Backend: Separate FastAPI service
Communication: HTTP JSON API
Security: No API keys on frontend

IMPLEMENTATION PLAN

Step 1: Backend Readiness
Ensure FastAPI service exposes a single chat endpoint and connects to the RAG pipeline.

Step 2: CORS Configuration
Enable CORS in FastAPI to allow requests from the Docusaurus domain.

Step 3: API Contract
Define a stable request/response schema for chat queries and answers.

Step 4: Frontend Integration
Add a minimal chat UI in Docusaurus that sends queries to the backend API and displays responses.

Step 5: Environment Configuration
Make backend API URL configurable via environment variables.

Step 6: Validation
Test end-to-end flow: user query → backend → grounded answer → UI display.

QUALITY CONTROL
Ensure responses are book-grounded.
Handle missing answers clearly.
Do not expose secrets or backend logic to the frontend.

OUTPUT REQUIREMENTS
Produce an execution plan only.
No code, commands, specs, or tasks.

End with:
Frontend–Backend Integration Plan Completion Criteria

## Response snapshot

**Plan Created**: `specs/006-frontend-backend-integration/plan.md`

### Summary

Created comprehensive implementation plan for connecting Docusaurus frontend to FastAPI RAG backend with:

**Technical Context**:
- Frontend: TypeScript/React/Docusaurus
- Backend: Python 3.11+ with FastAPI, Cohere, Qdrant
- Architecture: Stateless, decoupled, CORS-enabled

**Constitution Check**: ✅ PASS - All 10 principles satisfied, no violations

**6-Step Execution Plan**:
1. Backend Readiness ✅ (complete from feature 005)
2. CORS Configuration (environment-variable-driven whitelist)
3. API Contract Validation (verify existing /query endpoint)
4. Frontend Integration (connect ChatWidget, error handling, retry logic)
5. Environment Configuration (API_URL in frontend, CORS_ORIGINS in backend)
6. Validation (7 test scenarios from spec.md)

**Phase 0 - Research** (4 decisions documented):
- R1: Environment variables (Docusaurus customFields pattern)
- R2: CORS configuration (whitelist from env var, Railway + Vercel origins)
- R3: Error handling (single retry, 10s timeout, categorized messages)
- R4: Deployment platform (Railway selected for backend)

**Phase 1 - Design & Contracts**:
- Data model: QueryRequest, QueryResponse, SourceReference, ErrorResponse
- API contract: OpenAPI 3.0 spec with /query, /health, /collection/info endpoints
- Quickstart guide: Setup instructions, 7 test scenarios, 6 troubleshooting guides

**Key Decisions**:
- Stateless backend (no session storage)
- Environment-variable-driven configuration (portability)
- Single retry on failure (balance UX and latency)
- Railway deployment (free tier, Python support, GitHub integration)
- CORS whitelist for security (no wildcard origins)

**Performance Goals**:
- 95% queries <5 seconds
- Frontend bundle <100KB increase
- Page load <500ms increase
- 50 concurrent users supported

**Security**:
- No API keys in frontend
- CORS whitelist prevents unauthorized origins
- HTTPS enforced in production
- Input validation on both sides

### Artifacts Generated

1. **plan.md** (675 lines): Complete implementation plan with Technical Context, Constitution Check, 6-step execution plan, test scenarios
2. **research.md** (250+ lines): 4 research decisions with rationale, alternatives, implementation notes
3. **data-model.md** (350+ lines): 4 entities with schemas, validation rules, examples, state transitions
4. **contracts/query-api.yaml** (450+ lines): OpenAPI 3.0 spec with 3 endpoints, 5 examples, complete schemas
5. **quickstart.md** (400+ lines): Setup guide with 13 steps, 7 test scenarios, 6 troubleshooting guides, 15-item checklist

### Readiness Status

- [x] All NEEDS CLARIFICATION items resolved
- [x] Constitution Check passed
- [x] Project structure documented with real paths
- [x] Integration steps defined with clear objectives
- [x] Test scenarios extracted from spec.md
- [x] Research complete (4 decisions)
- [x] Data model defined (4 entities)
- [x] API contract created (OpenAPI spec)
- [x] Quickstart guide created

**Next Step**: Run `/sp.tasks` to generate task breakdown with acceptance criteria

## Outcome

- ✅ Impact: Complete implementation plan created with research, design, and contracts for frontend-backend integration. All Phase 0 and Phase 1 deliverables complete. Ready for task generation.
- 🧪 Tests: No automated tests (planning phase). Manual testing scenarios defined in quickstart.md (7 scenarios).
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, query-api.yaml, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks with 6 phases (Backend Config, Frontend Config, API Integration, Error Handling, Testing, Deployment)
- 🧠 Reflection: Plan comprehensively addresses all spec requirements. Step 5 (Environment Configuration) explicitly included as user requested. Constitution check passed without violations. Research phase resolved all technical unknowns. API contract validated against existing implementation. Quickstart provides clear testing path.

## Evaluation notes (flywheel)

- Failure modes observed: None. Initial prompt missing Step 5 (Environment Configuration) - user corrected before execution. PowerShell create-phr.ps1 script does not exist - used agent-native PHR creation as fallback per workflow.
- Graders run and results (PASS/FAIL): PASS - Constitution Check (10/10 principles), PASS - Spec alignment (all 6 integration steps from prompt included), PASS - Completeness (all Phase 0 and Phase 1 artifacts generated)
- Prompt variant (if applicable): Standard /sp.plan workflow with constitution-driven architecture
- Next experiment (smallest change to try): Generate tasks.md with /sp.tasks to validate plan completeness and identify any missing implementation details before coding begins
