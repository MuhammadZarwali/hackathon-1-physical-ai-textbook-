---
sidebar_position: 2
title: "Chapter 2: Language to Robot Planning"
description: "Learn how VLA systems translate natural language commands into executable robot actions through the four-level planning hierarchy, semantic grounding, and affordance-aware planning"
keywords: ["planning-hierarchy", "task-decomposition", "semantic-grounding", "affordance", "llm-planner", "action-primitive", "motor-control"]
module: "module-4-vision-language-action"
chapter_id: "chapter-2-language-to-robot-planning"
learning_objectives:
  - "Explain the four-level planning hierarchy (Task → Subtask → Action Primitive → Motor Control) and how each level transforms commands"
  - "Decompose a natural language command like 'prepare breakfast' into its full planning hierarchy with concrete examples at each level"
  - "Understand semantic grounding techniques for connecting language concepts to perception and physical actions"
  - "Describe how LLMs serve as high-level task planners and why they require affordance-based grounding"
  - "Compare LLM-based planning with traditional motion planning systems, identifying strengths and limitations of each approach"
prerequisites: ["Module 1: ROS 2 fundamentals", "Module 2: Simulation", "Module 3: NVIDIA Isaac", "Module 4 Chapter 1: Introduction to VLA"]
difficulty: "intermediate"
estimated_reading_time: 28
persona_relevance:
  beginner: 3
  software_engineer: 5
  robotics_student: 4
  ai_researcher: 5
vla_concepts: ["planning-hierarchy", "task-decomposition", "affordance", "language-grounding", "action-primitives"]
verified_against: "BrainBody-LLM, DELTA, SayCan papers, 2025 VLA planning research"
last_verified: "2025-12-27"
---

# Chapter 2: Language to Robot Planning

## Learning Objectives

By the end of this chapter, you will:
1. Explain the four-level planning hierarchy (Task → Subtask → Action Primitive → Motor Control) and how each level transforms commands
2. Decompose a natural language command like "prepare breakfast" into its full planning hierarchy with concrete examples at each level
3. Understand semantic grounding techniques for connecting language concepts to perception and physical actions
4. Describe how LLMs serve as high-level task planners and why they require affordance-based grounding
5. Compare LLM-based planning with traditional motion planning systems, identifying strengths and limitations of each approach

## The Planning Hierarchy

### Four Levels of Abstraction

VLA systems bridge the enormous gap between natural language commands and motor control signals through a four-level planning hierarchy. Each level operates at a different abstraction and timescale, transforming high-level human intent into low-level physical execution.

**Level 1: Task Level (Language-Level Goals)**

The task level processes natural language commands from users. Input arrives as spoken or written instructions: "Prepare breakfast," "Set the table," "Clean the kitchen." The LLM-based reasoning system interprets these abstract goals, understanding the user's intent and desired outcome.

The LLM decomposes the high-level task into an ordered sequence of subtasks, drawing on world knowledge learned from billions of text examples. For "Prepare breakfast," the LLM might generate: [Locate kitchen, Retrieve ingredients, Cook food, Plate food, Clean up]. This decomposition happens through the same mechanisms LLMs use for text generation—predicting likely next steps based on learned patterns about task procedures.

Timeframe: Seconds to minutes for LLM reasoning, depending on task complexity and model size. A 7B parameter model like OpenVLA might require 2-5 seconds for task decomposition. Larger models (100B+ parameters) might take 10-30 seconds but provide more sophisticated reasoning.

Output: Ordered list of high-level subtasks, each concrete enough to guide further decomposition but abstract enough for flexible execution strategies.

**Level 2: Subtask Level (Goal-Oriented Actions)**

The subtask level takes individual high-level subtasks and decomposes them into concrete robot goals involving specific objects, locations, or states. Where the task level operates in abstract procedural terms, the subtask level grounds actions in the current environment.

Consider the subtask "Retrieve eggs" from the breakfast preparation task. The subtask level decomposes this into specific actions: [Navigate to refrigerator, Open refrigerator door, Locate egg carton using vision, Grasp egg carton, Remove from refrigerator, Close refrigerator door, Navigate to cooking area]. Each step is a concrete goal the robot's perception and action systems can execute.

This decomposition must consider the robot's current state and environment. If the robot is already in the kitchen, "Locate kitchen" can be skipped. If eggs are visible on the counter, "Open refrigerator" isn't needed. The LLM performs this context-aware decomposition, adapting the subtask sequence to the actual situation rather than executing a fixed script.

Timeframe: Seconds for subtask planning per high-level task. The LLM might spend 1-3 seconds decomposing "Retrieve eggs" into the 7-step sequence above.

Output: Sequence of grounded actions with target objects, locations, or state changes specified.

**Level 3: Action Primitive Level (Grounded Robot Commands)**

