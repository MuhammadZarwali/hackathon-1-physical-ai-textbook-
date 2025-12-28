# Tasks: Docusaurus UI Theme - Teal & Navy

**Input**: Design documents from `/specs/004-docusaurus-ui-theme/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No automated tests requested. Visual testing and Lighthouse audit during validation phase.

**Organization**: Tasks grouped by user story (US1-US4) to enable independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different CSS sections, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- File paths relative to: `physical-ai-textbook/docs/`

---

## Phase 1: Setup

**Purpose**: Prepare the CSS file structure and backup existing theme

- [x] T001 Backup existing custom.css to custom.css.backup in physical-ai-textbook/docs/src/css/
- [x] T002 Clear custom.css and add header comment block in physical-ai-textbook/docs/src/css/custom.css
- [x] T003 Verify Docusaurus dev server runs with empty custom.css

**Checkpoint**: Clean slate ready for theme implementation

---

## Phase 2: Foundational (Color System)

**Purpose**: Define all CSS custom properties that ALL user stories depend on

**CRITICAL**: All user stories require these color tokens to be defined first

### Light Mode Variables

- [x] T004 Define Teal primary color scale (--ifm-color-primary-*) in :root block in src/css/custom.css
- [x] T005 [P] Define Navy Blue custom variables (--theme-navy-*) in :root block in src/css/custom.css
- [x] T006 [P] Define neutral gray palette variables in :root block in src/css/custom.css
- [x] T007 [P] Define typography variables (line-height, font-color) in :root block in src/css/custom.css

### Dark Mode Variables

- [x] T008 Define dark mode Teal scale ([data-theme='dark']) in src/css/custom.css
- [x] T009 [P] Define dark mode Navy background colors ([data-theme='dark']) in src/css/custom.css
- [x] T010 [P] Define dark mode text colors ([data-theme='dark']) in src/css/custom.css
- [x] T011 [P] Define dark mode code highlighting color ([data-theme='dark']) in src/css/custom.css

### Validation

- [x] T012 Verify all color variables render correctly in browser dev tools
- [x] T013 Test light/dark mode toggle preserves variable definitions

**Checkpoint**: Color foundation complete - user story implementation can begin

---

## Phase 3: User Story 1 - Visual Brand Identity (Priority: P1) MVP

**Goal**: Establish Navy Blue structural elements (navbar, sidebar, footer) with Teal accents for professional brand identity

**Independent Test**: Load any page and verify Navy navbar, Navy sidebar, Teal active states render correctly

### Navbar Implementation (FR-006, FR-007, FR-008)

- [x] T014 [US1] Set .navbar background to Navy Blue in src/css/custom.css
- [x] T015 [P] [US1] Set .navbar__title color to white in src/css/custom.css
- [x] T016 [P] [US1] Set .navbar__link color to white with Teal hover in src/css/custom.css
- [x] T017 [P] [US1] Add .navbar__link--active Teal underline indicator in src/css/custom.css
- [x] T018 [P] [US1] Style .navbar__toggle (mobile menu icon) to white in src/css/custom.css
- [x] T019 [US1] Add dark mode navbar styles ([data-theme='dark'] .navbar) in src/css/custom.css

### Sidebar Implementation (FR-009, FR-010, FR-011)

- [x] T020 [US1] Set .menu background to Navy Blue in src/css/custom.css
- [x] T021 [P] [US1] Set .menu__link color to semi-transparent white in src/css/custom.css
- [x] T022 [P] [US1] Add .menu__link:hover subtle background overlay in src/css/custom.css
- [x] T023 [P] [US1] Add .menu__link--active Teal left border and background tint in src/css/custom.css
- [x] T024 [P] [US1] Style .menu__list-item-collapsible hover state in src/css/custom.css
- [x] T025 [US1] Add dark mode sidebar styles ([data-theme='dark'] .menu) in src/css/custom.css

### Footer Implementation

- [x] T026 [US1] Set .footer background to Navy Blue in src/css/custom.css
- [x] T027 [P] [US1] Set .footer__title color to white in src/css/custom.css
- [x] T028 [P] [US1] Set .footer__link-item color with Teal hover in src/css/custom.css
- [x] T029 [P] [US1] Set .footer__copyright color to muted white in src/css/custom.css
- [x] T030 [US1] Add dark mode footer styles ([data-theme='dark'] .footer) in src/css/custom.css

### Mobile Responsiveness (FR-028, FR-029)

- [x] T031 [US1] Verify navbar colors on mobile viewport (375px) in src/css/custom.css
- [x] T032 [US1] Verify sidebar drawer colors on mobile in src/css/custom.css

### Validation

- [x] T033 [US1] Test homepage renders with Navy navbar, sidebar, footer
- [x] T034 [US1] Test any chapter page renders with correct color scheme
- [x] T035 [US1] Test mobile viewport maintains color consistency

**Checkpoint**: User Story 1 complete - professional brand identity visible across site

---

## Phase 4: User Story 2 - Readable Content Experience (Priority: P2)

**Goal**: Optimize typography, code blocks, and admonitions for extended reading

**Independent Test**: Read a full chapter and verify text legibility, heading hierarchy, and callout visibility

### Typography (FR-012, FR-013, FR-014)

- [x] T036 [US2] Verify/set --ifm-font-family-base to system font stack in src/css/custom.css
- [x] T037 [P] [US2] Set body text color to dark gray (--ifm-font-color-base) in src/css/custom.css
- [x] T038 [P] [US2] Set heading color (--ifm-heading-color) to near-black in src/css/custom.css
- [x] T039 [P] [US2] Set line height (--ifm-line-height-base) to 1.65 in src/css/custom.css

### Code Blocks (FR-015)

- [x] T040 [US2] Style inline code with Teal-tinted background in src/css/custom.css
- [x] T041 [P] [US2] Style pre code blocks with light gray background in src/css/custom.css
- [x] T042 [P] [US2] Add dark mode code block styles in src/css/custom.css

### Admonitions (FR-021, FR-022, FR-023)

- [x] T043 [US2] Override .alert--info to use Teal border and background in src/css/custom.css
- [x] T044 [P] [US2] Override .alert--success and .admonition-tip to use Teal in src/css/custom.css
- [x] T045 [P] [US2] Verify .alert--warning keeps orange styling in src/css/custom.css
- [x] T046 [P] [US2] Verify .alert--danger keeps red styling in src/css/custom.css

### Content Background (FR-003)

- [x] T047 [US2] Verify main content area uses white background in src/css/custom.css
- [x] T048 [US2] Set --ifm-background-surface-color to off-white in src/css/custom.css

### Validation

- [x] T049 [US2] Test reading Module 1 Chapter 1 for typography clarity
- [x] T050 [US2] Verify persona callouts (info boxes) stand out with Teal
- [x] T051 [US2] Verify code blocks in chapters are clearly distinguished

**Checkpoint**: User Story 2 complete - optimal reading experience

---

## Phase 5: User Story 3 - Interactive Element Clarity (Priority: P3)

**Goal**: Ensure all interactive elements have clear Teal-based hover/focus feedback

**Independent Test**: Hover and click all interactive elements, verify Teal visual feedback

### Links (FR-016, FR-017)

- [x] T052 [US3] Verify links use Teal (--ifm-color-primary) by default in src/css/custom.css
- [x] T053 [P] [US3] Add link hover transition (150ms ease-in-out) in src/css/custom.css
- [x] T054 [P] [US3] Add link :hover lighter Teal color in src/css/custom.css

### Buttons (FR-018, FR-019)

- [x] T055 [US3] Style .button--primary with Teal background, white text in src/css/custom.css
- [x] T056 [P] [US3] Add .button--primary:hover darker Teal background in src/css/custom.css
- [x] T057 [P] [US3] Style .button--secondary with Teal border, transparent background in src/css/custom.css
- [x] T058 [P] [US3] Add .button--secondary:hover Teal background tint in src/css/custom.css

### Focus States (FR-020)

- [x] T059 [US3] Add global *:focus-visible Teal outline (2px solid) in src/css/custom.css
- [x] T060 [US3] Verify focus states visible on keyboard navigation

### Table of Contents

- [x] T061 [US3] Style .table-of-contents__link:hover with Teal in src/css/custom.css
- [x] T062 [P] [US3] Style .table-of-contents__link--active with Teal in src/css/custom.css

### Pagination

- [x] T063 [US3] Style .pagination-nav__link border on hover in src/css/custom.css
- [x] T064 [P] [US3] Style .pagination-nav__sublabel color in src/css/custom.css

### Validation

- [x] T065 [US3] Test all links in content have Teal color and hover effect
- [x] T066 [US3] Test keyboard navigation shows visible focus states
- [x] T067 [US3] Test pagination at bottom of chapters styled correctly

**Checkpoint**: User Story 3 complete - all interactive elements provide clear feedback

---

## Phase 6: User Story 4 - Dark Mode Consistency (Priority: P4)

**Goal**: Ensure dark mode maintains Navy/Teal scheme with proper contrast

**Independent Test**: Toggle dark mode and verify all elements maintain theme and readability

### Dark Mode Navbar/Sidebar/Footer

- [x] T068 [US4] Verify [data-theme='dark'] navbar uses darker Navy in src/css/custom.css
- [x] T069 [P] [US4] Verify [data-theme='dark'] sidebar uses darker Navy in src/css/custom.css
- [x] T070 [P] [US4] Verify [data-theme='dark'] footer uses darker Navy in src/css/custom.css

### Dark Mode Content

- [x] T071 [US4] Verify dark mode background is dark Navy (#0f172a) in src/css/custom.css
- [x] T072 [P] [US4] Verify dark mode text is light gray/white (#e2e8f0) in src/css/custom.css
- [x] T073 [P] [US4] Verify dark mode links use brighter Teal (#14b8a6) in src/css/custom.css

### Dark Mode Components

- [x] T074 [US4] Verify dark mode admonitions have appropriate contrast in src/css/custom.css
- [x] T075 [P] [US4] Verify dark mode code blocks have dark background in src/css/custom.css
- [x] T076 [P] [US4] Verify dark mode buttons maintain visibility in src/css/custom.css

### Dark Mode Toggle

- [x] T077 [US4] Test dark mode toggle in navbar works without page reload
- [x] T078 [US4] Verify dark mode preference persists across page navigation

### Validation

- [x] T079 [US4] Test dark mode on homepage - all elements visible
- [x] T080 [US4] Test dark mode on chapter page - text readable
- [x] T081 [US4] Toggle light/dark repeatedly - no flashing or broken styles

**Checkpoint**: User Story 4 complete - dark mode fully functional

---

## Phase 7: Polish & Cross-Cutting Validation

**Purpose**: Final validation, accessibility audit, cross-browser testing

### Accessibility Audit (SC-001, FR-005)

- [ ] T082 Run Lighthouse accessibility audit on homepage (target score > 90)
- [ ] T083 [P] Run Lighthouse accessibility audit on chapter page
- [ ] T084 [P] Verify WCAG AA contrast ratios using browser dev tools
- [ ] T085 Fix any contrast issues identified in audit

### Cross-Browser Testing (SC-002)

- [ ] T086 Test theme in Chrome (latest) - verify all user stories
- [ ] T087 [P] Test theme in Firefox (latest) - verify all user stories
- [ ] T088 [P] Test theme in Safari (latest) - verify all user stories
- [ ] T089 [P] Test theme in Edge (latest) - verify all user stories

### Responsive Testing (SC-003)

- [ ] T090 Test at 320px viewport width - verify mobile layout
- [ ] T091 [P] Test at 768px viewport width - verify tablet layout
- [ ] T092 [P] Test at 1920px viewport width - verify desktop layout

### Performance (SC-005)

- [ ] T093 Measure page load time before and after theme
- [ ] T094 Verify CSS file size is reasonable (< 10KB)

### Content Consistency (SC-007)

- [ ] T095 Verify Module 1 chapters display correctly with theme
- [ ] T096 [P] Verify Module 2 chapters display correctly with theme
- [ ] T097 [P] Verify Module 3 chapters display correctly with theme
- [ ] T098 [P] Verify Module 4 chapters display correctly with theme
- [ ] T099 Verify intro page displays correctly with theme

### Final Build Verification

- [x] T100 Run npm run build - verify no errors
- [x] T101 Run npm run serve - test production build locally

**Checkpoint**: Theme complete and validated - ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 - BLOCKS all user stories
- **US1 Visual Brand (Phase 3)**: Depends on Phase 2 completion
- **US2 Readable Content (Phase 4)**: Depends on Phase 2 completion
- **US3 Interactive Elements (Phase 5)**: Depends on Phase 2 completion
- **US4 Dark Mode (Phase 6)**: Depends on Phases 2-5 (validates dark variants)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 - Foundation
- **US2 (P2)**: Can start after Phase 2 - No dependency on US1
- **US3 (P3)**: Can start after Phase 2 - No dependency on US1/US2
- **US4 (P4)**: Depends on US1-US3 dark mode styles being in place

**Key Insight**: US1, US2, US3 can be implemented in parallel once Phase 2 completes. US4 validates dark mode variants added in US1-US3.

### Within Each User Story

- Light mode styles first
- Dark mode styles second
- Validation tasks last

---

## Parallel Execution Examples

### Phase 2: Foundational (can run 4 parallel streams)

```
Stream 1: T004 (Teal scale)
Stream 2: T005, T006, T007 (Navy, grays, typography)
Stream 3: T008 (dark Teal)
Stream 4: T009, T010, T011 (dark Navy, text, code)
```

### User Story 1: Navbar/Sidebar/Footer (after T014)

```
Navbar: T015, T016, T017, T018 in parallel
Sidebar: T021, T022, T023, T024 in parallel
Footer: T027, T028, T029 in parallel
```

### Phase 7: Cross-Browser Testing

```
T086 (Chrome), T087 (Firefox), T088 (Safari), T089 (Edge) in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T013)
3. Complete Phase 3: User Story 1 (T014-T035)
4. **STOP and VALIDATE**: Professional brand identity visible
5. Can deploy with just brand colors if needed

