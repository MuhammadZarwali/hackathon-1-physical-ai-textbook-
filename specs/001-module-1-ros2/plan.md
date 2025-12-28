# Implementation Plan: Module 1 - The Robotic Nervous System (ROS 2)

**Branch**: `001-module-1-ros2` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-module-1-ros2/spec.md`

**Note**: This plan covers the implementation of Module 1 educational content, Docusaurus infrastructure, and RAG chatbot integration for the Physical AI & Humanoid Robotics textbook.

## Summary

Implement Module 1 "The Robotic Nervous System (ROS 2)" as the foundation of an AI-native technical textbook. This module consists of three educational chapters covering ROS 2 fundamentals, communication primitives, and AI integration. The implementation includes:

1. **Educational Content**: Three conceptual chapters (no installation/tutorials) following constitution principles
2. **Docusaurus Infrastructure**: Static site generation with module/chapter organization and GitHub Pages deployment
3. **RAG Chatbot**: FastAPI backend + Qdrant vector DB + OpenAI GPT-4 for interactive learning
4. **AI-Native Features**: Semantic chunking, persona-based personalization, translation-ready English

**Primary Requirement**: Create high-quality educational content that teaches ROS 2 concepts to diverse learners (beginners, software engineers, robotics students, AI researchers) with RAG-powered Q&A support.

**Technical Approach** (from research.md):
- Docusaurus 3.x for content platform (docs-only mode)
- FastAPI + Qdrant + OpenAI for RAG backend
- Semantic chunking (200-500 words) on H2/H3 boundaries
- Persona-specific prompts and relevance filtering
- GitHub Pages deployment (frontend) + Railway/Render (backend)

## Technical Context

**Language/Version**:
- **Frontend**: Node.js 18+, Docusaurus 3.x, React 18
- **Backend**: Python 3.11+, FastAPI 0.109+
- **Content**: Markdown/MDX

**Primary Dependencies**:
- **Docusaurus**: @docusaurus/core, @docusaurus/preset-classic
- **FastAPI Backend**: fastapi, uvicorn, qdrant-client, openai, python-dotenv, pydantic
- **Vector DB**: Qdrant (Docker or Cloud)
- **LLM/Embeddings**: OpenAI API (GPT-4, text-embedding-3-large)

**Storage**:
- **Content**: Git repository (Markdown files)
- **Embeddings**: Qdrant vector database (3072-dim vectors)
- **User Preferences**: Client-side (localStorage or session)

**Testing**:
- **Content Validation**: Constitution compliance checklist (manual review)
- **Technical Accuracy**: ROS 2 concepts verified against docs.ros.org
- **RAG System**: Integration tests (query → retrieval → response)
- **Deployment**: GitHub Actions CI/CD for Docusaurus

**Target Platform**:
- **Frontend**: GitHub Pages (static site, HTTPS)
- **Backend**: Railway/Render (containerized FastAPI)
- **Browser**: Modern browsers (Chrome, Firefox, Safari, Edge)

**Project Type**: Web application (educational documentation site + API backend)

**Performance Goals**:
- **Chapter Load Time**: <2 seconds (static site, optimized)
- **RAG Query Response**: <3 seconds (embedding + retrieval + GPT-4 generation)
- **Concurrent Users**: 100+ (hackathon demo scale)
- **Reading Experience**: Smooth scrolling, no janky interactions

**Constraints**:
- **No Installation Content**: Chapters are conceptual/architectural only (per spec FR-009, FR-032)
- **Semantic Chunking**: 200-500 words per chunk (constitution Principle III)
- **Translation-Ready**: Short sentences, no idioms, technical terms in English (constitution Principle VI)
- **Hackathon Timeline**: Rapid development, prioritize core features over optimization

**Scale/Scope**:
- **Module 1**: 3 chapters (~6,000-8,000 words total content)
- **Future Modules**: 3 additional modules (Module 2-4, 9-12 chapters total)
- **RAG Database**: ~30-50 chunks for Module 1, ~120-200 chunks for full textbook
- **Users**: Hackathon judges + open access (potentially 100s-1000s over time)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Compliance Verification**:

### ✅ I. Educational Clarity & Structure
- **Requirement**: Clear learning objectives, step-by-step explanations, examples, summaries
- **Implementation**: Chapter template includes all required sections (see quickstart.md)
- **Validation**: Manual review against checklist before content approval
- **Status**: PASS - Template and spec define required structure

### ✅ II. Technical Accuracy
- **Requirement**: ROS 2 concepts must be verifiable against official documentation
- **Implementation**: research.md documents verified terminology; glossary tracking; citation format
- **Validation**: Cross-reference all ROS 2 claims with docs.ros.org before publication
- **Status**: PASS - Research phase verified core concepts; validation process defined

### ✅ III. AI-Native Design Principles
- **Requirement**: Modular, retrievable, semantically coherent chunks
- **Implementation**: 200-500 word chunks on H2/H3 boundaries; explicit definitions; consistent terminology
- **Validation**: Embedding script enforces chunking; RAG retrieval tests semantic coherence
- **Status**: PASS - data-model.md defines chunk schema; embedding pipeline enforces standards

### ✅ IV. RAG Chatbot Compatibility
- **Requirement**: Each section answers What/Why/How; self-contained
- **Implementation**: Chapter template enforces What/Why/How pattern; metadata for standalone retrieval
- **Validation**: RAG query tests with user-selected text only (no full-book context)
- **Status**: PASS - Template structure enforces RAG compatibility; test plan defined

### ✅ V. Personalization Support
- **Requirement**: Adaptable for 4 personas (Beginner, SWE, Robotics Student, AI Researcher)
- **Implementation**: Persona callouts in content (:::note For Beginners); RAG prompt adaptation
- **Validation**: Test RAG queries with each persona; verify appropriate explanation depth
- **Status**: PASS - data-model.md defines persona schema; research.md defines prompt adaptation

### ✅ VI. Multi-Language Support (Urdu Translation)
- **Requirement**: Translation-ready English (short sentences, no idioms, technical terms in English)
- **Implementation**: Writing guidelines in research.md; manual review for idioms/slang
- **Validation**: Readability check (avg sentence length <20 words); idiom detection
- **Status**: PASS - Guidelines documented; deferred Urdu translation to post-hackathon

### ✅ VII. Reusable AI Intelligence
- **Requirement**: Consistent structure for AI subagents (summarization, quiz generation)
- **Implementation**: Standardized chapter template; metadata schema enables task prompts
- **Validation**: (Bonus feature) Test summarization agent on completed chapters
- **Status**: PASS - Consistent structure defined; bonus feature implementation optional

### ✅ VIII. Documentation & Structure Standards
- **Requirement**: Markdown-compatible, Docusaurus best practices, H1-H4 hierarchy
- **Implementation**: Docusaurus 3.x with preset-classic; validated frontmatter schema
- **Validation**: Build succeeds without warnings; no broken links
- **Status**: PASS - Docusaurus configuration in quickstart.md; template enforces standards

### ✅ IX. Ethics & Integrity
- **Requirement**: No plagiarism, no hallucinated citations, verifiable sources
- **Implementation**: Original writing; citation format with URLs; research.md tracks sources
- **Validation**: Manual review for plagiarism; verify all citation URLs are accessible
- **Status**: PASS - Citation standards defined; validation process in content workflow

### ✅ X. Scope Control
- **Requirement**: Focus ONLY on Physical AI & Humanoid Robotics
- **Implementation**: Spec explicitly scopes ROS 2 for physical AI; out-of-scope section defined
- **Validation**: Content review rejects tangential AI topics (pure NLP, non-embodied vision)
- **Status**: PASS - Spec FR-044 enforces scope; out-of-scope section prevents creep

**Constitution Check Result**: ✅ **PASSED** - All 10 principles have defined implementation and validation strategies. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-module-1-ros2/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (schemas)
├── quickstart.md        # Phase 1 output (development guide)
├── contracts/           # Phase 1 output (API contracts)
│   └── rag-api.yaml     # OpenAPI spec for RAG backend
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
hackathon-1/
├── docs/                          # Docusaurus educational content
│   ├── docusaurus.config.js       # Docusaurus configuration
│   ├── sidebars.js                # Sidebar navigation
│   ├── src/
│   │   ├── components/            # Custom React components
│   │   │   └── ChatWidget.tsx     # RAG chatbot UI
│   │   ├── css/
│   │   │   └── custom.css         # Custom styles
│   │   └── pages/
│   │       └── index.tsx          # Landing page
│   ├── docs/                      # Educational content
│   │   ├── intro.md               # Textbook introduction
│   │   ├── module-1-ros2/         # Module 1: ROS 2
│   │   │   ├── _category_.json    # Module metadata
│   │   │   ├── chapter-1-introduction-to-ros2.md
│   │   │   ├── chapter-2-ros2-communication-model.md
│   │   │   └── chapter-3-bridging-ai-agents-with-ros2.md
│   │   ├── module-2-digital-twin/ # Future: Digital twins & Gazebo
│   │   ├── module-3-isaac-ai-brain/ # Future: NVIDIA Isaac
│   │   └── module-4-vision-language-action/ # Future: VLA systems
│   ├── static/                    # Static assets
│   │   └── img/                   # Diagrams, icons
│   ├── package.json
│   └── build/                     # Generated (GitHub Pages deploy)
│
├── rag-backend/                   # FastAPI RAG backend
│   ├── main.py                    # FastAPI application
│   ├── models.py                  # Pydantic schemas
│   ├── qdrant_client.py           # Qdrant integration
│   ├── embedding.py               # OpenAI embedding logic
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment variable template
│   ├── Dockerfile                 # Container for deployment
│   └── tests/
│       └── test_api.py            # Integration tests
│
├── scripts/                       # Build and deployment scripts
│   ├── embed_chapters.py          # Content embedding pipeline
│   ├── setup_qdrant.py            # Qdrant collection initialization
│   └── validate_content.py        # Constitution compliance checker
│
├── .github/
│   └── workflows/
│       └── deploy.yml             # GitHub Actions (Docusaurus → GitHub Pages)
│
├── specs/                         # Feature specifications
│   └── 001-module-1-ros2/         # This module
│
├── .specify/                      # Spec-Kit Plus templates
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   └── scripts/
│
├── history/                       # Prompt History Records
│   └── prompts/
│       ├── constitution/
│       └── 001-module-1-ros2/
│
├── README.md                      # Project overview
└── .gitignore
```

