---
sidebar_position: 2
title: "Chapter 2: ROS 2 Communication Model"
description: "Master the communication primitives that enable robots to coordinate sensors, AI, and actuators"
keywords: ["ros2", "nodes", "topics", "services", "actions", "publish-subscribe", "communication"]
module: "module-1-ros2"
chapter_id: "chapter-2-ros2-communication-model"
learning_objectives:
  - "Explain nodes as the fundamental computational units in ROS 2 systems"
  - "Describe topics, services, and actions and when to use each primitive"
  - "Diagram sensor-to-actuator data flow using correct communication patterns"
  - "Compare publish/subscribe, request/response, and action patterns for robot tasks"
prerequisites: ["Chapter 1: Introduction to ROS 2", "understanding of processes and message passing"]
difficulty: "beginner"
estimated_reading_time: 30
persona_relevance:
  beginner: 5
  software_engineer: 5
  robotics_student: 5
  ai_researcher: 4
ros2_concepts: ["nodes", "topics", "services", "actions", "publish-subscribe", "executors", "qos"]
verified_against: "docs.ros.org/en/humble/Concepts.html"
last_verified: "2025-12-25"
---

# Chapter 2: ROS 2 Communication Model

## Learning Objectives

By the end of this chapter, you will:
- Explain nodes as the fundamental computational units in ROS 2 systems
- Describe topics, services, and actions and when to use each primitive
- Diagram sensor-to-actuator data flow using correct communication patterns
- Compare publish/subscribe, request/response, and action patterns for robot tasks

## Nodes: The Computational Units

A node is an independent process that performs a specific computation in a ROS 2 system. Each node focuses on one task: reading sensor data, running a perception algorithm, planning a path, or controlling a motor. Nodes communicate with each other through well-defined interfaces, allowing complex robot behaviors to emerge from many simple components working together.

**Why nodes matter**: Breaking a robot system into nodes provides modularity and fault isolation. If a vision node crashes, the motor control nodes can continue operating safely. Teams can develop different nodes independently, test them separately, and integrate them through standardized communication interfaces.

**Node executors**: Each node runs within an executor, which manages the node's event loop and callbacks. When a message arrives on a topic or a service is called, the executor schedules the appropriate callback function to handle it. Executors can be single-threaded (processing one event at a time) or multi-threaded (processing multiple events concurrently). This design allows ROS 2 to balance real-time responsiveness with system complexity.

**Example**: A humanoid robot might have separate nodes for:
- Camera image processing
- Object detection using a vision AI model
- Balance control using IMU data
- Arm motion planning
- Gripper control
- Speech recognition
- Safety monitoring

Each node runs independently but coordinates through ROS 2 communication.

:::note For Beginners
Think of nodes as individual apps on your phone. Each app does one thing (camera, calculator, music player), and they can share data when needed. A robot's nodes work the same way—each handles one job, and they communicate to accomplish complex tasks together.
:::

## Topics and Publish/Subscribe

Topics implement the publish/subscribe communication pattern. A topic is a named bus where nodes can publish messages or subscribe to receive messages. Publishers send data without knowing who (if anyone) is listening. Subscribers receive data without knowing who sent it. This decoupling allows flexible system architectures.

**How it works**: A node publishes a message to a topic by sending data to that topic's name (e.g., `/camera/image`). Any node subscribed to that topic receives the message. Multiple nodes can publish to the same topic, and multiple nodes can subscribe. Messages flow one-way from publishers to subscribers.

**When to use topics**: Use topics for continuous data streams like sensor readings, state updates, or status information. Topics work well when you don't need confirmation that a message was received or when one producer needs to broadcast to many consumers.

**Example - Camera to Vision Pipeline**:
```python
# Publisher (camera node)
camera_publisher = node.create_publisher(Image, '/camera/image', 10)
camera_publisher.publish(image_msg)

# Subscriber (vision node)
def image_callback(msg):
    # Process the image for object detection
    objects = detect_objects(msg)

vision_subscriber = node.create_subscription(
    Image, '/camera/image', image_callback, 10)
```

