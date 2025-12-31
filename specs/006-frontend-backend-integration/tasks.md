---
description: "Implementation tasks for frontend-backend integration"
---

# Tasks: Frontend-Backend Integration for RAG Chatbot

**Input**: Design documents from `/specs/006-frontend-backend-integration/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: No automated tests - manual testing only per spec requirements (manual testing in browser)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This project uses **web application structure**:
- **Backend**: `physical-ai-textbook/rag-backend/`
- **Frontend**: `physical-ai-textbook/docs/`

---

## Phase 1: Setup (Backend Configuration)

**Purpose**: Configure backend for frontend cross-origin requests

**Note**: Backend RAG pipeline already exists from feature 005. This phase only adds CORS and environment documentation.

- [x] T001 Update physical-ai-textbook/rag-backend/.env.example to document CORS_ORIGINS variable
- [x] T002 Update physical-ai-textbook/rag-backend/.env with production CORS origins (localhost + Vercel URL)
- [x] T003 Verify CORS configuration in physical-ai-textbook/rag-backend/main_cohere.py (lines 29-37)

**Checkpoint**: Backend ready to accept cross-origin requests from frontend

---

## Phase 2: Foundational (Frontend Environment Configuration)

**Purpose**: Configure frontend to connect to backend API URL

**⚠️ CRITICAL**: No user story work can begin until frontend knows where backend is deployed

- [x] T004 Create physical-ai-textbook/docs/.env.development with API_URL=http://localhost:8001
- [x] T005 Create physical-ai-textbook/docs/.env.production with placeholder for backend URL
- [x] T006 Update physical-ai-textbook/docs/docusaurus.config.js to expose API_URL via customFields
- [x] T007 [P] Add .env.development and .env.production to physical-ai-textbook/docs/.gitignore

**Checkpoint**: Frontend configuration ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Ask Question and Receive Grounded Answer (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask questions via ChatWidget and receive book-grounded answers with source citations from the backend API.

**Independent Test**: Open http://localhost:3000, click chat button, ask "What is ROS 2?", verify response includes textbook content with clickable source links that navigate to correct sections.

### Implementation for User Story 1

- [x] T008 [US1] Read API_URL from Docusaurus config in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T009 [US1] Implement fetch call to POST /query endpoint in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T010 [US1] Add request body with question, mode, persona fields in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T011 [US1] Parse QueryResponse JSON (answer, sources, confidence) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T012 [US1] Display answer text in message bubble in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T013 [US1] Render sources list with clickable links in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T014 [US1] Add loading indicator (typing dots) during API call in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T015 [US1] Disable input field while query is processing in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx

**Manual Test Checklist for US1**:
- [ ] MT001 [US1] Chat button visible on all pages
- [ ] MT002 [US1] Chat panel opens with welcome message on button click
- [ ] MT003 [US1] Query "What is ROS 2?" returns grounded answer within 5 seconds
- [ ] MT004 [US1] Response displays source citations with chapter and section titles
- [ ] MT005 [US1] Clicking source link navigates to correct textbook section
- [ ] MT006 [US1] Loading indicator appears during API call

**Checkpoint**: User Story 1 complete - basic query/response flow working with source citations

---

## Phase 4: User Story 2 - Handle Out-of-Scope Questions Gracefully (Priority: P1)

**Goal**: Display clear "not covered" messages when user asks questions outside textbook scope, preventing hallucination.

**Independent Test**: Ask "What is the best pizza in New York?", verify response clearly states topic not covered with suggestions.

### Implementation for User Story 2

- [x] T016 [US2] Handle confidence="none" responses in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T017 [US2] Display "not covered" message styling (distinct from normal answers) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T018 [US2] Handle confidence="low" responses with warning indicator in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T019 [US2] Style confidence badges (high/medium/low/none) in physical-ai-textbook/docs/src/components/ChatWidget/styles.css

**Manual Test Checklist for US2**:
- [ ] MT007 [US2] Out-of-scope question "best pizza in NYC" returns clear "not covered" message
- [ ] MT008 [US2] "Not covered" message includes suggestions (ROS 2, Gazebo, Isaac, VLA)
- [ ] MT009 [US2] No hallucinated content in out-of-scope responses
- [ ] MT010 [US2] Low confidence responses show uncertainty indicator

**Checkpoint**: User Story 2 complete - out-of-scope questions handled gracefully

---

## Phase 5: User Story 3 - Resume Conversation Across Page Navigation (Priority: P2)

**Goal**: Preserve chat history when user navigates between textbook pages within same browser session.

**Independent Test**: Ask question on Chapter 1 page, navigate to Chapter 3, verify chat history preserved and can continue conversation.

### Implementation for User Story 3

- [x] T020 [US3] Implement conversation state management using browser sessionStorage in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T021 [US3] Save messages to sessionStorage after each query/response in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T022 [US3] Load messages from sessionStorage on component mount in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T023 [US3] Preserve chat panel open/closed state across page navigation in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T024 [US3] Add "Clear History" button to reset conversation in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx

**Manual Test Checklist for US3**:
- [ ] MT011 [US3] Ask question on Chapter 1, navigate to Chapter 3, verify history preserved
- [ ] MT012 [US3] Close chat panel, navigate to different page, reopen panel, verify history restored
- [ ] MT013 [US3] Ask follow-up question after navigation, verify context maintained
- [ ] MT014 [US3] Clear history button removes all messages
- [ ] MT015 [US3] History clears when browser tab/window closes

**Checkpoint**: User Story 3 complete - conversation persists across navigation

---

## Phase 6: User Story 4 - Receive Persona-Adapted Responses (Priority: P3)

**Goal**: Allow readers to select expertise level (beginner, software engineer, robotics student, AI researcher) for tailored explanations.

**Independent Test**: Select "Beginner" persona, ask "What is ROS 2?", verify response uses simple analogies without jargon.

### Implementation for User Story 4

- [x] T025 [US4] Add persona dropdown to chat header in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T026 [US4] Populate dropdown with 4 persona options (beginner, software_engineer, robotics_student, ai_researcher) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T027 [US4] Include selected persona in query request payload in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T028 [US4] Save selected persona to sessionStorage for persistence in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T029 [US4] Style persona dropdown to match Teal & Navy theme in physical-ai-textbook/docs/src/components/ChatWidget/styles.css

**Manual Test Checklist for US4**:
- [ ] MT016 [US4] Select "Beginner" persona, ask "What is ROS 2?", verify simple explanations
- [ ] MT017 [US4] Select "AI Researcher" persona, ask same question, verify technical depth
- [ ] MT018 [US4] Persona selection persists across page navigation
- [ ] MT019 [US4] Default persona (none selected) works correctly
- [ ] MT020 [US4] Dropdown styling matches existing chat widget theme

**Checkpoint**: User Story 4 complete - persona adaptation working

---

## Phase 7: Error Handling & Edge Cases

**Purpose**: Handle network failures, timeouts, malformed responses, and edge cases

**Dependencies**: All user stories must be implemented before comprehensive error handling

- [x] T030 Implement 10-second timeout using AbortController in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T031 [P] Add retry logic (single retry on failure) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T032 [P] Handle network failure errors (Failed to fetch) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T033 [P] Handle timeout errors (AbortError) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T034 [P] Handle 400 Bad Request errors in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T035 [P] Handle 500 Internal Server Error in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T036 [P] Handle JSON parse errors (malformed response) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T037 Display user-friendly error messages for each error type in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T038 [P] Prevent empty/whitespace-only query submission in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T039 [P] Prevent submission of queries >1000 characters in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T040 Cancel in-flight requests on component unmount in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx
- [x] T041 Handle rapid-fire queries (debounce or queue) in physical-ai-textbook/docs/src/components/ChatWidget/index.tsx

**Manual Test Checklist for Error Handling**:
- [ ] MT021 Stop backend, verify "connection lost" message appears
- [ ] MT022 Submit empty query, verify submission prevented
- [ ] MT023 Submit 1001-char query, verify submission prevented or truncated
- [ ] MT024 Submit 5 rapid queries, verify sequential processing
- [ ] MT025 Navigate away during query, verify no memory leaks

**Checkpoint**: Error handling complete - all edge cases covered

---

## Phase 8: Polish & Deployment Preparation

**Purpose**: Final touches for production deployment

- [x] T042 [P] Test on mobile devices (375px width) and verify responsive layout in physical-ai-textbook/docs/src/components/ChatWidget/styles.css
- [x] T043 [P] Verify dark mode support in physical-ai-textbook/docs/src/components/ChatWidget/styles.css
- [x] T044 [P] Check browser compatibility (Chrome, Firefox, Safari, Edge - last 2 versions)
- [x] T045 [P] Measure frontend bundle size increase (<100KB requirement)
- [x] T046 [P] Measure page load time impact (<500ms requirement)
- [x] T047 Update physical-ai-textbook/docs/.env.production with deployed backend URL (Railway)
- [x] T048 Verify CORS_ORIGINS in backend .env includes production Vercel URL
- [ ] T049 Deploy backend to Railway and verify /health endpoint
- [ ] T050 Update frontend environment variables in Vercel dashboard
- [ ] T051 Deploy frontend to Vercel and test production integration
- [ ] T052 Run complete end-to-end test suite on production URLs
- [x] T053 [P] Document deployment process in physical-ai-textbook/README.md
- [x] T054 [P] Update physical-ai-textbook/rag-backend/.env.example with all required variables

**Manual Test Checklist for Production**:
- [ ] MT026 Test production site on mobile (375px+)
- [ ] MT027 Test production site in dark mode
- [ ] MT028 Test production site across all target browsers
- [ ] MT029 Verify response times <5s for 95% of queries (use DevTools)
- [ ] MT030 Verify no API keys visible in browser Network tab
- [ ] MT031 Verify HTTPS enforced (no mixed content warnings)
- [ ] MT032 Verify source links work on production site
- [ ] MT033 Test all 4 user stories on production URLs

**Checkpoint**: Feature complete and deployed

---

## Implementation Strategy

### MVP Scope (Recommended First Delivery)

**User Story 1 only** (Phase 3):
- Basic query/response with source citations
- Loading indicator
- Minimal error handling (network failure only)

**Rationale**: This delivers core value - readers can ask questions and get book-grounded answers. All other features build on this foundation.

**Timeline**: Phases 1-3 (Tasks T001-T015) = ~15 tasks

### Incremental Delivery

After MVP:
1. **Add US2** (Phase 4): Out-of-scope handling - 4 tasks
2. **Add US3** (Phase 5): Conversation persistence - 5 tasks
3. **Add US4** (Phase 6): Persona adaptation - 5 tasks
4. **Add Error Handling** (Phase 7): Comprehensive edge cases - 12 tasks
5. **Polish & Deploy** (Phase 8): Production readiness - 13 tasks

**Total**: 54 implementation tasks + 33 manual test items

---

## Dependencies & Parallel Execution

### Phase Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1) ← Must complete first (MVP)
    ↓
Phase 4 (US2) ← Can run in parallel with US3 and US4
Phase 5 (US3) ← Can run in parallel with US2 and US4
Phase 6 (US4) ← Can run in parallel with US2 and US3
    ↓
Phase 7 (Error Handling) ← Requires all user stories complete
    ↓
Phase 8 (Polish & Deploy)
```