**Structure Decision**: Selected **Option 2: Web application** structure with separate `docs/` (Docusaurus frontend) and `rag-backend/` (FastAPI API) directories. This separation enables independent deployment: GitHub Pages for static content, Railway/Render for dynamic API.

**Rationale**:
- Docusaurus requires Node.js project structure with `docs/` convention
- FastAPI backend is Python-based, separate from frontend
- Clear separation of concerns: content authoring (Markdown) vs AI logic (Python)
- Independent scaling: static site CDN for content, serverless/containerized API for RAG queries

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations identified**. All constitution principles have compliant implementation strategies.

---

## Phase 0: Research & Technical Decisions

**Status**: ✅ **COMPLETED** (see research.md)

**Artifacts Generated**:
- `research.md`: Technical decisions for Docusaurus, RAG architecture, ROS 2 accuracy standards, content organization, personalization, Urdu translation

**Key Decisions**:
1. **Docusaurus 3.x** for educational content platform
2. **FastAPI + Qdrant + OpenAI GPT-4** for RAG chatbot
3. **Semantic chunking** (200-500 words on H2/H3 boundaries)
4. **Persona-based personalization** (4 personas with callouts + RAG prompts)
5. **Translation-ready English** (short sentences, no idioms)
6. **ROS 2 accuracy** verified against docs.ros.org

