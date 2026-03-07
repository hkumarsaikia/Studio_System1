# Studio_System1 Architecture

This file is the short architecture summary for the repository. The detailed reference lives in `docs\ARCHITECTURE.md`.

## YouTube Shorts Engine Overview

Studio_System1 is an automated animation engine that generates YouTube Shorts (120-second vertical videos) from structured instructions. Each Short is divided into **12 segments of 10 seconds**, and the engine renders each segment as an animated vector graphics scene.

```text
┌─────────────────────────────────────────────────────────┐
│                  120-Second YouTube Short                │
├─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬──┤
│ S1  │ S2  │ S3  │ S4  │ S5  │ S6  │ S7  │ S8  │ S9  │..│
│ 10s │ 10s │ 10s │ 10s │ 10s │ 10s │ 10s │ 10s │ 10s │  │
│300f │300f │300f │300f │300f │300f │300f │300f │300f │  │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴──┘
 S1-S12: 12 segments × 300 frames @ 30fps = 3600 total frames
```

## End-To-End Flow

1. **Topic Selection**: The `shorts` CLI command picks a topic from `data\raw\Topics.txt` (500 topics).
2. **Payload Generation**: Python generators create a 12-segment video JSON in `data\videos\`.
3. **Each segment contains**: narration script, visual direction, scene parameters, asset references.
4. **Asset Pipeline**: Python builders generate SVGs → Inkscape normalizes → transpiler creates React components.
5. **Rendering**: Remotion renders all 12 segments sequentially into a single 1080×1920 MP4 in `output\`.

## Main Subsystems

### Python CLI

`python -m src.studio.cli` is the entrypoint for:

- `shorts` — generate a YouTube Short from a single topic (select → build → validate → render)
- `build` — build or materialize all 500 video payloads
- `validate` — validate data library integrity
- `assets build` — run SVG generation and React transpilation
- `render` — render a video to MP4
- `thumbnail` — export frame thumbnails
- `clean` — clean output and temporary folders

### Shorts Pipeline

`src\studio\shorts_pipeline.py` orchestrates single-video generation:

1. Selects a topic (by index or randomly)
2. Generates the 12-segment video JSON with narration and visual directions
3. Validates all 12 segments have correct duration (300 frames) and required fields
4. Optionally renders to MP4

### Narrative Engine

`src\studio\generators\narrative_engine.py` procedurally generates three text layers per segment:

- **Subtext**: Display text shown on screen
- **Narration**: Voiceover script for the segment
- **Visual Direction**: Animation and camera direction notes

### Asset Toolchain

`python build_assets.py` delegates to `src\studio\assets\toolchain.py`, which:

- selects assets from `ASSET_SPECS`
- generates raw SVGs with Python builders
- runs Inkscape CLI for normalization
- optionally runs SVGO
- opens the processed SVG in Inkscape by default
- transpiles the processed SVG into a React component

### Remotion Engine

The `engine\` workspace holds the React/TypeScript rendering engine. Scene composition, generated SVG wrappers, motion helpers, and advanced visual effects all live there. Each of the 30+ visual components is mapped through `SceneFactory.tsx`.

### Local NVENC Layer

`engine\remotion.config.js` expects a local `engine\remotion-binaries-nvenc\` directory. That directory is not tracked in Git and must be recreated locally when you clone the repository if you want NVIDIA GPU encoding.

## Key Directories

```text
Studio_System1/
|- data/
|  |- raw/Topics.txt        # 500 topic ideas database
|  |- videos/                # Generated 12-segment video JSONs
|  \- assets/                # Raw and processed SVG assets
|- docs/
|- engine/
|  \- src/
|     |- scenes/             # SceneFactory, GenericScene, SceneBlock
|     |- components/         # 30+ visual components (2D, 3D, charts, fx)
|     \- core/               # Camera, TemplateLoader, SceneManager
|- output/
\- src/studio/
   |- generators/            # Topic library, blueprints, narrative engine
   |- render/                # Single and batch renderers
   |- assets/                # SVG asset toolchain
   \- shorts_pipeline.py     # YouTube Shorts orchestrator
```

## Detailed Reference

Use `docs\ARCHITECTURE.md` for the full directory map, runtime boundaries, and render configuration notes.
