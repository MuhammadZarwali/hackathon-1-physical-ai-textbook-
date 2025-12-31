---
id: 002
title: Frontend-Backend Integration Tasks
stage: tasks
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: 006-frontend-backend-integration
branch: 006-frontend-backend-integration
user: MuhammadZarwali
command: /sp.tasks
labels: ["task-generation", "user-stories", "implementation", "testing", "deployment"]
links:
  spec: specs/006-frontend-backend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/006-frontend-backend-integration/tasks.md
tests:
  - 33 manual test items defined (MT001-MT033)
---

## Prompt

Generate implementation tasks for frontend-backend integration feature based on:
- spec.md with 4 user stories (US1-P1, US2-P1, US3-P2, US4-P3)
- plan.md with 6-step execution plan
- research.md with 4 technical decisions
- data-model.md with API contract
- contracts/query-api.yaml with OpenAPI spec

Requirements:
- Organize tasks by user story for independent implementation
- Manual testing only (no automated tests per spec)
- Include exact file paths
- Mark parallelizable tasks with [P]
- Label tasks with user story (US1, US2, US3, US4)
- Provide MVP scope guidance
- Include dependency graph

## Response snapshot

**Tasks Created**: `specs/006-frontend-backend-integration/tasks.md`

### Task Organization

**8 Phases** organized by user story priority:

1. **Phase 1: Setup (Backend Configuration)** - 3 tasks
   - CORS configuration
   - Environment documentation
   - Backend readiness verification

2. **Phase 2: Foundational (Frontend Environment)** - 4 tasks
   - Environment variables (.env.development, .env.production)
   - Docusaurus config for API_URL
   - Gitignore updates

3. **Phase 3: User Story 1 (P1) - Query & Response** 🎯 MVP - 8 tasks
   - Fetch API integration
   - Request/response parsing
   - Message display
   - Source citations
   - Loading indicator

4. **Phase 4: User Story 2 (P1) - Out-of-Scope Handling** - 4 tasks
   - Confidence level handling
   - "Not covered" message styling
   - Low confidence warnings
   - Confidence badges

5. **Phase 5: User Story 3 (P2) - Conversation Persistence** - 5 tasks
   - SessionStorage state management
   - Message save/load
   - Panel state persistence
   - Clear history button

6. **Phase 6: User Story 4 (P3) - Persona Adaptation** - 5 tasks
   - Persona dropdown UI
   - Persona selection integration
   - Request payload inclusion
   - SessionStorage persistence
   - Theme styling

7. **Phase 7: Error Handling & Edge Cases** - 12 tasks
   - Timeout (10s with AbortController)
   - Retry logic (single retry)
   - Error categorization (network, timeout, 400, 500, parse)
   - Input validation (empty, >1000 chars)
   - Rapid-fire handling

8. **Phase 8: Polish & Deployment** - 13 tasks
   - Mobile responsiveness (375px+)
   - Dark mode verification
   - Browser compatibility
   - Performance checks (<100KB, <500ms)
   - Railway deployment
   - Production testing

### Key Metrics

**Total Tasks**: 54 implementation tasks
**Manual Tests**: 33 test items (MT001-MT033)
**Parallelizable**: 21 tasks marked [P]

**Task Distribution by User Story**:
- US1 (P1): 8 tasks + 6 tests = core query/response
- US2 (P1): 4 tasks + 4 tests = out-of-scope handling
- US3 (P2): 5 tasks + 5 tests = conversation persistence
- US4 (P3): 5 tasks + 5 tests = persona adaptation

**MVP Scope**: Phases 1-3 (15 tasks) = minimal viable chatbot

### Dependencies & Parallelization

**Phase Dependencies**:
```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1) ← MVP baseline
    ↓
Phase 4 (US2) ← Parallel
Phase 5 (US3) ← Parallel
Phase 6 (US4) ← Parallel
    ↓
Phase 7 (Error Handling)
    ↓
Phase 8 (Polish & Deploy)
```

**User Story Independence**:
- US1: Foundational (no dependencies)
- US2: Extends US1 (depends on query flow)
- US3: Independent (session management)
- US4: Independent (persona handling)

After US1 completes, US2/US3/US4 can run in parallel with different developers.

### Files Modified

**Backend** (3 tasks):
- physical-ai-textbook/rag-backend/.env.example (T001)
- physical-ai-textbook/rag-backend/.env (T002)
- physical-ai-textbook/rag-backend/main_cohere.py (T003 verify only)

