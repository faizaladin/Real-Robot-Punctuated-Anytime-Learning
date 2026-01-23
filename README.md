# Punctuated Anytime Learning on a Real Robot

Faiz Aladin, Jim O'Connor

Connecticut College

<p align="center">
  <img src="assets/header_image.png" alt="Header Image" width="100%">
</p>

This repository implements **Punctuated Anytime Learning (PAL)** to teach a 4-wheeled real-world robot how to effectively cover an area using a **Cyclic Genetic Algorithm (CGA)**.

The system trains a robot in an offline simulation to perform a "snake" coverage pattern. It periodically "punctuates" the learning process by validating the best evolving solution on the physical robot to correct simulation biases.

---

### Vision System
The robot uses an offboard camera to track its movement and assist with positioning.

<p align="center">
  <img src="assets/camera_image.png" alt="Camera Setup" width="600">
</p>

---

### Simulation & Training
The core learning happens in an offline simulation to speed up the evolutionary process. The results are then transferred to the real robot to bridge the reality gap.

<p align="center">
  <img src="assets/simulation_image.png" alt="Simulation" width="600">
</p>

---

### Automated Reset
We have implemented a reset function to have the robot return to the start position automatically. This ensures the entire training process is end-to-end.

https://github.com/user-attachments/assets/09d8d62e-7017-4d3c-8e16-91f6aca54ca8


