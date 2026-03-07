# Studio System Architecture

A data-driven rendering pipeline for producing high-quality **high-quality minimalist** animated videos using React, Remotion, WebGL, and Python "Graphics-as-Code".

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  data/raw/Topics.txt (500 topics)                               │
│       │                                                         │
│       ▼                                                         │
│  python studio.py build             ──▶  data/videos/*.json     │
│                                         (Video blueprints)      │
│       │                                                         │
│       ▼                                                         │
│  Python Graphics-as-Code Pipeline                               │
│  (build_assets.py)                                              │
│   ├── svgwrite Declarative Generators                           │
│   ├── Inkscape CLI Normalization                                │
│   └── CairoSVG Rasterization Preview                            │
│       │                                                         │
│       ▼                                                         │
│  engine/ (Remotion + WebGL)                                     │
│   ├── src/core/         SceneManager, Camera, Canvas3D          │
│   ├── src/components/   EffectsShowcase, TerrainGenerator,      │
│   │                     MorphingShape (Flubber), PixiCanvas     │
│   ├── src/utils/        motion.ts (Bezier/AnimeJS physics)      │
│       │                                                         │
│       ▼                                                         │
│  python studio.py render --all     ──▶  output/*.mp4            │
└─────────────────────────────────────────────────────────────────┘
```

## Dual-Engine Hardware Acceleration

The repository rendering capabilities transcend standard DOM nodes by integrating two specialized WebGL contexts strictly synchronized to Remotion's frame clock.

### 1. `THREE.js` & React Three Fiber (`<Canvas3D>`)
Handles all deep Z-index background layers.
- **`<TerrainGenerator>`**: A procedural topography engine leveraging `simplex-noise` to animate voxel/low-poly mountain ranges sliding across the screen. Mapped to color palettes via `chroma-js`.
- **`<ShaderBackground>`**: Runs custom raw GLSL fragment shaders (clouds, nebulas, nebulous gradients) directly on the GPU.

### 2. `PixiJS` (v8) Procedural Effects (`<PixiCanvas>`)
Handles 2D high-density particle emitters.
- Employs Remotion's `delayRender` API to asynchronously initialize the WebGL context.
- **`<WeatherSystem>`**: Renders thousands of rain streaks or snowflakes directionally.
- **`<ExplosionEffect>`**: Triggers physics-based bursts exact to specific Remotion frames.

## The Toolchain: "Graphics-as-Code"

The Studio System treats vector SVGs not as static external binaries, but as programmable configurations.

1. **Python Declarative Build**: Inside `assets/src/declarative_builder.py`, graphics are generated using `svgwrite` (e.g., `dwg.rect(fill="url(#gradient)")`), eliminating manual XML manipulation.
2. **Inkscape Shell Injection**: The pipeline runs `subprocess.Popen` to pass the raw XML to Inkscape. The script executes `--export-plain-svg` and calculates all relative transforms into absolute paths required for React mapping.
3. **Automated GUI Handoff**: Running `build_assets.py` now automatically pops open the native Inkscape Desktop UI displaying each freshly generated SVG, allowing quick visual iterations before React compilation. Use `--no-view` only when you need a headless batch run.

## Animation & Motion 

### Custom Cinematic Easing (`motion.ts`)
Standard React Spring physics are not aggressive enough for high-end studio explainer style. We built a library implementing `animejs` and `bezier-easing` logic:
- Extrapolates time slices across cubic bezier curves mimicking Adobe AfterEffects (`.swiftOut`, `.kurzPunch`).
- Exposes wrappers like `smoothPop(frame)` and `swingSettle(frame)` which drive transform matrices on characters and props.

### Mathematical Morphing
The `<MorphingShape>` component uses `flubber` to deterministically interpolate complex SVG `d="..."` paths (e.g. morphing a square directly into an intricate star vector) smoothly across 30 frames.
