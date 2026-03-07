# Detailed Architecture

This document describes the current repository structure and the runtime boundaries that matter when you are extending or operating the project.

## System Summary

Studio_System1 has three connected layers:

1. A Python orchestration layer under `src\studio\`.
2. An SVG production pipeline backed by Inkscape.
3. A Remotion/React engine under `engine\` for final MP4 rendering.

The repository is Windows-first. The documented operational path assumes PowerShell, local Inkscape, and a local NVENC-capable FFmpeg override when GPU rendering is required.

## Directory Map

```text
Studio_System1/
|- data/
|  |- assets/
|  |  |- raw/
|  |  \- processed/
|  |- raw/
|  |- videos/
|  |- asset_library.json
|  \- video_manifest.json
|- docs/
|- engine/
|  |- src/
|  |  |- components/
|  |  |  |- fx/
|  |  |  |- generated/
|  |  |  \- ...
|  |  |- scenes/
|  |  |- generated/
|  |  \- index.ts
|  |- remotion.config.js
|  \- package.json
|- examples/
|  \- video/
|- logs/
|- output/
|- presets/
|- src/
|  \- studio/
|     |- assets/
|     |- generators/
|     |- render/
|     |- utils/
|     |- cli.py
|     \- config.py
|- ARCHITECTURE.md
|- CONTRIBUTING.md
|- README.md
\- requirements.txt
```

## Python Layer

### `src\studio\config.py`

This file defines the repository-root-relative paths used by the rest of the Python modules. It is the source of truth for:

- `DATA_DIR`
- `VIDEOS_DIR`
- `RAW_ASSETS_DIR`
- `PROCESSED_ASSETS_DIR`
- `ENGINE_DIR`
- `LOGS_DIR`
- `OUTPUT_DIR`
- `REACT_COMPONENTS_DIR`

### `src\studio\cli.py`

The unified CLI is exposed as:

```powershell
python -m src.studio.cli --help
```

Current top-level commands are:

- `build`
- `render`
- `clean`
- `thumbnail`
- `metadata`
- `validate`
- `assets build`

The stable documented workflow uses `build`, `validate`, `assets build`, `render`, and `thumbnail`.

### Generators

The generators create and materialize video payloads into `data\videos\` and maintain the manifest files in `data\`.

### Render Adapters

`src\studio\render\render_single.py` and `src\studio\render\render_all.py` bridge the Python CLI to Remotion. Important behavior in the current implementation:

- `render_single.py` sets `REMOTION_VIDEO_ID` so the engine knows which payload to load.
- `NODE_OPTIONS` is set to `--max-old-space-size=14336`.
- Render concurrency is fixed to `10` in the Python command as well as in the Remotion config.
- Temporary Remotion and Chrome profile directories are cleaned after renders.

## SVG Asset Pipeline

### Entrypoints

Use either of these commands:

```powershell
python build_assets.py
python -m src.studio.cli assets build
```

`build_assets.py` is a thin wrapper around `src\studio\assets\toolchain.py`.

### Asset Specs

The current asset catalog in `ASSET_SPECS` is:

- `BackgroundCyber`
- `BackgroundSunset`
- `CharacterAngry`
- `CharacterGeek`
- `CharacterHappy`
- `CharacterSad`
- `PropDeclarativeRobot`
- `PropDeclarativeSaturn`
- `PropServer`
- `PropTelescope`

### Asset Stages

1. Python builder writes a raw SVG to `data\assets\raw\`.
2. Inkscape CLI exports a normalized SVG to `data\assets\processed\`.
3. Optional SVGO optimization runs through `npx svgo`.
4. The transpiler writes React components to `engine\src\components\generated\`.
5. `index.ts` is regenerated to export the generated components.

### Inkscape Integration

The toolchain searches for Inkscape in `PATH` and common Windows install locations such as `C:\Program Files\Inkscape\bin\inkscape.exe`.

By default, the toolchain opens the processed SVG in the Inkscape GUI after export. Use `--no-view` when you want a headless batch run.

## Remotion Layer

### Engine Layout

The React engine in `engine\src\` contains:

- reusable components
- generated SVG wrappers
- scene factories and scene-specific visual logic
- motion and effect helpers
- generated video manifest data used during render selection

### Render Configuration

`engine\remotion.config.js` currently configures the renderer to:

- allow `@` alias imports into `engine\src\`
- render JPEG intermediate frames
- mute the output by default
- use concurrency `10`
- request hardware acceleration when possible
- use Chromium ANGLE rendering
- point to `engine\remotion-binaries-nvenc\`
- force `h264_nvenc` for the FFmpeg stitcher step
- emit verbose logs so encoder selection is visible in terminal transcripts

### Local-Only Binary Override

The NVENC binary directory is intentionally local-only. It is excluded from Git because the FFmpeg binaries are large. When cloning the repository onto a new Windows machine, recreate `engine\remotion-binaries-nvenc\` locally before attempting GPU renders.

## Data Flow

```text
presets/raw topics or library inputs
        |
        v
python -m src.studio.cli build --materialize
        |
        v
data/videos/*.json + data/video_manifest.json
        |
        +--> python build_assets.py
        |         |
        |         v
        |   data/assets/raw/*.svg
        |         |
        |         v
        |   data/assets/processed/*.svg
        |         |
        |         v
        |   engine/src/components/generated/*.tsx
        |
        v
python -m src.studio.cli render video_503
        |
        v
output/*.mp4
        |
        v
examples/video/*.mp4
```

## Operational Notes

- `engine\build\` and `engine\remotion-binaries-nvenc\` are local artifacts and are not committed.
- `output\` and `examples\video\` contain example outputs that document current render capabilities.
- The repo is most predictable when commands are run from the repository root in PowerShell.

## Recommended Reading Order

1. `README.md`
2. `docs\SETUP_GUIDE.md`
3. `docs\ASSET_PRODUCTION_GUIDE.md`
4. `CONTRIBUTING.md`