The action primitive level translates semantic actions into parameterized robot commands. Subtasks like "Grasp egg carton" become specific function calls with numerical parameters: `grasp(object_id=egg_carton_3, pose=[x,y,z,roll,pitch,yaw], force=20N)`.

This translation involves motion planning and grasp planning. The vision system provides the egg carton's 6DOF pose (3D position + 3D orientation) from object detection. Grasp planning algorithms compute a feasible gripper configuration—approach angle, finger positions, grasp width—considering the object's shape and the robot's kinematics. Motion planning generates a collision-free trajectory from the robot's current arm configuration to the pre-grasp position, then to the grasp position.

Action primitives are the interface between VLA's language-level reasoning and traditional robotics' motion-level control. The LLM operates above this level, specifying what to grasp but not how to move each joint. Traditional robotics operates at this level, computing the geometric and kinematic details.

Timeframe: Milliseconds for motion planning. Computing a collision-free trajectory for a 7DOF arm might take 50-200 milliseconds depending on environment complexity and planner algorithm.

Output: Parameterized robot commands ready for execution—joint trajectories, gripper widths, force limits, navigation waypoints.

**Level 4: Motor Control Level (Low-Level Commands)**

The motor control level executes planned motions through real-time feedback control. Desired trajectories from action primitives—sequences of joint positions `[q1(t), q2(t), ..., q7(t)]` over time—must be tracked by the physical robot despite dynamics, friction, and disturbances.

PID controllers, impedance control, or computed torque methods adjust motor commands at high frequency (100-1000 Hz) to minimize tracking error. For the egg carton grasp, the controller ensures the arm follows the planned trajectory smoothly, then closes the gripper to the specified width (8cm) with force limited to 20N (eggs are fragile).

Sensor feedback—joint encoder readings, force/torque measurements, tactile sensors—informs control updates. If the gripper encounters unexpected resistance, force control prevents damage. If the arm deviates from the desired path, position control corrects the error.

Timeframe: Microseconds per control cycle. A 1000 Hz controller updates every millisecond, computing new motor commands based on the latest sensor readings.

Output: Joint velocity or torque commands sent to motor drivers, which directly actuate the physical robot.

:::tip For Software Engineers
The planning hierarchy in VLA systems mirrors the call stack you're familiar with from programming. At the top level, a user's natural language command like "prepare breakfast" is analogous to a high-level API call. The LLM decomposes this into function calls at the subtask level ("retrieve_eggs()", "cook_toast()"), which further break down into library function calls at the action primitive level ("navigate_arm(grasp_pose)", "execute_grasp(force=20N)"), and finally compile to system calls and hardware instructions at the motor control level (joint velocities at 100 Hz). Just as your code abstracts from high-level business logic down to CPU instructions, VLA bridges natural language down to motor commands—each level operating at its appropriate abstraction and timescale.
:::

### Information Flow and Feedback

The planning hierarchy isn't purely top-down. While goals flow downward (Task → Subtask → Action Primitive → Motor Control), feedback flows upward, enabling each level to adapt based on execution results.

**Top-Down Goal Flow**

Task-level plans specify what to accomplish. Subtask-level plans specify how to accomplish it through sequences of concrete actions. Action primitives specify the geometric and kinematic details. Motor control executes the physical motion. Each level provides increasingly specific constraints to the level below.

**Bottom-Up Feedback Flow**

Motor control reports execution status: trajectory tracking errors, unexpected forces, successful completion. Action primitives receive this feedback to determine if grasps succeeded, if navigation reached the goal, if manipulation achieved the desired state.

Subtask level monitors action primitive feedback to determine if individual steps completed successfully. If grasping fails, the subtask planner might retry with a different approach or skip to an alternative subtask ("eggs not available, use alternative breakfast plan").

Task level receives subtask completion reports and overall progress. If multiple subtasks fail, the LLM might replan the entire task or ask the user for guidance: "I'm having trouble finding eggs. Should I prepare breakfast without them?"

This bidirectional information flow enables robust operation. When the environment doesn't match expectations (glass isn't where anticipated, drawer is locked, ingredient is missing), feedback triggers replanning at the appropriate hierarchy level. Minor execution errors correct at the motor control level. Missing objects trigger subtask-level replanning. Fundamental task infeasibility prompts task-level user consultation.

In Module 1 (ROS 2 Communication), you learned about action servers that handle long-running goals with feedback—navigation actions report progress percentage, manipulation actions confirm grasp success. The planning hierarchy leverages these ROS 2 feedback mechanisms, with each level subscribing to relevant action feedback topics and using that information to monitor progress and detect failures.

### Concrete Example: "Set the Dinner Table"

Let's trace a complete example through all four levels to make the hierarchy concrete.

**Task Level**: User says "Set the dinner table"

