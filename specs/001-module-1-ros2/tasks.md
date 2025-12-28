# Tasks: Module 1 - The Robotic Nervous System (ROS 2)

**Input**: Design documents from `/specs/001-module-1-ros2/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are NOT explicitly requested in the specification. This task list focuses on content creation, RAG implementation, and deployment.

**Organization**: Tasks are grouped by user story (US1, US2, US3) to enable independent implementation and testing of each chapter.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `docs/` (Docusaurus frontend), `rag-backend/` (FastAPI backend), `scripts/` (build utilities)
- Educational content stored in `docs/docs/module-1-ros2/`
- Backend API in `rag-backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Docusaurus project and RAG backend infrastructure

- [x] T001 Create project directory structure per plan.md (docs/, rag-backend/, scripts/, .github/workflows/)
- [x] T002 Initialize Docusaurus project with `npx create-docusaurus@latest Physical AI & Humanoid Robotics` in project root
- [x] T003 [P] Initialize Python virtual environment and install FastAPI dependencies in rag-backend/
- [x] T004 [P] Create .gitignore for Node.js (docs/node_modules/, docs/build/) and Python (rag-backend/venv/, rag-backend/__pycache__/)
- [x] T005 [P] Create .env.example in rag-backend/ with placeholders for OPENAI_API_KEY and QDRANT_URL

**Checkpoint**: Basic project structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY content/RAG work can begin

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Configure Docusaurus for docs-only mode in docs/docusaurus.config.ts (routeBasePath: '/', disable blog)
- [x] T007 Configure GitHub Pages deployment in docs/docusaurus.config.ts (set url, baseUrl, organizationName, projectName)
- [x] T008 [P] Create module directory structure: docs/docs/module-1-ros2/ folder
- [x] T009 [P] Create _category_.json in docs/docs/module-1-ros2/ with module metadata
- [x] T010 [P] Setup FastAPI application structure in rag-backend/main.py with CORS middleware for localhost:3000
- [x] T011 [P] Create Pydantic models in rag-backend/models.py (QueryRequest, QueryResponse, Source, EmbedRequest)
- [x] T012 [P] Setup Qdrant client configuration in rag-backend/qdrant_config.py (Docker or Cloud connection)
- [x] T013 [P] Create Qdrant collection initialization script in scripts/setup_qdrant.py
- [x] T014 [P] Implement /health endpoint in rag-backend/main.py
- [x] T015 Create GitHub Actions workflow in .github/workflows/deploy.yml for Docusaurus deployment to GitHub Pages
- [x] T016 Create intro.md landing page in docs/docs/ with textbook overview
- [x] T017 Test Docusaurus local build with `npm run build` in docs/ directory

**Checkpoint**: ✅ Foundation ready - Docusaurus builds successfully, FastAPI structure ready, GitHub Actions configured. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Understanding ROS 2 Purpose and Architecture (Priority: P1) 🎯 MVP

**Goal**: Deliver Chapter 1 "Introduction to ROS 2" teaching beginners what ROS 2 is, why it exists, and its role in physical AI

**Independent Test**: Learners can explain: (1) what problem ROS 2 solves, (2) why distributed communication matters for robots, (3) how ROS 2 differs from monolithic architectures. Chapter passes constitution compliance checklist.

### Content Creation for User Story 1

- [x] T018 [US1] Create chapter-1-introduction-to-ros2.md in docs/docs/module-1-ros2/ with frontmatter per data-model.md schema
- [x] T019 [US1] Write "Learning Objectives" section in chapter-1-introduction-to-ros2.md (4 objectives per spec FR-007)
- [x] T020 [US1] Write "What is ROS 2?" section in chapter-1-introduction-to-ros2.md (plain language, FR-001, 200-500 words)
- [x] T021 [US1] Write "What Problem ROS 2 Solves" section in chapter-1-introduction-to-ros2.md (modularity, communication, reusability, distributed computation per FR-002, 300-400 words)
- [x] T022 [US1] Write "ROS 2 Architecture Overview" section in chapter-1-introduction-to-ros2.md (high-level, no implementation details per FR-003, 250-350 words)
- [x] T023 [US1] Write "Why ROS 2 Matters for Physical AI" section in chapter-1-introduction-to-ros2.md (FR-004, humanoid use case, 200-300 words)
- [x] T024 [US1] Write "ROS 2 vs ROS 1" section in chapter-1-introduction-to-ros2.md (conceptual comparison per FR-005, 250-350 words)
- [x] T025 [US1] Write "The Nervous System Analogy" section in chapter-1-introduction-to-ros2.md (nodes as neurons per FR-006, 200-300 words)
- [x] T026 [US1] Add persona callouts (:::note For Beginners, :::tip For AI Researchers) in chapter-1-introduction-to-ros2.md
- [x] T027 [US1] Write "Summary" section in chapter-1-introduction-to-ros2.md (3-5 key takeaways per FR-008, 150-200 words)
- [x] T028 [US1] Add "Further Reading" section with citations to docs.ros.org and design.ros2.org in chapter-1-introduction-to-ros2.md

