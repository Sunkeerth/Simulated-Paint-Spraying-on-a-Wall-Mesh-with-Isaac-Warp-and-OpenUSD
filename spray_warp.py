import os
import math
import numpy as np
from PIL import Image

import warp as wp
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf

wp.init()

WIDTH = 512
HEIGHT = 512
FRAMES = 120
PARTICLES = 200

# ===== REALISTIC SPRAY SETTINGS =====
SPRAY_PRESSURE = 0.25     # paint strength
SPRAY_WIDTH = 0.35        # cone width
SPRAY_DISTANCE = 3.5      # range
SPRAY_SMOOTH = 0.12       # softness
PARTICLES = 2500          # density


os.makedirs("output/textures", exist_ok=True)

# -----------------------------
# PAINT BUFFER
# -----------------------------
paint = np.zeros((HEIGHT*WIDTH), dtype=np.float32)
paint_wp = wp.array(paint, dtype=float)

# -----------------------------
# RANDOM STATES (IMPORTANT)
# -----------------------------
rng_states = wp.array([wp.rand_init(i) for i in range(PARTICLES)], dtype=wp.uint32)

# -----------------------------
# WARP SPRAY KERNEL
# -----------------------------
# @wp.kernel
# def spray_kernel(
#     states: wp.array(dtype=wp.uint32),
#     nozzle_x: float,
#     nozzle_y: float,
#     paint: wp.array(dtype=float),
#     width: int,
#     height: int
# ):
#     tid = wp.tid()

#     state = states[tid]

#     angle = wp.randf(state) * 0.9 - 0.45
#     dist  = wp.randf(state) * 3.5

#     states[tid] = state

#     x = nozzle_x + dist * wp.cos(angle)
#     y = nozzle_y + dist * wp.sin(angle)

#     # ⚠️ convert width/height to float
#     w = float(width)
#     h = float(height)

#     u = (x + 2.0) / 4.0
#     v = y / 3.0

#     px = int(u * w)
#     py = int(v * h)

#     if px > 2 and px < width-2 and py > 2 and py < height-2:
#         idx = py * width + px
#         paint[idx] = wp.min(paint[idx] + 0.6, 1.0)

@wp.kernel
def spray_kernel(
    states: wp.array(dtype=wp.uint32),
    nozzle_x: float,
    nozzle_y: float,
    paint: wp.array(dtype=float),
    width: int,
    height: int,
    pressure: float,
    cone: float,
    max_dist: float,
    softness: float
):
    tid = wp.tid()
    state = states[tid]

    # cone spray
    angle = (wp.randf(state) - 0.5) * cone * 2.0
    dist  = wp.randf(state) * max_dist

    states[tid] = state

    x = nozzle_x + dist * wp.cos(angle)
    y = nozzle_y + dist * wp.sin(angle)

    u = (x + 2.0) / 4.0
    v = y / 3.0

    w = float(width)
    h = float(height)

    px = int(u * w)
    py = int(v * h)

    if px > 3 and px < width-3 and py > 3 and py < height-3:

        # distance fade physics
        fade = 1.0 - (dist / max_dist)
        fade = wp.max(fade, 0.0)

        intensity = pressure * fade

        idx = py * width + px
        paint[idx] = wp.min(paint[idx] + intensity, 1.0)



# -----------------------------
# RUN SIMULATION
# -----------------------------
print("🔥 Running REAL WARP spray simulation")

for frame in range(FRAMES):

    nozzle_x = -1.8 + frame*(3.6/(FRAMES-1))
    nozzle_y = 1.5 + math.sin(frame*0.08)*0.3

    # wp.launch(
    #     kernel=spray_kernel,
    #     dim=PARTICLES,
    #     inputs=[rng_states, nozzle_x, nozzle_y, paint_wp, WIDTH, HEIGHT]
    # )

    wp.launch(
    kernel=spray_kernel,
    dim=PARTICLES,
    inputs=[
        rng_states,
        nozzle_x,
        nozzle_y,
        paint_wp,
        WIDTH,
        HEIGHT,
        SPRAY_PRESSURE,
        SPRAY_WIDTH,
        SPRAY_DISTANCE,
        SPRAY_SMOOTH
    ]
)


    wp.synchronize()

    img = paint_wp.numpy().reshape((HEIGHT, WIDTH))
    img = np.clip(img,0,1)

    rgb = np.zeros((HEIGHT,WIDTH,3),dtype=np.uint8)
    rgb[:,:,0] = (img*255).astype(np.uint8)

    Image.fromarray(rgb).save(f"output/textures/frame_{frame:03d}.png")

