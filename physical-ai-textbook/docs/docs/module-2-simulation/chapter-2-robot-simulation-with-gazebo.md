---
sidebar_position: 2
title: "Chapter 2: Robot Simulation with Gazebo"
description: "Understand how Gazebo simulates physics, robot models, and behavior, and how it integrates with ROS 2 for humanoid robotics"
keywords: ["gazebo", "physics-engine", "urdf", "sdf", "ros2-integration", "robot-modeling", "simulation"]
module: "module-2-simulation"
chapter_id: "chapter-2-robot-simulation-with-gazebo"
learning_objectives:
  - "Explain Gazebo's role as a physics-based simulator for robotics"
  - "Describe how physics engines simulate gravity, collisions, and joint dynamics"
  - "Understand URDF and SDF robot model formats at a conceptual level"
  - "Diagram the ROS 2 + Gazebo communication flow for sensor data and control commands"
prerequisites: ["Chapter 1: Introduction to Digital Twins", "Module 1: ROS 2 Communication Model"]
difficulty: "beginner"
estimated_reading_time: 30
persona_relevance:
  beginner: 4
  software_engineer: 5
  robotics_student: 5
  ai_researcher: 3
simulation_concepts: ["gazebo", "physics-engine", "urdf", "sdf", "ros2-gazebo-bridge"]
verified_against: "https://gazebosim.org/docs"
last_verified: "2025-12-26"
---

# Chapter 2: Robot Simulation with Gazebo

## Learning Objectives

By the end of this chapter, you will:
- Explain Gazebo's role as a physics-based simulator for robotics
- Describe how physics engines simulate gravity, collisions, and joint dynamics
- Understand URDF and SDF robot model formats at a conceptual level
- Diagram the ROS 2 + Gazebo communication flow for sensor data and control commands

## What Gazebo Simulates

Gazebo is an open-source, physics-based robot simulator widely used in research, education, and industry. While Chapter 1 discussed digital twins conceptually, Gazebo is a specific tool that brings those digital twins to life. It simulates everything a robot experiences: the pull of gravity on its body, the impact of feet hitting the ground, camera images of the environment, and motor forces moving joints.

**What makes Gazebo powerful**: Unlike simple 3D visualization tools that just display robot models, Gazebo calculates actual physics. When you command a simulated humanoid to lift its leg, Gazebo computes how that action affects the robot's center of mass, whether it tips over, and how much force each remaining foot must apply to maintain balance. This physics-based approach means behaviors developed in Gazebo transfer to real robots—the simulated robot obeys the same physical laws as its real-world counterpart.

Gazebo simulates three core aspects of robotics systems:

**1. Physics**: Gravity pulls objects downward. Collisions create impact forces. Friction resists sliding motion. Joint constraints limit how links can move relative to each other. Springs and dampers add compliance. Physics simulation updates these forces 1,000 times per second, calculating how every force affects every moving part. For a humanoid, this means simulating 20-30 joints simultaneously, computing balance dynamics, ground contact forces, and the effects of arm motions on overall stability.

**2. Sensors**: Cameras render images based on the simulated scene's geometry, lighting, and materials. LiDAR sensors cast virtual rays to measure distances to obstacles, returning 3D point clouds. IMUs (Inertial Measurement Units) report the robot's orientation, angular velocity, and linear acceleration. Force sensors detect contact forces at grippers or feet. Each sensor produces data in the same format as its real-world equivalent, allowing perception algorithms developed in simulation to work on physical robots without modification.

**3. Actuators**: Motors and servos that move robot joints. Gazebo simulates motor dynamics—how commanded torques produce actual joint movements, accounting for motor inertia, gear ratios, and friction. When a control algorithm commands "move knee joint to 45 degrees," Gazebo calculates the torque needed, applies it through the physics engine, and reports back the actual achieved position (which might differ slightly due to dynamic effects).

:::note For Beginners
Think of Gazebo as the physics engine in modern video games, but for robots instead of game characters. When you play a racing game and your car's suspension compresses realistically over bumps, that's a physics engine at work. When you see debris scatter convincingly from an explosion, physics is simulating those forces. Gazebo does the same thing for robots: it makes sure that when a humanoid lifts its leg, the physics of balance, weight shift, and ground contact all behave realistically. The difference is that game engines prioritize looking realistic, while Gazebo prioritizes being realistic—because the behaviors developed in Gazebo will eventually run on real hardware.
:::

**Why Gazebo for humanoid robotics**: Humanoid robots present unique simulation challenges. They have many joints (20-30) that must coordinate precisely for stable movement. They operate in complex environments with varied terrain, obstacles, and lighting. They rely heavily on sensor fusion—combining camera, LiDAR, and IMU data for perception and control. Gazebo handles all these challenges with a mature, well-tested simulation framework that integrates seamlessly with ROS 2 (which you learned about in Module 1).