### User Story Independence

- **US1**: No dependencies (foundational)
- **US2**: Depends on US1 (extends query handling)
- **US3**: Independent of US2 and US4 (session management)
- **US4**: Independent of US2 and US3 (persona handling)

**Parallel Opportunities**:
After US1 is complete, US2, US3, and US4 can be implemented in parallel by different developers.

### Task-Level Parallelization

**Within US1** (Phase 3):
- T008-T015 are sequential (all modify index.tsx)

**Within US2** (Phase 4):
- T016-T018 modify index.tsx (sequential)
- T019 modifies styles.css (can run in parallel with T016-T018)

**Within US3** (Phase 5):
- T020-T024 are sequential (state management dependencies)

**Within US4** (Phase 6):
- T025-T028 modify index.tsx (sequential)
- T029 modifies styles.css (can run in parallel with T025-T028)

**Within Phase 7** (Error Handling):
- T030-T036 can run in parallel (different error types)
- T037 must complete after T030-T036 (displays errors)
- T038-T041 can run in parallel after T037

**Within Phase 8** (Polish):
- T042-T046 can run in parallel (independent checks)
- T047-T051 are sequential (deployment order)
- T052 must complete after T051 (tests deployed site)
- T053-T054 can run in parallel (documentation)

### Example Parallel Execution