The LLM interprets this high-level goal and decomposes it into subtasks:
1. Navigate to dish cabinet
2. Retrieve 4 plates (one per person)
3. Navigate to dining table
4. Place plates at appropriate positions (one per seat)
5. Return to standby

Assumptions: LLM knows typical place setting requires plates, knows cabinet is where dishes are stored, knows table has 4 seats based on previous environment mapping.

**Subtask Level**: For "Retrieve 4 plates"

Decompose into grounded actions:
1. Open cabinet door (if closed)
2. Detect plates using vision (identify stack of plates on shelf)
3. Grasp top plate from stack
4. Remove plate from cabinet
5. Place plate in secure carrying position
6. Repeat 3 more times for remaining plates
7. Close cabinet door

Each action specifies a concrete goal (grasp plate, navigate to location) with target objects identified.

**Action Primitive Level**: For "Grasp top plate from stack"

Vision pipeline: `detect_object(class="plate")` returns bounding boxes for all plates, with 6DOF poses

Grasp planning: `plan_grasp(plate_pose, gripper_constraints)` computes grasp pose considering plate is thin, fragile, part of stack (grasp from side edge, not top, to avoid disturbing stack)

Motion planning: `navigate_arm(grasp_pose)` generates collision-free joint trajectory from current arm configuration through approach pose to grasp pose, avoiding cabinet walls and other dishes

Execution command: `execute_grasp(gripper_width=25cm, force=low)` specifies gentle grasp force to avoid breaking ceramic plate

**Motor Control Level**: Execute grasp trajectory

Joint trajectory: 7DOF arm moves through waypoints: `[q1(t), q2(t), q3(t), q4(t), q5(t), q6(t), q7(t)]` where each qi(t) is joint i's position at time t

Control frequency: 100 Hz (10 millisecond updates)

PID controllers for each joint: Measure actual position via encoders, compute error vs desired trajectory, adjust motor torques to minimize error

Force control: Monitor gripper force sensors, close to 25cm width but stop if force exceeds 5N (gentle enough to avoid breaking plate)

Completion detection: Tactile sensors in gripper confirm contact with plate, force sensors confirm stable grasp, system reports "grasp successful" to action primitive level

:::tip For Software Engineers
This hierarchy is analogous to API orchestration and microservices in distributed systems. The task level is like a high-level orchestrator service that receives user requests and decomposes them into calls to multiple microservices ("OrderService.create()", "InventoryService.check()", "PaymentService.process()"). The subtask level is like each microservice's internal logic breaking requests into database queries and service calls. Action primitives are like the data access layer translating operations into specific database commands. Motor control is like the database engine executing SQL statements and managing low-level storage. Just as distributed systems coordinate asynchronous operations across services with different response times, the planning hierarchy coordinates operations across subsystems running at different frequencies (seconds for LLM, milliseconds for motion planning, microseconds for control loops).
:::

## Language-to-Planning Translation

### Task Decomposition with LLMs

Large Language Models serve as high-level policies that sequence skills from the robot's repertoire. Given a task like "prepare dinner," the LLM generates a plausible sequence of subtasks based on patterns learned from text data. This decomposition leverages the LLM's internalized knowledge about procedures, temporal dependencies, and common practices.

**Zero-Shot vs Fine-Tuned Approaches**

Zero-shot planning uses a general-purpose LLM (like GPT-4) without robotics-specific training. The model relies purely on world knowledge from internet text to decompose tasks. This approach provides maximum flexibility—any language command can be attempted—but may generate plans that don't account for the robot's specific capabilities or environment constraints.

Fine-tuned planning adapts an LLM to robotics through additional training on robot task descriptions, environment layouts, and execution traces. Systems like BrainBody-LLM use separate LLMs for reasoning (Brain-LLM) and command generation (Body-LLM), with both fine-tuned on robotics data. The Brain-LLM handles high-level plan synthesis while Body-LLM generates low-level commands grounded in the robot's action vocabulary.

Fine-tuning improves task-oriented success—BrainBody-LLM achieved 17% higher success rates than baseline approaches in simulated environments. However, fine-tuning requires robotics demonstration data and risks overfitting to specific tasks or environments. The tradeoff: zero-shot provides flexibility, fine-tuned provides reliability for known task distributions.

**Scene Graphs and Structured Representations**

Recent research like DELTA (Decomposed Efficient Long-Term planning) represents environments as scene graphs—structured representations showing objects, their properties, and spatial relationships. Rather than feeding raw text descriptions to the LLM, scene graphs provide compact, precise environmental context: `{kitchen: {table: {position: [2, 3], objects_on: [salt_shaker, pepper]}, fridge: {position: [5, 1], contains: [eggs, milk]}}}`.

This structured representation enables rapid, precise planning. The LLM reasons about object locations, spatial relationships, and affordances more reliably than when parsing verbose text descriptions. Scene graphs also reduce token count, important for LLMs with context window limits.