### Validation for User Story 1

- [x] T029 [US1] Verify all ROS 2 concepts in chapter-1-introduction-to-ros2.md against docs.ros.org (cross-reference FR-001 to FR-010 with official docs)
- [x] T030 [US1] Run constitution compliance checklist on chapter-1-introduction-to-ros2.md (Educational Clarity, Technical Accuracy, AI-Native Design, RAG Compatibility)
- [x] T031 [US1] Check translation-readiness: average sentence length <20 words, no idioms/slang in chapter-1-introduction-to-ros2.md
- [x] T032 [US1] Verify semantic chunking: each H2/H3 section is 200-500 words and self-contained in chapter-1-introduction-to-ros2.md
- [x] T033 [US1] Test local Docusaurus build includes Chapter 1 in sidebar navigation

**Checkpoint**: Chapter 1 complete, validated, builds successfully. Learners can understand ROS 2's purpose and architecture. Ready for embedding and RAG integration.

---

## Phase 4: User Story 2 - Mastering ROS 2 Communication Primitives (Priority: P2)

**Goal**: Deliver Chapter 2 "ROS 2 Communication Model" teaching communication primitives (nodes, topics, services, actions)

**Independent Test**: Learners can: (1) diagram sensor-to-actuator data flow using correct primitives, (2) explain when to use topics vs services vs actions, (3) describe publish/subscribe pattern. Chapter passes constitution checklist.

### Content Creation for User Story 2

- [x] T034 [US2] Create chapter-2-ros2-communication-model.md in docs/docs/module-1-ros2/ with frontmatter per data-model.md schema
- [x] T035 [US2] Write "Learning Objectives" section in chapter-2-ros2-communication-model.md (focus on communication primitives)
- [x] T036 [US2] Write "Nodes: The Computational Units" section in chapter-2-ros2-communication-model.md (FR-011, executors per FR-018, 250-350 words)
- [x] T037 [US2] Write "Topics and Publish/Subscribe" section in chapter-2-ros2-communication-model.md (FR-012, many-to-many messaging, 300-400 words)
- [x] T038 [US2] Write "Services: Request/Response Communication" section in chapter-2-ros2-communication-model.md (FR-013, synchronous, blocking, 250-350 words)
- [x] T039 [US2] Write "Actions: Long-Running Tasks with Feedback" section in chapter-2-ros2-communication-model.md (FR-014, feedback, cancellation, 300-400 words)
- [x] T040 [US2] Write "Comparing Communication Primitives" section in chapter-2-ros2-communication-model.md (FR-015, decision criteria table, 250-350 words)
- [x] T041 [US2] Write "Sensor-to-Brain-to-Actuator Pipeline" section in chapter-2-ros2-communication-model.md (FR-016, conceptual flow, 250-350 words)
- [x] T042 [US2] Write "Humanoid Robot Example: Camera to Motion" section in chapter-2-ros2-communication-model.md (FR-017, data flow through primitives, 300-400 words)
- [x] T043 [US2] Write "Deterministic vs Non-Deterministic Communication" section in chapter-2-ros2-communication-model.md (FR-019, QoS basics, 200-300 words)
- [x] T044 [US2] Add small illustrative code snippets (5-15 lines) showing node/topic/service structure per FR-020 in chapter-2-ros2-communication-model.md
- [x] T045 [US2] Add persona callouts for Software Engineers (compare to REST APIs) and Robotics Students (control theory) in chapter-2-ros2-communication-model.md
- [x] T046 [US2] Write "Summary" section in chapter-2-ros2-communication-model.md (FR-022, 150-200 words)
- [x] T047 [US2] Add "Further Reading" section with citations to docs.ros.org in chapter-2-ros2-communication-model.md

### Validation for User Story 2