**Industry usage**: While Chapter 1 mentioned that Boston Dynamics uses NVIDIA Isaac Sim and Sanctuary AI uses Isaac Lab, the principles are identical—these are physics-based simulators like Gazebo, just with different performance characteristics and features. Research labs worldwide use Gazebo because it's free, open-source, and has extensive documentation and community support. Many of the concepts you learn about Gazebo (physics engines, sensor models, robot descriptions) apply directly to other simulators. Learning Gazebo teaches you how robot simulation works generally, not just one specific tool.

## Physics Engines and Realism

At Gazebo's core is a physics engine—software that computes how forces affect object motion. When you drop a ball in simulation, the physics engine calculates how gravity accelerates it downward, how it bounces when hitting the ground, and how friction eventually brings it to rest. For humanoid robots with dozens of moving parts and complex contact scenarios (feet on ground, hands grasping objects), physics engines must solve thousands of equations per simulation step.

### The Four Physics Engines in Gazebo

Gazebo supports four different physics engines, each with different strengths. Users can choose which engine to use based on their robot type and simulation goals.

**1. ODE (Open Dynamics Engine)**
- **Type**: Maximal coordinate solver
- **Optimization**: Performance over many independent moving objects
- **Best for**: Scenarios with multiple robots or many separate objects (warehouse with multiple robots and scattered packages)
- **Default**: This is Gazebo's default physics engine, installed automatically

**2. Bullet**
- **Type**: Maximal coordinate solver (like ODE)
- **Origin**: Developed originally for video game physics
- **Best for**: Complex collision scenarios with many interacting objects
- **Characteristics**: Fast collision detection, good for real-time constraints

**3. DART (Dynamic Animation and Robotics Toolkit)**
- **Type**: Featherstone-based reduced-coordinate solver
- **Optimization**: Kinematic chains with many joints
- **Best for**: Humanoid robots, robotic arms, articulated systems
- **Characteristics**: Efficient for systems like humanoids where many joints connect in a tree structure (torso → legs → feet, torso → arms → hands)

**4. Simbody**
- **Type**: Featherstone-based reduced-coordinate solver (like DART)
- **Origin**: Developed for biomechanics research
- **Best for**: Lifelike motion, biologically-inspired robots
- **Characteristics**: High accuracy for articulated body dynamics

| Physics Engine | Type | Best For | Typical Use Case |
|----------------|------|----------|------------------|
| **ODE** (default) | Maximal coordinates | Many independent objects | Multi-robot warehouses, object manipulation with many pieces |
| **Bullet** | Maximal coordinates | Complex collisions, real-time | Fast-paced scenarios, games, quick prototyping |
| **DART** | Featherstone (reduced) | Humanoids, robotic arms | Atlas, Optimus, any robot with 15+ joints in kinematic chains |
| **Simbody** | Featherstone (reduced) | Biomechanics, natural motion | Human motion simulation, biologically-inspired robots |

:::info For Robotics Students
The key technical distinction is between maximal coordinate methods (ODE, Bullet) and reduced-coordinate Featherstone algorithms (DART, Simbody). Maximal methods represent each rigid body's position and orientation independently—6 coordinates per body. For a humanoid with 20 links, that's 120 coordinates, and you must enforce joint constraints via constraint forces. Solving these constraint equations is O(n³) in the number of bodies.

Featherstone's articulated-body algorithm exploits the kinematic tree structure: each joint adds just one coordinate (for revolute joints). For a humanoid with 20 joints, that's only 20 generalized coordinates. The algorithm propagates forces and accelerations through the tree in O(n) time—linear in the number of joints. For humanoids with 20-30 degrees of freedom, this makes real-time simulation (100-1000 Hz) computationally feasible. This is why DART and Simbody are preferred for articulated robots.
:::

### What Physics Engines Simulate

Regardless of which engine Gazebo uses, all physics engines simulate the same fundamental phenomena:

**Gravity**: A constant downward force proportional to mass. For a humanoid robot weighing 60 kg, gravity applies roughly 600 Newtons downward on its center of mass. When the robot lifts one leg, its center of mass shifts—the physics engine continuously recalculates the net gravitational force and torques about the remaining contact points.

**Collisions and contact**: When two surfaces touch (foot hitting ground, hand grasping object, robot bumping obstacle), the physics engine detects the collision and computes contact forces. These forces prevent interpenetration—solid objects can't pass through each other. Contact forces depend on material properties: a rubber foot on concrete behaves differently than metal on ice.

**Friction**: Resistance to sliding motion. Static friction prevents a stationary object from sliding until the applied force exceeds a threshold. Kinetic friction opposes motion once sliding starts. For humanoid walking, foot-ground friction is critical—too little friction (icy surface) makes walking impossible, too much friction (sticky floor) wastes energy. The Coulomb friction model approximates this with a friction coefficient.

