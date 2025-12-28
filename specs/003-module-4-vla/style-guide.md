# Style Guide: Module 4 - Vision-Language-Action (VLA) Systems

**Feature**: Module 4 - VLA Systems
**Date**: 2025-12-27
**Status**: ✅ Completed - Phase 2 (Foundational Design)

## Purpose

This document defines writing conventions for Module 4 to ensure consistency with Modules 1-3 and adherence to the project constitution.

---

## Writing Conventions

**Status**: ✅ Documented
**Task**: T022 - Document writing conventions

### Tone

**Conversational yet Authoritative**:
- Write as if explaining to a colleague, not lecturing from a textbook
- Use "you" to address the reader directly ("By the end of this chapter, you will...")
- Avoid overly formal academic language ("one must understand" → "you need to understand")
- Balance accessibility with technical precision

**Examples from Module 3**:
- Good: "Think of CPUs and GPUs like two different types of workers..."
- Good: "This is why robotics needs GPU-accelerated AI..."
- Avoid: "It is incumbent upon the reader to comprehend..."

**Accessible yet Precise**:
- Define technical terms on first use, then use consistently
- Use precise terminology where appropriate (don't oversimplify to incorrectness)
- Provide context before diving into technical details

### Sentence Structure

**Active Voice Preferred**:
- Use: "The LLM decomposes the task into subtasks"
- Avoid: "The task is decomposed into subtasks by the LLM"
- Exception: Passive voice acceptable when actor is unknown or less important

**Sentence Length**:
- Target: 15-25 words average per sentence
- Mix short (10-15 words) and medium (20-30 words) sentences for rhythm
- Avoid sentences longer than 35 words (break into two sentences)
- One idea per sentence

**Paragraph Length**:
- Target: 3-6 sentences per paragraph (80-150 words)
- Single-sentence paragraphs acceptable for emphasis or transitions
- Maximum 200 words per paragraph (break for readability)

### Technical Terms

**Define on First Use in Each Chapter**:
- Chapter 1 must define: VLA, LLM, semantic grounding, action primitive, end-to-end learning
- Chapter 2 must define: Planning hierarchy, affordance, task decomposition, motion planning
- Chapter 3 must define: Autonomy level, HRI, perception subsystem, dual-system architecture

**Consistent Terminology Across Chapters**:
- Use "Vision-Language-Action (VLA)" not "vision-language-action model" or "VLA system"
- Use "Large Language Model (LLM)" not "language model" or "large language model"
- Use "action primitive" not "primitive action" or "action command"
- Use "ROS 2" not "ROS2" or "ROS 2.0"
- Use "Isaac ROS" not "IsaacROS" or "Isaac-ROS"

**VLA-Specific Terms to Define**:
| Term | Definition (First Use) | Subsequent Usage |
|------|----------------------|------------------|
| VLA | Vision-Language-Action (VLA) system | VLA |
| LLM | Large Language Model (LLM) | LLM |
| Semantic Grounding | Connecting abstract language concepts to concrete perception and action | Semantic grounding or grounding |
| Action Primitive | Parameterized robot command at intermediate abstraction level | Action primitive |
| Affordance | What actions are physically possible given object properties | Affordance |
| Planning Hierarchy | Four-level structure from language to motor control | Planning hierarchy or hierarchy |
| Dual-System | Architecture separating slow reasoning (System 2) from fast control (System 1) | Dual-system |

### Examples and Analogies

**Real-World Applications (Not Toy Scenarios)**:
- Use: "Household robots preparing meals, folding laundry"
- Use: "Industrial humanoids for flexible manufacturing"
- Use: "Tesla Optimus, Boston Dynamics Atlas"
- Avoid: "Simple pick-and-place task" (too generic)
- Avoid: "Ball-in-cup game" (toy scenario)

**Technology-Agnostic Analogies**:
- Good: "LLM as translator between human and robot language"
- Good: "ROS 2 like message queues in distributed systems"
- Good: "Emergency stops like power tool safety guards"
- Avoid: Brand-specific analogies ("like configuring your iPhone")

**Relatable to Diverse Backgrounds**:
- Beginner: Everyday experiences (following GPS, using translator app)
- Software Engineer: Programming concepts (call stacks, ORMs, message queues)
- Robotics Student: Robotics fundamentals (kinematics, control loops, motion planning)
- AI Researcher: ML concepts (multimodal learning, cognitive architectures, grounding problem)

---

## Frontmatter Template

**Status**: ✅ Defined
**Task**: T022 - Document frontmatter template

### Required Fields

All Module 4 chapters must include these YAML frontmatter fields:

```yaml
---
sidebar_position: [1, 2, or 3]  # Chapter number
title: "Chapter [N]: [Title]"
description: "[One-sentence chapter description]"
keywords: [list, of, relevant, keywords]
module: "module-4-vision-language-action"
chapter_id: "chapter-[N]-[slug]"
learning_objectives:
  - "[Objective 1]"
  - "[Objective 2]"
  - "[Objective 3-5 total]"
prerequisites: [list of prerequisite modules/chapters]
difficulty: "[beginner/intermediate/advanced]"
estimated_reading_time: [minutes]
persona_relevance:
  beginner: [1-5 rating]
  software_engineer: [1-5 rating]
  robotics_student: [1-5 rating]
  ai_researcher: [1-5 rating]
vla_concepts: [list, of, vla, concepts, covered]
verified_against: "[source or date]"
last_verified: "2025-12-27"
---
```

### Example Frontmatter (Chapter 1)

```yaml
---
sidebar_position: 1
title: "Chapter 1: Introduction to Vision-Language-Action"
description: "Understand what VLA systems are, how they differ from traditional robotics, and why LLMs enable robots to follow natural language instructions"
keywords: ["vla", "vision-language-action", "llm", "robotics", "semantic-grounding", "rt-2", "openvla", "humanoid"]
module: "module-4-vision-language-action"
chapter_id: "chapter-1-introduction-to-vla"
learning_objectives:
  - "Explain what Vision-Language-Action (VLA) systems are and identify their three core components"
  - "Describe how VLA systems differ from traditional perception-only robotic architectures"
  - "Understand the role of Large Language Models in enabling robots to follow natural language instructions"
  - "Identify real-world applications of VLA systems in household, industrial, and humanoid robotics"
  - "Recognize how VLA represents a paradigm shift from pre-programmed robots to reasoning robots"
prerequisites: ["Module 1: ROS 2 fundamentals", "Module 2: Simulation", "Module 3: NVIDIA Isaac"]
difficulty: "beginner"
estimated_reading_time: 25
persona_relevance:
  beginner: 5
  software_engineer: 4
  robotics_student: 4
  ai_researcher: 4
vla_concepts: ["vla-system", "llm-robotics", "semantic-grounding", "end-to-end-learning", "vision-language-action-integration"]
verified_against: "RT-2 paper (Google DeepMind), OpenVLA paper, 2025 VLA research"
last_verified: "2025-12-27"
---
```

---

## Docusaurus Conventions

**Status**: ✅ Documented
**Task**: T022 - Document Docusaurus conventions

### Heading Hierarchy

**H1: Chapter Title (One Per File)**:
```markdown
# Chapter 1: Introduction to Vision-Language-Action
```
- One H1 per file (chapter title)
- Matches frontmatter title field
- First content after frontmatter (after learning objectives list)

**H2: Major Sections**:
```markdown
## What is a Vision-Language-Action System?
```
- Main content sections (3-5 per chapter)
- Should appear in table of contents
- Use sentence case for titles

**H3: Subsections**:
```markdown
### The Three Core Components
```
- Subdivisions within H2 sections
- Maximum depth: H3 (avoid H4 if possible)
- Use descriptive titles that indicate content

**H4: Detailed Points (Avoid Deeper Nesting)**:
```markdown
#### Vision Component
```
- Only use when absolutely necessary for organization
- NEVER use H5 or deeper (flatten structure instead)

### Callout Syntax

**Docusaurus Admonition Syntax**:

**For Beginners** (blue "note" style):
```markdown
:::note For Beginners
[Beginner-friendly content with everyday analogies]
:::
```

**For Software Engineers** (green "tip" style):
```markdown
:::tip For Software Engineers
[Programming concepts, software architecture analogies]
:::
```

**For Robotics Students** (cyan "info" style):
```markdown
:::info For Robotics Students
[Robotics fundamentals, control systems, kinematics connections]
:::
```

**For AI Researchers** (yellow "warning" style - stands out):
```markdown
:::warning For AI Researchers
[ML concepts, theoretical AI, research directions]
:::
```

**Callout Content Guidelines**:
- Length: 50-120 words (3-7 sentences)
- Start with connection to persona's background
- Include specific comparison or analogy
- Tie back to main concept
- Avoid generic statements ("This is important because...")

### Code Blocks

**Conceptual Pseudo-Code Only** (No Implementation Code):

Module 4 is conceptual educational content. Code blocks should show:
- **Conceptual representations**: `grasp(object_id=cup, force=20N)`
- **Pseudo-code for illustration**: Function-like notation showing hierarchy
- **Architecture diagrams as text**: ASCII-art workflows

**Do NOT Include**:
- Actual Python/C++ implementation code
- API documentation or function signatures
- Complete runnable programs
- Framework-specific code (except ROS 2 concept illustration)

**Example - Acceptable**:
```markdown
```
Voice Command → Speech Recognition →
  VLA Planner (LLM) → ROS 2 Action Goals →
    Isaac Perception + Nav2 + MoveIt →
      Hardware Controllers → Physical Robot
```
```

### Links and Cross-References

**Internal Cross-References (to Other Modules)**:
```markdown
In Module 1 (ROS 2 Communication), we learned about action servers that handle long-running goals with feedback...
```
- Natural language references, not explicit hyperlinks
- Mention module number and chapter/concept name
- Explain why cross-reference is relevant

**External Links** (Research Papers, Documentation):
- Inline in text: "Systems like RT-2 (Google DeepMind)"
- No explicit URLs in body text (distracting)
- URLs acceptable in footnotes or references section if needed

**File Path References** (When Explaining Project Structure):
```markdown
The chapter will be located at:
`physical-ai-textbook/docs/docs/module-4-vision-language-action/chapter-1-introduction-to-vla.md`
```
- Use backticks for file paths
- Include from project root when helpful

---

## Content Quality Standards

### What/Why/How Structure

**Every Major Section Should Answer**:

1. **What**: Define the concept clearly
   - "A VLA system is a multimodal foundation model that integrates vision, language, and action..."

2. **Why**: Explain importance or motivation
   - "VLA enables natural language robot control because users can speak naturally rather than programming explicit commands..."

3. **How**: Describe mechanism or process
   - "The LLM decomposes 'prepare breakfast' into subtasks, each subtask maps to action primitives, which execute as motor commands..."

**Order**: Usually What → Why → How, but flexible based on pedagogical needs

### Semantic Chunking

**200-500 Words Per Semantic Chunk for RAG Optimization**:

- Each H3 subsection should be 200-500 words (complete idea)
- This length optimizes for RAG retrieval (vector similarity search)
- Too short (< 150 words): Lacks context for meaningful retrieval
- Too long (> 600 words): Multiple concepts mixed, harder to retrieve specific info

**Chunk Boundaries**:
- Natural topic breaks (H2/H3 headings)
- Include necessary context within each chunk
- Self-contained enough to be understood independently

### Persona Callout Guidelines

**When to Use**:
- After introducing new complex concept (H2 section)
- When analogy strengthens understanding
- To connect module content to persona's background
- NOT every section needs callouts (4-6 per chapter total)

**How to Distribute**:
- Chapter 1: Emphasize Beginner (3) + AI Researcher (2) + Robotics Student (1)
- Chapter 2: Emphasize Software Engineer (3) + AI Researcher (2) + Robotics Student (1-2)
- Chapter 3: Balance all four personas (1-2 each)

**What Makes a Good Callout**:
- ✓ Specific comparison to persona's domain ("like call stacks in programming")
- ✓ Actionable insight persona can use
- ✓ Connects new concept to familiar concept
- ✗ Generic commentary ("This is an important topic")
- ✗ Information already in main text (redundant)
- ✗ Oversimplification that loses accuracy

---

## Additional Guidelines

### Readability Targets

- **Flesch-Kincaid Grade Level**: 10-12 (accessible to undergraduates)
- **Sentence variety**: Mix simple, compound, and complex sentences
- **Jargon**: Define on first use, use consistently thereafter
- **Acronyms**: Spell out on first use with acronym in parentheses: "Large Language Model (LLM)"

### Comparison Tables

- **Minimum 1 per chapter** (Success Criterion SC-011)
- Use markdown table syntax
- 5-8 rows typical (enough for meaningful comparison)
- Include concrete examples in each cell (not just abstract descriptions)

### Learning Objectives

- **Start each chapter** with 3-5 numbered learning objectives
- Use action verbs: Explain, Describe, Understand, Identify, Compare, Design
- Specific and measurable (student should know if they achieved it)
- Match chapter summary at end

### Chapter Summaries

- **End each chapter** with 200-300 word summary
- Bullet points or short paragraphs
- Recap key concepts covered
- Reinforce learning objectives
- Chapters 1-2: Include "What's Next" teaser (50-100 words) for next chapter

---

**Note**: Phase 2 (Foundational Research & Design) completed. Style guide finalized for Module 4 content creation.
