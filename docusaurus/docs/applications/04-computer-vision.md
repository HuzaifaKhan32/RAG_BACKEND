---
id: computer-vision
title: 'Chapter 4: Computer Vision for Robotics'
---

## Giving Machines the Sense of Sight

Of all the senses, vision provides the richest and most dense source of information about the world. For a physical AI to operate intelligently and autonomously in unstructured environments, the ability to see and understand is not just a luxury—it's a necessity. Computer vision is the field of AI that deals with how computers can gain high-level understanding from digital images or videos.

### The Camera: The Eye of the Robot

It all starts with the sensor. Robotic vision systems use various types of cameras:

-   **Monocular Cameras**: A single camera, just like a single eye. It provides a 2D projection of the 3D world. Inferring depth (the third dimension) from a single 2D image is a classic, challenging problem in computer vision.
-   **Stereo Cameras**: Two cameras spaced a known distance apart, mimicking human binocular vision. By finding corresponding points in the two images and measuring the **disparity** (the difference in pixel location), the system can triangulate the 3D position of that point, creating a depth map.
-   **RGB-D Cameras**: These cameras provide both a standard RGB color image and a per-pixel depth (D) image. They are a game-changer for robotics. Common technologies include:
    -   **Structured Light**: Projects a known pattern of infrared light into the scene and observes how it deforms over the surfaces of objects.
    -   **Time-of-Flight (ToF)**: Emits a pulse of infrared light and measures the precise time it takes for the light to bounce back to the sensor.

### Fundamental Computer Vision Tasks for Robotics

A robot doesn't just need to *see* an image; it needs to *interpret* it. This interpretation happens through a pipeline of tasks.

#### 1. Image Classification
The most basic task: "What is in this image?" The algorithm takes an image as input and outputs a single label (e.g., "cat", "dog", "car"). While simple, it's the foundation upon which more complex tasks are built.

#### 2. Object Detection
"What objects are in this image, and where are they?" An object detection algorithm outputs a list of **bounding boxes** (the coordinates of a rectangle enclosing the object) and a class label for each box. This is critical for a robot that needs to locate and interact with specific objects.

#### 3. Semantic Segmentation
"What is the category of each pixel in this image?" Instead of just drawing a box around an object, semantic segmentation assigns a class label to every single pixel. The output is a segmentation map where all pixels belonging to "person" are one color, all pixels for "road" are another, and so on. This provides a much more detailed understanding of the scene, crucial for autonomous driving and navigation.

#### 4. Instance Segmentation
A combination of object detection and semantic segmentation. It answers: "What objects are in this image, where are they, and which pixels belong to each *instance* of an object?" If there are three people in a scene, instance segmentation will identify each person as a distinct object with its own pixel mask.

![A comparison of detection and segmentation tasks](/img/placeholder.svg)
*Figure 4.1: From left to right: Object Detection, Semantic Segmentation, and Instance Segmentation. Each provides an increasing level of scene understanding.*

### The Rise of Convolutional Neural Networks (CNNs)

Modern computer vision is dominated by a specific type of deep learning model: the **Convolutional Neural Network (CNN)**. Unlike a standard neural network, a CNN uses a mathematical operation called a **convolution**.

A convolution involves sliding a small filter (or **kernel**) over the input image. This kernel is a small matrix of weights. At each position, the kernel is multiplied with the underlying patch of the image, and the results are summed up to produce a single output pixel in a "feature map."

This architecture is powerful for two reasons:
1.  **Parameter Sharing**: The same kernel is used across the entire image, so the network doesn't need to learn a separate detector for an object in the top-left corner versus the bottom-right. This makes CNNs highly efficient.
2.  **Hierarchy of Features**: Early layers in the network learn to detect simple features like edges, corners, and colors. Deeper layers combine these simple features to detect more complex patterns like textures, parts of objects (a wheel, an eye), and eventually, whole objects.

### From Pixels to Action

For a robot, the output of a vision algorithm is rarely the final answer. It's an input to a decision-making or control process.
-   The 3D coordinates of an object from an object detector can become the target for an inverse kinematics solver.
-   A segmentation map showing the floor can be used to generate a traversable path for a mobile robot.
-   The pose of a human from a vision system can be used to predict their intent in a human-robot interaction scenario.

Vision is the bridge from the unstructured, chaotic real world to the structured, mathematical world of robotic control.