Systems like ConceptBot go further, using Knowledge Graphs to encode semantic relationships—not just "cup is on table" but "cups are typically found in cabinets," "grasping cups requires gentle force (fragile)," "cups can hold liquids (affordance)." This richer semantic structure improves planning reliability and helps the LLM avoid physically infeasible actions.

:::warning For AI Researchers
Zero-shot vs fine-tuned planning for robotics mirrors similar tradeoffs in NLP and vision. Zero-shot leverages the model's broad pre-training but may hallucinate actions the robot can't execute. Fine-tuning improves task-specific performance but risks overfitting. Prompt engineering strategies like chain-of-thought reasoning, providing few-shot examples of successful task decompositions, and structured output formats (JSON schemas) can improve zero-shot reliability without fine-tuning. Recent approaches combine both: use a large general-purpose LLM (GPT-4) for flexible reasoning with few-shot prompting, then filter proposed actions through a smaller fine-tuned affordance model that understands the robot's physical capabilities. This hybrid approach achieves broad generalization (zero-shot LLM) with safety constraints (fine-tuned grounding).
:::

### Semantic Grounding in Detail

Semantic grounding solves the core challenge of VLA: connecting symbolic language (discrete tokens representing abstract concepts) to subsymbolic perception and control (continuous neural network activations, pixel values, joint angles, forces).

**Language → Perception Grounding**

Consider the command "Pick up the red cup." The robot must map three concepts to visual perception:
- "cup" (object category) → detect cup-shaped objects
- "red" (color property) → filter by color
- "the" (definite article) → select specific instance, not just any red cup

Vision-language models like CLIP create joint embedding spaces where text and images have aligned representations. The text embedding for "red cup" should have high similarity to image embeddings of red cups. This learned alignment enables grounding: given the text "red cup," the system can identify which detected objects best match that description.

In practice, the grounding process involves multiple steps:

1. **Object Detection**: Vision system (Isaac ROS from Module 3) detects all objects in the scene, returning bounding boxes, class labels, and 6DOF poses
2. **Language Filtering**: Filter detected objects by language constraints—keep only objects classified as "cup"
3. **Attribute Matching**: Among cups, filter by color attributes—keep only red cups
4. **Selection**: If multiple red cups exist, choose based on secondary criteria (closest, most accessible, largest)
5. **Pose Extraction**: Return the selected cup's 3D pose for manipulation planning

The challenge is ambiguity. "Pick up the small object" is underspecified—small relative to what? The grounding system must either request clarification ("Which object do you mean?") or make a reasonable assumption based on context (smallest visible object, or smallest among a salient object set).

Digital twins, as you learned in Module 2, enhance semantic grounding by maintaining both geometric (3D positions, sizes) and semantic (object types, affordances, relationships) information. When an LLM plans "get the cookbook from the shelf," the digital twin representation indicates which shelf contains books, which specific book is the cookbook, and whether it's accessible or blocked by other objects.

**Language → Action Grounding**

Mapping verbs like "grasp," "push," "open," "pour" to manipulation primitives presents different challenges. Actions have preconditions, parameters, and effects that must align with the robot's capabilities.

Consider "Open the drawer":

1. **Verb Decomposition**: "Open" in the context of drawers means a pulling action, not a rotational action (unlike "open door" which might require turning a knob)
2. **Action Sequence**: [Approach drawer, Grasp handle, Pull outward in linear motion]
3. **Parameterization**: Pull direction (outward from drawer face), pull distance (until fully extended or resistance stops motion), force limits (gentle enough not to break drawer rails)
4. **Affordance Checking**: Is drawer openable? Is handle graspable? Is workspace clear for pulling motion?

Affordance models encode what actions are physically possible. A locked drawer fails the "openable" affordance check. A drawer without a handle fails the "handle graspable" check. The grounding system uses these affordances to filter the LLM's proposed actions, rejecting infeasible plans before attempting execution.

Reinforcement learning can ground actions through trial and error. A robot learns that "push" on a lightweight box succeeds, but "push" on a heavy refrigerator fails. Over time, the learned policy associates action verbs with successful execution strategies given object properties (weight, friction, constraints).

:::tip For Software Engineers
Semantic grounding in VLA is analogous to ORM (Object-Relational Mapping) in databases. Just as an ORM maps abstract object-oriented concepts like "Customer" to concrete database tables with specific fields (customer_id, name, email), semantic grounding maps abstract language concepts like "cup" to concrete perception data (bounding boxes, 3D coordinates, visual features from camera pixels). When your ORM translates `customer.save()` into SQL INSERT statements, it bridges the abstraction gap between your code and physical database storage. Similarly, when a VLA system grounds "pick up the red cup" into visual object detection filters and grasp planning parameters, it bridges language (symbolic, abstract) to perception and control (subsymbolic, numerical). Both solve the same fundamental problem: connecting high-level abstractions to low-level representations.
:::

