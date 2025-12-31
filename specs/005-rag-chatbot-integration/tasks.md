# Tasks: RAG Chatbot Integration

**Input**: Design documents from `/specs/005-rag-chatbot-integration/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/rag-api.yaml, research.md, quickstart.md

**Tests**: No automated tests requested. Manual E2E validation during implementation.

**Organization**: Tasks grouped by user story (US1-US5) to enable independent implementation.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- File paths relative to: `physical-ai-textbook/`

---

## Phase 1: Setup

**Purpose**: Prepare project structure and install dependencies for Cohere integration

- [ ] T001 Add Cohere SDK to requirements.txt in rag-backend/requirements.txt
- [ ] T002 [P] Create .env.example with COHERE_API_KEY placeholder in rag-backend/.env.example
- [ ] T003 [P] Update .env with COHERE_API_KEY in rag-backend/.env
- [ ] T004 Verify Cohere API connection with test script

**Checkpoint**: Cohere SDK installed and API connection verified

---

## Phase 2: Foundational (Embedding Pipeline)

**Purpose**: Create Cohere embedding service and index textbook content

**CRITICAL**: All user stories require indexed content to function

### Cohere Embedding Service

- [ ] T005 Create CohereEmbeddingService class in rag-backend/embedding_cohere.py
- [ ] T006 [P] Implement embed_documents() method for document embeddings in rag-backend/embedding_cohere.py
- [ ] T007 [P] Implement embed_query() method for query embeddings in rag-backend/embedding_cohere.py
- [ ] T008 Update qdrant_service.py vector_size to 1024 for Cohere in rag-backend/qdrant_service.py

### Content Indexing

- [ ] T009 Audit all 12 chapter files for consistent frontmatter in docs/docs/
- [ ] T010 Create embed_chapters_cohere.py script in scripts/embed_chapters_cohere.py
- [ ] T011 [P] Implement semantic chunking by H2 sections in scripts/embed_chapters_cohere.py
- [ ] T012 [P] Implement metadata preservation (chapter, section, URL) in scripts/embed_chapters_cohere.py
- [ ] T013 Run embedding script to index all chapters to Qdrant Cloud
- [ ] T014 Verify all chunks indexed with collection info endpoint

**Checkpoint**: ~100 chunks indexed in Qdrant Cloud with Cohere embeddings

---

## Phase 3: User Story 1 - Global Mode Query (Priority: P1) MVP

**Goal**: Enable users to ask questions about any chapter and receive grounded answers

**Independent Test**: Ask "What is ROS 2?" and verify response matches Module 1, Chapter 1 content

### Cohere Chat Service

- [ ] T015 [US1] Create CohereChatService class in rag-backend/chat_cohere.py
- [ ] T016 [P] [US1] Implement generate_response() method with grounding prompt in rag-backend/chat_cohere.py
- [ ] T017 [P] [US1] Implement _build_preamble() method for system prompt in rag-backend/chat_cohere.py

### Query Endpoint

- [ ] T018 [US1] Create main_cohere.py FastAPI application in rag-backend/main_cohere.py
- [ ] T019 [P] [US1] Define QueryRequest Pydantic model in rag-backend/main_cohere.py
- [ ] T020 [P] [US1] Define QueryResponse Pydantic model in rag-backend/main_cohere.py
- [ ] T021 [P] [US1] Define SourceReference Pydantic model in rag-backend/main_cohere.py
- [ ] T022 [US1] Implement POST /query endpoint for global mode in rag-backend/main_cohere.py
- [ ] T023 [US1] Implement query embedding using CohereEmbeddingService in rag-backend/main_cohere.py
- [ ] T024 [US1] Implement Qdrant similarity search in /query endpoint in rag-backend/main_cohere.py
- [ ] T025 [US1] Implement response generation using CohereChatService in rag-backend/main_cohere.py

### Source Attribution

- [ ] T026 [US1] Build source references from retrieved chunks in rag-backend/main_cohere.py
- [ ] T027 [US1] Include source attribution in QueryResponse in rag-backend/main_cohere.py

### Confidence Scoring

- [ ] T028 [US1] Implement confidence scoring based on similarity thresholds in rag-backend/main_cohere.py
- [ ] T029 [US1] Add confidence field to QueryResponse in rag-backend/main_cohere.py

### Validation

- [ ] T030 [US1] Test global query "What is ROS 2?" returns Module 1 content
- [ ] T031 [US1] Test global query "What is a digital twin?" returns Module 2 content
- [ ] T032 [US1] Verify response time < 5 seconds

**Checkpoint**: User Story 1 complete - global mode queries working with source attribution

---

## Phase 4: User Story 3 - Grounded Responses Only (Priority: P1)

**Goal**: Ensure chatbot declines out-of-scope questions and never hallucinates

**Independent Test**: Ask "What is the latest Tesla robot model?" and verify chatbot declines to answer

### No Results Handling

- [ ] T033 [US3] Implement no-results detection in /query endpoint in rag-backend/main_cohere.py
- [ ] T034 [US3] Return clear "not found" message when no chunks retrieved in rag-backend/main_cohere.py
- [ ] T035 [US3] Add suggestion to rephrase question in error response in rag-backend/main_cohere.py

### Low Confidence Handling

- [ ] T036 [US3] Implement low-confidence detection (score < 0.7) in rag-backend/main_cohere.py
- [ ] T037 [US3] Add uncertainty indicator in response for marginal scores in rag-backend/main_cohere.py

### Grounding Enforcement

- [ ] T038 [US3] Add strict grounding instructions to system prompt in rag-backend/chat_cohere.py
- [ ] T039 [US3] Implement "textbook doesn't cover" partial response in rag-backend/chat_cohere.py

### Validation

- [ ] T040 [US3] Test out-of-scope question "What is latest Tesla robot?" returns decline
- [ ] T041 [US3] Test partially covered topic returns partial answer with caveat
- [ ] T042 [US3] Verify no hallucinated content in responses

**Checkpoint**: User Story 3 complete - grounding validated, hallucination prevented

---

## Phase 5: User Story 2 - Selected-Text Mode (Priority: P2)

**Goal**: Enable users to ask questions about highlighted text passages only

**Independent Test**: Select code example, ask "What does this code do?", verify focused response

### Mode Parameter

- [ ] T043 [US2] Add mode parameter validation (global/selected) in rag-backend/main_cohere.py
- [ ] T044 [US2] Add selected_text parameter to QueryRequest in rag-backend/main_cohere.py
- [ ] T045 [US2] Require selected_text when mode="selected" in rag-backend/main_cohere.py

### Selected-Text Processing

- [ ] T046 [US2] Implement selected-text embedding in /query endpoint in rag-backend/main_cohere.py
- [ ] T047 [US2] Implement search restricted to selected text context in rag-backend/main_cohere.py
- [ ] T048 [US2] Implement text length validation (10-5000 chars) in rag-backend/main_cohere.py

### Fallback Handling

- [ ] T049 [US2] Implement fallback when selected text lacks answer in rag-backend/main_cohere.py
- [ ] T050 [US2] Offer to search full book when selected mode fails in rag-backend/main_cohere.py

### Validation

- [ ] T051 [US2] Test selected-text query on code block
- [ ] T052 [US2] Test selected-text query on paragraph
- [ ] T053 [US2] Test fallback when unrelated question asked on selection

**Checkpoint**: User Story 2 complete - selected-text mode working with fallback

---

## Phase 6: User Story 4 - Source Attribution UI (Priority: P2)

**Goal**: Display clickable source references that navigate to textbook sections

**Independent Test**: Ask any question and verify response includes clickable chapter/section links

### Frontend ChatWidget Component

- [ ] T054 [US4] Create ChatWidget component directory in docs/src/components/ChatWidget/
- [ ] T055 [US4] Create ChatWidget index.tsx main component in docs/src/components/ChatWidget/index.tsx
- [ ] T056 [P] [US4] Create ChatPanel.tsx for chat UI in docs/src/components/ChatWidget/ChatPanel.tsx
- [ ] T057 [P] [US4] Create styles.css for widget styling in docs/src/components/ChatWidget/styles.css

### Chat UI Elements

- [ ] T058 [US4] Implement floating chat button (collapsed state) in docs/src/components/ChatWidget/index.tsx
- [ ] T059 [US4] Implement collapsible chat panel (bottom-right) in docs/src/components/ChatWidget/ChatPanel.tsx
- [ ] T060 [P] [US4] Implement message history display in docs/src/components/ChatWidget/ChatPanel.tsx
- [ ] T061 [P] [US4] Implement loading/error states in docs/src/components/ChatWidget/ChatPanel.tsx

### Source Links

- [ ] T062 [US4] Display source references as clickable links in docs/src/components/ChatWidget/ChatPanel.tsx
- [ ] T063 [US4] Navigate to textbook section on source click in docs/src/components/ChatWidget/ChatPanel.tsx

### Theme Integration

- [ ] T064 [US4] Style widget to match Teal & Navy theme in docs/src/components/ChatWidget/styles.css
- [ ] T065 [US4] Create Root.tsx for global widget injection in docs/src/theme/Root.tsx

### Validation

- [ ] T066 [US4] Test widget renders on all pages
- [ ] T067 [US4] Test source links navigate to correct sections
- [ ] T068 [US4] Verify bundle size < 100KB addition

**Checkpoint**: User Story 4 complete - chat widget with clickable source attribution

---

## Phase 7: User Story 5 - Persona-Aware Responses (Priority: P3)

**Goal**: Adapt response complexity based on user's selected expertise level

**Independent Test**: Set persona to "AI Researcher" and verify responses assume AI knowledge

### Persona Definitions

- [ ] T069 [US5] Create personas.py with Persona dataclass in rag-backend/personas.py
- [ ] T070 [P] [US5] Define Beginner persona with prompt modifier in rag-backend/personas.py
- [ ] T071 [P] [US5] Define Software Engineer persona in rag-backend/personas.py
- [ ] T072 [P] [US5] Define Robotics Student persona in rag-backend/personas.py
- [ ] T073 [P] [US5] Define AI Researcher persona in rag-backend/personas.py

### Persona Integration

- [ ] T074 [US5] Add persona parameter to QueryRequest in rag-backend/main_cohere.py
- [ ] T075 [US5] Pass persona to CohereChatService.generate_response() in rag-backend/main_cohere.py
- [ ] T076 [US5] Apply persona prompt modifier in _build_preamble() in rag-backend/chat_cohere.py

### Frontend Persona Selection

- [ ] T077 [US5] Add persona dropdown to ChatWidget in docs/src/components/ChatWidget/ChatPanel.tsx
- [ ] T078 [US5] Send selected persona with query requests in docs/src/components/ChatWidget/index.tsx
- [ ] T079 [US5] Remember persona preference in session in docs/src/components/ChatWidget/index.tsx

### Validation

- [ ] T080 [US5] Test Beginner persona explains from fundamentals
- [ ] T081 [US5] Test Software Engineer persona uses programming analogies
- [ ] T082 [US5] Test AI Researcher persona assumes ML knowledge

**Checkpoint**: User Story 5 complete - persona-aware responses working

---

## Phase 8: Frontend Integration (Mode Toggle)

**Purpose**: Complete frontend with mode toggle and text selection detection

### Mode Toggle

- [ ] T083 Add mode toggle switch (Global/Selected) in docs/src/components/ChatWidget/ChatPanel.tsx
- [ ] T084 [P] Implement mode state management in docs/src/components/ChatWidget/index.tsx
- [ ] T085 Send mode with query requests in docs/src/components/ChatWidget/index.tsx

### Text Selection

- [ ] T086 Implement text selection detection on page in docs/src/components/ChatWidget/index.tsx
- [ ] T087 Auto-switch to Selected-Text mode on selection in docs/src/components/ChatWidget/index.tsx
- [ ] T088 Pass selected text to query endpoint in docs/src/components/ChatWidget/index.tsx

### Validation

- [ ] T089 Test mode toggle switches between global/selected
- [ ] T090 Test text selection triggers selected mode
- [ ] T091 Test selected text passed correctly to API

**Checkpoint**: Frontend integration complete - full chat functionality

---

## Phase 9: Polish & Cross-Cutting Validation

**Purpose**: Final validation, security, and deployment readiness

### API Endpoints

- [ ] T092 Implement GET /health endpoint in rag-backend/main_cohere.py
- [ ] T093 [P] Implement GET /collection/info endpoint in rag-backend/main_cohere.py
- [ ] T094 [P] Implement POST /embed admin endpoint in rag-backend/main_cohere.py

### Security

- [ ] T095 Verify API keys only in backend .env in rag-backend/
- [ ] T096 [P] Implement input validation and sanitization in rag-backend/main_cohere.py
- [ ] T097 [P] Configure CORS for allowed origins in rag-backend/main_cohere.py

### Edge Cases

- [ ] T098 Test empty message returns "Please enter a question"
- [ ] T099 [P] Test very long input (>1000 chars) handled gracefully
- [ ] T100 [P] Test concurrent requests (simulate 5+ simultaneous)

### Error Handling

- [ ] T101 Implement graceful error handling for Cohere API failures in rag-backend/main_cohere.py
- [ ] T102 [P] Implement graceful error handling for Qdrant failures in rag-backend/main_cohere.py
- [ ] T103 Display user-friendly error messages in frontend in docs/src/components/ChatWidget/ChatPanel.tsx

### Final Build

- [ ] T104 Run npm run build in docs/ - verify no errors
- [ ] T105 Test production build locally
- [ ] T106 Deploy updated site to Vercel
- [ ] T107 Verify chatbot operational on live site

**Checkpoint**: RAG chatbot complete and deployed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 - BLOCKS all user stories
- **US1 Global Query (Phase 3)**: Depends on Phase 2 completion - MVP
- **US3 Grounding (Phase 4)**: Depends on Phase 3 - extends /query endpoint
- **US2 Selected-Text (Phase 5)**: Depends on Phase 3 - adds mode parameter
- **US4 Source UI (Phase 6)**: Can start after Phase 3 - frontend work
- **US5 Personas (Phase 7)**: Depends on Phases 3+6 - bonus feature
- **Frontend Integration (Phase 8)**: Depends on Phases 4+5+6
- **Polish (Phase 9)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Foundation for all other stories - MVP
- **US3 (P1)**: Extends US1 with grounding validation
- **US2 (P2)**: Extends US1 with selected-text mode
- **US4 (P2)**: Frontend can parallel with US2/US3 backend work
- **US5 (P3)**: Bonus feature, depends on US1+US4

**Key Insight**: US1 is the MVP. US4 (frontend) can start while US2/US3 backend work proceeds in parallel.

---

## Parallel Execution Examples

### Phase 2: Foundational (Backend + Scripts)

```
Stream 1: T005, T006, T007, T008 (Cohere service)
Stream 2: T009, T010, T011, T012 (Embedding script)
Converge: T013, T014 (Run embedding)
```

### Phase 3: US1 Global Query

```
Stream 1: T015, T016, T017 (Chat service)
Stream 2: T019, T020, T021 (Pydantic models)
Converge: T018, T022-T029 (Endpoint implementation)
```

### Phase 6 + Phase 5: Frontend + Selected-Text Mode

```
Stream 1: T054-T068 (US4 Frontend)
Stream 2: T043-T053 (US2 Backend)
Both can proceed after US1 complete
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T014)
3. Complete Phase 3: User Story 1 (T015-T032)
4. **STOP and VALIDATE**: Global mode RAG working
5. Can deploy MVP with just global query capability

### Incremental Delivery

1. Setup + Foundational → Cohere embeddings indexed
2. Add US1 (Global Query) → Core RAG functionality
3. Add US3 (Grounding) → No hallucination guarantee
4. Add US2 (Selected-Text) → Contextual queries
5. Add US4 (Source UI) → Frontend with attribution
6. Add US5 (Personas) → Personalization bonus
7. Polish → Security and deployment

---

## Summary

| Phase | Tasks | Parallel Tasks | Purpose |
|-------|-------|----------------|---------|
| Setup | 4 | 2 | Cohere SDK setup |
| Foundational | 10 | 4 | Embedding pipeline |
| US1 (P1) | 18 | 8 | Global mode query |
| US3 (P1) | 10 | 0 | Grounding validation |
| US2 (P2) | 11 | 0 | Selected-text mode |
| US4 (P2) | 15 | 6 | Frontend + sources |
| US5 (P3) | 14 | 8 | Persona-aware |
| Frontend | 9 | 2 | Mode toggle |
| Polish | 16 | 7 | Security + deploy |
| **Total** | **107** | **37** | |

**MVP Scope**: Phases 1-3 (32 tasks) delivers core global query RAG functionality
**Full Scope**: All phases (107 tasks) delivers complete RAG chatbot with all features
