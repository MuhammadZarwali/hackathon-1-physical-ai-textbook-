# Module 2 Style Guide
**Extracted from Module 1 (ROS 2) for consistency**

**Purpose**: Ensure Module 2 chapters match Module 1's proven style, structure, and formatting

**Created**: 2025-12-26

**Source**: Analysis of all 3 Module 1 chapters

---

## Frontmatter Structure

Every chapter must include YAML frontmatter with these exact fields (in this order):

```yaml
---
sidebar_position: [1, 2, or 3]
title: "Chapter [N]: [Chapter Title]"
description: "[One-sentence chapter summary]"
keywords: ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5", "keyword6"]
module: "module-2-simulation"
chapter_id: "chapter-[n]-[slug]"
learning_objectives:
  - "[Objective 1]"
  - "[Objective 2]"
  - "[Objective 3]"
  - "[Objective 4]"
prerequisites: ["[prereq1]", "[prereq2]"]
difficulty: "[beginner|intermediate|advanced]"
estimated_reading_time: [number in minutes]
persona_relevance:
  beginner: [1-5 relevance score]
  software_engineer: [1-5 relevance score]
  robotics_student: [1-5 relevance score]
  ai_researcher: [1-5 relevance score]
[domain]_concepts: ["concept1", "concept2", "concept3"]
verified_against: "[URL to authoritative source]"
last_verified: "YYYY-MM-DD"
---
```

**Key Notes**:
- `module` should be `"module-2-simulation"` for all Module 2 chapters
- `[domain]_concepts` should be `simulation_concepts` (e.g., `["digital-twin", "physics-engine", "gazebo"]`)
- `verified_against` should link to Gazebo docs or authoritative simulation resources
- `keywords` should include simulation-specific terms

---

## Document Structure

### 1. Chapter Title (H1)
```markdown
# Chapter [N]: [Title]
```

### 2. Learning Objectives Section
```markdown
## Learning Objectives

By the end of this chapter, you will:
- [Objective 1 - start with action verb: Explain, Describe, Identify, Compare, etc.]
- [Objective 2]
- [Objective 3]
- [Objective 4]
```

**Pattern**: Always 3-4 objectives, written as learner-focused outcomes (you will...), starting with Bloom's taxonomy verbs

### 3. Main Content Sections (H2)
- Use descriptive section headings that indicate topic
- Typical pattern: Introduction → Concepts → Examples → Advanced Topics → Practical Applications

### 4. Subsections (H3)
- Break complex sections into digestible subsections
- Keep hierarchy shallow (rarely use H4)

### 5. Summary Section
```markdown
## Summary

This chapter [summarized what was covered].

**Key takeaways**:
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]
- [Bullet point N]

**Next**: [One sentence teasing next chapter]
```

**Pattern**: Summary always includes "This chapter..." opening, bulleted key takeaways, and explicit "Next" pointer

### 6. Further Reading Section
```markdown
## Further Reading

- [Link 1 Title](URL)
- [Link 2 Title](URL)
- [Link 3 Title](URL)
```

**Pattern**: 3-5 curated links to official docs or authoritative sources, always in markdown link format with descriptive text

---

## Heading Hierarchy Standards

**Observed Pattern**:
- **H1**: Chapter title only (once per document)
- **H2**: Major section headings (5-8 per chapter)
- **H3**: Subsection headings (2-4 per H2 section)
- **H4**: Rare, used only for nested lists or very specific sub-topics

**Naming Conventions**:
- Use Title Case for all headings
- Keep headings concise (2-8 words typical)
- Use descriptive, concept-focused names (not generic like "Overview" or "Details")

---

## Persona Callout Format

Module 1 uses **Docusaurus admonitions** with specific persona types. Follow this exact format:

### Beginner Persona
```markdown
:::note For Beginners
[Simple analogy comparing technical concept to everyday experience. Use concrete examples. Keep to 2-3 sentences.]
:::
```

**Characteristics**:
- Uses simple, everyday analogies (phone apps, restaurants, driving)
- Avoids technical jargon
- Explains "what" and "why" without deep "how"

### Software Engineer Persona
```markdown
:::tip For Software Engineers
[Compare robotics concept to familiar software patterns: microservices, APIs, databases, web frameworks. Include specific technology names. 2-4 sentences.]
:::
```

**Characteristics**:
- References distributed systems, web APIs, message queues
- Uses software engineering terminology (REST, pub/sub, async)
- Draws parallels to familiar tools (Docker, Kubernetes, RabbitMQ)

### Robotics Student Persona
```markdown
:::info For Robotics Students
[Connect to robotics theory: control systems, kinematics, dynamics. Mention equations or formal concepts. 2-4 sentences.]
:::
```