### Incremental Delivery

1. Setup + Foundational → Color system ready
2. Add US1 (Visual Brand) → Navy navbar/sidebar/footer visible
3. Add US2 (Readable Content) → Typography and callouts optimized
4. Add US3 (Interactive Elements) → All hover/focus states working
5. Add US4 (Dark Mode) → Full light/dark theme support
6. Polish → Accessibility and cross-browser verified

### Single Developer Timeline

Sequential execution following priority order:
- Phase 1: ~15 minutes
- Phase 2: ~30 minutes
- Phase 3 (US1): ~45 minutes
- Phase 4 (US2): ~30 minutes
- Phase 5 (US3): ~30 minutes
- Phase 6 (US4): ~20 minutes
- Phase 7: ~30 minutes

**Estimated Total**: 3-4 hours

---

## Summary

| Phase | Tasks | Parallel Tasks | Purpose |
|-------|-------|----------------|---------|
| Setup | 3 | 0 | Prepare CSS file |
| Foundational | 10 | 7 | Color variables |
| US1 (P1) | 22 | 14 | Brand identity |
| US2 (P2) | 16 | 9 | Readability |
| US3 (P3) | 16 | 10 | Interactivity |
| US4 (P4) | 14 | 9 | Dark mode |
| Polish | 20 | 12 | Validation |
| **Total** | **101** | **61** | |

**MVP Scope**: Phases 1-3 (35 tasks) delivers professional brand identity
**Full Scope**: All phases (101 tasks) delivers complete themed experience
