# 🚀 NVIDIA Warp + OpenUSD Industrial Spray Simulation

A research-oriented physics-based spray painting simulation built using NVIDIA Isaac Warp and Pixar OpenUSD to model real-world industrial coating processes.

# 🎨 Simulated Paint Spraying on a Wall Mesh using Isaac Warp & OpenUSD

A physics-inspired spray painting simulation built using NVIDIA Isaac Warp and OpenUSD, demonstrating how paint particles accumulate over time on a wall surface and visualized in a fully animated 3D scene.

This project models a robotic/industrial spray-painting workflow with configurable spray parameters and real-time visualization.

🚀 Project Overview : 

This simulation demonstrates:

A moving spray nozzle emitting paint in a triangular fan pattern
Real-time paint accumulation on a wall surface
Time-based texture updates mapped onto a 3D wall mesh
Visualization using Pixar OpenUSD (usdview)
The goal is to replicate an industrial robotic paint spraying process using physics-inspired computation and USD-based visualization.

Key Features : 

✔️ Realistic spray emission simulation
✔️ Adjustable spray pressure, width, and density
✔️ Incremental paint accumulation over time
✔️ Animated nozzle movement
✔️ Texture-based surface update system
✔️ OpenUSD 3D scene visualization
✔️ Research-level simulation workflow 

Project Architecture :

                 ┌────────────────────┐
                 │   Spray Nozzle     │
                 │ (Animated motion)  │
                 └─────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Isaac Warp Kernel   │
                │ Particle emission   │
                │ Spray cone physics  │
                └─────────┬──────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Paint Accumulation     │
              │ Texture buffer update  │
              └─────────┬──────────────┘
                        │
                        ▼
          ┌──────────────────────────────┐
          │ OpenUSD Material + Texture   │
          │ UV mapping + animation       │
          └─────────┬────────────────────┘
                    │
                    ▼
              🎬 usdview Visualization

Project Structure :

Simulated-Paint-Spraying/
│
├── spray_warp.py              # Main simulation script
├── README.md                  # Project documentation
│
├── output/
│   ├── final_scene.usda       # OpenUSD scene
│   └── textures/              # Generated paint frames
│       ├── frame_000.png
│       ├── frame_001.png
│       └── ...
│
├── images/                    # (Add screenshots here)
├── video/                     # (Add demo video here)


⚙️ How It Works :

1️⃣ Surface Modeling :
A wall mesh is created using OpenUSD with UV mapping.

2️⃣ Spray Simulation :
Isaac Warp kernel generates a triangular fan spray using:
Random particle emission
Distance-based spread
Adjustable spray density

3️⃣ Paint Accumulation : 

Paint impact is stored in a texture buffer and updated every frame.

4️⃣ Visualization : 
Each frame is saved as a texture and applied to the wall material.
The animation is visualized using usdview. 


▶️ How to Run :

1. Install dependencies
pip install warp-lang numpy pillow

2. Run simulation
python3 spray_warp.py

3. Open visualization
usdview output/final_scene.usda

Press ▶ Play in usdview.