**Message delivery**: Topics operate asynchronously. The publisher sends a message and immediately continues without waiting for subscribers to process it. This enables high-frequency data streams (cameras publishing at 30 FPS, IMUs at 100 Hz) without blocking the publisher.

:::tip For Software Engineers
Topics are like message queues (RabbitMQ, Kafka) or pub/sub systems (Redis Pub/Sub). Publishers and subscribers are loosely coupled—they only need to agree on the topic name and message type. This pattern scales well for event-driven architectures and high-throughput data streams.
:::

## Services: Request/Response Communication

Services implement synchronous request/response communication. A service client sends a request to a service server and waits for a response. Unlike topics, services are bidirectional and blocking: the client pauses until it receives a reply.

**How it works**: A server node advertises a service with a specific name (e.g., `/add_two_ints`). A client node calls the service by sending a request message. The server processes the request and sends back a response message. The client receives the response and continues execution.

**When to use services**: Use services for infrequent, transactional operations that require confirmation or return computed results. Examples include configuration changes, triggering behaviors, or querying for information that requires computation.

**Example - Inverse Kinematics**:
```python
# Service server (kinematics node)
def compute_ik(request, response):
    # Calculate joint angles for desired end-effector position
    response.joint_angles = inverse_kinematics(request.target_pose)
    response.success = True
    return response

ik_service = node.create_service(
    ComputeIK, '/compute_ik', compute_ik)

# Service client (motion planner node)
client = node.create_client(ComputeIK, '/compute_ik')
request = ComputeIK.Request()
request.target_pose = desired_pose
future = client.call_async(request)
# Wait for response...
response = future.result()
```

**Blocking behavior**: Service calls block the client until the server responds or a timeout occurs. For long-running computations, this can freeze the calling node. That's why services are best for quick operations (under 100ms). For longer tasks, use actions instead.

:::note For Beginners
Services are like asking someone a question and waiting for an answer. You stop what you're doing until they respond. This works well for occasional requests but not for continuous communication or tasks that take a long time.
:::

## Actions: Long-Running Tasks with Feedback

Actions provide a communication pattern for long-running tasks that need feedback during execution and support for cancellation. An action client sends a goal to an action server, receives periodic feedback while the task runs, and gets a final result when complete.

**How it works**: Actions have three components:
1. **Goal**: The client sends a goal describing the desired outcome
2. **Feedback**: The server periodically sends progress updates while working
3. **Result**: The server sends a final result when the goal completes (or fails)

The client can cancel the goal at any time, and the server must handle cancellation gracefully.

**When to use actions**: Use actions for tasks that take significant time (seconds to minutes), where you need progress updates, or where cancellation is important. Examples include navigation to a location, grasping an object, or executing a motion plan.

**Example - Robot Arm Motion**:
```python
# Action server (arm controller node)
def execute_motion(goal_handle):
    target_position = goal_handle.request.target

    for waypoint in trajectory:
        # Move to next waypoint
        move_arm(waypoint)

        # Send feedback
        feedback = MoveArm.Feedback()
        feedback.current_position = get_current_position()
        goal_handle.publish_feedback(feedback)

        if goal_handle.is_cancel_requested:
            return MoveArm.Result(success=False)

    return MoveArm.Result(success=True)

arm_action_server = ActionServer(
    node, MoveArm, '/move_arm', execute_motion)

# Action client (task planner)
client = ActionClient(node, MoveArm, '/move_arm')
goal = MoveArm.Goal(target=desired_position)

# Send goal and receive feedback
goal_handle = client.send_goal_async(goal, feedback_callback=on_feedback)
```

**Cancellation**: If a humanoid robot is moving its arm toward an object but a safety system detects a person nearby, the action can be canceled immediately. The arm controller receives the cancellation and stops the motion safely.

