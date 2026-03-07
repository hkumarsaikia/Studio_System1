# Studio_System1

Studio_System1 is an **automated YouTube Shorts animation engine** that converts structured instructions into animated vector graphics videos exported as MP4 files. Instead of editing videos manually, you provide segment instructions and the system generates the entire Short programmatically.

## How It Works

Each YouTube Short is a **120-second video** divided into **12 segments of 10 seconds each**. The engine:

1. **Selects a topic** from a database of 500 ideas in `data\raw\Topics.txt`.
2. **Generates a structured payload** with 12 segments, each containing narration, visual direction, and scene parameters.
3. **Renders animated vector graphics** using a Remotion/React engine with 30+ visual component types.
4. **Exports the final MP4** at 1080×1920 (9:16 vertical) resolution.

### The 12-Segment Structure

| Segment | Label | Visual | Purpose |
|---------|-------|--------|---------|
| 1 | Topic frame | Crowd | Title card introducing the topic |
| 2 | Hook | Icons | Why this topic matters |
| 3 | System boundary | Network | Define the scope |
| 4 | Cause layer 1 | Math equation | Primary driver |
| 5 | Cause layer 2 | Flow diagram | Secondary mechanisms |
| 6 | Cause layer 3 | Data lattice | Feedback loops |
| 7 | Data lens | Neural core | Statistical evidence |
| 8 | Real world scene | City backdrop | Ground-level impact |
| 9 | Ecology/externalities | Animals | Hidden costs |
| 10 | Macro trend | Globe | Future trajectory |
| 11 | Actionable takeaway | Icons | What you can do |
| 12 | Closing | Crowd | Final reflection |

Each segment produces exactly **300 frames at 30fps = 10 seconds**. The full Short is **3600 frames = 120 seconds**.

## Quick Start: Generate a YouTube Short

```powershell
# Generate a Short from topic #42 (builds payload, validates, prints summary)
python -m src.studio.cli shorts --topic-index 42

# Generate from a random topic
python -m src.studio.cli shorts --random

# Generate AND render to MP4
python -m src.studio.cli shorts --topic-index 42 --render
```

## Documentation Map

- `README.md` — project overview and quick start.
- `ARCHITECTURE.md` — high-level system summary.
- `docs\ARCHITECTURE.md` — detailed subsystem and data flow reference.
- `docs\SETUP_GUIDE.md` — Windows clone and setup instructions.
- `docs\ASSET_PRODUCTION_GUIDE.md` — SVG, Inkscape, and generated component workflow.
- `CONTRIBUTING.md` — contributor workflow and verification checklist.

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

Generate a YouTube Short from a single topic:

```powershell
python -m src.studio.cli shorts --topic-index 42
python -m src.studio.cli shorts --random
python -m src.studio.cli shorts --topic-index 42 --render
```

Build or refresh the full 500-video payload library:

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
|  |- raw/Topics.txt          # 500 topic ideas database
|  \- videos/                  # Generated 12-segment video JSONs
|- docs/
|- engine/
|  |- src/
|  \- remotion-binaries-nvenc/ # local only, not tracked
|- examples/
|  \- video/
|- output/
\- src/studio/
   |- generators/              # Topic library and narrative engine
   |- render/                  # Single and batch renderers
   |- assets/                  # SVG asset toolchain
   \- shorts_pipeline.py       # YouTube Shorts orchestrator
```

## Output Locations

- `data\assets\raw\` — Python-generated source SVGs.
- `data\assets\processed\` — Inkscape-normalized SVGs.
- `engine\src\components\generated\` — generated React wrappers for processed SVGs.
- `output\` — direct render outputs.
- `examples\video\` — copied showcase videos.

## Notes

- `build_assets.py` opens Inkscape automatically by default after processing each SVG. Use `--no-view` for headless runs.
- `engine\build\` and `engine\remotion-binaries-nvenc\` are intentionally excluded from Git.
- Each video payload contains 12 segments with `narration`, `visualDirection`, and `segmentIndex` fields for complete scene control.
- The `shorts` command chains topic selection → payload generation → validation → optional rendering in a single step.
