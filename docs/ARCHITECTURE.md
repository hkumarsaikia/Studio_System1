# Studio System Architecture

A data-driven Remotion pipeline for producing 500 high-quality, 2-minute (12-scene) **Kurzgesagt-style** vector explainer videos.

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
│   ├── src/core/         SceneManager, Camera, MotionLayer,      │
│   │                     TemplateLoader, SvgDefs                 │
│   ├── src/components/   Person, SystemIcons, FlowDiagram, …     │
│   ├── src/scenes/       GenericScene, SceneFactory, SceneBlock  │
│   ├── src/styles/       theme.ts, typography.ts, global.css     │
│   ├── src/hooks/        useElasticAnim, useSceneAnimation       │
│   ├── src/overlays/     CinematicText, Vignette, LightLeak,    │
│   │                     CinematicGrain, ScanLines               │
│   ├── src/templates/    ExplainerCinematic, DataInfographic, …  │
│   └── src/utils/        dataParser, propsValidator,             │
│                         sceneTiming, sceneTransitions           │
│       │                                                         │
│       ▼                                                         │
│  python studio.py render --all     ──▶  output/*.mp4            │
│  python studio.py thumbnail --all  ──▶ output/thumbnails/*.png  │
│  python studio.py metadata --all   ──▶ output/metadata/*.json   │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
Studio_System1/
├── studio.py                   # Unified CLI entry point
├── scripts/                    # Python pipeline logic
│   ├── __init__.py             # Package marker
│   ├── build_topic_library.py  # Master builder: Topics.txt → 500 JSONs
│   ├── generate_blueprints.py  # Standalone blueprint generator
│   ├── render.py               # Render single video logic
│   ├── render_all.py           # Batch render wrapper logic
│   ├── metadata_generator.py   # YouTube metadata factory
│   ├── export_thumbnail.py     # Thumbnail exporter
│   ├── clean_output.py         # Workspace cleanup
│   ├── validate_library.py     # Library integrity checker
│   ├── logic/
│   │   ├── __init__.py         # Sub-package marker
│   │   └── NarrativeEngine.py  # Story structure generator
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
│   ├── remotion.config.js      # Webpack aliases, codec, concurrency
│   ├── tsconfig.json           # TypeScript config with @/ path alias
│   ├── package.json            # Node dependencies
│   └── src/
│       ├── Root.tsx             # Entry: loads video by REMOTION_VIDEO_ID
│       ├── index.ts             # Remotion registerRoot
│       ├── core/                # Camera, SceneManager, MotionLayer,
│       │                        #   TemplateLoader, SvgDefs
│       ├── components/          # SVG graphics: Person, SystemIcons,
│       │                        #   Crowd, FlowDiagram, GeoEarth, etc.
│       ├── scenes/              # GenericScene, SceneFactory, SceneBlock
│       ├── styles/              # theme.ts, typography.ts, global.css
│       ├── hooks/               # useElasticAnim, useSceneAnimation
│       ├── overlays/            # CinematicText, Vignette, LightLeak,
│       │                        #   CinematicGrain, ScanLines,
│       │                        #   GradientOverlay
│       ├── templates/           # ExplainerCinematic, DataInfographic,
│       │                        #   ProtestCinematic, ShortsVertical
│       ├── utils/               # dataParser, propsValidator,
│       │                        #   sceneTiming, sceneTransitions,
│       │                        #   audioSync
│       └── generated/           # videoManifest.js (auto-generated)
├── logs/                       # Render & engineering logs
└── output/                     # Rendered videos, thumbnails, metadata
```

## Rendering Pipeline

1. **Blueprint Generation** — `python studio.py build --materialize` reads Topics.txt and writes 500 JSON files with 12 scenes each, including camera actions, category palettes, and visual types.

2. **Engine Rendering** — Remotion loads JSON via `REMOTION_VIDEO_ID`. Each scene flows through: `SvgDefs` → `Background` (with ambient particles + vignette) → `Camera` → `MotionLayer` → `SceneFactory` → `CinematicText` → overlay stack.

3. **Camera System** — 7 named moves: `slow_zoom_in`, `pan_right`, `pan_left`, `static_focus`, `dramatic_pull_back`, `slow_pan_up`, `slow_pan_down`.

4. **Scene Sequencing** — Uses Remotion's `<Series>` for frame-exact transitions. Each scene is 300 frames (10 seconds at 30fps).

5. **Batch Render** — `python studio.py render --all` skips existing outputs, cleans tmp every N renders, logs results.

## Visual Component Library

| Component | Props | Purpose |
|-----------|-------|---------|
| `Person` | mood, skin, shirt, size | Parametric human figure with breathing animation, 4 moods, cast shadows |
| `SystemIcons` | name, color, size | 25+ layered SVG icons with drop shadows and gradients |
| `SystemIconGrid` | icons, size, color | Auto-layout grid of SystemIcons in glass cards |
| `FlowDiagram` | labels, direction | 2–6 node flow charts |
| `SystemNetwork` | nodes | Pentagon network graph with tsparticles background |
| `DataBars` | values | Animated bar chart |
| `Crowd` | count | Group of Person figures with staggered spring entrances |
| `GeoEarth` | — | D3-powered globe with landmasses and orbit ring |
| `NeuralCore` | — | AI neural network visualization |
| `GenerativeDataLattice` | accentColor | p5.js procedural lattice animation |
| `CityStreetBackdrop` | — | Urban scene backdrop |
| `AnimalSilhouettes` | animals | Ecology visuals |
| `GradientOrb` | — | Glowing gradient sphere |
| `MatrixRain` | — | Digital rain effect |
| `CyberHUD` | — | Sci-fi heads-up display overlay |

## Graphics Architecture (Kurzgesagt Style)

### Global SVG Definitions (`SvgDefs.tsx`)
Injected at the root of every scene, providing:
- `#kurzDropShadow` — Soft drop shadow for 3D depth
- `#kurzIntenseShadow` — Intense shadow for prominent elements
- `#neonGlow` — Multi-pass Gaussian blur for glowing elements
- `#skinGlow` — Radial gradient for volumetric skin rendering
- `#metalShine` — Linear gradient for metallic surfaces
- `#deepVignette` — Radial gradient for atmospheric vignetting

### Elastic Animations (`useElasticAnim.ts`)
Spring physics hook using Remotion's `spring()` with configurable stiffness, damping, and mass for bouncy pop-in effects.

### Ambient Particles
30 floating dust particles per scene with deterministic randomness, upward drift, and sinusoidal wobble.

## Category System

| Category | Accent | Videos |
|----------|--------|--------|
| EVERYDAY SYSTEMS | `#38bdf8` | 1–100 |
| MONEY & ECONOMICS | `#22c55e` | 101–200 |
| INFORMATION SYSTEMS | `#f472b6` | 201–300 |
| POWER & INSTITUTIONS | `#a78bfa` | 301–400 |
| FUTURE SYSTEMS | `#14b8a6` | 401–500 |

Additional palettes: Tropical Sunset, Arctic Aurora, Neon City, Pastel Dream, Desert Storm, Deep Ocean, Lavender Night, Golden Empire, Spring Meadow, Rose Quartz, Midnight Electric, Cosmic Dust.
