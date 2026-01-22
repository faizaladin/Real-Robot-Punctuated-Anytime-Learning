# Punctuated Anytime Learning on a Real Robot
### This repository implements **Punctuated Anytime Learning (PAL)** to teach a 4-wheeled real-world robot how to effectively cover an area using a **Cyclic Genetic Algorithm (CGA)**.

![Image Header](assets/header_image.png)

### The robot uses an offboard camera to track its move and help with positioning
![Camera](assets/camera_image.png)

### The system trains a robot in an offline simulation to perform a "snake" coverage pattern and periodically ("punctuates") the learning process by validating the best evolving solution on the physical robot to correct simulation biases.

![Simulation](assets/simulation_image.png)

### Additionally we have implemented a reset functiomn to have the robot return to the start position so the entire training process is human free. 

![Reset](assets/Reset.mp4)