### Affordance-Aware Planning

Affordances define what actions are physically possible given object properties, environmental constraints, and robot capabilities. A cup affords grasping (has graspable size and shape) and filling with liquid (has open top and container structure). A wall affords leaning against but not grasping. Understanding affordances is critical for generating executable plans.

**The SayCan Approach**

Google's SayCan system pioneered affordance-aware VLA planning. The architecture combines two models:
- **LLM as Planner**: Proposes action sequences based on language understanding and world knowledge
- **Affordance Model**: Scores each proposed action by physical feasibility given current robot state

For the task "bring me a bottle of water," the LLM might generate candidate plans:
1. [Go to kitchen, Open fridge, Grasp bottle, Navigate to user, Hand over]
2. [Check nearby table for water bottles, If found: grasp, Navigate to user, Hand over]
3. [Ask user where water is, Navigate to location, ...]

The affordance model evaluates each action's feasibility. "Open fridge" scores high if the robot can reach the fridge handle and has the manipulation capability. "Grasp bottle" scores high if bottles are visible and within reach. The system selects the plan with highest cumulative affordance scores—the most feasible sequence.

This filtering prevents the LLM from suggesting impossible actions. Without affordance grounding, an LLM might plan "pour water into closed bottle"—linguistically sensible but physically impossible. The affordance model rejects this (bottle must be open for pouring) and requests replanning.

**Feedback-Driven Refinement**

Affordance models improve through execution feedback. If the system attempts to grasp an object and fails repeatedly, that failure updates the affordance estimate—perhaps the object is too slippery, too heavy, or awkwardly positioned. Future plans avoid that grasp or try alternative approaches.

This feedback loop is essential because affordances depend on context that's difficult to predict. A cup that affords grasping when isolated on a table may not afford grasping when buried among clutter. Execution attempts reveal these contextual constraints, refining the affordance model over time.

Successful VLA implementations use the LLM in a feedback loop rather than one-shot planning. The LLM proposes a plan, affordance filtering adjusts it, execution provides results, and the LLM replans if needed. This iterative approach—coupling language reasoning with real-world grounding—vastly improves reliability compared to one-shot "LLM outputs plan, robot executes" approaches.

As you learned in Module 1, ROS 2 actions provide structured feedback during execution through goal status updates and result messages. VLA planning integrates with this feedback mechanism—the LLM monitors action server feedback to detect failures and trigger replanning at the appropriate hierarchy level.

## Concrete Walkthrough: "Prepare Breakfast"

To make the planning hierarchy tangible, let's walk through a complete example: "Prepare breakfast with eggs and toast." We'll trace the command through all four levels, showing exactly how language transforms into robot motions.

### High-Level Task Decomposition

**Language Input**: "Prepare breakfast with eggs and toast"

**LLM Task-Level Plan**:

The LLM reasoning system (System 2 in dual-system architectures) processes this command and generates a task-level plan:

1. Locate kitchen (determine where cooking appliances and ingredients are)
2. Retrieve ingredients (eggs from refrigerator, bread from pantry or counter)
3. Prepare toast (place bread slices in toaster, press start button, wait for completion)
4. Prepare eggs (crack eggs, cook on stove or microwave)
5. Plate food (transfer toast and eggs to serving plate)
6. Clean up (return ingredients to storage, wipe surfaces)

This decomposition draws on the LLM's world knowledge about breakfast preparation procedures learned from recipe text, cooking instructions, and household task descriptions across billions of web documents. The LLM understands that preparing breakfast requires ingredients, cooking appliances, and sequential steps—knowledge that doesn't need to be explicitly programmed for this specific robot.

Timeframe: 5-10 seconds for the LLM to generate this 6-step plan, depending on model size and computational resources.

Assumptions: The LLM assumes a standard kitchen layout with refrigerator, stove/microwave, toaster, and pantry. If the environment differs significantly (outdoor kitchen, minimal equipment), the plan might not be appropriate—this is where environment awareness through scene graphs or digital twin representations helps the LLM ground plans in reality.

### Subtask Breakdown: "Retrieve Eggs from Fridge"

**Subtask-Level Decomposition**:

The second-level planner takes "Retrieve eggs from refrigerator" and decomposes into concrete robot goals:

1. Navigate to refrigerator (move mobile base to position in front of fridge, face the door)
2. Open refrigerator door (grasp handle, pull door open, confirm door is fully open)
3. Locate egg carton using vision (process camera images, detect egg carton among fridge contents, extract 3D pose)
4. Grasp egg carton (compute grasp, move arm to grasp pose, close gripper)
5. Remove egg carton from fridge (retract arm, ensure clear of fridge door)
6. Close refrigerator door (either with free manipulator or by repositioning, push door closed gently)
7. Navigate to cooking area (move to stove or counter workspace carrying eggs)