**Developer A** (US2):
- T016: Handle confidence="none"
- T017: Style "not covered" messages
- T018: Handle confidence="low"

**Developer B** (US3):
- T020: SessionStorage state management
- T021: Save messages to storage
- T022: Load messages on mount

**Developer C** (US4):
- T025: Add persona dropdown
- T026: Populate dropdown options
- T027: Include persona in request

**Developer D** (CSS):
- T019: Confidence badge styles (US2)
- T029: Persona dropdown styles (US4)

All four developers can work simultaneously after US1 (T001-T015) is complete.

---

## Testing Strategy

**Manual Testing Only** (per spec requirements):
- No automated tests required
- Each user story has independent test criteria
- Manual test checklists provided for each phase (MT001-MT033)
- Use quickstart.md test scenarios for validation

**Test Environments**:
1. **Local Development**: Frontend localhost:3000, Backend localhost:8001
2. **Production**: Frontend vercel.app, Backend railway.app

**Testing Tools**:
- Browser DevTools (Network tab, Console)
- Multiple browsers (Chrome, Firefox, Safari, Edge)
- Mobile device emulation (DevTools responsive mode)
- Performance measurement (Lighthouse, DevTools Performance)

---

## Task Summary

**Total Implementation Tasks**: 54
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 4 tasks
- Phase 3 (US1): 8 tasks
- Phase 4 (US2): 4 tasks
- Phase 5 (US3): 5 tasks
- Phase 6 (US4): 5 tasks
- Phase 7 (Error Handling): 12 tasks
- Phase 8 (Polish & Deploy): 13 tasks