- [x] T048 [US2] Verify all ROS 2 concepts in chapter-2-ros2-communication-model.md against docs.ros.org (nodes, topics, services, actions, executors, QoS)
- [x] T049 [US2] Run constitution compliance checklist on chapter-2-ros2-communication-model.md
- [x] T050 [US2] Check translation-readiness and semantic chunking in chapter-2-ros2-communication-model.md
- [x] T051 [US2] Verify code snippets are syntactically correct (no fictional APIs) in chapter-2-ros2-communication-model.md
- [x] T052 [US2] Test local Docusaurus build includes Chapter 2 in sidebar navigation

**Checkpoint**: Chapter 2 complete, validated, builds successfully. Learners understand communication primitives and can apply them to robot system design.

---

## Phase 5: User Story 3 - Connecting AI Agents to ROS 2 (Priority: P3)

**Goal**: Deliver Chapter 3 "Bridging AI Agents with ROS 2" teaching AI-ROS 2 integration for Physical AI systems

**Independent Test**: Learners can: (1) diagram natural-language-to-robot-action flow using ROS 2 primitives, (2) explain high-level planning vs low-level control separation, (3) identify safety boundaries. Chapter passes constitution checklist.

### Content Creation for User Story 3

- [x] T053 [US3] Create chapter-3-bridging-ai-agents-with-ros2.md in docs/docs/module-1-ros2/ with frontmatter per data-model.md schema
- [x] T054 [US3] Write "Learning Objectives" section in chapter-3-bridging-ai-agents-with-ros2.md (focus on AI-ROS 2 integration)
- [x] T055 [US3] Write "Python Agents as Cognitive Layers" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-024, AI as brain, 250-350 words)
- [x] T056 [US3] Write "Introduction to rclpy (Conceptual)" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-025, purpose not exhaustive API, 250-350 words)
- [x] T057 [US3] Write "ROS 2 as LLM-to-Robot Interface" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-026, language models to physical actions, 300-400 words)
- [x] T058 [US3] Write "High-Level Planning vs Low-Level Control" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-027, separation of concerns, 250-350 words)
- [x] T059 [US3] Write "ROS 2 Controllers as Motor Cortex" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-033, motor cortex analogy, 200-300 words)
- [x] T060 [US3] Write "Safety and Control Boundaries" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-028, safety mechanisms, 300-400 words)
- [x] T061 [US3] Write "Example: Natural Language Command to ROS 2 Action" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-029, end-to-end flow, 350-450 words)
- [x] T062 [US3] Write "Why This Matters for Humanoid Robots" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-030, Physical AI context, 200-300 words)
- [x] T063 [US3] Write "Preparing for Vision-Language-Action Systems" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-031, conceptual groundwork, 200-300 words)
- [x] T064 [US3] Add persona callouts for AI Researchers (ML systems parallels) and Software Engineers (Python integration patterns) in chapter-3-bridging-ai-agents-with-ros2.md
- [x] T065 [US3] Write "Summary" section in chapter-3-bridging-ai-agents-with-ros2.md (FR-034, 150-200 words)
- [x] T066 [US3] Add "Further Reading" section with citations to docs.ros.org and rclpy documentation in chapter-3-bridging-ai-agents-with-ros2.md

### Validation for User Story 3

- [x] T067 [US3] Verify all ROS 2 and rclpy concepts in chapter-3-bridging-ai-agents-with-ros2.md against official documentation
- [x] T068 [US3] Run constitution compliance checklist on chapter-3-bridging-ai-agents-with-ros2.md
- [x] T069 [US3] Check translation-readiness and semantic chunking in chapter-3-bridging-ai-agents-with-ros2.md
- [x] T070 [US3] Verify no Isaac Sim or Gazebo content leaked into chapter (FR-032 compliance) in chapter-3-bridging-ai-agents-with-ros2.md
- [x] T071 [US3] Test local Docusaurus build includes Chapter 3 in sidebar navigation

**Checkpoint**: All three chapters complete, validated, build successfully. Module 1 content ready for RAG embedding and chatbot integration.

---

## Phase 6: RAG Backend Implementation

**Purpose**: Implement FastAPI backend with Qdrant and OpenAI integration for RAG chatbot

**Prerequisites**: Foundational phase (T006-T017) complete, at least Chapter 1 content available for testing

