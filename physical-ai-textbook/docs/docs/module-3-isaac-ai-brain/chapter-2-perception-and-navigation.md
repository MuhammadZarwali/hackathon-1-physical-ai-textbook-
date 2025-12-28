---
sidebar_position: 2
title: "Chapter 2: Perception and Navigation"
description: "Master how robots perceive their environment through Visual SLAM, plan paths through complex spaces, and navigate autonomously using GPU-accelerated perception pipelines"
keywords: ["perception", "visual-slam", "navigation", "isaac-ros", "nav2", "costmap", "path-planning"]
module: "module-3-isaac-ai-brain"
chapter_id: "chapter-2-perception-and-navigation"
learning_objectives:
  - "Explain how robots perceive environments through cameras, depth sensors, LiDAR, and IMUs"
  - "Describe Visual SLAM as simultaneous mapping and localization using camera data"
  - "Understand navigation as a pipeline: perception → mapping → planning → obstacle avoidance → motion"
  - "Compare CPU-based vs GPU-accelerated perception performance for real-time robotics"
prerequisites: ["Chapter 1: Introduction to NVIDIA Isaac", "Module 1: ROS 2 Communication Model", "Module 2: Sensor Simulation"]
difficulty: "intermediate"
estimated_reading_time: 30
persona_relevance:
  beginner: 4
  software_engineer: 5
  robotics_student: 5
  ai_researcher: 4
isaac_concepts: ["visual-slam", "perception-pipeline", "navigation", "isaac-ros", "nav2", "costmap"]
verified_against: "https://navigation.ros.org/"
last_verified: "2025-12-26"
---

# Chapter 2: Perception and Navigation

## Learning Objectives

By the end of this chapter, you will:
- Explain how robots perceive environments through cameras, depth sensors, LiDAR, and IMUs
- Describe Visual SLAM as simultaneous mapping and localization using camera data
- Understand navigation as a pipeline: perception → mapping → planning → obstacle avoidance → motion
- Compare CPU-based vs GPU-accelerated perception performance for real-time robotics

## Robot Perception Fundamentals

Perception is how robots understand their surroundings. Unlike humans who integrate vision, hearing, touch, and proprioception effortlessly, robots must explicitly process sensor data to build an internal representation of the world. This representation—where am I, what objects are nearby, what's the layout—drives all subsequent decisions: where to move, what to grasp, how to avoid obstacles.

In Module 2 Chapter 3, you learned about individual sensor types (cameras, LiDAR, IMU) and their simulation. This chapter focuses on how robots use these sensors together for perception—the process of converting raw sensor data into actionable understanding.

**The perception challenge**: Raw sensor data is enormous and low-level. A single 1920x1080 RGB image contains 2,073,600 pixels (width × height) with 3 color values each—over 6 million numbers. A robot receives 30 of these images per second from each camera (some robots have 5-10 cameras). Processing this flood of data to answer high-level questions ("Is there a person in front of me?" "Where is the doorway?" "Am I about to collide with furniture?") requires sophisticated algorithms and significant computational power.

**Sensor suite for perception**:

| Sensor Type | Data Provided | Update Rate | Range | Key Use |
|-------------|---------------|-------------|-------|---------|
| **RGB Camera** | Color images | 30-60 Hz | 1-50m visual | Object detection, scene understanding, visual features |
| **Depth Camera** | Distance per pixel | 30-60 Hz | 0.5-5m | Nearby obstacle detection, 3D reconstruction |
| **LiDAR** | 3D point clouds | 5-40 Hz | 0.1-100m | Long-range mapping, SLAM, terrain analysis |
| **IMU** | Orientation, acceleration | 100-1000 Hz | N/A (internal) | Balance, motion tracking, sensor fusion |

**Why multiple sensors**: Each sensor has blind spots or failure modes. Cameras fail in darkness or glare. Depth cameras fail outdoors (sunlight overwhelms infrared). LiDAR can't detect transparent surfaces. IMUs drift over time. Using all four together—sensor fusion—compensates for individual weaknesses and provides robust perception across varied conditions.