**Total Manual Test Items**: 33
- US1: 6 tests
- US2: 4 tests
- US3: 5 tests
- US4: 5 tests
- Error Handling: 5 tests
- Production: 8 tests

**Parallelizable Tasks**: 21 tasks marked with [P]

**User Story Breakdown**:
- US1 (P1): 8 tasks + 6 tests
- US2 (P1): 4 tasks + 4 tests
- US3 (P2): 5 tasks + 5 tests
- US4 (P3): 5 tasks + 5 tests

**Suggested MVP**: Phases 1-3 only (15 tasks) delivers core query/response functionality

**Files Modified**:
- Backend: physical-ai-textbook/rag-backend/.env.example (T001), .env (T002)
- Frontend Config: physical-ai-textbook/docs/.env.development (T004), .env.production (T005, T047), docusaurus.config.js (T006), .gitignore (T007)
- Frontend Component: physical-ai-textbook/docs/src/components/ChatWidget/index.tsx (T008-T041, most tasks)
- Frontend Styles: physical-ai-textbook/docs/src/components/ChatWidget/styles.css (T019, T029, T042-T043)
- Documentation: physical-ai-textbook/README.md (T053)

---

**Tasks Status**: ✅ READY FOR IMPLEMENTATION

**Next Command**: `/sp.implement` to execute tasks (or manual implementation following this breakdown)
