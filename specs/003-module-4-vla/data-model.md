# Data Model: Module 4 - Vision-Language-Action (VLA) Systems

**Feature**: Module 4 - VLA Systems
**Date**: 2025-12-27
**Status**: Draft - To be completed in Phase 2 (Foundational Design)

## Purpose

This document defines the key VLA entities and concepts used consistently across all three chapters of Module 4.

## Key Entities

### 1. Vision-Language-Action System

**Status**: ✅ Defined
**Task**: T014 - Define VLA entities

**Definition**: A Vision-Language-Action (VLA) system is a multimodal foundation model that integrates three core capabilities to enable robots to follow natural language instructions in open-world environments.

**3 Core Components**:

1. **Vision Component**
   - **Purpose**: Environmental perception and scene understanding
   - **Inputs**: RGB cameras, depth sensors, LiDAR, proprioception
   - **Outputs**: Object detection, semantic segmentation, 3D mapping, scene graphs
   - **Technologies**: Convolutional neural networks, vision transformers (DINOv2, SigLIP), Isaac ROS perception

2. **Language Component**
   - **Purpose**: Natural language understanding, reasoning, and task interpretation
   - **Inputs**: Voice commands, text instructions, user preferences
   - **Outputs**: Task plans, subtask decompositions, affordance queries
   - **Technologies**: Large language models (GPT-4, PaLM, Llama 2), speech recognition (Whisper)

3. **Action Component**
   - **Purpose**: Physical behavior execution through planning and motor control
   - **Inputs**: High-level task plans, environmental constraints, sensor feedback
   - **Outputs**: Low-level robot actions (joint commands, gripper control, navigation goals)
   - **Technologies**: Motion planning (RRT, optimization-based), ROS 2 action servers, control systems

**How VLA Differs from Traditional Robotics**:
- **Traditional**: Separate perception pipelines, manual task programming, explicit goal specification
- **VLA**: End-to-end learning from perception + language to actions, natural language interface, generalization via pre-training

**Real-World Examples**:
- RT-2 (Google DeepMind): Manipulating household objects following language instructions
- Helix (Figure AI): Humanoid upper-body control for domestic tasks
- OpenVLA: Open-source 7B-parameter model for manipulation research

**Use Cases**:
- Household robots: "Prepare breakfast", "Clean the living room", "Fold the laundry"
- Industrial automation: "Sort the red parts into bin A", "Inspect the welded joints"
- Humanoid assistants: "Bring me the TV remote", "Help me set the table"

### 2. Large Language Model (LLM) for Robotics

**Status**: ✅ Defined
**Task**: T014 - Define VLA entities

**Definition**: A Large Language Model in robotics context is a pre-trained AI model that provides high-level reasoning capabilities, enabling robots to decompose natural language commands into executable task plans.