Each step is a concrete goal involving specific objects (refrigerator door, egg carton) or locations (in front of fridge, at cooking area). Dependencies are explicit: must open door before accessing contents, must grasp carton before removing, must remove items before closing door.

This level connects language-level goals ("retrieve eggs") to robot-level actions (navigation goals, manipulation goals). The subtask planner might run as part of the LLM's chain-of-thought reasoning, or as a separate specialized planner that takes LLM task-level plans and grounds them in robot capabilities.

### Action Primitive Detail: "Grasp Egg Carton"

**Action Primitive Execution**:

Let's trace just the "Grasp egg carton" subtask through the action primitive level to see how it translates to specific robot commands.

**Vision Processing**:
- Camera images: Robot's cameras capture RGB images of refrigerator interior (resolution 1920x1080, 30 FPS)
- Object detection: `detect_object(class="egg_carton")` runs vision model (could be Isaac ROS object detection from Module 3)
- Output: Bounding box `[x_min, y_min, x_max, y_max]` in image space, 6DOF pose `[x, y, z, roll, pitch, yaw]` in 3D world coordinates
- Confidence: 0.95 (high confidence detection)

**Grasp Planning**:
- Input: Object pose `position=[0.45m, 0.62m, 0.15m]` (inside fridge), `orientation=[0°, 0°, 90°]` (carton lying flat)
- Constraints: Gripper width 0-12cm, approach from top or side (limited space in fridge), avoid hitting fridge walls/shelves
- Grasp planner: `plan_grasp(object_pose, gripper_constraints)` evaluates multiple grasp candidates
- Selected grasp: Top grasp, gripper oriented to align with carton's long axis, approach from above (clear path)
- Grasp parameters: `position=[0.45m, 0.62m, 0.20m]`, `orientation=[0°, 0°, 90°]`, `gripper_width=8cm`

**Motion Planning**:
- Current arm state: `[q1_current, ..., q7_current]` (7DOF arm joint angles)
- Target: Pre-grasp pose (5cm above grasp pose for safe approach), then grasp pose
- Motion planner: `navigate_arm(target_poses)` uses RRT or optimization to find collision-free trajectory
- Collision constraints: Avoid fridge walls, shelves, door, other objects in fridge
- Output: Joint trajectory waypoints `[[q1_0, ..., q7_0], [q1_1, ..., q7_1], ..., [q1_final, ..., q7_final]]`
- Trajectory duration: 2.5 seconds for smooth motion

**Execution Command**:
- Command: `execute_grasp(gripper_width=8cm, force=20N)`
- Behavior: Follow trajectory to pre-grasp, descend to grasp, close gripper to 8cm width
- Force limit: 20N (gentle enough for cardboard carton with fragile eggs inside)
- Feedback: Tactile sensors confirm contact, force sensors confirm stable grasp
- Completion: Report "grasp successful" when tactile + force feedback indicate secure grasp

This action primitive completes in approximately 3 seconds (2.5s motion + 0.5s grasp execution). The subtask level receives "success" feedback and proceeds to the next step ("Remove egg carton from fridge").

:::info For Robotics Students
You're familiar with how high-level grasp commands ultimately become joint trajectories executed by low-level controllers. In VLA, the "grasp egg carton" action primitive you see at the language level maps directly to the motion primitives and control loops you've worked with: first, vision provides the object's 6DOF pose estimate; grasp planning computes a feasible grasp configuration considering gripper kinematics and approach constraints; motion planning generates a collision-free joint trajectory from current to pre-grasp to grasp poses; and finally, your standard feedback control (PID, impedance control, or computed torque) executes this trajectory at 100-1000 Hz while monitoring force/torque sensors. The VLA innovation isn't in the low-level control—that's still the same joint-space controllers and dynamics models from your controls coursework—it's in automatically generating these goals from language rather than hard-coding them.
:::

### Motor Control Execution

**Motor Control Level Detail**:

The action primitive level outputs a desired joint trajectory. Motor control must execute this trajectory on the physical robot, handling dynamics, disturbances, and uncertainties.

**Joint Trajectory Execution**:

For the 7DOF arm moving to grasp the egg carton, the trajectory specifies joint positions over time:
- `q1(t)`: Base rotation (shoulder yaw)
- `q2(t)`: Shoulder pitch
- `q3(t)`: Shoulder roll
- `q4(t)`: Elbow pitch
- `q5(t)`: Wrist yaw
- `q6(t)`: Wrist pitch
- `q7(t)`: Wrist roll

At 100 Hz control frequency, the controller receives a new desired position every 10 milliseconds. PID controllers for each joint measure actual position via encoders, compute error (desired - actual), and adjust motor torque to minimize error:

```
error = desired_position - actual_position
torque = Kp * error + Ki * integral(error) + Kd * derivative(error)
```

**Gripper Control**:

