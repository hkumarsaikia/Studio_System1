# Studio_System1

Studio_System1 is a Windows-first video pipeline that combines Python data generation, an Inkscape-backed SVG asset workflow, and a Remotion/React renderer for final MP4 output.

## What This Repository Contains

- A unified Python CLI for building video payloads, validating the data set, exporting thumbnails, and launching renders.
- An SVG asset toolchain that generates source SVGs from Python, normalizes them through Inkscape, and transpiles them into React components.
- A Remotion engine with local NVENC support for NVIDIA GPU accelerated H.264 renders.
- Example rendered outputs under `output\` and `examples\video\`.

## Documentation Map

- `README.md` - project overview and fast start.
- `ARCHITECTURE.md` - high-level system summary.
- `docs\ARCHITECTURE.md` - detailed subsystem and data flow reference.
- `docs\SETUP_GUIDE.md` - Windows clone and setup instructions.
- `docs\ASSET_PRODUCTION_GUIDE.md` - SVG, Inkscape, and generated component workflow.
- `CONTRIBUTING.md` - contributor workflow and verification checklist.

## Requirements

- Windows 10 or Windows 11
- Git
- Python 3.12+
- Node.js 20+
- Inkscape installed locally
- Optional for GPU rendering: NVENC-capable `ffmpeg.exe` and `ffprobe.exe`

Install Python packages from `requirements.txt` and JavaScript packages from `engine\package.json`.

## Clone This Repository On Windows

```powershell
Set-Location C:\Users\hkuma
git clone https://github.com/hkumarsaikia/Studio_System1.git
Set-Location .\Studio_System1
```

If you want the mirror repository instead, clone `https://github.com/hkumarsaikia/Codex.git`.

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

If PowerShell blocks the virtual environment activation script, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
```

## Local NVENC Setup

The repository uses `engine\remotion.config.js` to point Remotion at `engine\remotion-binaries-nvenc`. That directory is intentionally ignored by Git because the local FFmpeg binaries are large.

Create the folder locally and copy a working Windows NVENC FFmpeg build into it:

```powershell
New-Item -ItemType Directory -Force .\engine\remotion-binaries-nvenc | Out-Null
Copy-Item .\engine\node_modules\@remotion\compositor-win32-x64-msvc\* .\engine\remotion-binaries-nvenc\ -Force
Copy-Item C:\path\to\nvenc\ffmpeg.exe .\engine\remotion-binaries-nvenc\ffmpeg.exe -Force
Copy-Item C:\path\to\nvenc\ffprobe.exe .\engine\remotion-binaries-nvenc\ffprobe.exe -Force
.\engine\remotion-binaries-nvenc\ffmpeg.exe -encoders | Select-String h264_nvenc
```

If you do not want GPU encoding, adjust `engine\remotion.config.js` before rendering.

## Core Commands

Build or refresh the video payload library:

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
```

Generate SVG assets and open them in Inkscape automatically:

```powershell
python build_assets.py
python build_assets.py --asset CharacterHappy
python build_assets.py --no-view
```

The equivalent unified CLI form is:

```powershell
python -m src.studio.cli assets build
python -m src.studio.cli assets build --asset CharacterHappy --no-view
```

Render a video from the current library:

```powershell
python -m src.studio.cli render video_503
python -m src.studio.cli thumbnail video_503 --frame 150
```

## Repository Layout

```text
Studio_System1/
|- data/
|  |- assets/
|  |  |- raw/
|  |  \- processed/
|  \- videos/
|- docs/
|- engine/
|  |- src/
|  \- remotion-binaries-nvenc/   # local only, not tracked
|- examples/
|  \- video/
|- output/
\- src/studio/
```

## Output Locations

- `data\assets\raw\` - Python-generated source SVGs.
- `data\assets\processed\` - Inkscape-normalized SVGs.
- `engine\src\components\generated\` - generated React wrappers for processed SVGs.
- `output\` - direct render outputs.
- `examples\video\` - copied showcase videos.

## Current Showcase Outputs

The repository already contains example outputs such as:

- `output\video_503_full_combined_nvenc_t10.mp4`
- `output\video_503_full_combined_inkscape_svg_nvenc_t10.mp4`
- `examples\video\combined_features_video_503_full.mp4`
- `examples\video\combined_features_video_503_inkscape_svg.mp4`

## Notes

- `build_assets.py` opens Inkscape automatically by default after processing each SVG. Use `--no-view` for headless runs.
- `engine\build\` and `engine\remotion-binaries-nvenc\` are intentionally excluded from Git.
- The documented stable workflow is `build`, `validate`, `assets build`, `render`, and `thumbnail` through `python -m src.studio.cli`, plus `python build_assets.py` for direct asset work.