**Joint constraints and dynamics**: Joints connect rigid bodies while constraining their relative motion. A revolute joint (like a knee or elbow) allows rotation about one axis but prevents translation and rotation about other axes. The physics engine enforces these constraints while simulating joint dynamics—motors apply torques, inertia resists changes in motion, friction in bearings dissipates energy, and dampers smooth oscillations.

**Forces and torques**: External forces (gravity, collisions) and internal forces (motors, springs) all contribute to rigid body motion. The physics engine sums forces to compute linear acceleration (F = ma) and sums torques to compute angular acceleration (τ = Iα, where I is rotational inertia). Integration of accelerations yields velocities, and integration of velocities yields positions—all updated at high frequency (typically 1000 Hz) for stability.

### The Realism vs Performance Trade-off

Perfect physical accuracy is impossible—reality includes countless effects (material deformation, air resistance, thermal expansion) that are too computationally expensive to simulate in real-time. Physics engines make trade-offs: which effects to model accurately, which to approximate, and which to ignore entirely.

**Higher realism (slower simulation)**:
- Small timesteps (0.0001 seconds) capture fast dynamics accurately
- Complex contact models with compliant materials, detailed friction
- Precise collision detection for irregular shapes
- Simulated material properties: elasticity, plasticity, fracture

**Higher performance (faster than real-time)**:
- Larger timesteps (0.001 seconds) allow faster-than-real-time simulation
- Simplified contact: point contacts instead of surface patches
- Bounding box collision detection instead of precise mesh collisions
- Rigid bodies only (no deformation)

For humanoid robot development, the sweet spot is typically "sufficient realism for control development, fast enough for reinforcement learning." A walking controller doesn't need to simulate individual material fibers flexing in the robot's feet—it needs overall contact forces accurate enough that balance strategies learned in simulation work on real hardware. Gazebo defaults (ODE physics at 1000 Hz) achieve this balance for most humanoid applications.

:::tip For Software Engineers
This trade-off mirrors database choices in backend development: consistency vs availability vs partition tolerance (CAP theorem). You can't have perfect realism (consistency), real-time performance (availability), and simulation of all physical phenomena (partition tolerance)—pick two. Most robotics applications choose "good enough realism" and "real-time or faster" while sacrificing perfect physical accuracy. Just as eventual consistency works for many web applications despite not being "true" ACID transactions, approximate physics works for most robot development despite not being "true" Newtonian mechanics at molecular scales.
:::

## Robot Models: URDF and SDF (Conceptual)

To simulate a robot, Gazebo needs a description of its structure: what parts exist, how they connect, how much they weigh, and how they look. Two file formats serve this purpose: URDF (Unified Robot Description Format) and SDF (Simulation Description Format). While you won't write these files by hand (that's beyond the scope of this conceptual chapter), understanding what they describe is essential.

### URDF: The ROS-Native Robot Description

URDF is an XML-based format originally developed for ROS (and now used in ROS 2) to describe robot structure. Remember from Module 1 that ROS 2 uses nodes to organize computation—URDF defines the physical robot those nodes control.

**What URDF describes**:

**Links**: Rigid bodies that make up the robot. For a humanoid, links include torso, head, upper arm, forearm, hand, thigh, shin, foot. Each link specifies:
- **Visual properties**: 3D mesh or primitive shape (box, cylinder, sphere) for rendering
- **Collision properties**: Simplified geometry for collision detection (often simpler than visual for performance)
- **Inertial properties**: Mass, center of mass, and inertia tensor (how mass distributes spatially)

**Joints**: Connections between links that define how they can move relative to each other. Joint types include:
- **Revolute**: Rotates about one axis (knee, elbow)
- **Continuous**: Revolute with no angle limits (wheel)
- **Prismatic**: Slides along one axis (telescoping link)
- **Fixed**: No relative motion (rigidly attached)

Each joint specifies the parent link, child link, axis of rotation/translation, joint limits (min/max angles), and dynamics (damping, friction).

**Example conceptual structure** for a simplified humanoid arm:
```
Root: torso (link)
  └─ shoulder_joint (revolute, horizontal rotation)
      └─ upper_arm (link)
          └─ elbow_joint (revolute, vertical rotation)
              └─ forearm (link)
                  └─ wrist_joint (revolute)
                      └─ hand (link)
```

This tree structure defines how motion propagates: rotating the shoulder moves the entire arm, rotating the elbow moves only the forearm and hand, and rotating the wrist moves only the hand.

**URDF limitations**:
- Describes only a single robot in isolation (cannot specify multiple robots in one file)
- Cannot describe the robot's pose within a world (starting position and orientation)
- Lacks simulation-specific properties like sensor noise, friction coefficients, or environmental factors
- Does not support plugins for custom behaviors