- [x] T072 [P] Implement /query endpoint in rag-backend/main.py per contracts/rag-api.yaml (embed query, search Qdrant, generate GPT-4 response)
- [x] T073 [P] Implement /embed endpoint in rag-backend/main.py per contracts/rag-api.yaml (ingest chapter content, create chunks, generate embeddings)
- [x] T074 [P] Implement OpenAI embedding logic in rag-backend/embedding.py (text-embedding-3-large integration)
- [x] T075 [P] Implement Qdrant integration in rag-backend/qdrant_client.py (search, upsert, collection management)
- [x] T076 Implement persona-based prompt adaptation in rag-backend/personas.py (4 persona system prompts per research.md)
- [x] T077 [P] Create embedding pipeline script in scripts/embed_chapters.py (parse Markdown, chunk on H2/H3, extract metadata, embed, upload to Qdrant)
- [x] T078 [P] Add error handling and logging to rag-backend/main.py
- [x] T079 [P] Create Dockerfile for rag-backend/ with Python 3.11 and dependencies
- [x] T080 Test /health endpoint returns 200 OK
- [ ] T081 Test /query endpoint with sample question about Chapter 1 using curl or Postman

**Checkpoint**: RAG backend functional, can answer questions about embedded content.

---

## Phase 7: Content Embedding & RAG Integration

**Purpose**: Embed all Module 1 chapters into Qdrant and validate RAG retrieval quality

**Prerequisites**: Phase 6 complete (RAG backend), all three chapters complete (Phase 3-5)

- [ ] T082 Run scripts/setup_qdrant.py to create "textbook_chunks" collection in Qdrant
- [ ] T083 Run scripts/embed_chapters.py on chapter-1-introduction-to-ros2.md to create embeddings
- [ ] T084 [P] Run scripts/embed_chapters.py on chapter-2-ros2-communication-model.md to create embeddings
- [ ] T085 [P] Run scripts/embed_chapters.py on chapter-3-bridging-ai-agents-with-ros2.md to create embeddings
- [ ] T086 Verify Qdrant contains 30-50 chunks total for Module 1 (check chunk count in Qdrant dashboard or API)
- [ ] T087 Test RAG query: "What is ROS 2?" - verify retrieval from Chapter 1 and correct answer
- [ ] T088 Test RAG query: "What are ROS 2 topics?" - verify retrieval from Chapter 2 and correct answer
- [ ] T089 Test RAG query: "How do AI agents connect to ROS 2?" - verify retrieval from Chapter 3 and correct answer
- [ ] T090 Test persona adaptation: same query with "beginner" vs "ai_researcher" persona, verify different explanation depths
- [ ] T091 Test user-selected text retrieval: provide selected passage, verify RAG uses it as additional context

**Checkpoint**: All Module 1 content embedded in Qdrant, RAG retrieves relevant chunks, GPT-4 generates accurate answers.

---

## Phase 8: Chat UI Integration (React Widget in Docusaurus)

**Purpose**: Create and integrate React chat widget into Docusaurus for user interaction

**Prerequisites**: Phase 6 (RAG backend), Phase 7 (content embedded), Docusaurus builds successfully

- [ ] T092 Create ChatWidget.tsx React component in docs/src/components/ with chat interface UI
- [ ] T093 Implement text selection capture logic in ChatWidget.tsx (detect user-highlighted text on page)
- [ ] T094 Add persona selector dropdown in ChatWidget.tsx (Beginner, Software Engineer, Robotics Student, AI Researcher)
- [ ] T095 Implement fetch call to RAG backend /query endpoint in ChatWidget.tsx
- [ ] T096 Display AI response with source citations (chapter, section, URL) in ChatWidget.tsx
- [ ] T097 Add chat history display in ChatWidget.tsx (store in component state)
- [ ] T098 Embed ChatWidget component into Docusaurus layout (add to docs/src/theme/Root.tsx or similar)
- [ ] T099 Style ChatWidget.tsx for responsive design (mobile-friendly, fixed position bottom-right)
- [ ] T100 Test chat widget: open Docusaurus site, select text from Chapter 1, ask question, verify response
- [ ] T101 Test persona selector: switch persona, ask same question, verify different explanation style

**Checkpoint**: Chat widget functional in Docusaurus, users can ask questions and receive RAG-powered answers.

---

## Phase 9: Deployment & Production Configuration

**Purpose**: Deploy Docusaurus to GitHub Pages and FastAPI backend to Railway/Render