:::note For Beginners
Robot perception is like how you navigate a dark room with a flashlight, your hands touching walls, and your inner ear tracking balance. The flashlight (camera) shows what's ahead, your hands (depth sensor, LiDAR) feel nearby obstacles, and your inner ear (IMU) knows if you're tilting or turning. Your brain fuses all these senses to understand where you are and where to step next. Robots do the same thing, just using cameras, depth sensors, LiDAR, and IMUs instead of biological senses. Fusion means combining all sensor data to get a complete picture that no single sensor provides alone.
:::

## Visual SLAM Explained

SLAM—Simultaneous Localization and Mapping—is a foundational technique in mobile robotics. The problem: a robot in an unknown environment needs a map to navigate, but needs to know its location to build an accurate map. SLAM solves both simultaneously.

**The chicken-and-egg problem**:
- **Localization** requires a map (to determine "where am I" you need landmarks: "I'm 2 meters from that wall")
- **Mapping** requires localization (to draw accurate maps you need to know where the robot was when it observed each landmark)

**SLAM's solution**: Maintain probabilistic estimates of both the map and robot pose, updating both as new sensor data arrives. Each sensor reading slightly improves the map estimate AND the localization estimate. Over time, as the robot explores, both estimates converge to high accuracy.

**Visual SLAM (VSLAM)** uses cameras as the primary sensor. Instead of LiDAR (which directly measures distances), VSLAM extracts visual features from images (corners, edges, distinctive patterns) and tracks how these features move between frames. Feature motion reveals the robot's motion (structure from motion) and the 3D locations of landmarks.

### How Visual SLAM Works (Conceptual)

**Step 1: Feature Extraction**
The robot's camera captures an image. A feature detection algorithm (like ORB—Oriented FAST and Rotated BRIEF) finds distinctive points—corners, high-contrast edges, textured regions that are easy to recognize in future frames. A typical image yields 500-2000 features.

**Step 2: Feature Tracking**
As the robot moves, the next camera frame shows the same features from a slightly different viewpoint. The VSLAM algorithm matches features between frames: "This corner in the new image is the same corner from the previous image, just viewed from 10cm to the right."

**Step 3: Motion Estimation**
By tracking how features moved between frames, the algorithm estimates the camera's motion (and thus the robot's motion). If features moved leftward in the image, the robot moved rightward. If features grew larger, the robot moved forward. This is visual odometry—estimating motion from visual changes.

**Step 4: Map Building**
Knowing the robot's motion, the algorithm calculates the 3D positions of observed features (triangulation from multiple viewpoints). These feature positions build the map—a collection of 3D landmarks (feature points) with known locations.

**Step 5: Loop Closure**
When the robot revisits a previously mapped area, it recognizes old features. This "loop closure" corrects accumulated drift—if odometry estimated the robot moved 10 meters but loop closure shows it's back at a landmark only 9.5 meters from the start, the algorithm corrects the map and pose estimate. Loop closure is critical for long-term SLAM accuracy.

**Step 6: Optimization**
The algorithm jointly optimizes robot poses (where was the robot at each timestep) and landmark positions (where are features in 3D) to minimize errors across all observations. This is typically solved via graph optimization (GraphSLAM) or filtering (Extended Kalman Filter, particle filter).

:::info For Robotics Students
Visual SLAM is fundamentally a state estimation problem. The state includes robot pose (position, orientation) and map (landmark positions)—potentially thousands of variables. Observations (camera images with detected features) provide noisy measurements of this state. The challenge: estimate all state variables given all observations, accounting for measurement noise and motion uncertainty.

