# Setup Guide — Running Studio_System1 on a New Laptop

This guide walks through setting up the entire Studio_System1 video rendering pipeline from scratch on a fresh Windows machine.

---

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| **Windows** | 10 or 11 | Operating system |
| **Git** | Latest | Clone the repository |
| **Python** | 3.12.0 | Automation scripts (build library, render, metadata) |
| **Node.js** | LTS (v20+) | Remotion video engine |
| **ffmpeg** | Latest | Video encoding (used by Remotion) |

---

## Step 1 — Install Required Software

Open **Windows PowerShell** (`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`) and run:

```powershell
# Install Git
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements

# Install Python 3.12.0
winget install --id Python.Python.3.12 -v 3.12.0 -e --silent --accept-package-agreements --accept-source-agreements

# Install Node.js LTS
winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements

# Install ffmpeg
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
```

> **Important**: After installing, close and reopen PowerShell so the new PATH entries take effect.

---

## Step 2 — Clone the Repository

```powershell
cd C:\Users\YourUsername
git clone https://github.com/hkumarsaikia/Studio_System1.git
cd Studio_System1
```

---

## Step 3 — Create a Python Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> The project uses only Python standard library modules, so no `pip install` is needed. The `requirements.txt` file documents this.

---

## Step 4 — Install Node.js Dependencies

```powershell
cd engine
npm install
cd ..
```

This installs Remotion, React, and all rendering dependencies listed in `engine/package.json`.

---

## Step 5 — Generate the Video Library

```powershell
python automation/build_topic_library.py --materialize
```

This creates:
- `data/videos/video_001.json` through `video_500.json` (500 video data files)
- `data/video_manifest.json`
- `engine/src/generated/videoManifest.js`

---

## Step 6 — Start the Engineering Logger

Before working, activate the logging system:

```powershell
. .\start-logging.ps1
```

This records all terminal activity to `engineering.log`.

---

## Step 7 — Render a Video

```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Render a single video
python automation/render.py video_001

# Render with custom quality (lower CRF = better quality, bigger file)
python automation/render.py video_001 --crf 15
```

Output is saved to `output/video_001.mp4`.

> **Note**: The first render will download a headless Chrome browser (~150 MB) for Remotion. This only happens once.

---

## Step 8 — Batch Render (Optional)

```powershell
# Render all 500 videos
python automation/render_all.py

# Smoke test — render first 5
python automation/render_all.py --limit 5

# Resume from a specific video
python automation/render_all.py --start-from video_120
```

---

## Step 9 — Generate Metadata & Thumbnails (Optional)

```powershell
# Generate YouTube metadata for one video
python automation/metadata_generator.py --video-id video_001

# Export thumbnail
python automation/export_thumbnail.py video_001 --frame 150
```

---

## Step 10 — Deactivate When Done

```powershell
deactivate
```

---

## Troubleshooting

### `npx` / `node` / `npm` not recognized
Your PATH may not include Node.js. Either:
- Restart PowerShell after installing Node.js, or
- Manually add to PATH: `$env:Path = "C:\Program Files\nodejs;" + $env:Path`

### `python` not recognized
Either:
- Restart PowerShell after installing Python, or
- Use the full path: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\python.exe`

### `"crf" and "videoBitrate" can not both be set`
This has already been fixed in `engine/remotion.config.js`. If you see this error, ensure you have the latest version of the repo.

### ffmpeg not found during render
The render script auto-discovers ffmpeg from the WinGet install path. If it still fails, add ffmpeg to PATH manually:
```powershell
$env:Path = "C:\path\to\ffmpeg\bin;" + $env:Path
```

### Script execution disabled
If PowerShell blocks `.ps1` scripts, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Project Structure

```
Studio_System1/
├── automation/           # Python automation scripts
│   ├── render.py         # Single-video renderer
│   ├── render_all.py     # Batch renderer
│   ├── build_topic_library.py  # Generates 500 video JSONs
│   ├── metadata_generator.py   # YouTube metadata
│   ├── export_thumbnail.py     # Thumbnail exporter
│   ├── validate_library.py     # Data integrity checker
│   └── logic/            # Shared logic (NarrativeEngine)
├── engine/               # Remotion video engine (Node.js)
│   ├── src/              # React/TypeScript components
│   ├── public/           # Static assets (SVGs, audio)
│   ├── package.json      # Node.js dependencies
│   └── remotion.config.js
├── data/                 # Video data and topics
│   ├── Topics.txt        # 500 topic list
│   ├── videos/           # Generated video JSON files
│   └── schema.json       # Master data schema
├── presets/              # Render presets (resolution, FPS)
├── output/               # Rendered videos (gitignored)
├── start-logging.ps1     # Engineering logger
├── render_wrapper.ps1    # Batch render wrapper with logging
├── requirements.txt      # Python dependencies (stdlib only)
├── SETUP_GUIDE.md        # This file
├── README.md             # Project overview
└── ARCHITECTURE.md       # System architecture docs
```