**Prerequisites**: All content complete (Phase 3-5), RAG backend complete (Phase 6), chat widget integrated (Phase 8)

- [ ] T102 Update CORS configuration in rag-backend/main.py to allow production GitHub Pages URL (https://[username].github.io)
- [ ] T103 Create .env file in rag-backend/ with OPENAI_API_KEY and QDRANT_URL (use Qdrant Cloud or self-hosted URL)
- [ ] T104 Test Docusaurus production build locally with `npm run build` in docs/
- [ ] T105 Deploy FastAPI backend to Railway or Render (follow platform-specific deployment guide)
- [ ] T106 Update ChatWidget.tsx with production RAG backend URL (Railway/Render deployment URL)
- [ ] T107 Enable GitHub Pages in repository settings (Settings → Pages → Source: GitHub Actions)
- [ ] T108 Push code to main branch to trigger GitHub Actions workflow (.github/workflows/deploy.yml)
- [ ] T109 Verify Docusaurus site deployed successfully to GitHub Pages (visit https://[username].github.io/hackathon-1/)
- [ ] T110 Test end-to-end: visit production site, read Chapter 1, ask question via chat widget, verify RAG response
- [ ] T111 Test performance: measure Chapter 1 load time (<2 seconds), RAG query response time (<3 seconds)
- [ ] T112 Test with multiple browsers (Chrome, Firefox, Safari, Edge) for compatibility

**Checkpoint**: Full system deployed and functional. Docusaurus on GitHub Pages, FastAPI on Railway/Render, RAG chatbot answering questions.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, accessibility, and bonus features

**Prerequisites**: Phase 9 complete (deployed and functional)

- [ ] T113 [P] Create textbook introduction page in docs/docs/intro.md with project overview, learning path, how to use the chatbot
- [ ] T114 [P] Add README.md in project root with setup instructions, deployment guide, contribution guidelines
- [ ] T115 [P] Create glossary page in docs/docs/glossary.md with ROS 2 terminology definitions
- [ ] T116 [P] Validate all cross-chapter references are self-contained (no broken context for RAG retrieval)
- [ ] T117 [P] Run accessibility audit on Docusaurus site (ARIA labels, keyboard navigation, screen reader compatibility)
- [ ] T118 [P] Add error handling to ChatWidget.tsx (display user-friendly messages when RAG backend is unavailable)
- [ ] T119 [P] Implement rate limiting on /query endpoint in rag-backend/main.py (10 queries/min for demo)
- [ ] T120 [P] Add loading spinner to ChatWidget.tsx while waiting for RAG response
- [ ] T121 Document deployment steps in quickstart.md (already exists, verify completeness)
- [ ] T122 Run final constitution compliance review on all three chapters (all 10 principles)

**Checkpoint**: Production-ready textbook with polished UX, accessible, documented.

---

## Phase 11: Bonus Features (Optional, Hackathon Extra Credit)

**Purpose**: Implement bonus features for additional hackathon points

**Prerequisites**: Phase 10 complete (core system polished)

### Bonus 1: AI Subagent for Chapter Summarization

- [ ] T123 [Bonus] Create summarization agent in scripts/summarize_chapter.py that reads chapter Markdown and generates summary
- [ ] T124 [Bonus] Test summarization agent on Chapter 1, verify summary captures key concepts (200-250 words)
- [ ] T125 [Bonus] Generate summaries for all three chapters and add to chapter frontmatter or separate summary page

### Bonus 2: Quiz Generation from Chapter Content

- [ ] T126 [Bonus] Create quiz generation agent in scripts/generate_quiz.py that extracts concepts and generates multiple-choice questions
- [ ] T127 [Bonus] Test quiz generator on Chapter 1, verify questions test learning objectives
- [ ] T128 [Bonus] Add quiz UI component to Docusaurus (optional interactive quiz at end of each chapter)

### Bonus 3: Urdu Translation Preparation

- [ ] T129 [Bonus] Export chapter content to translation-friendly format (preserve code blocks, technical terms)
- [ ] T130 [Bonus] Configure Docusaurus i18n for Urdu language support (i18n config in docusaurus.config.js)
- [ ] T131 [Bonus] Translate Chapter 1 to Urdu (if time permits and translator available)
- [ ] T132 [Bonus] Add language switcher to Docusaurus navbar (English ↔ Urdu)

**Note**: Bonus features are optional and should only be attempted if core features (T001-T122) are complete and tested.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T005) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T006-T017) completion
- **User Story 2 (Phase 4)**: Depends on Foundational (T006-T017) completion - can run parallel with US1 if multiple contributors
- **User Story 3 (Phase 5)**: Depends on Foundational (T006-T017) completion - can run parallel with US1/US2 if multiple contributors
- **RAG Backend (Phase 6)**: Depends on Foundational (T006-T017) completion - can start before all content complete
- **Content Embedding (Phase 7)**: Depends on RAG Backend (T072-T081) AND at least one chapter (US1, US2, or US3)
- **Chat UI (Phase 8)**: Depends on RAG Backend (T072-T081) and Foundational (T006-T017)
- **Deployment (Phase 9)**: Depends on all content (Phase 3-5), RAG Backend (Phase 6), and Chat UI (Phase 8)
- **Polish (Phase 10)**: Depends on Deployment (Phase 9)
- **Bonus (Phase 11)**: Depends on Polish (Phase 10) - truly optional

