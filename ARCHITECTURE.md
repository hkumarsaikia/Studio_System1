# Studio_System1 Architecture

This file is the short architecture summary for the repository. The detailed reference lives in `docs/ARCHITECTURE.md`.

## End-To-End Flow

1. `python -m src.studio.cli build --materialize` reads `data/raw/Topics.txt`.
2. Missing storyboard skeletons are created in `data/storyboards/` for `video_001` through `video_500`.
3. Storyboards are compiled into production payloads in `data/videos/`.
4. Demo payloads are stored separately in `data/demos/`.
5. `python build_assets.py` generates and normalizes SVG assets, then transpiles them into React components.
6. `python -m src.studio.cli render <video_id>` renders production Shorts one segment at a time and stitches the `12` MP4 segments into the final output.
7. `python -m src.studio.cli metadata <video_id>` generates deterministic metadata JSON from the storyboard.

## Main Subsystems

### Python CLI

`python -m src.studio.cli` is the entrypoint for:

- `build`
- `render`
- `clean`
- `thumbnail`
- `metadata`
- `validate`
- `assets build`

### Storyboard Compiler

The Python generation layer now treats `data/storyboards/` as the canonical authoring surface and `data/videos/` as derived data. The compiler is responsible for:

- segment scaffolding
- narration scaffolding
- asset reference mapping
- manifest generation
- demo migration and separation

### Asset Toolchain

`python build_assets.py` delegates to `src/studio/assets/toolchain.py`, which:

- generates raw SVGs
- normalizes SVGs with Inkscape
- optionally runs SVGO
- opens each processed SVG in Inkscape by default
- transpiles processed SVGs into React components

### Remotion Engine

The `engine/` workspace renders either:

- `MainComposition` for full demo renders
- `SegmentComposition` for one production segment at a time

Production rendering is segment-first by design.

## Key Directories

```text
Studio_System1/
|- data/
|  |- archive/
|  |- demos/
|  |- raw/
|  |- storyboards/
|  \- videos/
|- docs/
|- engine/
|- examples/
|- output/
|  |- metadata/
|  \- segments/
\- src/studio/
```

## Production Rules

- Production IDs are `video_001` through `video_500`.
- Every production video has exactly `12` segments.
- Every production segment is exactly `10` seconds.
- Every compiled production segment is exactly `300` frames.
- Production and demo namespaces must not collide.

## Detailed Reference

Use `docs/ARCHITECTURE.md` for the full directory map, schema rules, data contracts, and render flow.