GraphSLAM formulates this as a least-squares optimization: find robot poses and landmarks that best explain observed feature positions across all frames. EKF-SLAM uses a Kalman filter to incrementally update state estimates as new observations arrive. Both approaches model uncertainty—each pose and landmark has an associated covariance matrix indicating confidence. This probabilistic framework handles sensor noise and ambiguous observations gracefully. ORB-SLAM and RTAB-Map are both graph-based, running bundle adjustment to optimize poses and landmarks.
:::

### ORB-SLAM vs RTAB-Map

Two popular Visual SLAM algorithms serve different needs:

**ORB-SLAM** (Sparse SLAM):
- Produces sparse maps (feature points only, not full 3D surfaces)
- Extremely accurate localization (best-in-class pose estimation)
- Fast (real-time on CPU, even faster on GPU)
- Supports monocular, stereo, and RGB-D cameras
- Limitation: Struggles in textureless environments (blank walls, uniform floors) with few features

**RTAB-Map** (Dense SLAM):
- Produces dense 3D point clouds (full environmental geometry)
- Optimized for large-scale, long-term operation with loop closure
- More robust in feature-limited environments
- Supports stereo and RGB-D (not monocular)
- More computationally intensive than sparse SLAM

**Which to use**: Navigation benefits from sparse maps (ORB-SLAM)—knowing where walls and obstacles are is sufficient for path planning. 3D reconstruction or manipulation benefits from dense maps (RTAB-Map)—grasping objects requires knowing their full 3D shape, not just feature points.

## Navigation as a Decision Pipeline

