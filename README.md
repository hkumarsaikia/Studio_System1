# Studio System

A data-driven Remotion pipeline for producing 500 high-quality, 2-minute (12-scene) **Kurzgesagt-style** vector explainer videos.

## What This System Delivers

- 500-topic library parsed from `data/raw/Topics.txt`
- Materialized video JSON payloads in `data/videos/video_001.json` … `video_500.json`
- Runtime selection of any video via `REMOTION_VIDEO_ID`
- **Kurzgesagt-level vector graphics** — multi-layered SVGs with radial gradients, `feDropShadow` filters, and volumetric lighting via `SvgDefs.tsx`
- 30+ reusable vector SVG components (Person, SystemIcons, FlowDiagram, GeoEarth, NeuralCore, etc.)
- Parametric **Person** component with 4 mood states, continuous breathing animation, and cast floor shadows
- **Elastic spring animations** via `useElasticAnim` hook (bouncy pop-in entrances for all elements)
- **Ambient floating particles** and deep cinematic vignettes baked into every background
- 7 programmatic camera moves (zoom, pan, pull-back, static)
- 20+ category-specific color palettes with 100+ curated modern colors
- 5 background modes: gradient, mesh, aurora, vortex, starfield
- Frame-exact scene transitions using Remotion `<Series>`
- Audio sync with graceful fallback to silence on missing files
- Batch render, metadata generation, and thumbnail export via unified CLI
- Robust environment parsing (Node.js and FFmpeg resolved from PATH)

## Quick Start (Unified CLI)

We manage the entire pipeline using the `studio.py` CLI at the root of the repository.

### 1. Build the 500-video library

```bash
python studio.py build --materialize
```

Outputs:
- `data/videos/video_XXX.json` (500 files)
- `data/video_manifest.json`
- `engine/src/generated/videoManifest.js`

### 2. Render Videos

```bash
# Render a single video
python studio.py render video_001

# Render all videos (with resume support)
python studio.py render --all

# Smoke test (render first 5)
python studio.py render --all --limit 5

# Resume rendering
python studio.py render --all --start-from video_120

# Force re-render everything
python studio.py render --all --force
```

### 3. Generate Metadata

Generate YouTube-ready JSON metadata:

```bash
python studio.py metadata video_001
python studio.py metadata --all
```

### 4. Export Thumbnails

```bash
python studio.py thumbnail video_001 --frame 150
python studio.py thumbnail --all --limit 10
```

### 5. Validate library integrity

```bash
python studio.py validate
```

### 6. Cleanup workspace

Purges output and temporary directories to save space.

```bash
python studio.py clean             # clean everything
python studio.py clean --tmp-only  # just engine/tmp
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Video Engine | Remotion 4 (React + TypeScript) |
| Animation | `spring()` physics, `framer-motion`, `@react-spring/web` |
| Data Viz | D3.js, d3-geo, d3-scale-chromatic |
| Generative Art | p5.js, simplex-noise |
| Particles | @tsparticles/react + slim |
| Color Engine | `polished` (dynamic lighten/darken/transparentize) |
| SVG Optimization | SVGO |
| Pipeline CLI | Python 3.12+ (standard library only) |

## Documentation

- [System Architecture](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Asset Production Guide](docs/ASSET_PRODUCTION_GUIDE.md)
- [Contributing](CONTRIBUTING.md)

## Notes

- Headless render requires Remotion browser dependencies in your environment
- Audio files follow the convention `engine/public/audio/video_XXX_scene_YY.mp3`
- Missing audio defaults to silence (no crash)
- Batch renderer auto-cleans `engine/tmp` every 10 renders to save disk space
- All video JSONs conform to `scripts/templates/master_schema.json`
- TypeScript strict mode is enabled; `@/` path aliases resolve via `tsconfig.json` paths
