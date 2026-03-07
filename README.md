# Studio System (Automated YouTube Shorts Engine)

This is a custom animation engine designed to automatically generate YouTube Shorts using code, rather than manual video editing. It converts structured instructions into animated vector graphics videos exported as MP4 files. 

Instead of designing every video from scratch, this is a programmable pipeline where videos are assembled piece by piece based on provided instructions.

## The 12-Segment Architecture

Each YouTube Short is treated as a structured sequence of visual parts:
- **Duration**: A full short is 120 seconds long (2 minutes).
- **Segments**: The video is divided into exactly twelve segments, each lasting ten seconds.
- **Independent Units**: Every 10-second segment is an independent unit of animation, allowing the engine to generate the video systematically by rendering one segment at a time and sequencing them together.

For every segment, detailed instructions describe the script/narration, the visual direction, the graphical objects that should appear, and the scene's visual look. Each 10-second segment has its own miniature storyboard written in a structured JSON format.

## Content & Assets

**Topics Database:** The topics for the videos come from text files containing large collections of ideas (e.g., `data/Topics.txt`). When a video is generated, the system selects a topic, which determines the scene sequence, narration, and visual explanations.

**Reusable Graphics:** Assets (characters, icons, objects) are not random. They are designed specifically for the scenes as reusable vector graphics. The engine loads the required assets and animates them according to the segment's instructions.

## The Python Controller

All orchestration is handled through code:
- **Render Engine**: Handles the creation of vector graphics animations (Remotion).
- **Python Pipeline**: Acts as the master controller. The Python script reads the video instructions, organizes the twelve segments, and directs the rendering engine on how to construct the scenes before exporting the final MP4.

Once the engine is configured, you never need to manually edit a video timeline. To create a new short, you simply provide the segment instructions and run the Python script.

---

## Technical Features

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