**Characteristics**:
- References control theory, kinematics, state estimation
- Mentions degrees of freedom, configuration space, feedback loops
- Connects practical implementation to theoretical foundations

### AI Researcher Persona
```markdown
:::tip For AI Researchers
[Connect to ML/AI concepts: training systems, model architectures, distributed training. Use AI terminology. 2-4 sentences.]
:::
```

**Characteristics**:
- References ML frameworks (PyTorch, TensorFlow), training pipelines
- Draws parallels to model serving, data pipelines, GPU clusters
- Connects to research areas (reinforcement learning, vision transformers, VLAs)

**Placement Rules**:
- 4-6 persona callouts per chapter (at least 1 of each type)
- Place immediately after introducing a new concept that could benefit from different perspectives
- Never stack multiple callouts consecutively—separate with at least one paragraph
- Distribute evenly throughout chapter (not clustered at beginning/end)

---

## Writing Style Guidelines

### Tone and Voice
- **Conversational yet professional**: Use "you" and "your" to address reader
- **Active voice**: "ROS 2 provides" not "is provided by ROS 2"
- **Accessible**: Explain technical terms on first use
- **Engaging**: Use rhetorical questions, examples, and analogies

### Paragraph Structure
- **Opening paragraph per section**: State what the section covers and why it matters
- **Body paragraphs**: 3-5 sentences typical, focus on one concept per paragraph
- **Transition smoothly**: Connect ideas between paragraphs

### Sentence Structure
- **Vary length**: Mix short, punchy sentences with longer explanatory ones
- **Keep complex sentences clear**: Use commas, semicolons, dashes appropriately
- **Start with context**: "When X happens, Y occurs" rather than "Y occurs when X happens"

### Technical Terminology
- **Define on first use**: "DDS (Data Distribution Service)" then "DDS" thereafter
- **Explain acronyms**: Never assume familiarity
- **Bold key terms**: Use **bold** for first mention of critical concepts
- **Use consistent terms**: If you call it "node" in one place, don't switch to "process" elsewhere

### Examples and Analogies
- **Real-world robotics examples**: Reference Boston Dynamics, Tesla, PAL Robotics, Agility Robotics
- **Everyday analogies for beginners**: Phone networks, restaurants, nervous system, driving
- **Software analogies for engineers**: Microservices, REST APIs, message queues, Docker
- **Concrete over abstract**: "A humanoid robot walking" vs "locomotion systems"

---

## Code Block Standards

### Format
````markdown
```python
# Comment explaining what this code does
code_here
```
````

or

````markdown
```cpp
// C++ example if needed
code_here
```
````

**Usage**:
- 2-3 code examples per chapter maximum (not more—keep conceptual)
- Each code block must have a comment explaining its purpose
- Keep code snippets SHORT (5-15 lines typical)
- Show structure/pattern, not complete implementations
- Always introduce code block with text: "Example - [what it demonstrates]:"

### Code Block Placement
- Use to illustrate communication patterns, not full implementations
- Place after explaining the concept in prose
- Follow with 1-2 sentences interpreting what the code shows

---

## Definition Patterns

### Bold Definitions
```markdown
**Definition**: [Term] is [clear, concise definition in one sentence].
```

**Usage**: First introduction of critical concepts

### Inline Explanations
```markdown
Term (explanation in parentheses that clarifies or provides synonyms)
```

**Example**: "Each node runs within an executor, which manages the node's event loop and callbacks."

### "What, Why, How" Structure
Many sections follow this pattern:
1. **What it is**: Define the concept
2. **Why it matters**: Explain significance/motivation
3. **How it works**: Describe mechanism/implementation
4. **When to use**: Provide guidance on application

---

## List Formatting Standards

### Bulleted Lists
- Use bullet points for:
  - Features or characteristics (no particular order)
  - Examples or use cases
  - Key takeaways

### Numbered Lists
- Use numbers for:
  - Sequential steps (workflows, processes)
  - Ordered priorities
  - Logical progressions

### Definition Lists (Markdown)
```markdown
**Term**: Description or definition following the bold term.
```

---

## Table Standards

### Comparison Tables
Example from Module 1:

```markdown
| **Column 1** | **Column 2** | **Column 3** |
|--------------|--------------|--------------|
| Value A      | Value B      | Value C      |
| Value D      | Value E      | Value F      |
```

**Characteristics**:
- Bold headers using `**Header**`
- Align columns visually in source (not required for rendering, but improves readability)
- Keep cell content concise (1-2 lines per cell)
- Use tables for 3-5 row comparisons (not longer)