Once a robot perceives its environment (where am I, what's around me), navigation answers: how do I get from here to my goal safely and efficiently? This requires a multi-stage pipeline that transforms high-level goals ("go to the kitchen") into low-level motor commands ("rotate wheels at 0.5 m/s forward, 0.1 rad/s turning").

The standard navigation pipeline in ROS 2 uses Nav2—the Navigation 2 stack. Nav2 provides a complete framework for autonomous mobile robot navigation, integrating perception, mapping, planning, and control.

### The Navigation Pipeline (End-to-End)

**Input**: Goal pose (target position and orientation)
**Output**: Motion commands (linear velocity, angular velocity)
**Process**: Multiple stages transform goal to motion

**Stage 1: Perception**
Sensors capture environmental data:
- Cameras provide images for Visual SLAM
- LiDAR scans measure obstacle distances
- Depth cameras detect nearby objects
- IMU tracks robot orientation and motion

Recall from Module 1 that sensors publish data to ROS 2 topics. As you learned in Module 1 Chapter 2, topics enable high-frequency sensor data streaming—cameras publish at 30 Hz, LiDAR at 10-40 Hz, IMUs at 100-1000 Hz.

**Stage 2: Mapping and Localization (SLAM)**
A SLAM node subscribes to sensor topics and processes the data:
- Builds or updates a map of the environment (walls, obstacles, open space)
- Estimates robot pose within that map (position and orientation)
- Publishes map data to `/map` topic
- Publishes pose estimate to `/amcl_pose` topic (AMCL = Adaptive Monte Carlo Localization)

This is the Visual SLAM from the previous section, running continuously as the robot explores or navigates.

**Stage 3: Costmap Generation**
The costmap is a 2D grid representation of navigable space. Each grid cell has a cost:
- **0 (free)**: Safe to traverse
- **255 (lethal)**: Obstacle present (collision if robot enters this cell)
- **1-254 (inflated)**: Near obstacle (higher cost discourages robot from passing too close)

Nav2 maintains two costmaps:
- **Global costmap**: Covers the full mapped area, used for long-range path planning
- **Local costmap**: Covers only nearby area (5-10m radius), updated at high frequency for obstacle avoidance

Costmaps combine multiple layers:
- Static map layer (from SLAM)
- Obstacle layer (recent sensor scans showing dynamic obstacles like people)
- Inflation layer (adds safety buffer around all obstacles based on robot size)

**Stage 4: Global Path Planning**
Given the goal pose and global costmap, the global planner computes an optimal path from current position to goal. Algorithms include:
- **Hybrid A***: Grid-based search accounting for robot kinematics (can't turn instantly)
- **Smac Planner**: State-lattice planner for complex constraints
- **Dijkstra**: Simple shortest-path algorithm (baseline)

The output: a sequence of waypoints from start to goal that avoids known obstacles and minimizes path length (or travel time, or energy consumption, depending on cost function).

**Stage 5: Local Planning and Obstacle Avoidance**
The global path assumes static obstacles. Reality includes dynamic obstacles (people walking, doors opening). The local planner adapts the global path in real time based on the local costmap (which updates continuously with recent sensor data).

Local planning algorithms:
- **DWA (Dynamic Window Approach)**: Samples velocity commands, simulates trajectories forward, chooses best (collision-free, goal-directed)
- **TEB (Timed Elastic Band)**: Optimizes trajectory considering time and dynamics
- **MPPI (Model Predictive Path Integral)**: Samples many possible trajectories, weights by cost, generates control from weighted average

The local planner publishes velocity commands (`/cmd_vel` topic) at 10-20 Hz—frequently enough to react to moving obstacles but not so fast that planning becomes computationally expensive.

**Stage 6: Motion Execution**
A motor controller node subscribes to `/cmd_vel` and translates velocity commands to wheel motors (for wheeled robots) or leg joints (for humanoids). As you learned in Module 1, this controller uses the same ROS 2 topics and feedback loops we've discussed throughout the textbook.

**The complete loop**: Sensors → SLAM → Costmap → Global Plan → Local Plan → Motion Commands → Robot Moves → Sensors (repeat at 10-20 Hz).

:::tip For Software Engineers
This navigation pipeline is analogous to how distributed systems handle requests with multiple processing stages. Perception is like an API gateway receiving requests (sensor data), SLAM is like a caching layer maintaining state (the map), global planning is like route planning in a microservices mesh (find the service path), local planning is like load balancing with circuit breakers (avoid overloaded services / obstacles), and motion execution is like the final service handler. Each stage processes data, adds value, and passes results to the next. Like any good distributed system, failure in one stage doesn't crash the whole pipeline—recovery behaviors handle errors gracefully.
:::

## Isaac ROS: GPU-Accelerated Perception

Everything described so far—Visual SLAM, costmaps, path planning—can run on CPUs using standard ROS 2 packages. So why does Isaac ROS matter? The answer: real-time performance at high resolutions with complex AI models.

### The Performance Problem

Standard CPU-based perception bottlenecks at high frame rates and resolutions:

**Object detection** (CPU):
- Small model (MobileNet-SSD): 50-100ms per 640x480 image → 10-20 FPS max
- Large model (Faster R-CNN): 500-1000ms per image → 1-2 FPS max

**Stereo depth estimation** (CPU):
- 640x480 stereo pair: 100-200ms → 5-10 FPS max
- 1920x1080 stereo pair: 500ms+ → &lt;2 FPS

**Visual SLAM** (CPU):
- Feature extraction + matching: 30-50ms per frame
- Loop closure detection: 100-500ms when checking large map
- Combined: 10-30 FPS achievable but unstable

These frame rates are marginal for control loops that benefit from 30-60 Hz perception updates. A robot navigating at 1 m/s with 10 FPS perception only gets new obstacle data every 10cm of travel—potentially too late to react to suddenly appearing obstacles (person stepping into path, door closing).

### GPU Acceleration Impact

**Object detection** (GPU via Isaac ROS):
- Small model: 5-10ms per image → 100-200 FPS
- Large model (YOLO, Faster R-CNN): 20-40ms → 25-50 FPS

**Stereo depth estimation** (GPU):
- 640x480: 5-15ms → 60-200 FPS
- 1920x1080: 15-30ms → 30-60 FPS

**Visual SLAM** (GPU via Isaac Elbrus):
- Feature extraction + matching: 3-8ms per frame
- Full VSLAM pipeline: 60-120 FPS possible

**Speedup**: 10-50x faster than CPU for most perception tasks.

**Why this matters**: At 60 FPS perception, a robot navigating at 1 m/s gets new obstacle data every 1.6cm of travel. The robot can react to suddenly appearing obstacles almost instantly, enabling safe navigation in dynamic human environments. High frame rates also smooth control—perception feeds planning feeds control at high frequency, reducing jerky motions and improving stability.

| Perception Task | CPU Performance | GPU Performance | Speedup | Impact |
|-----------------|-----------------|-----------------|---------|--------|
| Object Detection (YOLO) | 10-20 FPS | 100-200 FPS | 10-20x | Real-time multi-object tracking |
| Stereo Depth | 5-10 FPS | 60-120 FPS | 12-24x | Smooth obstacle avoidance |
| Visual SLAM | 10-30 FPS | 60-120 FPS | 4-12x | Stable real-time mapping |
| Semantic Segmentation | 2-5 FPS | 30-60 FPS | 15-30x | Dense scene understanding |

:::info For Robotics Students
The control frequency matters for stability. Classical control theory teaches that feedback loops require sampling at 10-100x the system bandwidth for stable operation. For a humanoid walking at 2 steps/second (0.5 Hz), perception should ideally run at 5-50 Hz minimum. For manipulation tasks with faster dynamics (reaching at 1 m/s), perception should run at 30-60 Hz. GPU acceleration makes these frame rates feasible with modern AI models, enabling closed-loop perception-control that would be impossible on CPUs. This is why companies building production robots (Boston Dynamics, Tesla) invest in GPU-accelerated perception—it's not optional for real-time Physical AI, it's mandatory.
:::

### Isaac ROS Packages and NITROS

Isaac ROS provides GPU-accelerated versions of common perception tasks. These packages integrate with standard ROS 2—they publish and subscribe to the same topics as CPU-based packages, but process data on GPU for massive speedup.

**Key Isaac ROS packages**:

**Isaac ROS Visual SLAM**: Implements stereo visual-inertial odometry (estimating robot motion from cameras + IMU) using the Isaac Elbrus GPU-accelerated library. Provides real-time SLAM at 60+ FPS, publishing map and pose estimates to standard ROS 2 topics (`/map`, `/visual_slam/tracking/odometry`).

**Isaac ROS AprilTag**: Detects fiducial markers (AprilTags—printed patterns used for localization) and estimates their 3D pose. GPU acceleration provides 10-50x speedup over CPU-based AprilTag detection, enabling detection of many tags simultaneously at high frame rates (useful for warehouse robots that use ceiling-mounted tags for localization).

**Isaac ROS Image Pipeline**: GPU-accelerated versions of standard image processing (debayering, rectification, resizing, format conversion). These are the preprocessing steps before AI inference—converting raw camera data to formats neural networks expect. On CPU, preprocessing can take 20-50ms and bottleneck perception. On GPU, it takes 2-5ms and becomes negligible.

**NITROS (NVIDIA Isaac Transport for ROS)**: Standard ROS 2 copies data between nodes through shared memory (CPU RAM). For perception pipelines where data flows through multiple nodes (camera → debayer → rectify → resize → object detection → tracking), each copy adds latency and uses memory bandwidth. NITROS optimizes this by:
- Enabling zero-copy GPU-to-GPU transfer (data stays in GPU memory throughout pipeline)
- Type negotiation (nodes agree on optimal message formats to minimize conversions)
- Reduced latency (eliminating CPU-GPU copies saves milliseconds per step)

Result: Multi-stage perception pipelines run with minimal latency overhead. Data enters the GPU at the camera driver, processes through multiple GPU-accelerated nodes, and exits as high-level perception (detected objects, SLAM pose, semantic map) ready for planning nodes.

## Autonomous Indoor Navigation (Conceptual Example)

Let's walk through a complete navigation scenario showing how all components—perception, SLAM, planning, Isaac ROS acceleration—integrate into a functioning autonomous system.

**Scenario**: A service robot in a hospital receives a goal: "Navigate from current location (nurse's station) to Room 305."

### Phase 1: Initialization

The robot starts at a known location (nurse's station) in a pre-existing map of the hospital. It has:
- A 2D occupancy grid map (from prior SLAM) showing hallways, rooms, walls
- Initial pose estimate (x, y, orientation) within this map
- Goal location (Room 305 position on the map)

Sensors are streaming data:
- Front-facing camera publishing to `/camera/image` at 30 FPS
- Depth camera publishing to `/depth/image` at 30 FPS
- 360-degree LiDAR publishing to `/scan` at 10 Hz
- IMU publishing to `/imu/data` at 100 Hz

### Phase 2: Perception and Localization

**Isaac ROS Visual SLAM** node subscribes to `/camera/image` and `/imu/data`. It:
- Extracts visual features from camera images (corners, edges, textures)
- Tracks features between frames to estimate robot motion (visual odometry)
- Matches current features against the pre-existing map (relocalization)
- Fuses visual odometry with IMU data for robust pose estimation
- Publishes updated pose to `/visual_slam/tracking/odometry` at 60 FPS (GPU acceleration enables high rate)

**Localization accuracy**: By matching observed features against the map, Visual SLAM localizes the robot to within 5-10cm accuracy—sufficient for navigating hallways and entering rooms.

### Phase 3: Costmap Update

**Nav2 costmap node** subscribes to:
- `/scan` (LiDAR data showing nearby obstacles)
- `/depth/image` (depth camera for close-range obstacles)
- `/map` (global map from SLAM)

It generates two costmaps:

**Global costmap**: Covers the entire hospital map (50m x 50m). Marks:
- Walls as lethal obstacles (cost = 255)
- Known furniture as lethal
- Inflation around all obstacles (cost decreases with distance)
- Free space as traversable (cost = 0)

**Local costmap**: Covers just 5m radius around robot. Marks:
- Recent LiDAR detections (people walking, medical carts, temporary obstacles)
- Depth camera obstacles (very close objects)
- Inflation around all obstacles
- Updates at 10 Hz (as new sensor scans arrive)

The local costmap captures dynamic obstacles not in the static map—critical for safety in hospitals where people frequently walk the hallways.

### Phase 4: Global Path Planning

**Nav2 global planner** receives:
- Current pose (from Visual SLAM)
- Goal pose (Room 305)
- Global costmap (hospital map with obstacles)

It computes an optimal path using Hybrid A* algorithm:
1. Search from current position toward goal
2. Avoid all lethal obstacles (walls, furniture)
3. Minimize path length while staying in free space
4. Account for robot's turning radius (can't rotate in place, need smooth turns)

Output: Sequence of waypoints from nurse's station to Room 305, perhaps 50 waypoints over 30 meters of hallway distance.

This global plan publishes once (or re-plans if goal changes or robot deviates significantly).

### Phase 5: Local Planning and Obstacle Avoidance

**Nav2 local planner** (also called controller) receives:
- Global path (waypoints to follow)
- Current pose and velocity
- Local costmap (dynamic obstacles)

At 20 Hz, it:
1. Samples possible velocity commands (speed + turning rate combinations)
2. Simulates forward: "If I drive at 0.8 m/s straight, where will I be in 0.5 seconds?"
3. Evaluates each simulated trajectory:
   - Does it hit obstacles in local costmap? (reject if yes)
   - Does it progress toward next waypoint? (prefer trajectories that follow global plan)
   - Is it smooth and comfortable? (prefer gentle accelerations)
4. Chooses best velocity command
5. Publishes to `/cmd_vel` topic

The local planner runs continuously, reacting to dynamic obstacles. If a person steps into the hallway, the local costmap updates (new obstacle), and the local planner chooses a velocity command that avoids the person—perhaps slowing down, or slightly deviating from the global path.

### Phase 6: Motion Execution

A motor controller subscribes to `/cmd_vel` and translates velocity commands to wheel motor commands (or leg joint commands for humanoid walkers). The robot moves according to these commands. As it moves:
- Visual SLAM updates pose estimate (robot moved 10cm forward)
- LiDAR detects new obstacles (people, carts)
- Costmap updates with new obstacle information
- Local planner adjusts `/cmd_vel` to avoid obstacles and follow the path
- Cycle repeats at 20 Hz until the robot reaches Room 305

### Success: Goal Reached

When the robot's pose estimate (from Visual SLAM) matches the goal pose within tolerance (position within 0.2m, orientation within 10 degrees), Nav2 declares success. The robot stops at Room 305, ready for its next task (deliver medication, transport equipment, etc.).

:::tip For Software Engineers
This pipeline is a classic event-driven architecture. Sensors publish events (new images, new scans) to topics. Perception nodes consume events and publish derived events (poses, maps, detected obstacles). Planning nodes consume perception events and publish control events (velocity commands). Each component is loosely coupled—upgrading the Visual SLAM algorithm doesn't affect the local planner, as long as pose estimates still publish to the same topic. This is microservices architecture applied to robotics: independent services (nodes) communicating via message bus (ROS 2 topics), with each service doing one thing well and the composition delivering complex emergent behavior (autonomous navigation).
:::

## Summary

This chapter explored how robots perceive their environment and navigate autonomously using Visual SLAM, Nav2, and GPU-accelerated perception via Isaac ROS.

**Key takeaways**:
- Robot perception combines multiple sensors (cameras, depth, LiDAR, IMU) to build robust environmental understanding despite individual sensor limitations
- Visual SLAM solves simultaneous localization and mapping: use camera images to estimate both robot motion and environmental structure (3D landmarks)
- ORB-SLAM produces sparse maps with high localization accuracy; RTAB-Map produces dense 3D maps robust to feature-limited environments
- Navigation is a multi-stage pipeline: Perception → SLAM (mapping/localization) → Costmaps (grid representation) → Global Planning (waypoint path) → Local Planning (obstacle avoidance) → Motion Commands
- Nav2 provides the complete ROS 2 navigation stack with global and local planners, costmap generation, and recovery behaviors coordinated via Behavior Trees
- GPU acceleration via Isaac ROS enables 10-50x faster perception: object detection at 100+ FPS, stereo depth at 60+ FPS, Visual SLAM at 60+ FPS
- NITROS optimizes ROS 2 data flow with zero-copy GPU-to-GPU transfer, reducing latency in multi-stage perception pipelines
- Costmaps bridge perception and planning: convert sensor data (point clouds, images) to grid representation (free vs obstacle) that planning algorithms use
- High perception frame rates (30-60 FPS) enable smooth real-time control and fast reaction to dynamic obstacles (people, moving objects)
- Isaac ROS packages are drop-in replacements for standard ROS 2 perception—same topics, same interfaces, but GPU-accelerated execution

**Next**: Chapter 3 addresses the critical challenge of deploying simulation-trained AI to real robots: understanding the sim-to-real gap, using domain randomization to bridge it, and deploying AI to edge devices (Jetson) with limited compute and power budgets.

## Further Reading

- [Nav2 Official Documentation](https://navigation.ros.org/)
- [Visual SLAM Technology Review](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2024.1347985/full)
- [Nav2 Costmap Configuration](https://docs.nav2.org/configuration/packages/configuring-costmaps.html)
- [Isaac ROS Developer Page](https://developer.nvidia.com/isaac/ros)
- [ORB-SLAM3 Official Repository](https://github.com/UZ-SLAMLab/ORB_SLAM3)
- [RTAB-Map Documentation](http://introlab.github.io/rtabmap/)
- [Nav2 Behavior Trees Guide](https://navigation.ros.org/behavior_trees/index.html)
