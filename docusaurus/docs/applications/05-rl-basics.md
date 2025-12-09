---
id: rl-basics
title: 'Chapter 5: Reinforcement Learning Basics'
---

## Learning from Experience

How do we learn to ride a bike? No one gives us an exact mathematical model of the bicycle's dynamics or a step-by-step instruction manual. We learn through trial and error. We try something, we fall (negative feedback), we adjust, and we try again until we succeed (positive feedback). This is the core idea behind Reinforcement Learning (RL).

Reinforcement Learning is a paradigm of machine learning where an **agent** learns to make a sequence of decisions in an **environment** to maximize a cumulative **reward**. It is one of the most promising avenues for developing general-purpose, autonomous physical AI, as it allows robots to learn complex behaviors from scratch with minimal human supervision.

### The Language of RL

To understand RL, we must first learn its key concepts, which are formalized in the framework of a **Markov Decision Process (MDP)**.

-   **Agent**: The learner and decision-maker. In our case, the robot.
-   **Environment**: The world in which the agent exists and interacts.
-   **State (S)**: A complete description of the state of the environment. For a mobile robot, this might include its position, velocity, and a map of its surroundings.
-   **Action (A)**: A decision the agent can make. For example, the torques to apply to each motor.
-   **Reward (R)**: A scalar feedback signal the agent receives from the environment after taking an action in a state. The reward tells the agent how good or bad that action was. A robot might get a +1 reward for reaching a goal and a -1 for colliding with an obstacle.
-   **Policy (π)**: This is the "brain" of the agent. The policy is a function that maps a state to an action. It defines the agent's behavior. The goal of RL is to find the optimal policy, denoted π*, which maximizes the total expected reward.
-   **Value Function (V(s))**: The value function estimates the total expected future reward an agent can get starting from a given state `s` and following a specific policy. It represents how "good" it is to be in a particular state.
-   **Q-Function (Q(s, a))**: The Q-function (or state-action value function) is even more specific. It estimates the total expected future reward of taking a specific action `a` from a specific state `s` and then following the policy thereafter.

![The agent-environment interaction loop in RL](/img/placeholder.svg)
*Figure 5.1: The agent observes a state, takes an action based on its policy, and receives a reward and the next state from the environment.*

### The Goal: Maximize Expected Cumulative Reward

The agent's goal is not to maximize the immediate reward, but the sum of all rewards it will receive in the future, often called the **return** or **cumulative reward**. To prevent this sum from being infinite, we often introduce a **discount factor (γ)**, a number between 0 and 1. Rewards received further in the future are "discounted" and are worth less than immediate rewards.

`Return = R_t+1 + γ*R_t+2 + γ^2*R_t+3 + ...`

### Major Approaches to Reinforcement Learning

There are two main families of RL algorithms:

#### 1. Value-Based Methods
In value-based methods, the primary goal is to learn the value function (or Q-function) of the optimal policy. The policy itself is then implicit: in any given state, the agent simply chooses the action that leads to the state with the highest value.

A classic example is **Q-Learning**. In Q-learning, we maintain a big table (the Q-table) with an entry for every state-action pair. We update this table using the **Bellman Equation**, which iteratively refines the Q-value estimates based on the rewards received.

`Q(s, a) <- Q(s, a) + α * [R + γ * max(Q(s', a')) - Q(s, a)]`

The problem with this tabular approach is that it's infeasible for problems with large or continuous state spaces, like most of robotics. This is where deep learning comes in. In **Deep Q-Networks (DQN)**, instead of a table, we use a neural network to approximate the Q-function.

#### 2. Policy-Based Methods
In policy-based methods, we don't learn a value function. Instead, we directly optimize the policy itself. We parameterize the policy as a neural network that takes a state as input and outputs a probability distribution over the possible actions.

We then adjust the weights of this network to make "good" actions (actions that led to high rewards) more likely and "bad" actions less likely. A popular family of policy-based methods is called **Policy Gradient**.

### Actor-Critic: The Best of Both Worlds
Actor-Critic methods combine the strengths of both value-based and policy-based approaches. They use two neural networks:
-   The **Actor**: This is the policy network. It takes the state and decides which action to take.
-   The **Critic**: This is the value network (or Q-network). It evaluates the action taken by the actor by estimating the value of the resulting state.

The critic's job is to provide a better, more stable learning signal to the actor. Instead of relying on the raw, often noisy, reward from the environment, the actor learns based on the critic's "critique." This leads to more stable and efficient learning. Popular actor-critic algorithms include A2C (Advantage Actor-Critic) and A3C (Asynchronous Advantage Actor-Critic).

Reinforcement learning is a powerful but challenging tool. Designing good reward functions, ensuring stable learning, and bridging the gap between simulation and the real world (Sim2Real) are all major areas of research that we will touch on in subsequent chapters.