**Frontend Config** (4 tasks):
- physical-ai-textbook/docs/.env.development (T004)
- physical-ai-textbook/docs/.env.production (T005, T047)
- physical-ai-textbook/docs/docusaurus.config.js (T006)
- physical-ai-textbook/docs/.gitignore (T007)

**Frontend Component** (38 tasks):
- physical-ai-textbook/docs/src/components/ChatWidget/index.tsx (T008-T041, majority)

**Frontend Styles** (4 tasks):
- physical-ai-textbook/docs/src/components/ChatWidget/styles.css (T019, T029, T042-T043)

**Documentation** (2 tasks):
- physical-ai-textbook/README.md (T053)
- physical-ai-textbook/rag-backend/.env.example (T054)

### Testing Strategy

**Manual Testing Only** (per spec requirements):
- No automated tests generated
- 33 manual test items (MT001-MT033)
- Test environments: localhost (dev) + production (Vercel/Railway)
- Tools: Browser DevTools, multi-browser testing, mobile emulation

**Test Coverage**:
- MT001-MT006: US1 basic query/response
- MT007-MT010: US2 out-of-scope handling
- MT011-MT015: US3 conversation persistence
- MT016-MT020: US4 persona adaptation
- MT021-MT025: Error handling
- MT026-MT033: Production deployment

### Implementation Strategy

**Recommended MVP** (Phases 1-3):
- 15 tasks total
- Delivers core value: query → grounded answer with sources
- Estimated effort: 4-6 hours for single developer

**Incremental Delivery**:
1. MVP (US1): 15 tasks → basic chatbot working
2. Add US2: +4 tasks → out-of-scope handling
3. Add US3: +5 tasks → conversation persistence
4. Add US4: +5 tasks → persona adaptation
5. Add Error Handling: +12 tasks → production-grade reliability
6. Polish & Deploy: +13 tasks → production deployment

**Parallel Development** (post-MVP):
- 4 developers can work simultaneously on US2/US3/US4/CSS
- Example: Dev A (US2), Dev B (US3), Dev C (US4), Dev D (styles)

### Format Validation

✅ **All tasks follow checklist format**:
- Checkbox: `- [ ]` present on all 54 tasks
- Task ID: T001-T054 sequential
- [P] marker: 21 tasks marked parallelizable
- [Story] label: US1-US4 labels on user story tasks
- File paths: All tasks include exact paths

✅ **User Story Organization**:
- Each story has dedicated phase
- Independent test criteria per story
- Clear checkpoints after each story

✅ **Dependencies Documented**:
- Phase dependency graph included
- User story independence matrix provided
- Parallel execution examples per phase

## Outcome

- ✅ Impact: Complete task breakdown with 54 implementation tasks organized by 4 user stories. Manual testing strategy with 33 test items. Clear MVP scope (15 tasks). Parallel execution opportunities identified.
- 🧪 Tests: Manual testing only (33 test items). No automated tests per spec requirements. Test environments defined (localhost dev + production).
- 📁 Files: 1 file created (tasks.md). 7 files to be modified during implementation (backend config, frontend config, ChatWidget component/styles, docs).
- 🔁 Next prompts: Run `/sp.implement` to execute tasks, or manually implement following task order. After MVP (T001-T015), can parallelize US2/US3/US4.
- 🧠 Reflection: Tasks successfully organized by user story for independent implementation. MVP clearly defined (US1 only = 15 tasks). Parallel opportunities maximize development efficiency post-MVP. All edge cases from spec covered in Phase 7. Manual testing aligns with spec requirements (no automated tests requested).

## Evaluation notes (flywheel)

- Failure modes observed: None. Task generation aligned with spec user stories, plan execution steps, and available design documents (research, data-model, contracts, quickstart).
- Graders run and results (PASS/FAIL): PASS - Format validation (all 54 tasks follow checklist format with checkbox, ID, story label, file path), PASS - User story organization (4 stories with independent test criteria), PASS - Completeness (all spec requirements covered across 8 phases)
- Prompt variant (if applicable): Standard /sp.tasks workflow with user-story-driven organization
- Next experiment (smallest change to try): Implement MVP (Phases 1-3, tasks T001-T015) to validate task granularity and completeness before proceeding with remaining user stories
