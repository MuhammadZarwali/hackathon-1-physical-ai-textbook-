---
description: "Task list for Module 2 content creation - The Digital Twin: Simulation & Virtual Environments"
---

# Tasks: Module 2 - The Digital Twin: Simulation & Virtual Environments

**Input**: Design documents from `/specs/001-module-2/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No automated tests for educational content. Validation tasks included for word count, readability, and RAG compatibility.

**Organization**: Tasks are grouped by user story (P1, P2, P3) to enable independent chapter creation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files/chapters, no dependencies)
- **[Story]**: Which user story (chapter) this task belongs to (US1=Chapter 1, US2=Chapter 2, US3=Chapter 3)
- Include exact file paths in descriptions

## Path Conventions

- **Content directory**: `physical-ai-textbook/docs/docs/module-2-simulation/`
- **Planning artifacts**: `specs/001-module-2/`
- **Reference content**: `physical-ai-textbook/docs/docs/module-1-ros2/` (Module 1 chapters for style consistency)

---

## Phase 1: Setup (Research & Infrastructure)

**Purpose**: Research, style analysis, and directory structure setup before content creation

**⏱️ Estimated Duration**: 4-6 hours

- [ ] T001 Create Module 2 directory structure at `physical-ai-textbook/docs/docs/module-2-simulation/`
- [ ] T002 Create `_category_.json` sidebar configuration file in module-2-simulation directory
- [ ] T003 [P] Read all 3 Module 1 chapters and extract style guide to `specs/001-module-2/style-guide.md`
- [ ] T004 [P] Research Boston Dynamics digital twin examples and document in `specs/001-module-2/research.md`
- [ ] T005 [P] Research Tesla Optimus simulation pipeline and add to research.md
- [ ] T006 [P] Research Sanctuary AI Phoenix simulation approach and add to research.md
- [ ] T007 [P] Research Figure AI humanoid simulation strategy and add to research.md
- [ ] T008 [P] Research academic/open-source digital twin examples (IHMC, PAL Robotics) and add to research.md
- [ ] T009 [P] Research Gazebo physics engines (ODE, Bullet, DART) trade-offs and add to research.md
- [ ] T010 [P] Research URDF/SDF robot model formats and create analogies for research.md
- [ ] T011 [P] Research Gazebo-ROS 2 integration mechanisms (ros_gz_bridge) and document in research.md
- [ ] T012 [P] Research camera simulation (RGB, depth, fisheye) techniques and add to research.md
- [ ] T013 [P] Research LiDAR simulation (raycast patterns, noise models) and add to research.md
- [ ] T014 [P] Research IMU simulation (acceleration, gyroscope, magnetometer) and add to research.md
- [ ] T015 [P] Research sim-to-real gap strategies (domain randomization, transfer learning) and add to research.md
- [ ] T016 [P] Research environment design best practices (lighting, surfaces, obstacles) and add to research.md
- [ ] T017 Consolidate research.md and validate all 5+ digital twin examples documented
- [ ] T018 Validate style-guide.md captures frontmatter structure, persona format, and heading patterns from Module 1

**Checkpoint**: Research complete - 5+ real-world examples documented, Gazebo/sensor concepts researched, Module 1 style guide extracted

---

## Phase 2: Content Planning (Blocking Prerequisites)

**Purpose**: Detailed outlines and templates that MUST be complete before ANY chapter writing can begin

**⚠️ CRITICAL**: No chapter content creation can begin until this phase is complete

**⏱️ Estimated Duration**: 3-4 hours

- [ ] T019 Create detailed outline for Chapter 1 with section headings and word allocations in `specs/001-module-2/content-outline.md`
- [ ] T020 Add detailed outline for Chapter 2 with section headings and word allocations to content-outline.md
- [ ] T021 Add detailed outline for Chapter 3 with section headings and word allocations to content-outline.md
- [ ] T022 Map all 37 functional requirements from spec.md to sections in content-outline.md
- [ ] T023 [P] Create 2-3 example persona callouts for Beginner type in `specs/001-module-2/persona-examples.md`
- [ ] T024 [P] Create 2-3 example persona callouts for Software Engineer type in persona-examples.md
- [ ] T025 [P] Create 2-3 example persona callouts for Robotics Student type in persona-examples.md
- [ ] T026 [P] Create 2-3 example persona callouts for AI Researcher type in persona-examples.md
- [ ] T027 Validate persona-examples.md has 8-12 total examples with appropriate tone for each type
- [ ] T028 Create Chapter 1 markdown file with frontmatter and empty section headings at `physical-ai-textbook/docs/docs/module-2-simulation/chapter-1-introduction-to-digital-twins.md`
- [ ] T029 Create Chapter 2 markdown file with frontmatter and empty section headings at `physical-ai-textbook/docs/docs/module-2-simulation/chapter-2-robot-simulation-with-gazebo.md`
- [ ] T030 Create Chapter 3 markdown file with frontmatter and empty section headings at `physical-ai-textbook/docs/docs/module-2-simulation/chapter-3-sensors-and-environments.md`
- [ ] T031 Validate all 3 chapter files have correct Docusaurus frontmatter matching Module 1 pattern
- [ ] T032 Build Docusaurus site and verify Module 2 appears in sidebar with correct chapter order

**Checkpoint**: Planning complete - detailed outlines with word counts, persona templates, chapter structure files created and validated

---

## Phase 3: User Story 1 - Learn Digital Twin Fundamentals (Priority: P1) 🎯 MVP

**Goal**: Students with no robotics background can read Chapter 1 and explain what a digital twin is, why simulation is critical, and how it fits into the humanoid robotics development pipeline.

**Independent Test**: Have a robotics beginner read Chapter 1 and successfully explain (1) what a digital twin is using an analogy, (2) why simulation reduces costs/risks, and (3) list 3 specific use cases where simulation is essential.

**Target**: Chapter 1 (3,500-4,000 words) with 4-6 persona callouts

**⏱️ Estimated Duration**: 8-10 hours

### Implementation for User Story 1 (Chapter 1 Content)

- [ ] T033 [US1] Write Chapter 1 introduction section (300-400 words) defining "digital twin" in first 500 words (FR-001)
- [ ] T034 [US1] Write "What Is a Digital Twin?" section (500-600 words) with beginner-friendly analogies (FR-005)
- [ ] T035 [US1] Add 💡 Beginner persona callout to "What Is a Digital Twin?" section with video game sandbox analogy
- [ ] T036 [US1] Add 🛠️ Software Engineer persona callout comparing digital twins to staging environments
- [ ] T037 [US1] Write "Simulation vs Physical Reality" section (600-700 words) with comparison table (FR-002)
- [ ] T038 [US1] Create comparison table: Cost, Safety, Speed, Realism trade-offs for simulation vs physical reality
- [ ] T039 [US1] Add 🤖 Robotics Student persona callout explaining hardware-in-the-loop testing
- [ ] T040 [US1] Write "Why Robots Learn in Simulation First" section (700-800 words) explaining development pipeline (FR-004)
- [ ] T041 [US1] Add 🧠 AI Researcher persona callout connecting simulation to AI training data generation
- [ ] T042 [US1] Write "Digital Twins in Humanoid Development" section (800-900 words) with 3+ real-world examples (FR-003)
- [ ] T043 [US1] Add Boston Dynamics Atlas simulation example with specific details from research.md
- [ ] T044 [US1] Add Tesla Optimus simulation pipeline example with specific details from research.md
- [ ] T045 [US1] Add Sanctuary AI Phoenix example with specific details from research.md
- [ ] T046 [US1] Add 💡 Beginner persona callout explaining why humanoids need more simulation than simpler robots
- [ ] T047 [US1] Write Chapter 1 summary section (400-500 words) reinforcing key takeaways (FR-006)
- [ ] T048 [US1] Write "What's Next" teaser (100-150 words) connecting to Chapter 2 Gazebo content (FR-010)
- [ ] T049 [US1] Validate Chapter 1 word count is 3,500-4,000 words (FR-008)
- [ ] T050 [US1] Validate Chapter 1 has 4-6 persona callouts distributed across sections (FR-007, SC-006)
- [ ] T051 [US1] Validate Chapter 1 has no installation instructions, code, or CLI commands (FR-009, SC-009)
- [ ] T052 [US1] Validate Chapter 1 comparison table is properly formatted and complete (FR-002)
- [ ] T053 [US1] Validate Chapter 1 frontmatter has learning objectives and estimated reading time (FR-006, FR-032)

**Checkpoint**: Chapter 1 complete and independently testable - students can explain digital twins, simulation value, and real-world examples

---

## Phase 4: User Story 2 - Understand Gazebo Simulation Architecture (Priority: P2)

**Goal**: Students with ROS 2 knowledge (Module 1) can read Chapter 2 and explain how Gazebo simulates physics, robot models, and sensor behavior, plus how it integrates with ROS 2 for humanoid robotics.

**Independent Test**: Have a student explain the Gazebo simulation pipeline (robot model → physics engine → ROS 2 communication) and describe how a humanoid walking loop would be simulated conceptually.

**Target**: Chapter 2 (4,000-4,500 words) with 4-6 persona callouts, 3+ Module 1 cross-references

**⏱️ Estimated Duration**: 10-12 hours

### Implementation for User Story 2 (Chapter 2 Content)

- [ ] T054 [US2] Write Chapter 2 introduction section (300-400 words) explaining Gazebo's role as physics-based simulator (FR-011)
- [ ] T055 [US2] Write "What Gazebo Simulates" section (600-700 words) covering gravity, collisions, friction, joints (FR-012)
- [ ] T056 [US2] Add 💡 Beginner persona callout using "video game physics engine" analogy for Gazebo
- [ ] T057 [US2] Write "Physics Engines and Realism" section (500-600 words) discussing ODE, Bullet, DART trade-offs (FR-012, FR-016)
- [ ] T058 [US2] Add 🛠️ Software Engineer persona callout comparing physics engine choice to database selection trade-offs
- [ ] T059 [US2] Write "Robot Models (URDF & SDF - Conceptual)" section (700-800 words) explaining purpose and structure (FR-013)
- [ ] T060 [US2] Add 🛠️ Software Engineer persona callout: "URDF is like a JSON schema for robot hardware"
- [ ] T061 [US2] Add 🤖 Robotics Student persona callout explaining when to use URDF vs SDF
- [ ] T062 [US2] Write "ROS 2 + Gazebo Communication Flow" section (800-900 words) with conceptual diagram description (FR-014)
- [ ] T063 [US2] Add conceptual diagram description: sensor data flow, control commands, clock synchronization between Gazebo and ROS 2
- [ ] T064 [US2] Add cross-reference to Module 1 Chapter 2 ROS 2 nodes and topics (first of 3 required, FR-017)
- [ ] T065 [US2] Write "Example: Simulated Humanoid Walking Loop (Conceptual)" section (900-1000 words) with detailed walkthrough (FR-015)
- [ ] T066 [US2] Add walkthrough: perception → planning → control → actuation → feedback loop for simulated walking
- [ ] T067 [US2] Add cross-reference to Module 1 Chapter 2 ROS 2 services for control commands (second of 3, FR-017)
- [ ] T068 [US2] Add cross-reference to Module 1 Chapter 3 on bridging AI agents with ROS 2 (third of 3, FR-017)
- [ ] T069 [US2] Add 🧠 AI Researcher persona callout connecting walking loop to RL training in simulation
- [ ] T070 [US2] Write Chapter 2 summary section (400-500 words) reinforcing Gazebo pipeline and ROS 2 integration
- [ ] T071 [US2] Write "What's Next" teaser (100-150 words) connecting to Chapter 3 sensor simulation
- [ ] T072 [US2] Validate Chapter 2 word count is 4,000-4,500 words (FR-019)
- [ ] T073 [US2] Validate Chapter 2 has 4-6 persona callouts with at least one per major section (FR-018, SC-006)
- [ ] T074 [US2] Validate Chapter 2 has 3+ Module 1 cross-references (FR-017, SC-010)
- [ ] T075 [US2] Validate Chapter 2 formatting and style matches Module 1 chapters (FR-020)
- [ ] T076 [US2] Validate Chapter 2 has no full URDF/SDF files or terminal commands (FR-013, SC-009)
- [ ] T077 [US2] Validate Chapter 2 frontmatter and estimated reading time correct (FR-032)

**Checkpoint**: Chapter 2 complete and independently testable - students can explain Gazebo simulation pipeline and ROS 2 integration

---

## Phase 5: User Story 3 - Master Sensor Simulation and Environment Design (Priority: P3)

**Goal**: Students preparing for Physical AI careers can read Chapter 3 and understand how virtual sensors are simulated, how environmental factors affect perception, and how simulation data prepares AI systems for real-world deployment.

**Independent Test**: Have a student design a virtual environment for training a humanoid to navigate stairs, specifying which sensors to simulate, environmental factors to vary, and how to validate realism.

**Target**: Chapter 3 (4,000-4,500 words) with 4-6 persona callouts, focus on AI Researcher perspective

**⏱️ Estimated Duration**: 10-12 hours

### Implementation for User Story 3 (Chapter 3 Content)

- [ ] T078 [US3] Write Chapter 3 introduction section (300-400 words) explaining why sensor simulation is critical for Physical AI (FR-021)
- [ ] T079 [US3] Write "Why Sensors Must Be Simulated" section (500-600 words) connecting to AI perception systems
- [ ] T080 [US3] Add 🧠 AI Researcher persona callout on how simulation data feeds ML training pipelines
- [ ] T081 [US3] Write "Camera, Depth, LiDAR, and IMU Simulation" section (900-1000 words) covering all sensor types (FR-022)
- [ ] T082 [US3] Add subsection on camera simulation (RGB, depth) with behavioral descriptions from research.md
- [ ] T083 [US3] Add subsection on LiDAR simulation with raycast pattern descriptions from research.md
- [ ] T084 [US3] Add subsection on IMU simulation (accel, gyro, mag) with data characteristics from research.md
- [ ] T085 [US3] Create comparison table: Camera vs LiDAR trade-offs (range, resolution, weather sensitivity, compute cost)
- [ ] T086 [US3] Add 💡 Beginner persona callout using smartphone sensors as analogy for robot IMUs
- [ ] T087 [US3] Add 🛠️ Software Engineer persona callout comparing sensor fusion to API data aggregation
- [ ] T088 [US3] Write "Environmental Factors (light, surfaces, obstacles)" section (700-800 words) covering perception challenges (FR-024)
- [ ] T089 [US3] Add 🤖 Robotics Student persona callout on lighting conditions affecting camera perception
- [ ] T090 [US3] Write "Simulation Data for AI Models" section (600-700 words) explaining data formats, volume, domain randomization (FR-025)
- [ ] T091 [US3] Add 🧠 AI Researcher persona callout on domain randomization techniques and sample complexity
- [ ] T092 [US3] Write "Simulation Limits and Reality Gaps" section (800-900 words) addressing sim-to-real gap honestly (FR-026)
- [ ] T093 [US3] Add strategies: realistic rendering, physics tuning, domain randomization, transfer learning (FR-026)
- [ ] T094 [US3] Add 🧠 AI Researcher persona callout on quantifying reality gap and adaptive techniques
- [ ] T095 [US3] Write environment design guidance subsection (400-500 words) for specific scenarios (navigation, manipulation, locomotion) (FR-027)
- [ ] T096 [US3] Add 🤖 Robotics Student persona callout on stairs navigation environment design example
- [ ] T097 [US3] Write Chapter 3 summary section (400-500 words) reinforcing sensor simulation and sim-to-real strategies
- [ ] T098 [US3] Write "What's Next" teaser (100-150 words) hinting at Module 3 (AI/ML integration for robot control)
- [ ] T099 [US3] Validate Chapter 3 word count is 4,000-4,500 words (FR-029)
- [ ] T100 [US3] Validate Chapter 3 has 4-6 persona callouts with focus on AI Researcher type (FR-028, SC-006)
- [ ] T101 [US3] Validate Chapter 3 sensor noise, latency, and failure modes are explained (FR-023)
- [ ] T102 [US3] Validate Chapter 3 has no real hardware setup instructions or wiring diagrams (FR-030, SC-009)
- [ ] T103 [US3] Validate Chapter 3 comparison table is properly formatted (SC-011)
- [ ] T104 [US3] Validate Chapter 3 frontmatter and estimated reading time correct (FR-032)

**Checkpoint**: Chapter 3 complete and independently testable - students can design virtual environments and understand sim-to-real challenges

---

## Phase 6: Module-Level Validation & Polish

**Purpose**: Cross-chapter validation, RAG optimization, and final quality checks

**⏱️ Estimated Duration**: 4-5 hours

### Content Validation

- [ ] T105 Validate total Module 2 word count is 11,500-12,500 words across all 3 chapters (SC-005)
- [ ] T106 Validate all 3 chapters use consistent terminology with Module 1 (FR-031)
- [ ] T107 Validate all persona callouts use exact emoji format: 💡🛠️🤖🧠 (FR-034)
- [ ] T108 Count total persona callouts across module (should be 12-18 total, SC-006)
- [ ] T109 Count Module 1 cross-references across module (should be 5+, SC-010)
- [ ] T110 Validate all chapters have comparison tables or decision matrices (FR-035, SC-011)
- [ ] T111 Validate beginner-friendly analogies appear in every major section (SC-012)
- [ ] T112 Count real-world humanoid robotics examples cited (should be 5+ across module, SC-013)
- [ ] T113 Validate technical jargon (digital twin, URDF, SDF, IMU, LiDAR) defined on first use in each chapter (SC-014)
- [ ] T114 Review all persona callouts for actionable insights vs general commentary (SC-015)

### Readability & Style

- [ ] T115 Run Flesch-Kincaid readability test on all 3 chapters (target: Grade Level 10-12, SC-004)
- [ ] T116 Validate Chapter 1 estimated reading time is 25 minutes based on word count
- [ ] T117 Validate Chapter 2 estimated reading time is 30 minutes based on word count
- [ ] T118 Validate Chapter 3 estimated reading time is 30 minutes based on word count
- [ ] T119 Validate total module reading time is 85 minutes (within 90-120 minute target, SC-008)
- [ ] T120 Review all 3 chapters for consistent writing tone matching Module 1 (FR-033)

### RAG Compatibility

- [ ] T121 Validate all chapters can be semantically chunked by H2/H3 sections (200-500 words per chunk)
- [ ] T122 Validate each major section has explicit definitions and can stand alone conceptually
- [ ] T123 Validate frontmatter keywords are descriptive and aid retrieval (FR-032)
- [ ] T124 Build Docusaurus site and verify no broken links or build errors
- [ ] T125 Verify all 3 chapters load in under 2 seconds in browser

### RAG Embedding (After Content Complete)

- [ ] T126 Run embedding pipeline script on Chapter 1: `python scripts/embed_chapters_gemini.py` (embed chapter-1-introduction-to-digital-twins.md)
- [ ] T127 Run embedding pipeline script on Chapter 2 (embed chapter-2-robot-simulation-with-gazebo.md)
- [ ] T128 Run embedding pipeline script on Chapter 3 (embed chapter-3-sensors-and-environments.md)
- [ ] T129 Verify Module 2 chunks appear in Qdrant collection (expected: 35-40 chunks)
- [ ] T130 Test RAG query: "What is a digital twin?" with beginner persona - verify Chapter 1 content retrieved
- [ ] T131 Test RAG query: "How does Gazebo simulate physics?" with robotics_student persona - verify Chapter 2 content retrieved
- [ ] T132 Test RAG query: "How do I design a simulation environment?" with ai_researcher persona - verify Chapter 3 content retrieved
- [ ] T133 Test RAG query: "What is the sim-to-real gap?" across all personas - verify Chapter 3 section retrieved
- [ ] T134 Validate RAG response time is under 5 seconds for all test queries

**Checkpoint**: Module 2 complete, validated, and embedded in RAG system - ready for student testing and feedback

---

## Phase 7: Student Testing & Comprehension (Optional - Post-Launch)

**Purpose**: Validate learning outcomes with real students (deferred to post-launch for MVP)

**Note**: These tasks validate success criteria SC-001, SC-002, SC-003, SC-007, SC-008 but require actual student participants.

### Comprehension Testing

- [ ] T135 Create comprehension quiz for Chapter 1 (10 questions testing FR-001 through FR-010)
- [ ] T136 Create comprehension quiz for Chapter 2 (10 questions testing FR-011 through FR-020)
- [ ] T137 Create comprehension quiz for Chapter 3 (10 questions testing FR-021 through FR-030)
- [ ] T138 Recruit 5-10 students from target audience (robotics beginners, software engineers, AI students)
- [ ] T139 Have students read Chapter 1 and take quiz (target: 90% can define digital twin, SC-001)
- [ ] T140 Have students read Chapter 2 and take quiz (target: 85% can describe Gazebo pipeline, SC-002)
- [ ] T141 Have students read Chapter 3 and complete environment design exercise (target: 80% success, SC-003)
- [ ] T142 Calculate overall quiz pass rate (target: 85% at 70%+ correct, SC-007)
- [ ] T143 Time students reading all 3 chapters (target: average 90-120 minutes, SC-008)
- [ ] T144 Gather qualitative feedback on clarity, analogies, and persona callout usefulness
- [ ] T145 Identify sections students found confusing or too advanced - create revision tasks if needed
- [ ] T146 Document student testing results in `specs/001-module-2/student-feedback.md`

**Checkpoint**: Module 2 validated with real students - success criteria met or improvement areas identified

---

## Summary

**Total Tasks**: 146 tasks across 7 phases

**Task Breakdown by Phase**:
- Phase 1 (Setup): 18 tasks (research & infrastructure)
- Phase 2 (Planning): 14 tasks (outlines & templates) - **BLOCKING**
- Phase 3 (US1 - Chapter 1): 21 tasks (3,500-4,000 words)
- Phase 4 (US2 - Chapter 2): 24 tasks (4,000-4,500 words)
- Phase 5 (US3 - Chapter 3): 27 tasks (4,000-4,500 words)
- Phase 6 (Validation): 30 tasks (quality checks & RAG embedding)
- Phase 7 (Student Testing): 12 tasks (optional, post-launch)

**Task Breakdown by User Story**:
- User Story 1 (Chapter 1): 21 content tasks (T033-T053)
- User Story 2 (Chapter 2): 24 content tasks (T054-T077)
- User Story 3 (Chapter 3): 27 content tasks (T078-T104)

**Parallel Opportunities**:
- Phase 1: T003-T016 can run in parallel (research tasks)
- Phase 2: T023-T026 can run in parallel (persona example creation)
- Each user story (chapter) is independent after Phase 2 complete
- Chapters 1, 2, 3 could theoretically be written by different authors simultaneously after outlines complete

**MVP Scope Recommendation**: Complete through Phase 3 (User Story 1 - Chapter 1 only)
- Delivers: Complete Chapter 1 (3,500-4,000 words) on digital twin fundamentals
- Students can: Understand what digital twins are and why simulation matters
- Can test independently: Quiz students on digital twin definition, simulation value, real-world examples
- Allows: Early feedback before investing in Chapters 2 & 3

**Full Module Delivery**: Complete through Phase 6 (all 3 chapters + validation)
- Delivers: Complete Module 2 (11,500-12,500 words) embedded in RAG system
- Students can: Progress from digital twin basics → Gazebo architecture → sensor simulation & environments
- Ready for: Production deployment and student access

**Dependencies**:
1. Phase 1 (Setup) → Phase 2 (Planning) [BLOCKING]
2. Phase 2 (Planning) → Phase 3, 4, 5 (Content Creation) [BLOCKING]
3. Phase 3, 4, 5 (All Chapters) → Phase 6 (Validation) [BLOCKING]
4. Phase 6 (Validation) → Phase 7 (Student Testing) [OPTIONAL]

**Independent Testing per Story**:
- **US1 (Chapter 1)**: Have robotics beginner read and explain digital twins, simulation value, 3 use cases
- **US2 (Chapter 2)**: Have ROS 2 student explain Gazebo pipeline (model → physics → ROS 2 comm)
- **US3 (Chapter 3)**: Have AI student design virtual environment specifying sensors, factors, validation

**Implementation Strategy**:
1. **MVP First**: Complete Phase 1, 2, and Phase 3 (Chapter 1 only) for early validation
2. **Incremental Delivery**: Add Chapter 2 (Phase 4), then Chapter 3 (Phase 5) based on feedback
3. **Parallel Work**: After Phase 2 complete, different authors can work on different chapters simultaneously
4. **Quality Gates**: Phase 6 validation catches cross-chapter inconsistencies before RAG embedding
5. **Student Validation**: Phase 7 provides real-world feedback for future improvements

**Success Metrics** (from spec.md):
- SC-001: 90% can define digital twin (Chapter 1 quiz)
- SC-002: 85% can describe Gazebo pipeline (Chapter 2 quiz)
- SC-003: 80% can design virtual environment (Chapter 3 exercise)
- SC-004: Flesch-Kincaid Grade Level 10-12 (T115 readability test)
- SC-005: 11,500-12,500 total words (T105 word count)
- SC-006: 4-6 persona callouts per chapter (T108 count validation)
- SC-007: 85% quiz pass rate at 70%+ (T142 student testing)
- SC-008: 90-120 minute completion time (T119, T143 timing validation)
- SC-009: Zero installation/code (T051, T076, T102 validation)
- SC-010: 5+ Module 1 cross-references (T109 count validation)