**Capabilities in Robotic Context**:
- **Task Decomposition**: Breaking "prepare breakfast" into subtasks (retrieve ingredients, cook, plate)
- **Common-Sense Reasoning**: Understanding temporal ordering (must grasp before placing), feasibility (can't pour liquid into closed container)
- **World Knowledge**: Knowing typical object locations (dishes in cabinet, food in refrigerator)
- **Natural Language Interface**: Parsing user commands, asking clarification questions, reporting status
- **Zero-Shot Generalization**: Handling novel tasks without explicit programming

**Role in VLA Systems**:
- **High-Level Planner**: Serves as cognitive layer generating task sequences
- **Semantic Reasoner**: Bridges symbolic language and subsymbolic perception/control
- **Affordance Query Engine**: Determines what actions are possible given current state
- **Feedback Loop Participant**: Iteratively refines plans based on execution outcomes

**Architecture Patterns**:
- **Dual-System (2025 trend)**: LLM as System 2 (slow, deliberate reasoning) + visuomotor policy as System 1 (fast, reactive control)
- **End-to-End VLA**: Single unified model processing vision + language → actions (RT-2, OpenVLA)
- **LLM-as-Planner**: LLM generates plans, traditional robotics handles execution (SayCan, DELTA)

**Examples**:
- **GPT-4**: High-level task planning, commonsense reasoning (used in research systems)
- **RT-2**: Vision-language-action model treating actions as language tokens
- **OpenVLA**: 7B-parameter open-source model with Llama 2 base
- **PaLM-E**: 562B-parameter embodied multimodal LLM integrating sensor data
- **System 2 in Helix/Groot**: VLM for scene understanding and language comprehension

**Key Limitation**: LLMs lack physical intuition; must be grounded with perception and affordance models to ensure feasible plans.

### 3. Planning Hierarchy

**Status**: ✅ Defined
**Task**: T014 - Define VLA entities

**Definition**: The Planning Hierarchy is a multi-level structure that decomposes natural language goals into motor control commands, bridging high-level reasoning with low-level robot execution.

**4 Hierarchical Levels**:

1. **Task Level (Language-Level Goals)**
   - **Input**: Natural language command from user
   - **Reasoning**: LLM-based task understanding and decomposition
   - **Output**: Ordered sequence of high-level subtasks
   - **Example**: "Prepare breakfast" → [Locate kitchen, Retrieve ingredients, Cook food, Plate food, Clean up]
   - **Timeframe**: Seconds to minutes for LLM reasoning

2. **Subtask Level (Goal-Oriented Actions)**
   - **Input**: Single high-level subtask from task-level plan
   - **Reasoning**: Further decomposition into concrete robot goals
   - **Output**: Sequence of grounded actions with target objects/locations
   - **Example**: "Retrieve eggs" → [Navigate to fridge, Open fridge door, Locate egg carton, Grasp carton, Remove from fridge, Close door]
   - **Timeframe**: Seconds for subtask planning

3. **Action Primitive Level (Grounded Robot Commands)**
   - **Input**: Grounded action goal (e.g., "Grasp egg carton")
   - **Reasoning**: Motion planning, grasp planning, collision avoidance
   - **Output**: Parametrized robot commands (poses, trajectories, gripper widths)
   - **Example**: `grasp(object_id=egg_carton, pose=[x,y,z,roll,pitch,yaw], force=20N)` → motion plan from current pose to target
   - **Timeframe**: Milliseconds for motion planning

4. **Motor Control Level (Low-Level Commands)**
   - **Input**: Desired trajectory or pose from action primitive
   - **Reasoning**: Real-time feedback control (PID, impedance control)
   - **Output**: Joint velocities/torques sent to actuators at control frequency
   - **Example**: 7DOF arm joint trajectory, gripper closure command
   - **Timeframe**: Microseconds (control loops at 100-1000 Hz)

**Relationships Between Levels**:
- **Abstraction**: Each level operates at different time/spatial scales
- **Information Flow**: Top-down (goals) and bottom-up (feedback)
- **Integration Points**:
  - Task → Subtask: LLM reasoning
  - Subtask → Action Primitive: Semantic grounding (language to robot actions)
  - Action Primitive → Motor Control: Motion planning and control systems
  - Feedback: All levels receive state updates from lower levels

**Concrete Example Progression**:

| Level | Content |
|-------|---------|
| **Task** | "Set the dinner table" |
| **Subtask** | Navigate to cabinet, Retrieve plates (4x), Navigate to table, Place plates at positions |
| **Action Primitive** | For "Grasp plate": `detect_object(class="plate")` → `plan_grasp(plate_pose)` → `execute_grasp(force=low)` |
| **Motor Control** | Arm joint trajectory: `[q1(t), q2(t), ..., q7(t)]` executed at 100 Hz with torque limits |

**Why Hierarchy Matters for VLA**:
- **LLMs operate at Task/Subtask levels**: Reasoning about goals, not joint angles
- **Traditional robotics operates at Action Primitive/Motor Control levels**: Motion planning, control
- **VLA bridges the gap**: Semantic grounding connects language-level plans to robot-level execution

### 4. Semantic Grounding

**Status**: ✅ Defined
**Task**: T014 - Define VLA entities

**Definition**: Semantic Grounding is the process of connecting abstract language concepts to concrete physical perception and action, enabling robots to translate symbolic reasoning (language) into subsymbolic processing (vision, control).

**Two Primary Grounding Problems**:

**1. Language → Perception Grounding**
- **Challenge**: Mapping words like "cup", "door", "person" to visual object detection, scene understanding
- **Techniques**:
  - Vision-language models (CLIP, DINOv2) providing joint embedding spaces for images and text
  - Object detection models trained on labeled datasets (COCO, Open Images)
  - Object schemas connecting noun phrases to perceptual features (shape, color, texture)
  - Digital twins maintaining semantic labels + geometric information
- **Example**: User says "Pick up the red cup"
  - Perception: Vision system detects all cups in scene
  - Grounding: Filter to red-colored cups based on language constraint
  - Selection: Choose closest/most accessible red cup as target
- **Failure Case**: "Pick up the small object" (ambiguous without size reference)

**2. Language → Action Grounding**
- **Challenge**: Mapping verbs like "grasp", "push", "open" to manipulation primitives, navigation goals
- **Techniques**:
  - Affordance models filtering physically feasible actions given object properties
  - Plan hierarchies connecting verb phrases to action sequences ("open drawer" → grasp handle, pull)
  - Reinforcement learning grounding semantic actions in sensorimotor trajectories
  - Action primitives library mapping high-level verbs to parameterized robot functions
- **Example**: User says "Open the drawer"
  - Action Grounding: "Open" → manipulation sequence [Approach, Grasp handle, Pull outward]
  - Affordance Check: Is drawer openable? Is handle graspable? Is workspace clear?
  - Execution: Generate grasp pose for handle, plan pull trajectory
- **Failure Case**: "Open the window" (may be locked, too high, require different technique)

**Purpose of Semantic Grounding**:
- **Bridge Symbolic ↔ Subsymbolic**: Language (symbolic tokens) ↔ Perception/Control (continuous neural activations)
- **Enable Natural Interaction**: Users speak naturally without knowing robot's internal representations
- **Leverage World Knowledge**: LLMs provide semantic understanding trained on text; grounding connects to physical world
- **Handle Ambiguity**: Resolve underspecified commands using visual context and affordances

**Grounding Techniques in VLA Systems**:
- **Vision-Language Pre-training**: RT-2 trains on web images + captions, learns visual grounding at scale
- **Affordance Filtering (SayCan)**: LLM proposes actions → affordance model scores based on physical feasibility
- **Semantic Digital Twins (DELTA)**: Structured scene graphs provide grounding layer for LLM reasoning
- **Feedback-Driven Refinement**: Execution failures inform grounding corrections (e.g., cup not graspable → try different pose)

**Why Grounding is Core VLA Challenge**:
- LLMs excel at language reasoning but lack embodied experience
- Vision models detect objects but don't understand semantic relationships
- VLA success requires tight coupling between language understanding and physical capabilities

### 5. Autonomous Humanoid System

**Status**: ✅ Defined
**Task**: T014 - Define VLA entities

**Definition**: An Autonomous Humanoid System is an end-to-end integrated robot architecture that combines perception, planning (VLA), navigation, manipulation, and communication subsystems to perform complex tasks in human environments with minimal supervision.

**5 Core Subsystems**:

**1. Perception Subsystem**
- **Sensors**: RGB cameras (scene understanding), depth sensors (3D mapping), LiDAR (obstacle detection), proprioception (joint encoders, IMUs)
- **Processing**: Isaac ROS object detection, semantic segmentation, SLAM, human detection/tracking
- **Outputs**: Scene graphs, object poses, occupancy maps, human locations
- **ROS 2 Topics**: `/camera/image`, `/depth/image`, `/joint_states`, `/scan`

**2. Planning Subsystem (VLA Cognitive Layer)**
- **Inputs**: Voice commands (speech recognition), vision (scene understanding), task feedback
- **Processing**: LLM-based task decomposition, semantic grounding, affordance reasoning, replanning
- **Outputs**: ROS 2 action goals (navigation, manipulation), status reports
- **Components**: VLA Planner Node (rclpy), memory systems (task history, environment maps), world model

**3. Navigation Subsystem**
- **Inputs**: Navigation goals from planner, sensor data (cameras, LiDAR), current pose
- **Processing**: Global path planning (A*, RRT), local obstacle avoidance (DWA), localization (SLAM)
- **Outputs**: Mobile base velocity commands, balance control (for bipedal humanoids)
- **Technologies**: ROS 2 Nav2 stack, Isaac ROS Visual SLAM, MoveIt for whole-body motion

**4. Manipulation Subsystem**
- **Inputs**: Manipulation goals from planner (grasp, place, push), object poses from perception
- **Processing**: Grasp planning (grasp pose selection), motion planning (collision-free trajectories), force control
- **Outputs**: Arm joint trajectories, gripper commands, tactile feedback
- **Technologies**: MoveIt motion planning, Isaac Manipulator, grasp synthesis libraries

**5. Communication Subsystem**
- **User Interaction**: Voice input/output (Whisper, TTS), gesture recognition, mobile app control
- **Robot-to-Human**: Status reports ("I'm going to the kitchen"), capability limits ("I can't reach that"), intent signaling
- **System Integration**: ROS 2 DDS middleware connecting all subsystems, external cloud connectivity
- **HRI**: Transparency (communicating state), social awareness (respecting personal space)

**Integration Architecture**:
```
User Voice Command → Speech Recognition →
  VLA Planner Node (LLM) →
    ROS 2 Action Goals (Navigation + Manipulation) →
      Perception (Isaac ROS Vision) + Nav2 + MoveIt →
        Hardware Controllers (Motors, Grippers) →
          Physical Robot Execution
            ↓
      Feedback Loop: Sensor Data → Update World Model → Replan if needed
```

**Interaction Patterns**:

**Voice-to-Action Loop**:
1. User: "Bring me a glass of water"
2. Speech Recognition → LLM: Extract intent `fetch(object="water glass", destination="user")`
3. Task Planning: [Locate kitchen, Navigate, Identify glass, Grasp, Navigate to user, Hand over]
4. Execution: For each subtask, send ROS 2 action goals, monitor feedback
5. Status Communication: "I'm going to the kitchen" → "I found the glass" → "Here's your water"

**Failure Handling**:
- Perception fails (can't find glass): "I don't see any glasses, can you help me?"
- Navigation blocked: "There's an obstacle, I'm finding another route"
- Grasp fails: Retry with different pose, or report "I can't grasp this glass safely"

**Real-World Examples**:
- **Tesla Optimus**: Production-focused, neural network control, autonomous vehicle perception stack adaptation
- **Boston Dynamics Atlas**: Control-focused, dynamic motion expertise, Jetson Thor compute (2025)
- **Figure AI Helix**: VLA for humanoid, controls full upper body at high frequency

**Autonomy Level**: Most 2025 humanoids operate at L2-L3 autonomy (partial/conditional), with L4 (high) emerging for structured environments (factories, controlled homes).

### 6. Human-Robot Interaction (HRI) Principles

**Status**: ✅ Defined
**Task**: T014 - Define VLA entities

**Definition**: Human-Robot Interaction (HRI) Principles are guidelines ensuring safe, effective, and socially acceptable collaboration between humans and robots in shared environments.

**4 Core HRI Principles**:

**1. Transparency (Robot Communicates State)**
- **Principle**: Robot explicitly signals its intentions, state, and capabilities to humans
- **Implementations**:
  - Intent signaling: "I'm going to pick this up" (before grasping)
  - Progress updates: "I'm halfway to the kitchen" (during navigation)
  - Capability limits: "I can't reach that shelf" (when task infeasible)
  - Sensor displays: Show detected objects, planned paths (like self-driving car interfaces)
- **Why It Matters**: Humans can anticipate robot behavior, builds trust, enables collaboration
- **VLA Integration**: LLM generates natural language status reports, voice synthesis communicates to user

**2. Predictability (Consistent Behavior)**
- **Principle**: Robot exhibits consistent, understandable behavior patterns that humans can learn
- **Implementations**:
  - Smooth motions: Avoid sudden movements that startle humans
  - Consistent responses: Same command triggers same behavior pattern every time
  - Legible actions: Motions clearly indicate intent (e.g., approach object from visible angle so human sees grasp coming)
  - Predictable timing: Robot doesn't suddenly speed up or change plans mid-execution
- **Why It Matters**: Humans develop mental models of robot behavior, reduces anxiety, enables shared workspace
- **VLA Integration**: Planning system ensures consistent task decomposition; action primitives use smooth trajectories

**3. Safety (Collision Avoidance & Force Limiting)**
- **Principle**: Robot prioritizes human safety through multiple layers of protection
- **Implementations**:
  - **Sensor-Based Safety**: Continuous human detection/tracking (vision + depth), proximity zones (slow within 2m, stop within 0.5m)
  - **Planning-Based Safety**: Collision-free trajectory generation with safety margins, conservative grasp forces
  - **Reactive Safety**: Emergency stops when unexpected contact, compliant control (yielding to human touch)
  - **Fail-Safe Hardware**: E-stop buttons, watchdog timers, safe failure modes (controlled shutdown, lock joints)
  - **Force Limiting**: Limit joint torques to prevent injury (<150N impact force standard), soft padding on surfaces
- **Why It Matters**: Humans must feel physically safe to accept robot coworkers/assistants
- **VLA Integration**: Perception layer detects humans → planner avoids human-occupied regions → control limits forces

**4. Social Awareness (Respecting Human Social Norms)**
- **Principle**: Robot behaves according to social conventions, making interactions feel natural
- **Implementations**:
  - **Personal Space**: Maintain 1-2m distance from humans unless invited closer, don't loom over seated people
  - **Gaze Direction**: Look toward objects being manipulated, look at people being addressed (social eye contact)
  - **Social Norms**: Wait turn in doorways, don't interrupt conversations, approach from front (not behind)
  - **Context Sensitivity**: Quiet in bedrooms, faster in workshops, deferential in shared spaces
  - **Adaptability**: Learn user preferences (preferred interaction distance, communication style)
- **Why It Matters**: Humans judge robots by social standards; violations feel awkward or threatening
- **VLA Integration**: LLM encodes social norms from web-scale training; planner respects human context

**HRI Comparison Analogy**:
- **Transparency**: Like self-driving car displays showing detected objects and planned path
- **Predictability**: Like elevator always closing doors after 5 seconds (consistent timing)
- **Safety**: Like power tools with guards and emergency stops
- **Social Awareness**: Like service staff maintaining appropriate distance and eye contact

**HRI Challenges for VLA Systems**:
- LLMs understand social norms from text but must ground in physical behavior
- Real-time safety requires fast reactive control (System 1) not just slow reasoning (System 2)
- Transparency needs natural language generation integrated with action execution
- Social awareness requires understanding context beyond immediate task (e.g., recognize meeting in progress)

---

## Terminology Standards

*To be populated with consistent terminology usage guidelines*

---

**Note**: This file will be populated during Phase 2 (Foundational Research & Design) execution.