Despite these limitations, URDF remains the standard for robot description in ROS 2 because it serves its core purpose: telling ROS 2 what joints exist, how they connect, and what sensors are available. As you learned in Module 1, ROS 2 nodes publish to `/joint_states` topics and subscribe to control topics—URDF defines which joints those topics refer to.

### SDF: Gazebo's Simulation-Native Format

SDF (Simulation Description Format) was created specifically for Gazebo to address URDF's limitations. Where URDF describes robots, SDF describes complete simulated worlds: environments, robots, sensors, lighting, and physics parameters.

**What SDF includes beyond URDF**:

**World description**: The environment surrounding the robot. Ground planes, walls, obstacles, furniture—everything that isn't the robot itself. SDF can specify:
- Terrain models (flat ground, hills, stairs)
- Static objects (tables, walls, boxes)
- Dynamic objects (balls, packages to manipulate)
- Lighting (directional sunlight, spotlights, ambient light)

**Multiple models**: SDF files can describe multiple robots or objects in a single world. A warehouse simulation might include three humanoid robots, 100 storage boxes, 20 shelving units, and a floor—all in one SDF file.

**Physics parameters**: Global physics settings like gravity magnitude (9.81 m/s² on Earth, 1.62 m/s² on the Moon), physics engine choice (ODE, DART, etc.), and simulation timestep.

**Sensor specifications with noise**: While URDF can list what sensors exist, SDF specifies their characteristics—camera resolution, field of view, LiDAR range, scan rate, and critically, noise models. Chapter 3 will cover sensor noise in detail, but SDF is where those noise parameters live.

**Plugins**: Custom behaviors that extend simulation. A plugin might simulate wind forces, implement a custom sensor, or add visualization overlays. Plugins allow users to extend Gazebo without modifying its source code.

:::tip For Software Engineers
URDF is like a JSON schema defining a data structure (the robot), while SDF is like a Docker Compose file defining an entire runtime environment (the world). URDF answers "what joints and links exist" (schema), while SDF answers "what's the complete simulation setup, including environment, initial conditions, and runtime parameters" (compose file). Just as you might define a data model in JSON Schema but deploy it within a Docker Compose environment that includes databases, networks, and volumes, you define a robot in URDF but simulate it within an SDF world that includes terrain, lighting, and physics settings.
:::

### URDF to SDF Conversion

The good news: you rarely need to write SDF files from scratch if you already have a URDF. Gazebo automatically converts URDF to SDF when loading a robot. This conversion:
- Preserves all kinematic structure (links, joints)
- Preserves visual and collision geometry
- Adds default simulation parameters where URDF lacks them
- Wraps the robot in an SDF `<model>` element that can be placed in SDF worlds

You can also manually convert using the command line: `gz sdf -p robot.urdf > robot.sdf`. This generates an SDF file equivalent to the URDF, which you can then edit to add simulation-specific features.

**Why this matters**: ROS 2 ecosystems use URDF because it's the standard for robot description across tools (visualization, planning, control). Gazebo ecosystems use SDF because it's optimized for simulation. Automatic conversion bridges these ecosystems—you maintain your robot description in URDF (standard across tools), and Gazebo converts it on-the-fly for simulation. Best of both worlds.

## ROS 2 + Gazebo Communication Flow

Gazebo simulates the robot and environment. ROS 2 runs the AI, planning, and control nodes. For a complete system, these two must communicate: ROS 2 nodes need sensor data from Gazebo, and Gazebo needs control commands from ROS 2 nodes. This section describes how that communication works.

### Conceptual Architecture

Imagine a data flow diagram with two major components connected by message streams:

**Left side: Gazebo Simulation**
- Physics engine running at 1000 Hz, computing forces and motion
- Sensor models generating camera images, LiDAR scans, IMU readings
- Motor models receiving joint commands and producing motion
- Environment model containing terrain, obstacles, lighting

**Right side: ROS 2 Graph**
- Perception nodes subscribing to sensor topics, processing images and point clouds
- Planning nodes computing desired motions based on goals
- Control nodes publishing joint commands to achieve planned motions
- Safety nodes monitoring all data and ready to trigger emergency stops

**Connecting arrows: ROS 2 Topics**
- **Gazebo → ROS 2**: Sensor data flows from simulation to ROS 2 nodes
  - `/camera/image_raw` (camera images at 30 Hz)
  - `/scan` (LiDAR point clouds at 10-40 Hz)
  - `/imu/data` (IMU readings at 100 Hz)
  - `/joint_states` (current joint positions and velocities at 100 Hz)