print("✅ Spray simulation done")

# -----------------------------
# USD SCENE
# -----------------------------
stage = Usd.Stage.CreateNew("output/final_scene.usda")
UsdGeom.SetStageUpAxis(stage,UsdGeom.Tokens.y)
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(FRAMES-1)

UsdGeom.Xform.Define(stage,"/World")

# WALL
wall=UsdGeom.Mesh.Define(stage,"/World/Wall")
points=[(-2,0,0),(2,0,0),(2,3,0),(-2,3,0)]
wall.CreatePointsAttr(points)
wall.CreateFaceVertexCountsAttr([4])
wall.CreateFaceVertexIndicesAttr([0,1,2,3])

primvars=UsdGeom.PrimvarsAPI(wall)
uv=primvars.CreatePrimvar("st",
    Sdf.ValueTypeNames.TexCoord2fArray,
    UsdGeom.Tokens.varying)
uv.Set([(0,0),(1,0),(1,1),(0,1)])

# MATERIAL
# ================= MATERIAL =================
mat = UsdShade.Material.Define(stage, "/World/Mat")

# Preview Surface
shader = UsdShade.Shader.Define(stage, "/World/Mat/PreviewSurface")
shader.CreateIdAttr("UsdPreviewSurface")

# Texture shader
tex = UsdShade.Shader.Define(stage, "/World/Mat/Texture")
tex.CreateIdAttr("UsdUVTexture")

# IMPORTANT OUTPUT
tex.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)

# fallback color (very important)
tex.CreateInput("fallback", Sdf.ValueTypeNames.Float4).Set((1.0,0.0,0.0,1.0))

# scale fix
tex.CreateInput("scale", Sdf.ValueTypeNames.Float4).Set((1.0,1.0,1.0,1.0))

# wrap mode
tex.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("clamp")
tex.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("clamp")

# UV reader
uv_reader = UsdShade.Shader.Define(stage, "/World/Mat/stReader")
uv_reader.CreateIdAttr("UsdPrimvarReader_float2")
uv_reader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("st")
uv_reader.CreateOutput("result", Sdf.ValueTypeNames.Float2)

# connect UV → texture
tex.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(
    uv_reader.ConnectableAPI(), "result"
)

# connect texture → surface
shader.CreateInput(
    "diffuseColor",
    Sdf.ValueTypeNames.Color3f
).ConnectToSource(
    tex.ConnectableAPI(),
    "rgb"
)

# connect surface → material
mat.CreateSurfaceOutput().ConnectToSource(
    shader.ConnectableAPI(),
    "surface"
)

## bind material to wall (FINAL FIX)
binding = UsdShade.MaterialBindingAPI.Apply(wall.GetPrim())
binding.Bind(mat)



# animate texture
file_input = tex.CreateInput("file", Sdf.ValueTypeNames.Asset)

for f in range(FRAMES):
    # file_input.Set(Sdf.AssetPath(f"./textures/frame_{f:03d}.jpg"), f)
    file_input.Set(Sdf.AssetPath(f"./textures/frame_{f:03d}.jpg"), f)




# NOZZLE
nozzle=UsdGeom.Cylinder.Define(stage,"/World/Nozzle")
nozzle.CreateHeightAttr(0.5)
nozzle.CreateRadiusAttr(0.12)

xf=UsdGeom.Xformable(nozzle)
op=xf.AddTranslateOp()

for f in range(FRAMES):
    x=-1.8 + f*(3.6/(FRAMES-1))
    y=1.5 + math.sin(f*0.08)*0.3
    op.Set(Gf.Vec3f(x,y,1.3),f)

stage.GetRootLayer().Save()

print("\n🚀 SUCCESS FINAL")
print("OPEN WITH:")
print("usdview output/final_scene.usda")