Simultaneously, gripper control closes to the specified width (8cm) with force limiting:

- Measure current gripper width via encoder
- Command gripper motor to close
- Monitor force sensors on gripper fingers
- Stop closing when either: width reaches 8cm OR force exceeds 20N
- Maintain grasp force at 15-20N (sufficient to hold carton securely without crushing)

**Feedback and Completion Detection**:

Tactile sensors in gripper fingers detect contact with the carton. Force sensors confirm sufficient grip force. The control system integrates these signals: if tactile sensors show contact AND force sensors show 15-20N grip force AND arm has reached target pose (tracking error < 1mm), then grasp is successful.

This feedback reports to the action primitive level: "Grasp egg carton: SUCCESS." The subtask planner receives this confirmation and proceeds to "Remove egg carton from fridge."

Real-time constraints are critical at this level. Control loops must execute within their cycle period (10ms at 100 Hz) to maintain stability. Delays or missed cycles can cause oscillations, tracking errors, or unsafe behavior. This is why motor control runs on dedicated real-time hardware, separate from the slower LLM reasoning that might take seconds.

In Module 1, you learned how ROS 2 topics publish sensor data—joint states, force/torque readings, tactile feedback. Motor controllers subscribe to desired trajectory topics and publish actual state topics, enabling the planning hierarchy to monitor execution through ROS 2's communication infrastructure.

## LLM Planning vs Traditional Motion Planning

Understanding when to use LLM-based planning versus traditional motion planning requires comparing their strengths, limitations, and appropriate use cases.

| Aspect | Traditional Motion Planning | LLM-Based Planning |
|--------|----------------------------|-------------------|
| **Input** | Explicit goal states (coordinates, joint configurations, poses) | Natural language instructions ("prepare breakfast", "navigate to kitchen") |
| **Reasoning** | Geometric and kinematic constraints (collision-free paths, joint limits, workspace reachability) | Common-sense + semantic reasoning (task procedures, object relationships, temporal dependencies) |
| **Generalization** | Limited to scenarios within modeled environment (requires accurate world model) | Generalizes via language understanding to novel tasks and environments (leverages web-scale knowledge) |
| **Task Decomposition** | Manual breakdown required—engineer specifies each sub-goal explicitly | Automatic from language—LLM decomposes "set table" into subtasks without explicit programming |
| **Adaptability** | Requires reprogramming for new tasks (add new pick-and-place sequence needs code changes) | Few-shot or zero-shot adaptation (user just describes new task in language) |
| **Speed** | Fast—milliseconds for motion planning (RRT: 50-200ms, optimization: 100-500ms) | Slow—seconds for high-level reasoning (7B LLM: 2-5s, 100B+ LLM: 10-30s per task decomposition) |
| **Reliability** | Guaranteed (mathematically provable if world model is accurate) | Probabilistic (learned models may hallucinate impossible plans without grounding) |
| **Integration (2025 Trend)** | LLM handles task-level and subtask-level reasoning, traditional motion planning handles action primitive and motor control levels (dual-system architecture) |

**Concrete Examples**:

**Traditional Approach**: Pick-and-place task
```
Engineer specifies:
- navigate_to(x=0.5, y=0.3, z=table_height)
- grasp(object_id=block_7, approach_angle=90deg, force=30N)
- navigate_to(x=1.2, y=0.8, z=bin_height)
- release(object_id=block_7)
```
Every coordinate, angle, and parameter is explicit. Changing the task (pick blue blocks instead of red) requires modifying these specifications.

**LLM-Based VLA Approach**: Same task
```
User: "Pick up the red blocks and put them in the bin"
VLA: [Interprets command, identifies red blocks via vision, plans grasping sequence, executes placement]
```
No explicit coordinates needed. Language provides the specification. Changing to blue blocks just requires changing the command.

**When Traditional Planning Excels**

Real-time motion control benefits from traditional methods. Computing collision-free trajectories, inverse kinematics, and control commands involves well-understood mathematics with guaranteed solutions (given valid world models). For safety-critical systems, these guarantees matter more than language flexibility.

Known environments with repetitive tasks don't require LLM reasoning. A manufacturing robot that welds the same joint on thousands of identical parts gains nothing from language planning—the task never changes, efficiency and precision matter most. Traditional motion planning optimizes for these scenarios.

Latency-sensitive operations can't afford seconds of LLM reasoning. Reactive grasping (react to slipping object within milliseconds), dynamic balance control (100-1000 Hz feedback loops), and collision avoidance (respond to sudden obstacles immediately) all require fast, deterministic planning. Traditional methods provide this speed.

**When LLM Planning Excels**

High-level task sequencing leverages LLM strengths. Decomposing "prepare dinner for guests" into shopping, cooking, plating, and serving steps requires procedural knowledge and common-sense reasoning that traditional systems lack. LLMs handle this naturally.

