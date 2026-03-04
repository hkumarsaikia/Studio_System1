# Studio System Architecture

A data-driven Remotion pipeline for producing 500 high-quality, 2-minute (12-scene) vector explainer videos.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  data/raw/Topics.txt (500 topics)                               │
│       │                                                         │
│       ▼                                                         │
│  python studio.py build             ──▶  data/videos/*.json     │
│                                         (500 video blueprints)  │
│       │                                                         │
│       ▼                                                         │
│  engine/ (Remotion)                                             │
│   ├── src/core/         SceneManager, Camera, MotionLayer       │
│   ├── src/components/   Person, SystemIcons, FlowDiagram, …     │
│   ├── src/scenes/       GenericScene, SceneFactory, SceneBlock  │
│   ├── src/styles/       theme.js, typography.js, global.css     │
│   ├── src/hooks/        useSceneAnimation.js                    │
│   └── src/overlays/     CinematicText                           │
│       │                                                         │
│       ▼                                                         │
│  python studio.py render --all     ──▶  output/*.mp4            │
│  python studio.py thumbnail --all  ──▶ output/thumbnails/*.png  │
│  python studio.py metadata --all   ──▶ output/metadata/*.json   │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
Studio_System-main/
├── studio.py                   # Unified CLI entry point
├── scripts/                    # Python pipeline logic
│   ├── build_topic_library.py  # Master builder: Topics.txt → 500 JSONs
│   ├── generate_blueprints.py  # Standalone blueprint generator
│   ├── render.py               # Render single video logic
│   ├── render_all.py           # Batch render wrapper logic
│   ├── metadata_generator.py   # YouTube metadata factory
│   ├── export_thumbnail.py     # Thumbnail exporter
│   ├── clean_output.py         # Workspace cleanup
│   ├── validate_library.py     # Library integrity checker
│   └── templates/
│       └── master_schema.json  # Canonical video JSON schema
├── data/
│   ├── raw/                    
│   │   └── Topics.txt          # 500 topic titles
│   ├── videos/                 # 500 video JSON blueprints
│   ├── video_manifest.json     # Lookup manifest
│   └── schema.json             # JSON Schema
├── docs/                       # Project documentation
├── engine/                     # Remotion project (the "Director")
│   ├── src/
│   │   ├── Root.jsx            # Entry: loads video by REMOTION_VIDEO_ID
│   │   ├── core/               # Camera, SceneManager, MotionLayer
│   │   ├── components/         # SVG graphics: Person, SystemIcons, etc.
│   │   ├── scenes/             # GenericScene, SceneFactory, SceneBlock
│   │   ├── styles/             # theme.js, typography.js, global.css
│   │   ├── hooks/              # useSceneAnimation
│   │   ├── overlays/           # CinematicText
│   │   └── generated/          # videoManifest.js (auto-generated)
│   └── public/
│       ├── audio/              # Per-scene audio files
│       └── svg/                # External SVG assets
├── logs/                       # Render & engineering logs
└── output/                     # Rendered videos, thumbnails, metadata
```

## Rendering Pipeline

1. **Blueprint Generation** — `python studio.py build --materialize` reads Topics.txt and writes 500 JSON files with 12 scenes each, including camera actions, category palettes, and visual types.

2. **Engine Rendering** — Remotion loads the JSON via `REMOTION_VIDEO_ID` env var. Each scene flows through: Background → Camera → MotionLayer → SceneFactory → CinematicText.

3. **Camera System** — 7 named moves: `slow_zoom_in`, `pan_right`, `pan_left`, `static_focus`, `dramatic_pull_back`, `slow_pan_up`, `slow_pan_down`.

4. **Scene Sequencing** — Uses Remotion's `<Series>` for frame-exact transitions. Each scene is 300 frames (10 seconds at 30fps).

5. **Batch Render** — `python studio.py render --all` skips existing outputs, cleans tmp every N renders, logs results.

## Visual Component Library

| Component | Props | Purpose |
|-----------|-------|---------|
| `Person` | mood, skin, shirt | Parametric human figure (4 moods) |
| `SystemIcons` | name, color, size | 25+ proper SVG icons |
| `FlowDiagram` | labels, direction | 2–6 node flow charts |
| `SystemNetwork` | nodes | Pentagon network graph |
| `DataBars` | values | Animated bar chart |
| `Crowd` | count | Group of Person figures |
| `CityStreetBackdrop` | — | Urban scene backdrop |
| `LandscapeBackdrop` | — | Nature/horizon backdrop |
| `AnimalSilhouettes` | animals | Ecology visuals |

## Category System

| Category | Accent | Videos |
|----------|--------|--------|
| EVERYDAY SYSTEMS | `#38bdf8` | 1–100 |
| MONEY & ECONOMICS | `#22c55e` | 101–200 |
| INFORMATION SYSTEMS | `#f472b6` | 201–300 |
| POWER & INSTITUTIONS | `#a78bfa` | 301–400 |
| FUTURE SYSTEMS | `#14b8a6` | 401–500 |