- **ROS 2 → Gazebo**: Control commands flow from ROS 2 nodes to simulation
  - `/joint_group_position_controller/commands` (desired joint positions)
  - `/cmd_vel` (velocity commands for mobile bases)
  - `/joint_trajectory_controller/follow_joint_trajectory` (trajectory execution)

**Clock synchronization**: A special `/clock` topic broadcasts simulation time. Since simulation might run faster or slower than real-time (depending on complexity and compute power), all ROS 2 nodes use simulation time instead of wall-clock time. This keeps everything synchronized—sensor timestamps, control deadlines, and timeouts all reference simulation time, ensuring reproducible behavior regardless of simulation speed.

### Sensor Data Flow Example

Let's trace how camera data flows from Gazebo to a vision processing node:

**1. Simulation step**: Gazebo's physics engine advances by one timestep (0.001 seconds). All objects move according to forces and constraints. The simulated humanoid's head (with attached camera) is now at a new position and orientation.

**2. Camera rendering**: The camera sensor plugin renders an image from the camera's viewpoint. It ray-traces through the 3D scene, determining what the camera sees based on object geometry, materials, and lighting. This produces a 640x480 RGB image (or whatever resolution configured).

**3. ROS 2 message creation**: The camera plugin converts the rendered image into a ROS 2 `sensor_msgs/Image` message. This message includes:
   - Pixel data (RGB values for each pixel)
   - Timestamp (simulation time when the image was captured)
   - Camera metadata (resolution, encoding format)

**4. Topic publication**: The plugin publishes this message to the `/camera/image_raw` topic, using the same pub/sub mechanism you learned about in Module 1 Chapter 2.

**5. ROS 2 node subscription**: A vision processing node (perhaps running object detection) has subscribed to `/camera/image_raw`. It receives the message via its callback function.

**6. Processing**: The vision node processes the image—runs a neural network for object detection, identifies a person in the image, and publishes detected objects to `/detected_objects` topic.

**7. Action execution**: A planning node subscribed to `/detected_objects` receives this data and decides the humanoid should wave at the detected person. It sends an action goal to the arm controller (as you learned about actions in Module 1 Chapter 2).

:::note For Beginners
This is like a relay race where information passes from runner to runner. Gazebo is the first runner, generating camera images. It hands off to the vision AI (second runner), which finds objects in the image. The vision AI hands off to the planner (third runner), which decides what to do. Finally, the planner hands off to the controller (fourth runner), which actually moves the robot's arm to wave. Each runner (component) has one job and passes results to the next. ROS 2 topics are the baton handoffs that connect the relay team.
:::

### Control Command Flow Example

Now let's trace the reverse direction—commands flowing from ROS 2 to Gazebo:

**1. High-level goal**: An action client (perhaps connected to voice commands) sends a goal: "Wave right hand."

**2. Motion planning**: A motion planning node receives this goal and computes a trajectory—a sequence of joint angles over time that produces a waving motion. For a 7-joint arm, this might be 100 waypoints with 7 joint angles each.

**3. Trajectory publication**: The planner publishes this trajectory to a trajectory controller topic: `/arm_controller/follow_joint_trajectory`.

**4. Control loop**: The trajectory controller (a ROS 2 node) reads the next waypoint every 10ms (100 Hz control rate). For each waypoint, it computes desired joint positions and velocities.

**5. Command publication**: The controller publishes these low-level commands to `/arm_controller/command` topic—a message specifying target position and velocity for each joint.

**6. Gazebo subscription**: A Gazebo plugin subscribed to `/arm_controller/command` receives these commands.

**7. Motor simulation**: The plugin applies these commands to the simulated motors. In the physics engine, motors generate torques proportional to the position error (desired minus actual). The physics engine then solves dynamics: torques → angular accelerations → velocities → positions.

**8. Feedback**: The joint states (actual positions achieved) publish to `/joint_states`, closing the feedback loop. The controller compares desired vs actual states and adjusts future commands accordingly.

