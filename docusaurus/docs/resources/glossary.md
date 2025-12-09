---
id: glossary
title: Glossary of Terms
---

A comprehensive list of key terms and concepts from the field of Physical AI and Humanoid Robotics.

### A

**Action (A)**
In Reinforcement Learning, a decision the agent can make in its environment.

**Actuators**
The components of a robot that convert energy (usually electrical) into physical motion. The "muscles" of the robot.

**Actor-Critic**
A type of Reinforcement Learning algorithm that combines value-based and policy-based methods, using two neural networks: an "actor" to decide on actions and a "critic" to evaluate those actions.

**Agent**
In Reinforcement Learning, the learner and decision-maker (the robot).

### B

**Bellman Equation**
A fundamental equation in Reinforcement Learning used to iteratively update value estimates based on the rewards received.

**Bounding Boxes**
In computer vision, the coordinates of a rectangle enclosing a detected object.

### C

**Compliance**
The ability of a robot's joints to have some "give" or softness, rather than being perfectly stiff. Crucial for safe physical interaction.

**Computer Vision**
The field of AI that deals with how computers can gain high-level understanding from digital images or videos.

**Convolutional Neural Network (CNN)**
A specialized type of deep neural network that is the dominant architecture for modern computer vision tasks. It uses a mathematical operation called a convolution to efficiently process image data.

### D

**Denavit-Hartenberg (DH) convention**
A standard method for assigning coordinate frames to the links of a robot arm to simplify the forward kinematics calculations.

**Deep Q-Networks (DQN)**
A value-based Reinforcement Learning algorithm that uses a deep neural network to approximate the optimal Q-function, enabling Q-learning in high-dimensional state spaces.

**Discount Factor (γ)**
In Reinforcement Learning, a number between 0 and 1 that determines the present value of future rewards.

**Domain Adaptation**
A Sim2Real technique that involves training a model to translate between the simulated domain and the real-world domain (e.g., making simulated images look more realistic).

**Domain Randomization**
A Sim2Real technique where the parameters of the simulation (visuals, physics) are heavily randomized during training to force the learned policy to be more robust.

**Dynamics**
The study of motion that considers the forces and torques that cause it (the relationship between force, mass, and acceleration).

**Dynamic Stability**
The ability of a robot to maintain balance while in motion, often by constantly moving to keep its center of mass over its support polygon.

### E

**Embodied Agent**
An intelligent agent whose physical form (sensors, actuators, morphology) is an integral part of its intelligence, not just a passive vessel.

**Encoders**
Proprioceptive sensors attached to motor shafts to measure the precise angle of a joint.

**Environment**
In Reinforcement Learning, the world in which the agent exists and interacts.

**Exteroceptive Sensors**
Sensors that gather information about the environment external to the robot, such as cameras, LiDAR, and tactile sensors.

### F

**Feature Map**
In a CNN, the output of a convolutional layer, representing the detection of a specific feature across the input image.

**Force Closure**
A property of a grasp where the robot's fingers can apply forces to resist any arbitrary external force or torque on the object.

**Force-Torque Sensors**
Sensors, typically at a robot's wrist, that measure the forces and torques being applied, vital for contact-rich tasks.

**Forward Dynamics**
The study of calculating the resulting acceleration of a robot's joints given a set of applied joint torques. Used for simulation.

**Forward Kinematics**
The problem of calculating the position and orientation of a robot's end-effector given its joint angles.

**Foundation Models for Robotics**
Massive models trained on vast datasets of robotic and world data, intended to provide a general "common sense" understanding that can be fine-tuned for specific tasks.

### H

**Homogeneous Transformation Matrix**
A 4x4 matrix used in robotics to represent both a rotation and a translation in a single mathematical operation.

**Human-Robot Interaction (HRI)**
The multidisciplinary field that studies the science and design of interactions between humans and robots.

**Humanoid Locomotion**
The study of how to make bipedal robots walk, run, and navigate the world in a dynamically stable manner.

### I

**Inertial Measurement Units (IMUs)**
Sensors that provide a robot's orientation (roll, pitch, yaw) by fusing data from accelerometers, gyroscopes, and magnetometers.