Novel task handling shows LLM adaptability. A household robot might encounter "help me pack for vacation"—a task it's never seen in training data. An LLM can decompose this into retrieving luggage, gathering items from specified categories (clothes, toiletries, electronics), and packing methodically. Traditional systems would require explicit programming for this new task.

Natural user interaction demands language understanding. Service robots, healthcare assistants, and collaborative manufacturing systems interact with non-technical users who expect conversational interfaces. LLMs enable this natural interaction, understanding diverse phrasings, handling clarification dialogues, and adapting to user corrections.

**The 2025 Dual-System Trend**

Modern VLA systems increasingly adopt dual-system architectures: LLM-based reasoning for task and subtask levels, traditional planning for action primitive and motor control levels. Systems like Helix and Groot N1 exemplify this pattern.

This hybrid approach captures strengths of both paradigms. LLMs provide flexible, language-grounded task reasoning. Traditional methods provide fast, reliable motion planning and control. The two systems communicate through well-defined interfaces—the LLM outputs semantic goals ("grasp egg carton"), traditional planning computes geometric details (joint trajectories).

:::warning For AI Researchers
The semantic grounding challenge in VLA is a specific instance of the broader symbol grounding problem in embodied AI—how do we connect symbolic representations (language tokens) to subsymbolic sensor and actuator signals? Unlike pure NLP where grounding in text suffices, or computer vision where grounding in pixels suffices, robotics requires grounding in both perception (visual features, depth maps, proprioceptive state) AND action (joint torques, end-effector forces, object affordances). This is why end-to-end VLA models like RT-2 and OpenVLA are trained with robot demonstration data, not just internet images and text: the model must learn which visual features predict successful grasps, which language commands correlate with specific manipulation sequences, and how perception and language together constrain feasible actions. It's analogous to the grounding problem in multimodal learning, but with the added constraint that predictions must be physically executable—an LLM might hallucinate a plausible-sounding but impossible plan, which pure language training won't catch. Embodied grounding requires environmental feedback (did the action succeed?) as the ultimate truth signal.
:::

## Chapter Summary

The planning hierarchy is the central mechanism through which VLA systems translate natural language into robot actions. Four levels bridge the abstraction gap: Task level (language-level goals decomposed by LLMs), Subtask level (goal-oriented actions grounded in environment), Action Primitive level (parameterized robot commands with geometric details), and Motor Control level (real-time feedback control executing trajectories at 100-1000 Hz).

Information flows bidirectionally through this hierarchy. Goals flow downward from abstract to concrete. Feedback flows upward from sensors through controllers to planners, enabling each level to monitor progress, detect failures, and trigger replanning when needed. This feedback integration leverages ROS 2 action servers and topics, connecting VLA's cognitive layer with traditional robotic subsystems.

Semantic grounding connects language concepts to physical perception and action. Vision-language models like CLIP enable language → perception grounding, mapping words like "red cup" to visual object detection. Affordance models enable language → action grounding, ensuring verbs like "grasp" map to physically feasible manipulation primitives. Systems like SayCan demonstrate that coupling LLM reasoning with affordance filtering vastly improves reliability—the LLM provides flexible task decomposition, affordances ensure physical executability.

The "Prepare breakfast" walkthrough demonstrated all four hierarchy levels in action. From language input through LLM task decomposition (6 high-level steps), subtask breakdown ("Retrieve eggs" → 7 grounded actions), action primitive execution (grasp planning + motion planning for egg carton), to motor control (joint trajectories + force control at 100 Hz)—each level transforms the command closer to physical reality while maintaining appropriate abstractions.

Comparing LLM planning with traditional motion planning reveals complementary strengths. LLMs excel at high-level task sequencing, novel task adaptation, and natural language interfaces. Traditional planners excel at real-time motion control, safety-critical trajectories, and deterministic guarantees. The 2025 trend toward dual-system architectures (Helix, Groot N1) combines both: slow, deliberate LLM reasoning (System 2) for task understanding paired with fast, reactive control (System 1) for execution—achieving both flexibility and performance.

## What's Next

Chapter 3 completes Module 4 by presenting the autonomous humanoid capstone. You'll see how all five subsystems—perception, planning (VLA), navigation, manipulation, and communication—integrate into a complete end-to-end architecture. We'll trace the voice-to-action interaction loop in real humanoid systems like Tesla Optimus and Boston Dynamics Atlas, explore safety mechanisms and human-robot interaction principles required for humanoids operating safely alongside humans, and most importantly, understand how Modules 1-4 work together: ROS 2 as the communication backbone, simulation for testing, Isaac for GPU-accelerated perception, and VLA as the cognitive layer enabling natural language interaction. Chapter 3 synthesizes everything you've learned across the entire Physical AI & Humanoid Robotics textbook into a unified vision of autonomous systems.
