# Studio_System1 Architecture

This file is the short architecture summary for the repository. The detailed reference lives in `docs\ARCHITECTURE.md`.

## End-To-End Flow

1. Python generators materialize video payload JSON files into `data\videos\`.
2. Python asset builders generate raw SVG source files into `data\assets\raw\`.
3. Inkscape normalizes those SVGs into `data\assets\processed\`.
4. The SVG transpiler writes React components into `engine\src\components\generated\`.
5. Remotion renders the selected video ID into `output\`, and example copies can be saved under `examples\video\`.

## Main Subsystems

### Python CLI

`python -m src.studio.cli` is the entrypoint for:

- `build`
- `validate`
- `assets build`
- `render`
- `thumbnail`
- `clean`

### Asset Toolchain

`python build_assets.py` is the direct asset entrypoint. It delegates to `src\studio\assets\toolchain.py`, which:

- selects assets from `ASSET_SPECS`
- generates raw SVGs with Python builders
- runs Inkscape CLI for normalization
- optionally runs SVGO
- opens the processed SVG in Inkscape by default
- transpiles the processed SVG into a React component

### Remotion Engine

The `engine\` workspace holds the React/TypeScript rendering engine. Scene composition, generated SVG wrappers, motion helpers, and advanced visual effects all live there.

### Local NVENC Layer

`engine\remotion.config.js` expects a local `engine\remotion-binaries-nvenc\` directory. That directory is not tracked in Git and must be recreated locally when you clone the repository if you want NVIDIA GPU encoding.

## Key Directories

```text
Studio_System1/
|- data/
|- docs/
|- engine/
|- examples/
|- logs/
|- output/
\- src/studio/
```

## Detailed Reference

Use `docs\ARCHITECTURE.md` for the full directory map, runtime boundaries, and render configuration notes.
