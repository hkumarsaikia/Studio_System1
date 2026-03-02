# Studio System

A data-driven Remotion pipeline for producing 500 high-quality, 2-minute (12-scene) vector explainer videos.

## What this system supports

- 500-topic library parsed from `data/Topics.txt`
- Materialized video JSON payloads in `data/videos/video_001.json` ... `video_500.json`
- Runtime selection of any video via `REMOTION_VIDEO_ID`
- 25+ reusable vector SVG components (Person, SystemIcons, FlowDiagram, etc.)
- 7 programmatic camera moves (zoom, pan, pull-back, static)
- 5 category-specific color palettes with semantic brand colors
- Parametric Person component with 4 mood states
- Frame-exact scene transitions using Remotion `<Series>`
- Audio sync with graceful fallback to silence on missing files
- Batch render, metadata generation, and thumbnail export automation

## Quick Start

### Build the 500-video library

```bash
python automation/build_topic_library.py --materialize
```

Outputs:
- `data/videos/video_XXX.json` (500 files)
- `data/video_manifest.json`
- `engine/src/generated/videoManifest.js`

### Render one video

```bash
python automation/render.py video_001
```

### Render all videos (with resume support)

```bash
python automation/render_all.py
python automation/render_all.py --limit 5              # smoke test
python automation/render_all.py --start-from video_120 # resume
python automation/render_all.py --force                # re-render all
```

### Generate metadata

```bash
python automation/metadata_generator.py --video-id video_001
python automation/metadata_generator.py --all
```

### Export thumbnails

```bash
python automation/export_thumbnail.py video_001 --frame 150
python automation/export_thumbnail.py --all --limit 10
```

### Validate library integrity

```bash
python automation/validate_library.py
```

### Generate blueprints (standalone)

```bash
python automation/generate_blueprints.py --dry-run
```

### Cleanup workspace

```bash
python automation/clean_output.py             # clean everything
python automation/clean_output.py --tmp-only  # just engine/tmp
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for full system diagram, component library, and pipeline details.

## Asset Pipeline

See [ASSET_PRODUCTION_GUIDE.md](ASSET_PRODUCTION_GUIDE.md) for reusable asset strategy and production checklist.

## Notes

- Headless render requires Remotion browser dependencies in your environment
- Audio files follow the convention `public/audio/video_XXX_scene_YY.mp3`
- Missing audio defaults to silence (no crash)
- `render_all.py` auto-cleans `engine/tmp` every 10 renders to save disk space
- All video JSONs conform to `automation/templates/master_schema.json`