**All NEEDS CLARIFICATION items resolved** in research.md.

---

## Phase 1: Design & Contracts

**Status**: ✅ **COMPLETED**

**Artifacts Generated**:
1. `data-model.md`: Schemas for chapter metadata, RAG chunks, user personas, queries, module catalog, glossary
2. `quickstart.md`: Step-by-step development guide (Docusaurus setup, RAG backend, embedding pipeline, deployment)
3. `contracts/rag-api.yaml`: OpenAPI 3.0 specification for RAG backend (`/health`, `/query`, `/embed` endpoints)

**Key Design Elements**:

### Chapter Metadata Schema (YAML frontmatter):
- Required fields: sidebar_position, title, description, keywords, module, chapter_id
- Educational metadata: learning_objectives, prerequisites, difficulty, estimated_reading_time
- Persona relevance: 1-5 scale for each of 4 personas
- Technical accuracy: ros2_concepts, verified_against, last_verified

### RAG Chunk Schema (Qdrant documents):
- Content: 200-500 word text chunk + 3072-dim embedding vector
- Metadata: module, chapter, section_title, heading_level, content_type, keywords, ros2_concepts, persona_relevance, url, sequence, word_count
- Filters: Persona-based retrieval prioritizes high-relevance chunks

### API Contracts:
- `POST /query`: Submit question + optional selected text + persona → AI-generated answer + sources
- `POST /embed`: Ingest chapter content → create embeddings (admin endpoint)
- `GET /health`: Service health check

