# Setup Guide — Running Studio_System1

This guide walks through setting up the entire Studio_System1 video rendering pipeline from scratch on a fresh Windows machine.

---

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------| 
| **Windows** | 10 or 11 | Operating system |
| **Git** | Latest | Clone the repository |
| **Python** | 3.12+ | Pipeline CLI and builders (`studio.py`) |
| **Node.js** | LTS (v20+) | Remotion video engine |
| **ffmpeg** | Latest | Video encoding (used by Remotion) |

---

## Step 1 — Install Required Software

Open **Windows PowerShell** and run:

```powershell
# Install Git
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements

# Install Python 3.12
winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements

# Install Node.js LTS
winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements

# Install ffmpeg
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
```

> **Important**: After installing, close and reopen PowerShell so the new PATH entries take effect.

---

## Step 2 — Fix PowerShell Execution Policy

If PowerShell blocks `.ps1` scripts, run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

---

## Step 3 — Clone the Repository

```powershell
cd C:\Users\YourUsername
git clone https://github.com/hkumarsaikia/Studio_System1.git
cd Studio_System1
```

---

## Step 4 — Create a Python Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> The project uses only Python standard library modules, so no `pip install` is needed.

---

## Step 5 — Install Node.js Dependencies

```powershell
cd engine
npm install
cd ..
```

This installs all required packages including:
- **Remotion 4** — Video rendering engine
- **polished** — Dynamic color manipulation (darken, lighten, transparentize)
- **lucide-react** — High-quality icon library
- **D3.js** — Data visualization and geographic projections
- **p5.js** — Generative art and procedural animations
- **framer-motion** / **@react-spring/web** — Animation libraries
- **@tsparticles** — Particle system for network backgrounds
- **SVGO** — SVG optimization

---

## Step 6 — Generate the Video Library

```powershell
python studio.py build --materialize
```

This creates 500 video payload JSON files inside `data/videos/`.

---

## Step 7 — Verify Library Integrity

```powershell
python studio.py validate
```

Expected output: `Library validation passed` with visual distribution stats.

---

## Step 8 — Start the Engineering Logger

Before working, activate the logging automatically by opening a terminal via the VS Code "Studio Logger" profile or by running `StudioShell.bat` from File Explorer. All commands and outputs will be securely recorded to `logs/engineering.log`.

---

## Step 9 — Render a Video

```powershell
# Render a single video
python studio.py render video_001

# Render with custom quality (lower CRF = better quality, bigger file)
python studio.py render video_001 --crf 15
```

> **Hardware Note**: Rendering a full 5-minute WebGL 3D video generates 9,000 frames. The engine is hardcoded to maximize system resources (`--max-old-space-size=14336` for 14GB RAM and 10 CPU concurrency threads) to prevent out-of-memory stalls. Close background applications before rendering.

Output is saved to `output/video_001.mp4`.

---

## Step 10 — Batch Render (Optional)

```powershell
# Smoke test — render first 5
python studio.py render --all --limit 5

# Render all 500 videos
python studio.py render --all

# Resume from a specific video
python studio.py render --all --start-from video_120
```

---

## Step 11 — Generate Metadata & Thumbnails (Optional)

```powershell
# Generate YouTube metadata for one video
python studio.py metadata video_001

# Export thumbnail
python studio.py thumbnail video_001 --frame 150
```

---

## Troubleshooting

### `npx` / `node` / `ffmpeg` not found
Your PATH may not include Node.js or ffmpeg. Restart PowerShell or manually add them to PATH. The system automatically scans the global PATH to resolve binaries via `shutil.which`.

### Script execution disabled
Run the command from Step 2 above.

### TypeScript `@/` import errors in IDE
Ensure `engine/tsconfig.json` contains `"baseUrl": "."` and `"paths": { "@/*": ["src/*"] }`. These are already configured — restart your IDE if errors persist.

### Python `ModuleNotFoundError: No module named 'scripts'`
Run all Python commands from the repository root directory (`Studio_System1/`), not from inside `scripts/`.