### User Story Dependencies

- **User Story 1 (Chapter 1)**: Can start immediately after Foundational phase - No dependencies on other stories
- **User Story 2 (Chapter 2)**: Can start immediately after Foundational phase - Independent of US1 (though conceptually builds on it)
- **User Story 3 (Chapter 3)**: Can start immediately after Foundational phase - Independent of US1/US2 (though conceptually builds on both)

**Critical Path**: Setup → Foundational → User Story 1 (Chapter 1) → Content Embedding (Chapter 1) → RAG Backend → Chat UI → Deployment
**Parallel Opportunities**: US2 and US3 can proceed in parallel with US1 if multiple contributors available

### Within Each Phase

- Tasks marked [P] can run in parallel (different files, no dependencies)
- Content creation tasks within each user story are mostly sequential (write sections in order)
- Validation tasks depend on content creation tasks being complete

---

## Parallel Execution Examples

### Phase 2: Foundational (9 parallel tasks possible)

```bash
# Can run simultaneously:
T008 [P] Create module directory structure
T009 [P] Create _category_.json
T010 [P] Setup FastAPI application structure
T011 [P] Create Pydantic models
T012 [P] Setup Qdrant client configuration
T013 [P] Create Qdrant collection script
T014 [P] Implement /health endpoint
# (T006, T007, T015, T016, T017 are sequential or have light dependencies)
```

### Phase 3-5: User Stories (All three chapters can proceed in parallel)

```bash
# If you have 3 contributors:
Contributor A: Phase 3 (T018-T033) - User Story 1 / Chapter 1
Contributor B: Phase 4 (T034-T052) - User Story 2 / Chapter 2
Contributor C: Phase 5 (T053-T071) - User Story 3 / Chapter 3

# All three chapters can be written and validated simultaneously after Foundational phase
```

### Phase 6: RAG Backend (6 parallel tasks possible)

```bash
# Can run simultaneously:
T072 [P] Implement /query endpoint
T073 [P] Implement /embed endpoint
T074 [P] Implement OpenAI embedding logic
T075 [P] Implement Qdrant integration
T077 [P] Create embedding pipeline script
T078 [P] Add error handling and logging
T079 [P] Create Dockerfile
# (T076, T080, T081 are sequential)
```

### Phase 7: Content Embedding (3 parallel tasks)

```bash
# Can run simultaneously (after T082-T083):
T084 [P] Embed Chapter 2
T085 [P] Embed Chapter 3
# (T083 embeds Chapter 1, then T084-T085 can proceed in parallel)
```

---

## Implementation Strategy

### MVP First (Minimum Viable Product = User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T017) - **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 / Chapter 1 (T018-T033)
4. Complete Phase 6: RAG Backend (T072-T081) - minimal for testing
5. Complete Phase 7: Content Embedding for Chapter 1 (T082-T083, T086-T087)
6. **STOP and VALIDATE**: Chapter 1 content quality, RAG can answer questions about Chapter 1
7. Deploy MVP if ready or continue to Phase 4-5

**MVP Deliverable**: One complete chapter (Chapter 1) with functional RAG chatbot answering questions about ROS 2 fundamentals.

### Incremental Delivery

