# Studio_System1

Studio_System1 is a storyboard-first YouTube Shorts engine for Windows. The repository generates 2-minute vertical Shorts as code-driven animations, using Python to materialize structured storyboards and Remotion to render the final MP4.

## Production Model

The production path is fixed and explicit:

- `video_001` through `video_500` are reserved for production Shorts.
- Every production Short is `1080x1920`, `30fps`, `120` seconds long.
- Every production Short contains `12` independent segments.
- Every segment is `10` seconds and compiles to `300` frames.
- `data/storyboards/` is the canonical editable source of truth.
- `data/videos/` contains compiled production payloads only.
- `data/demos/` contains showcase and demo payloads only.

This means the authoring model is storyboard first, render payload second.

## What The Repository Does

- Reads topic ideas from `data/raw/Topics.txt`.
- Creates missing production storyboard skeletons in `data/storyboards/`.
- Preserves existing storyboard files unless you explicitly force regeneration.
- Compiles storyboards into render payloads in `data/videos/`.
- Validates storyboards, compiled payloads, and manifests with JSON schema.
- Builds SVG assets through an Inkscape-backed pipeline.
- Renders production videos segment-by-segment, then stitches the `12` MP4 segments into one final Short.
- Renders demo IDs separately from `data/demos/`.
- Generates deterministic YouTube metadata JSON from storyboard content.

## Documentation Map

- `README.md` - overview and fast-start commands.
- `ARCHITECTURE.md` - short architecture summary.
- `docs/ARCHITECTURE.md` - detailed system and data flow reference.
- `docs/SETUP_GUIDE.md` - Windows clone and setup instructions.
- `docs/ASSET_PRODUCTION_GUIDE.md` - SVG and Inkscape workflow.
- `docs/FINAL_TASK_PLAN.md` - current implemented platform plan and next steps.
- `docs/KNOWLEDGE_GRAPH.md` - graph datasets, dashboard views, and Chrome Dev preview flow.
- `CONTRIBUTING.md` - contributor workflow and verification checklist.

## Requirements

- Windows 10 or Windows 11
- Git
- Python 3.12+
- Node.js 20+
- Inkscape
- Python packages from `requirements.txt`
- JavaScript packages from `engine/package.json`
- Optional for GPU stitching: NVENC-capable `ffmpeg.exe` and `ffprobe.exe`

## Clone This Repository On Windows

```powershell
Set-Location C:\Users\hkuma
git clone https://github.com/hkumarsaikia/Studio_System1.git
Set-Location .\Studio_System1
```

Mirror repository:

```powershell
git clone https://github.com/hkumarsaikia/Codex.git
```

## Windows Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Set-Location .\engine
npm install
Set-Location ..
```

If PowerShell blocks virtual environment activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
```

## Local NVENC Setup

The repository expects a local `engine/remotion-binaries-nvenc/` directory when you want NVIDIA GPU encoding during the FFmpeg stitch step.

```powershell
New-Item -ItemType Directory -Force .\engine\remotion-binaries-nvenc | Out-Null
Copy-Item .\engine\node_modules\@remotion\compositor-win32-x64-msvc\* .\engine\remotion-binaries-nvenc\ -Force
Copy-Item C:\path\to\nvenc\ffmpeg.exe .\engine\remotion-binaries-nvenc\ffmpeg.exe -Force
Copy-Item C:\path\to\nvenc\ffprobe.exe .\engine\remotion-binaries-nvenc\ffprobe.exe -Force
.\engine\remotion-binaries-nvenc\ffmpeg.exe -encoders | Select-String h264_nvenc
```

## Core Commands

Build or refresh the production library:

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
```

Force regeneration of storyboard skeletons only when you intentionally want to overwrite authoring files:

```powershell
python -m src.studio.cli build --materialize --force-storyboards
```

Generate metadata:

```powershell
python -m src.studio.cli metadata video_002
python -m src.studio.cli metadata --all
```

Build SVG assets and open them in Inkscape automatically:

```powershell
python build_assets.py
python build_assets.py --asset CharacterHappy
python build_assets.py --no-view
```

Equivalent unified CLI form:

```powershell
python -m src.studio.cli assets build
python -m src.studio.cli assets build --asset BackgroundCyber --no-view
```

Render a production Short:

```powershell
python -m src.studio.cli render video_002
```

Render a demo payload:

```powershell
python -m src.studio.cli render demo_graphics_showcase_v2
```

Export a thumbnail:

```powershell
python -m src.studio.cli thumbnail video_002 --frame 150
```

## Repository Layout

```text
Studio_System1/
|- data/
|  |- archive/
|  |- assets/
|  |  |- raw/
|  |  \- processed/
|  |- demos/
|  |- raw/
|  |- storyboards/
|  |- videos/
|  |- asset_library.json
|  |- asset_requirements_500.json
|  |- demo_manifest.json
|  \- video_manifest.json
|- docs/
|- engine/
|  |- src/
|  \- remotion-binaries-nvenc/   # local only, not tracked
|- examples/
|  \- video/
|- logs/
|- output/
|  |- metadata/
|  \- segments/
\- src/studio/
```

## Output Locations

- `data/storyboards/` - canonical production storyboard JSON.
- `data/videos/` - compiled production render payload JSON.
- `data/demos/` - showcase and demo payload JSON.
- `data/asset_library.json` - stable asset ID catalog used by storyboards.
- `output/segments/<video_id>/` - per-segment MP4s for production renders.
- `output/<video_id>.mp4` - stitched final production render.
- `output/metadata/<video_id>.json` - generated YouTube metadata.
- `examples/video/` - saved example copies.

## Verified State

The current implementation has been verified with:

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
python -m src.studio.cli metadata video_002
Set-Location .\engine
npx tsc --noEmit
Set-Location ..
python -m src.studio.cli render video_002
```

`video_002` currently renders through the segment-first production path and stitches to a final `120.000000` second MP4.

## Notes

- Existing storyboard files are preserved unless `--force-storyboards` is supplied.
- `build_assets.py` opens Inkscape automatically by default. Use `--no-view` for headless runs.
- `engine/build/` and `engine/remotion-binaries-nvenc/` are intentionally excluded from Git.
- Demo IDs must use the `demo_*` namespace and do not count toward the 500 production Shorts.

## Knowledge Graph Dashboard

Regenerate the graph suite and open the standalone dashboard in Google Chrome Dev:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\open_knowledge_graph_preview.ps1
```

The dashboard lives in `tools/knowledge-graph-viewer/` and loads graph data from `data/knowledge-graph/`.