**Agent Context Update**: (Run after this plan is approved)
```bash
.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude
```

This will add Docusaurus 3.x, FastAPI, Qdrant, and OpenAI technologies to `.specify/memory/agent-context.md` (or equivalent agent-specific file).

---

## Phase 2: Implementation Phases (Next Steps)

**Note**: This plan stops here. Phase 2 tasks are defined by `/sp.tasks` command (not `/sp.plan`).

**Recommended Task Workflow** (for `/sp.tasks`):

### Phase 2.1: Docusaurus Infrastructure Setup
- Initialize Docusaurus project (`npx create-docusaurus`)
- Configure `docusaurus.config.js` for docs-only mode, GitHub Pages
- Create module folders and `_category_.json` files
- Create chapter template with frontmatter schema
- Test local build (`npm start`, `npm run build`)

### Phase 2.2: Module 1 Content Creation
- **Chapter 1**: Write "Introduction to ROS 2" (FR-001 to FR-010)
- **Chapter 2**: Write "ROS 2 Communication Model" (FR-011 to FR-023)
- **Chapter 3**: Write "Bridging AI Agents with ROS 2" (FR-024 to FR-035)
- Apply module-wide requirements (FR-036 to FR-044)
- Validate against constitution principles
- Peer review for technical accuracy (ROS 2 concepts vs docs.ros.org)

### Phase 2.3: RAG Backend Implementation
- Setup FastAPI project structure
- Implement `/health`, `/query`, `/embed` endpoints per contracts/rag-api.yaml
- Integrate Qdrant client (local Docker or Cloud)
- Integrate OpenAI API (embeddings + GPT-4)
- Implement persona-based prompt adaptation
- Write integration tests

### Phase 2.4: Content Embedding Pipeline
- Write `scripts/embed_chapters.py` (chunk Markdown, generate embeddings, upload to Qdrant)
- Run pipeline on Module 1 chapters
- Verify chunks in Qdrant (count, metadata, retrieval quality)
- Test RAG queries with sample questions

### Phase 2.5: RAG Chat UI Integration
- Create React chat widget component (`src/components/ChatWidget.tsx`)
- Implement text selection capture for context
- Add persona selector dropdown
- Integrate with FastAPI backend (`/query` endpoint)
- Embed chat widget into Docusaurus layout
- Style for responsive design