**Typical Use Cases**:
- Comparing different approaches/technologies
- Summarizing when to use different patterns
- Feature matrices

---

## Word Count and Pacing

### Chapter Length Targets
- **Chapter 1**: 3,500-4,000 words (introductory, conceptual)
- **Chapter 2**: 4,000-4,500 words (intermediate, architectural)
- **Chapter 3**: 4,000-4,500 words (advanced, integration)

### Section Length
- **Major sections (H2)**: 500-800 words typical
- **Subsections (H3)**: 200-400 words typical
- **Introductory paragraphs**: 50-100 words
- **Persona callouts**: 40-80 words each

### Pacing
- **Introduction sections**: Move quickly to concepts (don't over-explain motivation)
- **Core concepts**: Take time to explain thoroughly with examples
- **Advanced topics**: Build progressively, reference earlier concepts
- **Summary**: Keep concise, focus on actionable takeaways

---

## Cross-Referencing Standards

### Internal References
```markdown
As discussed in Chapter 1, [concept]...
We introduced [concept] earlier when discussing [topic]...
Recall that [concept] enables [functionality]...
```

**Pattern**: Reference previous chapters/sections when building on concepts

### External Links
```markdown
[Descriptive Link Text](https://full-url)
```

**Examples**:
- `[Official ROS 2 Documentation](https://docs.ros.org/en/humble/)`
- `[DDS: The Foundation of ROS 2](https://design.ros2.org/articles/ros_on_dds.html)`

**Placement**: Always in "Further Reading" section at end, occasionally inline for critical references

---

## Markdown Conventions

### Emphasis
- **Bold** (`**bold**`): First mention of key terms, emphasis on critical points
- *Italic* (`*italic*`): Rare, used for book titles or special emphasis
- `Code formatting` (`` `code` ``): Inline code, commands, file names, variable names

### Links
- Always use descriptive text: `[link text](url)`, never bare URLs
- Open external links in same tab (standard Markdown behavior)

### Blockquotes
- Not used in Module 1 chapters
- Admonitions (persona callouts) serve this purpose instead

---

## Quality Standards Checklist

Before finalizing any Module 2 chapter, verify:

- [ ] Frontmatter includes all required fields in correct order
- [ ] Learning objectives are learner-focused and use action verbs
- [ ] 4-6 persona callouts distributed throughout, at least 1 of each type
- [ ] Summary section includes "This chapter..." opening and "Next" pointer
- [ ] Further Reading section has 3-5 curated, working links
- [ ] All technical terms defined on first use
- [ ] Real-world robotics examples included (companies/products named)
- [ ] Analogies appropriate for different personas
- [ ] Heading hierarchy is clear (H1 → H2 → H3, rarely H4)
- [ ] Code blocks are SHORT (5-15 lines), with explanatory comments
- [ ] Tables used for comparisons (not long lists)
- [ ] No installation instructions or tool-specific CLI commands
- [ ] Consistent terminology throughout (same terms for same concepts)
- [ ] Word count within target range
- [ ] Professional yet conversational tone maintained

---

## Module 2-Specific Adaptations

Since Module 2 focuses on **digital twins and simulation**, adapt these patterns:

### Terminology Changes
- Replace "ROS 2" references with "Gazebo," "digital twin," "simulation"
- Replace "middleware" with "physics engine," "simulator"
- Replace "nodes/topics" with "simulation components," "sensor models"

### Example Sources
- Reference: Boston Dynamics (Atlas), Tesla (Optimus), Sanctuary AI, Agility Robotics
- For simulation: NVIDIA Isaac Sim, Gazebo Sim, Unity Robotics, MuJoCo
- Physics engines: ODE, Bullet, DART, PhysX

### Concept Domains
- `simulation_concepts` instead of `ros2_concepts`
- Verified against Gazebo documentation, simulation papers
- Learning objectives focus on understanding simulation vs implementation

### Persona Callout Adaptations
- **Beginner**: Compare simulation to video games, virtual training
- **Software Engineer**: Compare to testing environments, CI/CD, Docker containers
- **Robotics Student**: Reference sim-to-real transfer, system identification
- **AI Researcher**: Reference sim-based training (RL in simulation, domain randomization)

---

## Final Notes

This style guide is **descriptive** (based on Module 1) and **prescriptive** (must be followed for Module 2).

**Consistency is critical** for:
- Professional appearance
- Reader experience across modules
- RAG chatbot performance (consistent terminology improves retrieval)
- Maintainability and future updates

When in doubt, **refer to Module 1 chapters** as examples of proper style, structure, and formatting.