:::tip For AI Researchers
Actions are similar to asynchronous job systems with progress tracking (like distributed training jobs that report epoch progress). The feedback mechanism allows monitoring without polling, and cancellation enables early stopping when conditions change.
:::

## Comparing Communication Primitives

Each communication primitive serves different use cases. Choosing the right one depends on your requirements:

| **Primitive** | **Pattern** | **Timing** | **Use When** | **Example** |
|--------------|-------------|------------|--------------|-------------|
| **Topic** | One-way, many-to-many | Asynchronous | Continuous data streams, state updates | Camera images, sensor readings, robot pose |
| **Service** | Request/response | Synchronous (blocking) | Infrequent operations needing confirmation | Configuration changes, coordinate transforms, simple queries |
| **Action** | Goal/feedback/result | Asynchronous with updates | Long-running tasks with progress | Navigation, object grasping, motion execution |

**Decision criteria**:
- **Frequency**: Topics for high-frequency (greater than 1 Hz), services for occasional (less than 1 Hz), actions for single goals
- **Duration**: Topics and services for instant operations, actions for tasks taking seconds or more
- **Feedback needed**: Actions provide progress updates; topics and services do not
- **Cancellation needed**: Only actions support cancellation
- **Confirmation needed**: Services and actions confirm completion; topics do not

:::info For Robotics Students
This mirrors control theory abstractions: topics are like open-loop sensing (continuous measurement), services are like synchronous function calls (instant computation), and actions are like closed-loop controllers (goal-driven with feedback). Choose the pattern that matches your control requirements.
:::

## Sensor-to-Brain-to-Actuator Pipeline

Physical AI systems follow a perception-decision-action cycle. Sensors provide information about the environment, AI models (the "brain") make decisions, and actuators execute movements. ROS 2 communication primitives connect these components.

**Perception (Sensors → Brain)**: Sensors publish data on topics. Camera nodes publish images, LIDAR nodes publish point clouds, IMU nodes publish orientation and acceleration. Perception nodes subscribe to these topics and process the raw data into meaningful information (detected objects, estimated poses, recognized obstacles).

**Decision (Brain)**: AI and planning nodes receive perception data and decide what to do. A vision language model might subscribe to camera images and voice commands, then publish high-level goals. A motion planner might subscribe to obstacles and target positions, then compute a safe path.

**Action (Brain → Actuators)**: Control nodes receive commands and execute them on hardware. For quick responses (emergency stop), use a topic. For calculated movements (reach this position), use an action that provides feedback and supports cancellation.

**Example flow**:
1. Camera publishes images → `/camera/image` topic
2. Vision node subscribes, detects person → publishes to `/detected_objects` topic
3. Interaction node subscribes, decides to wave → sends action goal to `/wave_gesture`
4. Arm controller executes wave motion → publishes feedback on joint positions
5. Safety node monitors all topics → can cancel action if person gets too close

This pipeline mirrors the human nervous system: sensors (eyes, touch) send signals to the brain, the brain decides actions, and motor neurons trigger muscles—all through message passing.

## Humanoid Robot Example: Camera to Motion

Consider a humanoid robot greeting a visitor. This seemingly simple task requires coordinating multiple components through ROS 2 communication.

**Scenario**: Robot detects a person approaching and waves hello.

**Communication flow**:

1. **Perception**: Camera node publishes images at 30 FPS on `/camera/rgb/image` topic (publish/subscribe)
2. **Detection**: Person detection node subscribes to images, runs ML model, publishes detected persons on `/detected_persons` topic
3. **Decision**: Interaction planner subscribes to `/detected_persons`, determines person is approaching, calls `/get_wave_trajectory` service to compute arm motion
4. **Planning**: Trajectory service computes safe wave motion, returns waypoints
5. **Execution**: Interaction planner sends action goal to `/execute_arm_motion` with wave trajectory
6. **Control**: Arm controller action server moves joints along trajectory, publishing feedback every 100ms
7. **Monitoring**: Safety node subscribes to `/arm/joint_states` and `/detected_persons`, ready to cancel action if person gets too close