### Phase 2.6: Deployment & Testing
- Configure GitHub Actions workflow (`.github/workflows/deploy.yml`)
- Deploy Docusaurus to GitHub Pages
- Deploy FastAPI backend to Railway/Render
- Update CORS config with production URL
- End-to-end testing: Chapter content → RAG query → Correct answer
- Performance testing: Query response time, concurrent users

### Phase 2.7: Bonus Features (Optional)
- AI subagent for chapter summarization
- Quiz generation from chapter content
- Urdu translation preparation (export content, translation workflow)
- Accessibility improvements (ARIA labels, keyboard navigation)

---

## Success Criteria Mapping

**From spec.md, all 20 success criteria map to implementation phases:**

### Content Quality (SC-001 to SC-012):
- **SC-001 to SC-004**: Chapter content quality → Phase 2.2
- **SC-005 to SC-006**: RAG chatbot functionality → Phase 2.3, 2.4
- **SC-007**: Personalization → Phase 2.2 (callouts), Phase 2.3 (RAG prompts)
- **SC-008**: Technical accuracy → Phase 2.2 (validation against docs.ros.org)
- **SC-009**: Urdu translation → Phase 2.7 (bonus, post-hackathon)
- **SC-010**: Learner readiness → Phase 2.2 (content quality)
- **SC-011**: Reading time → Phase 2.2 (target 20-30 min per chapter)
- **SC-012**: AI subagents → Phase 2.7 (bonus)

### Constitution Compliance (SC-013 to SC-020):
- **SC-013**: Educational Clarity → Phase 2.2 (template enforcement)
- **SC-014**: Technical Accuracy → Phase 2.2 (ROS 2 verification)
- **SC-015**: AI-Native Design → Phase 2.4 (chunking enforcement)
- **SC-016**: RAG Compatibility → Phase 2.2 (What/Why/How pattern)
- **SC-017**: Multi-Language Support → Phase 2.2 (writing guidelines)
- **SC-018**: Documentation Standards → Phase 2.1, 2.2 (Docusaurus compliance)
- **SC-019**: Ethics & Integrity → Phase 2.2 (plagiarism review, citations)
- **SC-020**: Scope Control → Phase 2.2 (content review)

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| **ROS 2 Technical Inaccuracy** | High - Erodes trust, misleads learners | Verify all concepts against docs.ros.org; peer review by ROS 2 expert |
| **RAG Retrieval Quality** | Medium - Poor answers harm learning | Test with diverse queries; tune chunk size; adjust persona filters |
| **OpenAI API Costs** | Medium - Budget overrun for hackathon | Monitor usage; use caching; consider `text-embedding-3-small` for cost |
| **Content Completion Timeline** | High - 3 chapters = ~6-8k words | Prioritize Chapter 1; parallelize writing if multiple contributors |
| **Deployment Complexity** | Medium - Two platforms (GitHub Pages + Railway) | Follow quickstart.md; test locally first; use free tiers |
| **Persona Adaptation Quality** | Low - Suboptimal but not blocking | Start with Software Engineer base; refine prompts based on testing |

---

## Next Steps

1. **Approve this plan** (review by user/team)
2. **Run `/sp.tasks`** to generate detailed task list (Phase 2 breakdown)
3. **Execute tasks** in priority order:
   - Critical: Docusaurus setup → Chapter 1 content → RAG backend → Embedding pipeline → Deployment
   - Important: Chapters 2 & 3 → Chat UI → Testing
   - Nice-to-have: Bonus features (summarization, quizzes, Urdu)

4. **Checkpoints**:
   - After Phase 2.1: Docusaurus builds and deploys to GitHub Pages
   - After Phase 2.2 (Chapter 1): Validate against constitution checklist
   - After Phase 2.4: RAG system answers questions correctly
   - After Phase 2.6: Full system functional end-to-end

---

**Plan Complete**. Ready for `/sp.tasks` command to generate implementation tasks.