1. **Milestone 1**: Foundational infrastructure ready (Docusaurus builds, FastAPI runs, Qdrant connected)
2. **Milestone 2**: Chapter 1 complete, embedded, RAG answers questions → MVP DEPLOYED
3. **Milestone 3**: Chapter 2 complete, embedded → Deploy update with 2 chapters
4. **Milestone 4**: Chapter 3 complete, embedded → Deploy complete Module 1
5. **Milestone 5**: Chat UI integrated into Docusaurus → Full interactive experience
6. **Milestone 6**: Production deployment (GitHub Pages + Railway/Render) → Public access
7. **Milestone 7**: Polish and bonus features → Hackathon submission ready

Each milestone is independently testable and deliverable.

### Parallel Team Strategy

With 3 contributors:

1. **Phase 1-2**: Team works together on infrastructure setup (T001-T017)
2. **Once Foundational complete**:
   - **Contributor A**: User Story 1 / Chapter 1 (T018-T033)
   - **Contributor B**: User Story 2 / Chapter 2 (T034-T052)
   - **Contributor C**: RAG Backend (T072-T081)
3. **Once content and backend ready**:
   - **Contributor A**: Content Embedding (T082-T091)
   - **Contributor B**: User Story 3 / Chapter 3 (T053-T071)
   - **Contributor C**: Chat UI (T092-T101)
4. **Final phase**: Team collaborates on Deployment (T102-T112) and Polish (T113-T122)

---

## Task Summary

**Total Tasks**: 132 tasks (122 core + 10 bonus)
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 12 tasks
- **Phase 3 (User Story 1 / Chapter 1)**: 16 tasks (15 content + 1 checkpoint)
- **Phase 4 (User Story 2 / Chapter 2)**: 19 tasks (18 content + 1 checkpoint)
- **Phase 5 (User Story 3 / Chapter 3)**: 19 tasks (18 content + 1 checkpoint)
- **Phase 6 (RAG Backend)**: 10 tasks
- **Phase 7 (Content Embedding)**: 10 tasks
- **Phase 8 (Chat UI)**: 10 tasks
- **Phase 9 (Deployment)**: 11 tasks
- **Phase 10 (Polish)**: 10 tasks
- **Phase 11 (Bonus)**: 10 tasks (optional)

**Parallel Opportunities Identified**: 35+ tasks marked [P] can run in parallel

**Independent Test Criteria**:
- **User Story 1**: Learners can explain what ROS 2 is, why it matters, and how it differs from monolithic architectures
- **User Story 2**: Learners can diagram sensor-to-actuator flows and choose correct communication primitives
- **User Story 3**: Learners can design AI-ROS 2 integration architectures with appropriate safety boundaries

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 / Chapter 1) + minimal Phase 6-7 for RAG testing = ~33 tasks

**Format Validation**: ✅ All tasks follow checklist format with checkbox, ID, optional [P]/[Story] labels, and file paths

**Critical Path Duration Estimate** (sequential execution):
- Setup + Foundational: ~2-4 hours
- Chapter 1 content creation: ~6-8 hours (2,000-2,500 words)
- RAG backend implementation: ~4-6 hours
- Content embedding + testing: ~2-3 hours
- **Total MVP**: ~14-21 hours of focused work

**Full Module 1 Duration Estimate** (with parallelization):
- Add Chapters 2 & 3: +12-16 hours (if sequential), +6-8 hours (if parallel with 3 contributors)
- Chat UI + Deployment: +6-8 hours
- Polish: +3-4 hours
- **Total Full Module**: ~35-45 hours sequential, ~25-35 hours with 3-person team

---

## Notes

- **No tests explicitly requested**: Specification did not request TDD or automated tests, so test tasks are omitted. Focus is on content quality and manual validation.
- **Constitution compliance is manual**: Each chapter validated against 10 constitution principles via checklist review (not automated).
- **File paths are explicit**: Every task includes exact file path (e.g., docs/docs/module-1-ros2/chapter-1-introduction-to-ros2.md).
- **Semantic chunking enforced**: Chapter content tasks target 200-500 words per section to align with constitution and RAG requirements.
- **ROS 2 verification required**: Multiple tasks (T029, T048, T067) verify content against official docs.ros.org to ensure technical accuracy.
- **Persona callouts integrated**: Tasks T026, T045, T064 add persona-specific callouts to chapters for personalization support.
- **Translation-ready validation**: Tasks T031, T050, T069 check for short sentences, no idioms, active voice (constitution Principle VI).
- **Bonus features are truly optional**: Phase 11 should only be attempted if time permits after core features (T001-T122) are complete and tested.

This task list is immediately executable. Each task is specific enough for an LLM or human contributor to complete without additional context.
