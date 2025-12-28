# Implementation Plan: Module 2 - The Digital Twin: Simulation & Virtual Environments

**Branch**: `001-module-2` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-module-2/spec.md`

**Note**: This plan outlines the content creation workflow for Module 2 of the Physical AI & Humanoid Robotics textbook. This is an educational content project, not a software development project.

## Summary

Create Module 2 of the AI-native textbook covering digital twins, simulation environments, and virtual robot testing. The module consists of 3 conceptual chapters (11,500-12,500 words total) teaching students how robots are designed, tested, and trained in simulated environments using Gazebo and ROS 2 integration. Content must be RAG-optimized, persona-aware, and maintain consistency with Module 1's proven pedagogical approach. Technical approach: Write markdown chapters in Docusaurus with frontmatter, semantic chunking for RAG retrieval, and persona callouts for adaptive learning.

## Technical Context

**Language/Version**: Markdown (GitHub Flavored Markdown) with Docusaurus 3.x frontmatter
**Primary Dependencies**:
- Docusaurus 3.x (documentation platform)
- Node.js/npm (for Docusaurus build system)
- Existing Module 1 chapters (for style/format reference)
- RAG backend (Gemini API + Qdrant) for content ingestion

**Storage**: Markdown files in `physical-ai-textbook/docs/docs/module-2-simulation/` directory
**Testing**:
- Content validation: Word count verification, frontmatter validation, persona callout count
- RAG testing: Query-response testing with Gemini backend
- Readability: Flesch-Kincaid Grade Level 10-12 verification

**Target Platform**: Web browser (Docusaurus static site)
**Project Type**: Educational content creation (documentation project)
**Performance Goals**:
- Chapter load time <2 seconds
- Total module reading time: 90-120 minutes
- Student comprehension: 85% quiz pass rate (70%+ correct)
- RAG query response time: <5 seconds

**Constraints**:
- No installation instructions or CLI commands in content
- No full code listings or configuration files
- Conceptual focus only (no hands-on labs)
- Must maintain Module 1 consistency (persona format, frontmatter structure, writing style)
- Word count targets: Chapter 1 (3,500-4,000), Chapter 2 (4,000-4,500), Chapter 3 (4,000-4,500)

**Scale/Scope**:
- 3 chapters, 11,500-12,500 words total
- 4-6 persona callouts per chapter (12-18 total)
- 3+ comparison tables across module
- 5+ cross-references to Module 1
- 3+ real-world examples per chapter

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Educational Clarity & Structure
**Status**: COMPLIANT
- All chapters include learning objectives (FR-006, FR-032)
- Step-by-step concept progression (P1 fundamentals → P2 architecture → P3 advanced)
- Practical examples required (FR-003, FR-015, FR-027)
- Summary sections mandated (FR-006)
- Persona callouts provide scaffolding for different learner levels (FR-007, FR-018, FR-028)

### ✅ II. Technical Accuracy
**Status**: COMPLIANT
- ROS 2 concepts must match Module 1 terminology (FR-031)
- Real-world examples required from Boston Dynamics, Tesla, Sanctuary AI (FR-003)
- Gazebo physics simulation must reflect actual behavior (FR-012)
- URDF/SDF descriptions must be conceptually accurate (FR-013)
- Cross-references to Module 1 ensure consistency (FR-017)

### ✅ III. AI-Native Design Principles
**Status**: COMPLIANT
- Semantic independence required for RAG chunking (FR-014 conceptual diagram descriptions)
- Definitions explicit on first use (SC-014)
- Persona callouts provide context adaptation (FR-007, FR-018, FR-028)
- Each section can stand alone conceptually

### ✅ IV. RAG Chatbot Compatibility
**Status**: COMPLIANT
- Content will be chunked by H2/H3 sections (200-500 words per chunk)
- Frontmatter provides metadata for filtering (FR-032)
- Persona callouts support adaptive responses
- Conceptual focus (no code) makes content more retrievable

### ✅ V. Personalization Support
**Status**: COMPLIANT
- 4 persona types embedded throughout (💡 Beginner, 🛠️ Software Engineer, 🤖 Robotics Student, 🧠 AI Researcher)
- Each persona gets tailored analogies and context (FR-005 for beginners, FR-039 for software engineers)
- Distribution requirements ensure balanced coverage (FR-007, FR-018, FR-028, SC-006)

### ⚠️ VI. Multi-Language Support
**Status**: DEFERRED
- Initial release: English only
- Urdu translation planned for Module 1 Phase 11 (bonus features)
- Module 2 Urdu translation will follow same pattern
- No blockers: content structure supports future i18n

### ✅ VII. Reusable AI Intelligence
**Status**: COMPLIANT
- Content will be embedded into existing RAG system (already working for Module 1)
- Gemini embeddings (768-dim) + Qdrant vector DB
- Persona-based retrieval already tested in Module 1

### ✅ VIII. Documentation & Structure Standards
**Status**: COMPLIANT
- Docusaurus frontmatter required (FR-032)
- Sidebar positioning defined in spec
- Module 1 format precedent established (FR-020, FR-031)
- Clear file naming convention (chapter-1-introduction-to-digital-twins.md)

### ✅ IX. Ethics & Integrity
**Status**: COMPLIANT
- Technical accuracy required (Constitution II)
- Real-world examples only (FR-003)
- Honest discussion of simulation limitations (FR-026 sim-to-real gap)
- Proper attribution for industry examples

### ✅ X. Scope Control
**Status**: COMPLIANT
- Out of scope explicitly defined in spec (installation guides, code, alternative platforms)
- Focus maintained on conceptual understanding
- No feature creep: 3 chapters, defined word counts, specific learning outcomes

**VERDICT**: ✅ ALL GATES PASSED - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/001-module-2/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (research findings)
├── content-outline.md   # Phase 1 output (detailed chapter outlines)
├── style-guide.md       # Phase 1 output (Module 1 style analysis)
├── persona-examples.md  # Phase 1 output (persona callout templates)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
physical-ai-textbook/
└── docs/
    └── docs/
        ├── module-1-ros2/              # Existing Module 1 (reference)
        │   ├── chapter-1-introduction-to-ros2.md
        │   ├── chapter-2-ros2-communication-model.md
        │   └── chapter-3-bridging-ai-agents-with-ros2.md
        │
        └── module-2-simulation/         # NEW - This module
            ├── _category_.json          # Sidebar configuration
            ├── chapter-1-introduction-to-digital-twins.md
            ├── chapter-2-robot-simulation-with-gazebo.md
            └── chapter-3-sensors-and-environments.md
```

