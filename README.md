# Studio System (minimalist-Tier Architecture)

A highly advanced, data-driven vector graphics and programmatic rendering pipeline capable of producing 500 high-quality, fully automated explainer videos. 
This repository transcends standard programmatic video builders by integrating WebGL hardware acceleration, procedural physics, and an enterprise "Graphics-as-Code" declarative SVG python pipeline.

## Core Capabilities Developed

### 1. The React & Remotion Rendering Engine
The core compositor handles thousands of layers compiled into headless MP4s:
- **Frame-Exact Transitions**: Leveraging native Remotion timing configurations to handle scenes.
- **Dynamic Timeline**: Root Composition dynamically parses timeline duration from the `video_XXX.json` manifest (e.g. 5 minutes = 9000 frames @ 30fps).
- **Parametric SVGs**: Complex character components with states, breathing animations, and dynamically shifting floor shadows.
- **Cinematic Spring Physics**: Reusable `<SpringEntrances>` powered by dynamic React hooks.
- **Zustand Interoperability**: Orchestrating global cinematic state without heavy prop-drilling.

### 2. Hardware Acceleration & Procedural Worlds
Native 2D DOM nodes are not enough for cinematic visuals. We implemented synchronized WebGL:
- **Three.js & React Three Fiber (`<Canvas3D>`)**: Powers deep 3D backgrounds and `<TerrainGenerator>` which leverages procedural Simplex Noise algebra and Chroma.js color mappings to build voxel-style mountain ranges rolling beneath the camera.
- **PixiJS v8 2D Particle Engine (`<PixiCanvas>`)**: An isolated WebGL 2D bridge executing asynchronous rendering pipelines to fire millions of particles frame-perfectly during MP4 headless burns. Powering weather systems (Snow/Rain) and `ExplosionEffects`.
- **GLSL Shaders**: Custom fragment shaders driving animated atmospheric backgrounds directly on the GPU.

### 3. Graphics-as-Code: The Inkscape Python Toolchain
Instead of relying on rigid, pre-drawn external static images, developers define graphic assets as code using the custom programmatic backend builder.
- **Declarative Geometry (`svgwrite`)**: Python functions declaring mathematically perfect shapes, paths, and lighting gradients without error-prone XML writing.
- **Headless Inkscape CLI Link**: SVGs are automatically funneled directly to Inkscape's internal processing command-line to handle complex routines natively.
- **CairoSVG Rasterization**: Instantaneous creation of `_preview.png` references in the `/processed` directory.
- **Interactive Auto-GUI**: Running `python build_assets.py --view` instructs Python to launch the Inkscape Desktop UI and load the specific dynamically generated vector layer so you can adjust the generated code visually!

### 4. Advanced Easing & Motion Curves (`motion.ts`)
Remotion is wrapped internally with `bezier-easing` and `animejs`. We expose heavy AfterEffects-style tension physics (`swiftOut`, minimalist's `.overshoot`) through simple mapping hooks like `smoothPop()` and `swingSettle()`.

---

## Quick Start (Unified CLI)

We manage the entire pipeline using the `studio.py` CLI at the root of the repository.

### 1. Build the 500-video library
```bash
python -m src.studio.cli build --materialize
```
Outputs: `data/videos/video_XXX.json` files mapping complex scripts and visuals to specific frames.

### 2. The Graphics Toolchain
Regenerate all visual assets dynamically through the Python `svgwrite` and SVG-React transpiler script:
```bash
python -m src.studio.cli assets build
```

### 3. Render Videos
```bash
# Render a single video
python -m src.studio.cli render video_001

# Render all videos (with resume support)
python -m src.studio.cli render --all
```

## Tech Stack & Hardware Overview

| System | Library / Technology |
|-------|------------|
| **Core Engine** | Remotion 4 (React + TypeScript) |
| **Animation Physics** | `animejs`, `bezier-easing`, `@react-spring/web`, `framer-motion` |
| **Path Morphing** | `flubber`, `svg-path-commander` |
| **Data Viz** | `d3`, `d3-geo`, `topojson-client` |
| **State** | `zustand` |
| **Procedural 3D** | `three`, `@react-three/fiber`, `simplex-noise`, `chroma-js` |
| **Effects (2D WebGL)** | `pixi.js` (v8), `@pixi/particle-emitter` |
| **Python Toolchain** | `svgwrite`, `cairosvg`, Inkscape CLI hook |
| **Hardware Maxed** | Enforced 14GB Node.js RAM (`--max-old-space-size=14336`) and 10 CPU Concurrency Threads for 4K/1080p long-form renders. |