This control loop runs at 100 Hz—every 0.01 seconds, the controller reads current state, computes commands, and sends them to Gazebo. This high-frequency loop is necessary for stable robot control (remember, real-time communication was one of ROS 2's key improvements over ROS 1, which you learned in Module 1).

### Cross-References to Module 1 Concepts

This communication flow directly applies concepts from Module 1:

**From Module 1 Chapter 2 (ROS 2 Communication Model)**:
- **Topics for sensor data**: Gazebo publishes camera images, LiDAR scans, and IMU data to topics. Perception nodes subscribe to these topics—exactly the pub/sub pattern you learned. Sensor data is continuous and high-frequency, making topics the right choice.
- **Actions for goal-based motion**: When commanding complex motions (wave hand, walk to location), action servers handle long-running goals with feedback. The motion example above uses actions for high-level commands (wave) and topics for low-level control (joint positions).
- **Services for occasional queries**: If a control node needs to compute inverse kinematics (convert desired end-effector position to joint angles), it calls a service. The IK solver computes once and returns joint angles—a request/response pattern perfect for services.

**From Module 1 Chapter 1 (Introduction to ROS 2)**:
- **Nodes as computational units**: Each component (vision processing, motion planning, trajectory control, Gazebo sensor plugins) runs as an independent node. This modularity means you can develop and test each component separately.
- **DDS for reliable communication**: Under the hood, ROS 2 uses DDS (Data Distribution Service) for topic communication. This ensures reliable, real-time message delivery even when running many nodes and topics simultaneously.

## Simulated Humanoid Walking Loop (Conceptual)

Let's walk through a complete control cycle for a humanoid robot taking a single step in Gazebo. This example demonstrates how perception, planning, control, and physics simulation integrate in a feedback loop.

### Initial State: Humanoid Standing

The simulated humanoid stands on flat ground, both feet planted. Gazebo's physics engine ensures the robot is in static equilibrium—gravity pulls downward, but ground reaction forces from both feet balance it. All joints are at their initial positions, motors are idle (applying just enough torque to maintain posture), and sensors are streaming initial data:

- **IMU**: Reports zero angular velocity (robot not rotating), zero linear acceleration beyond gravity, orientation indicates "upright"
- **Joint encoders**: Report current joint angles for all 20-30 joints
- **Contact sensors** (at feet): Report force magnitudes indicating weight evenly distributed between both feet
- **Camera**: Shows the forward view of the environment

ROS 2 nodes receive this sensor data via topics. A state estimator node fuses IMU and joint encoder data to estimate the robot's full pose (position, orientation, joint angles). This estimated state publishes to `/robot_state` topic.

### Step 1: Perception

The walking controller node subscribes to `/robot_state` and `/contact_sensors`. From these topics, it determines:
- Current center of mass position (computed from joint angles and link masses)
- Current base orientation (from IMU)
- Contact forces at each foot (from contact sensors)
- Whether the robot is balanced (center of mass projection falls within support polygon formed by feet)

For humanoid walking, maintaining balance is critical. If the center of mass projects outside the foot contact area, the robot will tip over. The controller continuously monitors this condition.

### Step 2: Planning

The controller's goal: take one step forward with the right foot. This requires shifting weight to the left foot (so the right foot can lift), moving the right foot forward, then setting it down and shifting weight back to a balanced stance.

The planning phase computes a trajectory—desired joint angles over time—that achieves this goal safely:

**Phase A** (0.0-0.3s): Weight shift
- Shift center of mass leftward by adjusting hip and ankle angles
- Verify contact sensors show increasing force on left foot, decreasing on right
- Wait until right foot force near zero (safe to lift)

**Phase B** (0.3-0.8s): Leg swing
- Lift right foot by flexing hip and knee joints
- Swing right leg forward by extending hip while keeping knee flexed
- Extend right knee as foot approaches ground
- Maintain balance using left leg stance and arms for counterbalance

**Phase C** (0.8-1.0s): Foot placement and weight transfer
- Lower right foot to ground
- Verify contact sensor detects touch
- Gradually shift weight back to center, loading both feet equally
- Settle into stable bilateral stance

This plan consists of waypoints: specific joint angles at specific times. For a 20-joint humanoid with 100 waypoints over 1 second, that's 2,000 numbers (20 joints × 100 timesteps).

### Step 3: Control

A trajectory controller node receives the planned waypoints and executes them. At 100 Hz (every 0.01 seconds), it:

**Reads current state** from `/joint_states` topic (actual joint positions)

**Computes error** between desired position (from trajectory) and actual position

**Calculates control commands** using a control law (PID control is common):
- Proportional term: Correct based on current error
- Integral term: Correct for accumulated past errors
- Derivative term: Dampen oscillations

**Publishes commands** to `/joint_group_position_controller/commands` topic

Each command specifies target positions or torques for all joints. The controller adjusts these commands continuously based on feedback—if the right leg isn't lifting fast enough, increase hip flexion torque; if the robot tilts left, adjust ankle torques for balance.

### Step 4: Actuation

Gazebo plugins subscribed to control command topics receive these joint commands. For each joint:

**Motor model computes torque** based on position error (desired - actual) and velocity error

**Physics engine applies torque** to the joint in its dynamics simulation

**Joint moves** according to dynamics: torque / inertia = angular acceleration → integration → velocity → position

**New joint position feeds back** to `/joint_states` topic, closing the loop

The physics engine also simulates:
- **Gravity** pulling the robot downward continuously
- **Ground contact forces** when the foot touches down (Phase C)
- **Friction** between foot and ground preventing slipping
- **Center of mass motion** as the robot's weight distribution shifts
- **Gyroscopic effects** from moving limbs (like how swinging arms helps balance)

All of this happens in a single simulation timestep (0.001 seconds). The physics engine repeats this 1,000 times per second, ensuring smooth, accurate motion.

### Step 5: Feedback

At every timestep, sensors publish updated data:

**Joint encoders** report new positions: right hip angle now 25°, knee angle 40°, etc.

**IMU** reports new orientation: robot tilting slightly left (as expected during weight shift), angular velocity indicates ongoing rotation

**Contact sensors** report changing forces: left foot force increasing (weight shifting left), right foot force decreasing, then zero (foot lifted), then increasing again (foot planted)

**Camera** shows scene from new viewpoint as robot's head moves with body motion

These sensor readings flow to ROS 2 nodes via topics. The state estimator updates its internal model. The trajectory controller compares actual vs desired progress. Safety monitors check if the robot is deviating dangerously from the plan.

**If all goes well**: The trajectory controller continues through all waypoints. After 1 second, the robot has completed one step forward and stands balanced again. Success!

**If something goes wrong** (foot slips, unexpected obstacle): The controller detects anomalies via sensor feedback. It might execute a recovery motion (widen stance for stability) or trigger an emergency stop (if tipping irrecoverably).

### The Cycle Repeats

This entire cycle—perception, planning, control, actuation, feedback—repeats continuously at 100 Hz. For walking, the controller plans the next step while executing the current one. For manipulation, it adjusts grip force while monitoring tactile sensors. The tight feedback loop is what enables humanoid robots to maintain balance despite external disturbances and model uncertainties.

:::info For Robotics Students
This walking loop demonstrates closed-loop control with multiple feedback signals. The system is dynamically stable: small deviations from the desired trajectory (due to physics approximation errors, motor delays, or external disturbances) are continuously corrected via feedback. Compare this to open-loop control, where you'd send a sequence of joint commands without sensor feedback—any deviation would compound over time, causing the robot to drift from the desired path or lose balance.

The feedback loop also addresses model uncertainty. The planner uses an approximate model of robot dynamics (mass distribution, friction coefficients), but the real simulated robot (and eventually the physical robot) has slightly different parameters. Feedback compensates for these model errors: if the actual center of mass differs from predicted, the controller detects this via IMU and contact sensors and adjusts torques accordingly. This robustness to model errors is why feedback control is essential for real-world robotics.
:::

## Typical Simulation Pipeline for Humanoids

With an understanding of what Gazebo simulates and how it integrates with ROS 2, let's examine the typical workflow for developing a humanoid robot using simulation.

### The Development Workflow

**Step 1: Design Robot in CAD**

Mechanical engineers design the robot's physical structure in CAD software (SolidWorks, Fusion 360, Onshape). They specify dimensions, select materials, calculate masses, and determine joint types. CAD tools can export 3D meshes and assembly structures.

**Step 2: Export to URDF**

CAD assemblies convert to URDF using automated tools. These tools extract:
- Links (rigid body parts) with visual meshes, collision geometry, and inertial properties
- Joints connecting links with types (revolute, prismatic), axes, and limits
- Sensor mounting locations (where cameras, LiDAR, IMUs attach)

The URDF file now describes the complete robot structure. Engineers can load this into RViz (ROS 2's visualization tool) to verify the model looks correct—joint limits are reasonable, link masses are plausible, and sensors are positioned appropriately.

**Step 3: Load into Gazebo and Test Physics**

The URDF loads into Gazebo (converted automatically to SDF). Initial tests check basic physics:
- Does the robot stand without collapsing?
- Do joint limits prevent impossible configurations?
- Is the center of mass positioned where expected?
- Can motors generate enough torque for basic motions?

Engineers often discover issues at this stage: links are too heavy, joints have insufficient range of motion, collision geometry causes self-collisions. They iterate—adjust CAD, re-export URDF, re-test—until the design is physically sound.

**Step 4: Add Sensors and Test Perception**

With basic physics working, engineers add sensors (cameras, LiDAR, IMU) to the URDF. In Gazebo, they test sensor data quality:
- Does the camera field of view cover relevant areas?
- Is LiDAR range sufficient for the robot's intended environment?
- Do IMU readings match expected values during motion?

Perception algorithms (object detection, SLAM, pose estimation) run using these simulated sensors. If perception performs poorly, engineers adjust sensor placement, resolution, or field of view without rebuilding any physical hardware.

**Step 5: Implement Controllers and Test Behaviors**

Control engineers develop motion controllers (walking, balance, manipulation) using the sensor data. They implement ROS 2 nodes that subscribe to sensor topics and publish control commands. Behaviors are tested extensively in simulation:
- Can the robot walk on flat ground without falling?
- Does it recover from pushes (external disturbances)?
- Can it navigate around obstacles using LiDAR?
- Does manipulation succeed for various object shapes?

Thousands of test scenarios run automatically. Controllers iterate rapidly—adjust parameters, re-run tests, analyze failures. Simulation's instant reset makes this iteration fast.

**Step 6: Transfer to Physical Hardware**

Once simulation validates the robot design and control algorithms, physical prototyping begins. Manufacturing produces parts, assembly constructs the robot, and engineers install electronics and sensors.

The same ROS 2 control code runs on physical hardware (changing only the sensor and actuator interfaces from Gazebo topics to real drivers). Initial physical tests validate sim-to-real transfer. Discrepancies inform further tuning: adjust friction coefficients in simulation to match real surfaces, adjust motor models to match real actuator performance, adjust sensor noise models to match real sensor characteristics.

**Step 7: Iterate**

Physical testing reveals new challenges simulation didn't capture. Engineers refine the simulation to include these effects, train new controllers in improved simulation, then test again on hardware. This cycle continues throughout development.

:::tip For Software Engineers
This workflow mirrors modern web development: design in Figma (CAD for robots), implement locally with mock data (simulation), test extensively with integration tests (thousands of simulation scenarios), deploy to staging (physical prototype), validate in production (real environment), then instrument and refine based on telemetry (feedback from physical testing). Just as you'd never deploy a new web service directly to production without staging tests, you'd never deploy a humanoid robot design directly to hardware without simulation validation. The intermediate testing layer catches 95% of issues before they reach the expensive final stage.
:::

### Tuning for Realism vs Speed

One key decision in simulation: prioritize realism or speed?

**Realism-focused configuration** (for final validation):
- Small physics timestep (0.0001s) for accurate dynamics
- High-resolution contact models with detailed friction
- Precise collision detection using full robot meshes
- Sensor noise and dynamics modeled accurately
- **Result**: Runs slower than real-time, but behaviors transfer reliably to hardware

**Speed-focused configuration** (for reinforcement learning):
- Large physics timestep (0.001s) still captures essential dynamics
- Simplified contact models (point contacts)
- Coarse collision detection (bounding boxes)
- Minimal rendering (no detailed graphics)
- **Result**: Runs 10-100x faster than real-time, enabling millions of training examples per day

Most projects use both: train policies quickly with speed-focused simulation, then validate with realism-focused simulation before hardware testing. This gives the best of both worlds—rapid iteration and reliable transfer.

## Summary

This chapter explored how Gazebo simulates physics, robot models, and behavior, and how it integrates with ROS 2 for humanoid robotics development.

**Key takeaways**:
- Gazebo is an open-source physics-based simulator that calculates actual forces, collisions, and sensor data, not just visualization
- Four physics engines available: ODE (default, general-purpose), Bullet (fast collisions), DART (optimized for humanoid joint chains), and Simbody (biomechanics)
- DART and Simbody use Featherstone algorithms (O(n) complexity) making them best for humanoids with 20-30 joints
- URDF describes robot structure (links, joints, sensors) in a ROS-native format; SDF describes complete simulation worlds (robots, environments, physics parameters) in Gazebo's native format
- Gazebo automatically converts URDF to SDF, allowing ROS 2 ecosystems to maintain robot descriptions in URDF while simulating in Gazebo
- ROS 2 and Gazebo communicate via topics: sensor data flows from Gazebo to ROS 2 (cameras, LiDAR, IMU, joint states), control commands flow from ROS 2 to Gazebo (joint positions, velocities, trajectories)
- Clock synchronization ensures all ROS 2 nodes use simulation time, keeping behavior reproducible regardless of simulation speed
- A humanoid walking loop demonstrates the complete cycle: perception (read sensors) → planning (compute trajectory) → control (execute with feedback) → actuation (physics simulation) → feedback (new sensor readings)
- Development workflow: Design in CAD → Export to URDF → Test physics in Gazebo → Add sensors → Develop controllers → Transfer to hardware → Iterate
- Trade-off: realism (slow, accurate) vs speed (fast, approximate); most projects use both configurations at different development stages

**Next**: Chapter 3 explores how virtual sensors (cameras, LiDAR, IMUs) are simulated with realistic noise, how environmental factors affect perception, and how to bridge the sim-to-real gap for robust Physical AI systems.

## Further Reading

- [Gazebo Official Documentation](https://gazebosim.org/docs)
- [Gazebo: Four Physics Engines Explained](https://classic.gazebosim.org/blog/four_physics)
- [URDF in Gazebo Tutorial](https://classic.gazebosim.org/tutorials/?tut=ros_urdf)
- [ROS 2 and Gazebo Integration Guide](https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Gazebo.html)
- [Understanding Robot Model Formats](https://articulatedrobotics.xyz/tutorials/ready-for-ros/urdf/)
- [Featherstone's Articulated Body Algorithm (Research Paper)](https://royfeatherstone.org/spatial/)