**Structure Decision**: Educational content project using Docusaurus documentation structure. Chapters are markdown files with frontmatter metadata. No source code directory needed (content-only project). Module 2 follows Module 1's established directory pattern for consistency.

## Complexity Tracking

> **Not applicable** - All Constitution Check gates passed without violations.

## Phase 0: Research & Content Planning

### Objectives
1. Analyze Module 1 style, formatting, and pedagogical patterns
2. Research real-world digital twin examples in humanoid robotics
3. Identify Gazebo simulation concepts that need conceptual explanation
4. Research sim-to-real gap strategies and domain randomization approaches
5. Create detailed content outlines for all 3 chapters

### Tasks

#### T001: Analyze Module 1 for Style Consistency
**Goal**: Extract style guide from Module 1 chapters to ensure Module 2 consistency

**Actions**:
1. Read all 3 Module 1 chapters
2. Document:
   - Frontmatter structure and fields
   - Heading hierarchy and naming conventions
   - Persona callout format and placement
   - Section transitions and "What's Next" format
   - Analogy style (e.g., "Think of ROS 2 as...")
   - Table formatting and comparison matrices
   - Summary structure
3. Create `style-guide.md` with findings

**Output**: `specs/001-module-2/style-guide.md`

**Success Criteria**:
- Style guide captures all formatting conventions from Module 1
- Persona callout emoji usage documented (💡🛠️🤖🧠)
- Frontmatter template extracted
- Heading level patterns identified (# for title, ## for major sections, ### for subsections)

---

#### T002: Research Real-World Digital Twin Examples
**Goal**: Identify 5+ concrete examples of digital twins in humanoid robotics for Chapter 1

**Actions**:
1. Research Boston Dynamics' use of simulation for Atlas, Spot development
2. Research Tesla's Optimus simulation pipeline
3. Research Sanctuary AI's Phoenix simulation approach
4. Research Figure AI's humanoid simulation strategy
5. Research academic/open-source examples (e.g., IHMC, PAL Robotics)
6. Document for each:
   - What they simulate (physics, sensors, environments)
   - Why they use simulation (cost, safety, speed)
   - How simulation connects to real robot testing
   - Key takeaway for students

**Output**: Add findings to `specs/001-module-2/research.md` under "Digital Twin Examples"

**Success Criteria**:
- At least 5 real-world examples documented
- Each example has clear "why it matters" explanation
- Examples span different humanoid applications (walking, manipulation, navigation)
- Sources cited for verification

---

#### T003: Research Gazebo Simulation Concepts
**Goal**: Identify key Gazebo/physics simulation concepts to explain conceptually in Chapter 2

**Actions**:
1. Research physics engines (ODE, Bullet, DART) and their trade-offs
2. Research URDF/SDF model formats (purpose, structure, use cases)
3. Research Gazebo-ROS 2 integration mechanisms (ros_gz_bridge)
4. Research realistic simulation parameters (gravity, friction coefficients, material properties)
5. Research simulation performance vs realism trade-offs
6. Identify which concepts need analogies for software engineers (e.g., "URDF is like JSON schema for robots")

**Output**: Add findings to `specs/001-module-2/research.md` under "Gazebo Concepts"

**Success Criteria**:
- Key concepts identified with clear definitions
- Analogies drafted for each concept
- Technical accuracy verified against Gazebo documentation
- Complexity level appropriate for conceptual explanation (no deep math)

---

#### T004: Research Sensor Simulation and Sim-to-Real Gap
**Goal**: Research sensor simulation techniques and strategies for Chapter 3

**Actions**:
1. Research camera simulation (RGB, depth, fisheye) in Gazebo/Isaac Sim
2. Research LiDAR simulation (raycast patterns, noise models)
3. Research IMU simulation (acceleration, gyroscope, magnetometer)
4. Research sensor noise and latency modeling
5. Research sim-to-real gap challenges:
   - Domain randomization techniques
   - Transfer learning strategies
   - Reality gap quantification methods
6. Research environment design best practices:
   - Lighting variation
   - Surface material properties
   - Dynamic obstacles
   - Weather conditions (if applicable)

**Output**: Add findings to `specs/001-module-2/research.md` under "Sensor Simulation & Sim-to-Real"

**Success Criteria**:
- All sensor types covered (camera, LiDAR, IMU)
- Sim-to-real strategies documented with examples
- Environment design principles extracted
- Practical guidance for students designing virtual environments

---

#### T005: Create Detailed Chapter Outlines
**Goal**: Expand high-level spec requirements into detailed section-by-section outlines

**Actions**:
1. For each chapter, create detailed outline with:
   - Exact section headings (## and ###)
   - Paragraph-level guidance (what each paragraph should cover)
   - Word count allocation per section
   - Placement of persona callouts
   - Placement of tables/diagrams
   - Cross-references to Module 1
2. Ensure outlines satisfy all functional requirements from spec
3. Map acceptance scenarios to specific sections

**Output**: `specs/001-module-2/content-outline.md`

**Success Criteria**:
- All 37 functional requirements mapped to outline sections
- Word counts allocated (totals match spec targets)
- Persona callout placements identified (4-6 per chapter)
- Table/diagram locations specified
- Outline readable by content writer for immediate drafting

---

#### T006: Create Persona Callout Templates
**Goal**: Draft example persona callouts for each learner type to guide content creation

**Actions**:
1. Review Module 1 persona callouts for tone and structure
2. Create 2-3 example callouts for each persona type:
   - 💡 Beginner: Simple analogy, everyday language
   - 🛠️ Software Engineer: Parallel to familiar dev concepts
   - 🤖 Robotics Student: Technical depth, terminology
   - 🧠 AI Researcher: ML/AI integration perspective
3. Ensure examples span different topics (digital twins, Gazebo, sensors)
4. Validate tone matches Module 1

**Output**: `specs/001-module-2/persona-examples.md`

**Success Criteria**:
- 8-12 total example callouts (2-3 per persona)
- Examples demonstrate appropriate tone for each persona
- Examples show how to connect new concepts to existing knowledge
- Writer can use as templates for remaining callouts

---

### Research Deliverable

**Output File**: `specs/001-module-2/research.md`

**Contents**:
1. **Digital Twin Examples** (T002)
   - 5+ real-world humanoid robotics examples
   - Key takeaways for students
2. **Gazebo Concepts** (T003)
   - Physics engines, URDF/SDF, ROS 2 integration
   - Analogies for software engineers
3. **Sensor Simulation & Sim-to-Real** (T004)
   - Camera, LiDAR, IMU simulation
   - Domain randomization and transfer learning
   - Environment design principles
4. **Module 1 Style Guide** (T001)
   - Formatting conventions
   - Persona callout patterns
5. **Content Outlines** (T005)
   - Detailed section-by-section outlines for all 3 chapters
6. **Persona Examples** (T006)
   - Template callouts for each persona type

**Decision**: All research will inform Phase 1 content creation. No technical architecture decisions needed (this is content creation, not software development).

## Phase 1: Content Structure & Templates

### Objectives
1. Create Docusaurus directory and sidebar configuration
2. Create chapter markdown files with frontmatter and section headings
3. Validate structure against Module 1 consistency
4. Prepare for Phase 2 content writing (tasks.md generation)

### Tasks

#### T007: Create Module 2 Directory Structure
**Goal**: Set up Docusaurus directory for Module 2

**Actions**:
1. Create `physical-ai-textbook/docs/docs/module-2-simulation/` directory
2. Create `_category_.json` for sidebar configuration:
   ```json
   {
     "label": "Module 2: Simulation & Digital Twins",
     "position": 2,
     "link": {
       "type": "generated-index",
       "description": "Learn how robots are designed, tested, and trained in simulated environments before entering the physical world."
     }
   }
   ```
3. Verify Module 1 still builds correctly after adding new directory

**Output**: Directory structure created, sidebar configured

**Success Criteria**:
- Directory exists and is accessible to Docusaurus
- Sidebar configuration matches Module 1 pattern
- Docusaurus build succeeds (no broken links)

---

#### T008: Create Chapter 1 Template
**Goal**: Create `chapter-1-introduction-to-digital-twins.md` with structure

**Actions**:
1. Create markdown file with frontmatter:
   ```yaml
   ---
   sidebar_position: 1
   title: "Chapter 1: Introduction to Digital Twins"
   keywords: ["digital-twin", "simulation", "gazebo", "physical-ai", "robotics"]
   learning_objectives:
     - "Explain what a digital twin is and why simulation is critical for Physical AI"
     - "Compare simulation vs physical reality trade-offs"
     - "List real-world digital twin examples in humanoid robotics"
     - "Describe the role of simulation in the development pipeline"
   difficulty: "beginner"
   estimated_reading_time: 25
   ---
   ```
2. Add all section headings from content outline (T005)
3. Add placeholder comments indicating:
   - Word count targets per section
   - Persona callout placements
   - Table/diagram locations
4. Add empty "What's Next" teaser at end

**Output**: `physical-ai-textbook/docs/docs/module-2-simulation/chapter-1-introduction-to-digital-twins.md`

**Success Criteria**:
- File has valid Docusaurus frontmatter
- All required sections present (from FR-001 through FR-010)
- Structure matches content outline
- Placeholder comments guide writer

---

#### T009: Create Chapter 2 Template
**Goal**: Create `chapter-2-robot-simulation-with-gazebo.md` with structure

**Actions**:
1. Create markdown file with frontmatter:
   ```yaml
   ---
   sidebar_position: 2
   title: "Chapter 2: Robot Simulation with Gazebo"
   keywords: ["gazebo", "physics-simulation", "urdf", "sdf", "ros2", "simulation"]
   learning_objectives:
     - "Explain Gazebo's role as a physics-based simulator"
     - "Describe how physics engines simulate gravity, collisions, and joints"
     - "Understand URDF and SDF robot model formats conceptually"
     - "Explain ROS 2 + Gazebo communication flow"
     - "Describe a simulated humanoid walking loop"
   difficulty: "intermediate"
   estimated_reading_time: 30
   ---
   ```
2. Add all section headings from content outline (T005)
3. Add placeholder comments for:
   - Word count targets per section
   - Persona callout placements (emphasize Software Engineer and Robotics Student)
   - Table/diagram locations
   - Module 1 cross-references (at least 3)
4. Add empty "What's Next" teaser at end

**Output**: `physical-ai-textbook/docs/docs/module-2-simulation/chapter-2-robot-simulation-with-gazebo.md`

**Success Criteria**:
- File has valid Docusaurus frontmatter
- All required sections present (from FR-011 through FR-020)
- Structure matches content outline
- Cross-reference placeholders identified

---

#### T010: Create Chapter 3 Template
**Goal**: Create `chapter-3-sensors-and-environments.md` with structure

**Actions**:
1. Create markdown file with frontmatter:
   ```yaml
   ---
   sidebar_position: 3
   title: "Chapter 3: Sensors and Simulated Environments"
   keywords: ["sensors", "camera", "lidar", "imu", "simulation", "environment-design", "sim-to-real"]
   learning_objectives:
     - "Explain why sensor simulation is critical for Physical AI"
     - "Describe camera, LiDAR, and IMU simulation"
     - "Understand sensor noise, latency, and failure modes"
     - "Design virtual environments for robot training"
     - "Address the sim-to-real gap"
   difficulty: "intermediate"
   estimated_reading_time: 30
   ---
   ```
2. Add all section headings from content outline (T005)
3. Add placeholder comments for:
   - Word count targets per section
   - Persona callout placements (emphasize AI Researcher and Robotics Student)
   - Table/diagram locations
4. Add empty "What's Next" teaser at end

**Output**: `physical-ai-textbook/docs/docs/module-2-simulation/chapter-3-sensors-and-environments.md`

**Success Criteria**:
- File has valid Docusaurus frontmatter
- All required sections present (from FR-021 through FR-030)
- Structure matches content outline
- Sim-to-real gap section prominently placed

---

#### T011: Validate Module 2 Structure
**Goal**: Ensure Module 2 structure matches Module 1 consistency requirements

**Actions**:
1. Build Docusaurus site: `npm run build`
2. Verify all 3 chapters appear in sidebar
3. Verify chapter order (1, 2, 3)
4. Verify estimated reading times sum to 85 minutes (25+30+30)
5. Compare frontmatter structure to Module 1 chapters
6. Verify no broken links or build errors

**Output**: Validation report documenting any inconsistencies

**Success Criteria**:
- Docusaurus builds without errors
- All 3 chapters visible in sidebar with correct order
- Frontmatter matches Module 1 pattern
- Estimated reading times reasonable (total 85 min, target 90-120 min allows buffer for content expansion)

---

### Phase 1 Deliverables

1. **Module 2 Directory**: `physical-ai-textbook/docs/docs/module-2-simulation/`
2. **Sidebar Config**: `_category_.json`
3. **Chapter Templates** (3 files):
   - `chapter-1-introduction-to-digital-twins.md`
   - `chapter-2-robot-simulation-with-gazebo.md`
   - `chapter-3-sensors-and-environments.md`
4. **Validation Report**: Confirming structure consistency

**Decision**: Chapter templates include all required sections from spec, with placeholders guiding content creation in Phase 2 (via tasks.md). Frontmatter provides metadata for RAG retrieval and sidebar navigation.

## Phase 2: Task Generation (Not Included in /sp.plan)

**Note**: Phase 2 (task generation) is handled by the `/sp.tasks` command, which will be run separately after this plan is approved.

**Expected Tasks Output**:
- Task breakdown for writing Chapter 1 content (14 sections based on outline)
- Task breakdown for writing Chapter 2 content (15 sections based on outline)
- Task breakdown for writing Chapter 3 content (16 sections based on outline)
- Persona callout generation tasks (12-18 total)
- Table/diagram creation tasks (3+)
- Cross-reference validation tasks
- Word count verification tasks
- RAG embedding tasks (after content complete)
- Comprehension quiz creation tasks (for success criteria validation)

The `/sp.tasks` command will generate a dependency-ordered task list in `specs/001-module-2/tasks.md` based on this plan and the functional requirements in the spec.

## Risk Assessment

### High Risk
**Risk**: Content quality inconsistent with Module 1 (tone, depth, formatting)
**Mitigation**: T001 analyzes Module 1 thoroughly; T006 creates persona templates; all tasks reference style guide
**Impact if unmitigated**: Students notice jarring transition between modules; RAG chatbot provides inconsistent responses

**Risk**: Technical inaccuracies in Gazebo/simulation concepts
**Mitigation**: T003 research validates against official Gazebo docs; constitution requires technical accuracy; review by robotics expert recommended
**Impact if unmitigated**: Students learn incorrect concepts; erosion of trust; poor preparation for real-world simulation usage

### Medium Risk
**Risk**: Word count targets not met (too short or too long)
**Mitigation**: Content outline (T005) allocates word counts per section; tasks.md will include word count verification tasks
**Impact if unmitigated**: Module feels rushed (too short) or overwhelming (too long); reading time estimate inaccurate

**Risk**: Persona callout distribution uneven (some chapters have too few)
**Mitigation**: Content outline specifies callout placements; tasks.md will include persona callout generation tasks with targets
**Impact if unmitigated**: Some learner types feel underserved; adaptive learning less effective

### Low Risk
**Risk**: RAG embedding pipeline fails for Module 2 content
**Mitigation**: Pipeline already working for Module 1; Module 2 uses same chunk size and structure
**Impact if unmitigated**: Chatbot cannot answer Module 2 questions; manual debugging required

**Risk**: Docusaurus build breaks after adding Module 2
**Mitigation**: T011 validates build after structure creation; incremental testing during content writing
**Impact if unmitigated**: Site deployment blocked; fix required before merge

## Post-Implementation Notes

### Content Review Process (After tasks.md execution)
1. **Technical Review**: Robotics expert validates Gazebo/simulation accuracy
2. **Pedagogical Review**: Educator validates learning progression and clarity
3. **Style Review**: Compare against Module 1 for consistency
4. **RAG Testing**: Test persona-based queries against embedded Module 2 content
5. **Student Testing**: Pilot with 3-5 target audience members, gather comprehension feedback

### Success Metrics (From SC-001 through SC-015)
- **SC-001**: 90% of students can define "digital twin" after Chapter 1 (test with comprehension quiz)
- **SC-002**: 85% can describe Gazebo pipeline after Chapter 2 (test with conceptual diagram exercise)
- **SC-003**: 80% can design virtual environment after Chapter 3 (test with scenario-based question)
- **SC-004**: Flesch-Kincaid Grade Level 10-12 (validate with readability tool)
- **SC-005**: Total 11,500-12,500 words (validate with word count script)
- **SC-006**: 4-6 persona callouts per chapter (validate with grep/count)
- **SC-007**: 85% quiz pass rate at 70%+ correct (requires quiz creation and student testing)
- **SC-008**: 90-120 minute completion time (validate with student timing during pilot)
- **SC-009**: Zero installation instructions/code (validate with manual review)
- **SC-010**: 5+ Module 1 cross-references (validate with grep for "Module 1" and chapter links)

### Future Enhancements (Post-Module 2 Launch)
- Add actual diagrams/visualizations (conceptual descriptions are placeholders)
- Create interactive Gazebo demos (embedded in Docusaurus)
- Develop hands-on simulation labs (separate from conceptual textbook content)
- Add video walkthroughs of real-world digital twin examples
- Translate to Urdu (following Module 1 translation pattern)

## Constitution Re-Check (Post-Design)

**Re-evaluation after Phase 1 completion**:

All gates remain **PASSED**:
- ✅ Educational Clarity: Chapter templates include all required structural elements
- ✅ Technical Accuracy: Research phase (T003) validates concepts against official documentation
- ✅ AI-Native Design: Chapter structure supports semantic chunking
- ✅ RAG Compatibility: Frontmatter provides metadata for filtering
- ✅ Personalization: Persona callouts planned in templates
- ⚠️ Multi-Language: Still deferred (English only for initial release)
- ✅ Reusable Intelligence: Content structure matches Module 1 (proven RAG compatibility)
- ✅ Documentation Standards: Docusaurus frontmatter and sidebar config follow Module 1 pattern
- ✅ Ethics & Integrity: Research phase includes source verification
- ✅ Scope Control: Templates strictly follow spec requirements (no scope creep)

**Final Verdict**: ✅ **PROCEED TO PHASE 2 (/sp.tasks)** - All gates passed, plan ready for task generation.
