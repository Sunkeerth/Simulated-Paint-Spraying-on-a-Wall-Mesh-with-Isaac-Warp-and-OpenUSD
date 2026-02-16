# 🚀 NVIDIA Warp + OpenUSD Industrial Spray Simulation

![Python](https://img.shields.io/badge/Python-3.10-blue)
![OpenUSD](https://img.shields.io/badge/OpenUSD-3D%20Visualization-green)
![NVIDIA Warp](https://img.shields.io/badge/NVIDIA-Warp-yellow)
![Simulation](https://img.shields.io/badge/Simulation-Physics%20Based-orange)
![Status](https://img.shields.io/badge/Status-Research%20Project-success)

A **research-oriented physics-based industrial spray painting simulation** built using **NVIDIA Isaac Warp** and **Pixar OpenUSD** to model real-world robotic coating workflows and visualize paint accumulation on a 3D wall surface.

---

# 🎯 Project Overview

This project simulates an **industrial spray painting process** where a moving nozzle emits paint particles in a triangular fan pattern and gradually coats a wall surface.

The simulation includes:

- Spray particle emission physics  
- Paint accumulation over time  
- Animated nozzle motion  
- Real-time texture updates  
- OpenUSD 3D visualization  

The final output is visualized using **Pixar usdview**.

---

# 🧠 Key Features

✔️ Physics-inspired spray emission simulation  
✔️ Adjustable spray density, pressure, and width  
✔️ Incremental paint accumulation on surface  
✔️ Real-time texture updates  
✔️ Animated spray nozzle movement  
✔️ OpenUSD material & texture binding  
✔️ usdview visualization support  
✔️ Research-level simulation architecture  

---

# 🏗️ System Architecture

Simulated-Paint-Spraying/
│
├── spray_warp.py # Main simulation script
├── README.md # Documentation
│
├── output/
│ ├── final_scene.usda # OpenUSD scene file
│ └── textures/ # Generated paint textures
│ ├── frame_000.png
│ ├── frame_001.png
│ └── ...
│
├── images/ # Add screenshots here
├── video/ # Add demo video here 


---

# 🛠️ Technologies Used

## 🔷 OpenUSD (Pixar Universal Scene Description)
- 3D scene construction  
- Material & texture binding  
- Animation & visualization  

🌐 https://openusd.org  
🔗 https://github.com/PixarAnimationStudios/OpenUSD  

---

## 🔷 NVIDIA Isaac Warp
- Physics-based spray simulation  
- Particle emission modeling  
- GPU/CPU accelerated kernel computation  

🔗 https://github.com/NVIDIA/warp  

---

## 🔷 Python Libraries
- **NumPy** — numerical computation  
- **Pillow** — texture generation  
- **pxr (USD API)** — OpenUSD scene creation  
- **Warp** — simulation kernel  

---

# ⚙️ How It Works

### 1️⃣ Surface Modeling
A wall mesh is created using OpenUSD with UV mapping.

### 2️⃣ Spray Simulation
Warp kernel generates triangular spray particles using:
- Random emission  
- Distance-based spread  
- Adjustable spray density  

### 3️⃣ Paint Accumulation
Paint impacts wall and updates texture buffer per frame.

### 4️⃣ Visualization
Each frame saved as texture and mapped to wall material.  
Viewed in **usdview**.

---

# ▶️ How to Run

## Install dependencies
pip install warp-lang numpy pillow

## Open visualization
usdview output/final_scene.usda


Press ▶ Play inside usdview.

---

# 🖼️ Results

## Initial State
(Add screenshot here)


## Mid Spray
(Add screenshot here)


## Final Painted Wall
(Add screenshot here)


---

# 🎥 Demo Video

Upload video and add link:


---

# 🔬 Applications

- Robotic spray painting simulation  
- Industrial coating optimization  
- Digital twin manufacturing  
- Robotics research  
- Computer graphics simulation  

---

# 🧪 Future Improvements

- Full 3D particle simulation  
- GPU CUDA acceleration  
- Robotic arm integration  
- RTX rendering  
- Web visualization  

---

# 👨‍💻 Author

**Sunkeerth**  
AI & ML Engineer | Simulation Developer | Robotics & VR Enthusiast  

---

⭐ If you like this project, give it a star on GitHub.
