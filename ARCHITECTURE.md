# Studio System Architecture

This document outlines the professional directory structure and domain-driven design implemented in the Studio\_System1 codebase.

## 1. Directory Structure

```text
Studio_System1/
├── data/                       # Separation of data and configuration logic
│   ├── assets/                 # Replaces the legacy top-level 'assets/' folder
│   │   ├── raw/                # Unprocessed mathematically generated SVG source code
│   │   └── processed/          # Processed Inkscape/SVGO optimized outputs
│   ├── videos/                 # Materialized video timeline configuration files (video_XXX.json)
│   ├── asset_library.json      # Mapping manifest for standard SVG assets
│   ├── asset_requirements.json # Aggregated needs across video JSONs
│   └── video_manifest.json     # Global tracking manifest defining rendering scopes
├── engine/                     # Node.js React / Remotion engine
│   └── src/
│       ├── components/         # Domain-driven React Components
│       │   ├── 2d/             # Standard 2D UI, backdrop, crowds, network elements
│       │   ├── 3d/             # react-three-fiber, terrain generation, WebGL meshes
│       │   ├── charts/         # Data visualization widgets: line charts, donuts, progress rings
│       │   ├── fx/             # Particle effects, PixiCanvas, procedural effects shaders
│       │   └── generated/      # Auto-transpiled React components straight from processed SVGs
│       ├── core/               # Engine utilities (Camera, Motion Layers, Audio Processing)
│       └── scenes/             # Master scene orchestrators (GenericScene, SceneFactory)
├── output/                     # Rendered video and thumbnail distribution outputs
│   └── thumbnails/             # Rendered PNG frame grabs
├── presets/                    # Base definitions serving as inputs for the python generation pipeline
│   └── topics.json             # Core taxonomy of the 500-library
└── src/
    └── studio/                 # A fully compliant, consolidated Python package
        ├── assets/             # The "Graphics-as-Code" Builder Toolchain
        │   ├── background_builder.py
        │   ├── character_builder.py
        │   ├── declarative_builder.py
        │   ├── props_builder.py
        │   ├── toolchain.py    # Inkscape CLI processing wrapper 
        │   └── transpiler.py   # SVG-to-React TypeScript compiler
        ├── generators/         # Orchestration Logic
        │   ├── blueprints.py   # Translating topic strings to 12-scene JSONs
        │   ├── narrative_engine.py  # LLM Simulation engine mapping
        │   └── topic_library.py# Topic and library manifesting
        ├── render/             # Remotion CLI adapters
        │   ├── render_all.py
        │   └── render_single.py
        ├── utils/              # Diagnostics and Purging Utilities
        │   ├── clean.py
        │   ├── export_thumbnail.py
        │   └── validate.py
        ├── cli.py              # Single endpoint argparse interface (python -m src.studio.cli)
        └── config.py           # Absolute `pathlib` constants registry
```

## 2. Methodology & Core Decisions

### Unified Python Environment
By moving all loose scripts into `src/studio/`, we resolve issues related to Python path scoping and allow the package to dynamically resolve absolute roots independently of execution location via the `config.py` module.

### Data & Code Segregation
The separation of the `data/` directory ensures output artifacts (SVGs, timeline JSONs) are insulated from core code logic. This acts as a database and allows safe `.gitignore` filtering of production payloads without corrupting scripts.

### Graphics as Code
The Inkscape Python pipeline programmatically defines graphical assets. It transpiles declarative python objects into React `TSX` modules that are deposited straight into `engine/src/components/generated/`.

### Domain-Driven Component Tree
The React implementation groups independent domains (`2d`, `3d`, `fx`, `charts`) locally, effectively isolating dependencies (e.g., specific `three.js` dependencies remain functionally limited to `3d/`). This prevents module tangling and organizes large complex repos.