**Why this design works**:
- Topics for continuous sensing (camera, joint states) enable real-time awareness
- Service for quick computation (trajectory planning) provides immediate result
- Action for motion execution allows monitoring progress and emergency cancellation
- Nodes are independent—upgrading the vision model doesn't affect arm control

This exemplifies how ROS 2 communication primitives enable complex, coordinated behaviors from simple, modular components.

:::note For Beginners
This is like a restaurant where customers (sensors) send orders to the kitchen (brain/planner), and the kitchen sends cooking instructions to the chef (actuators). Everyone communicates through a specific system—waiters (topics) carry continuous updates, the manager (services) answers questions quickly, and complex orders (actions) are tracked until complete.
:::

## Deterministic vs Non-Deterministic Communication

ROS 2 communication can be configured for different reliability and timing guarantees through Quality of Service (QoS) policies. Understanding these trade-offs is essential for building robust robot systems.

**Deterministic communication**: In safety-critical systems, messages must arrive reliably and on time. A motor controller must receive position commands within milliseconds or the robot could fall. ROS 2 supports deterministic communication through QoS settings that guarantee message delivery and limit latency.

**Non-deterministic communication**: In best-effort scenarios, occasional message loss is acceptable for performance. A camera publishing at 30 FPS can tolerate dropped frames—the next frame arrives 33ms later. Using best-effort QoS reduces network overhead and improves throughput.

**QoS policies**: ROS 2 topics can configure:
- **Reliability**: Reliable (guaranteed delivery) vs Best-Effort (may drop messages)
- **Durability**: Transient-Local (late joiners receive last message) vs Volatile (only receive new messages)
- **History**: Keep-Last (buffer N recent messages) vs Keep-All (buffer everything)
- **Deadline**: Maximum time between messages before violation detected

**Choosing QoS**:
- Sensor data (camera, LIDAR): Best-effort, volatile, keep-last (performance over reliability)
- Control commands: Reliable, volatile, keep-last with deadline (real-time guarantees)
- State updates: Reliable, transient-local, keep-last (new subscribers get current state)

Proper QoS configuration ensures robot systems balance real-time performance with reliability requirements.

:::tip For Software Engineers
QoS is similar to configuring TCP vs UDP or message queue acknowledgment modes. Reliable QoS behaves like TCP (guaranteed delivery, ordered), while best-effort QoS behaves like UDP (fast but lossy). Choose based on your application's tolerance for latency vs message loss.
:::

## Summary

This chapter introduced the ROS 2 communication model that enables robot coordination.

**Key takeaways**:
- Nodes are independent computational units that perform specific tasks and communicate through well-defined interfaces
- Topics implement publish/subscribe for continuous data streams; publishers and subscribers are decoupled
- Services implement request/response for synchronous operations that need confirmation or computed results
- Actions implement goal-based communication for long-running tasks that require feedback and cancellation
- Choose primitives based on frequency, duration, feedback needs, and cancellation requirements
- The sensor-to-brain-to-actuator pipeline uses topics for perception, services for quick computations, and actions for coordinated movements
- QoS policies configure reliability and timing guarantees to balance performance with determinism

**Next**: Chapter 3 explores how AI agents connect to ROS 2, enabling high-level reasoning and natural language interaction with robot hardware.

## Further Reading

- [ROS 2 Concepts: Topics, Services, Actions](https://docs.ros.org/en/humble/Concepts/Basic/About-Topics.html)
- [Understanding Quality of Service Settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [Executors and Callback Groups](https://docs.ros.org/en/humble/Concepts/About-Executors.html)
- [ROS 2 Design: Why Different Communication Patterns](https://design.ros2.org/articles/actions.html)