**In-Hand Manipulation**
The task of adjusting an object's position and orientation within the robot's hand without putting it down.

**Instance Segmentation**
A computer vision task that identifies each object instance in an image and provides a pixel-level mask for each one.

**Inverse Dynamics**
The study of calculating the required joint torques to achieve a desired trajectory of joint positions, velocities, and accelerations. Used for control.

**Inverse Kinematics**
The problem of calculating the required joint angles to achieve a desired position and orientation for the robot's end-effector.

### K

**Kinematics**
The study of motion without considering the forces that cause it; the geometry of motion.

### L

**Lagrangian Dynamics**
A method for deriving the equations of motion for a mechanical system (like a robot) based on its kinetic and potential energy.

**Legibility**
A property of a robot's motion where its actions are easily understandable and predictable to a human observer.

**LiDAR (Light Detection and Ranging)**
A sensor that emits laser beams and measures their reflections to create a highly accurate 3D point cloud of the environment.

### M

**Manipulation**
The process of using a robotic arm or hand to interact with and change the state of objects in the environment.

**Markov Decision Process (MDP)**
The mathematical framework used to formalize Reinforcement Learning problems, consisting of states, actions, rewards, and transition probabilities.

### P

**Perception-Cognition-Action Loop**
The fundamental feedback cycle that drives all intelligent embodied agents, where the agent senses the world, thinks about it, and then acts upon it.

**Physical AI**
The convergence of AI, robotics, and sensory interaction to create intelligent agents that can perceive, reason, and act in the physical world.

**Policy (π)**
In Reinforcement Learning, the "brain" of the agent. It is a function that maps a state to an action, defining the agent's behavior.

**Policy Gradient**
A family of policy-based Reinforcement Learning algorithms that directly optimize the parameters of a policy network.

**Proprioceptive Sensors**
Sensors that measure the internal state of the robot, such as joint angles and orientation.

### Q

**Q-Function (Q(s, a))**
In Reinforcement Learning, a function that estimates the total expected future reward of taking a specific action `a` from a specific state `s` and then following a policy thereafter.

**Q-Learning**
A classic value-based Reinforcement Learning algorithm that learns the optimal Q-function iteratively.

### R

**Reality Gap**
The discrepancy between a physics simulation and the real world, which can cause policies trained in simulation to fail on a physical robot.

**Reinforcement Learning (RL)**
A paradigm of machine learning where an agent learns to make a sequence of decisions in an environment to maximize a cumulative reward.

**Reward (R)**
In Reinforcement Learning, a scalar feedback signal the agent receives from the environment that indicates how good or bad its last action was.

### S

**Semantic Segmentation**
A computer vision task that assigns a class label (e.g., "person", "road", "car") to every pixel in an image.

**Sensors**
Devices that measure a physical property and convert it into a signal that a computer can process. The "senses" of the robot.

**Shared Autonomy**
A control scheme where a robot and a human work together on a task, fluidly trading control and assisting each other.

**Sim2Real Transfer**
The subfield of robotics and RL dedicated to bridging the "reality gap" and transferring policies trained in simulation to the real world.

**Singularity**
A configuration of a robot arm where it loses one or more degrees of freedom, making certain movements impossible.

**Soft Robotics**
A subfield of robotics that focuses on building robots from compliant, flexible materials rather than rigid links.

**State (S)**
In Reinforcement Learning, a complete description of the state of the environment at a particular moment.

**Support Polygon**
The area on the ground enclosed by a robot's points of contact. For stable walking, the Zero-Moment Point must remain within this area.

**System Identification**
A Sim2Real technique that aims to make a simulation more accurate by measuring the physical properties of the real robot and tuning the simulator's parameters.

### T

**Tactile Sensors**
Sensors that give a robot a sense of touch, detecting properties like pressure and texture.

### V

**Value Function (V(s))**
In Reinforcement Learning, a function that estimates the total expected future reward an agent can get starting from a given state `s`.

### W

**Workspace**
The volume of space that a robot's end-effector can reach.

### Z

**Zero-Moment Point (ZMP)**
The point on the ground where the net moment of a robot's inertial and gravitational forces is zero. A key concept for controlling dynamically stable walking.
