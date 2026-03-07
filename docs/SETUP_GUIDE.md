# Windows Setup Guide

This guide describes the current supported setup for cloning and running Studio_System1 on Windows.

## 1. Install Required Software

Open Windows PowerShell and install the base tools you need:

```powershell
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements
winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
winget install --id OpenJS.NodeJS.LTS -e --accept-package-agreements --accept-source-agreements
winget install --id Inkscape.Inkscape -e --accept-package-agreements --accept-source-agreements
```

Optional tools:

- A Windows FFmpeg build with `h264_nvenc` support.
- GitHub CLI if you want to create repos or push from authenticated scripts.

Reopen PowerShell after installation so `git`, `python`, `npm`, and `inkscape` are available on `PATH`.

## 2. Clone The Repository On Windows

```powershell
Set-Location C:\Users\hkuma
git clone https://github.com/hkumarsaikia/Studio_System1.git
Set-Location .\Studio_System1
```

If you prefer the mirror, use `https://github.com/hkumarsaikia/Codex.git` instead.

## 3. Create And Activate A Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If script execution is blocked, run this once and reopen PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
```

## 4. Install Engine Dependencies

```powershell
Set-Location .\engine
npm install
Set-Location ..
```

## 5. Prepare Local NVENC Binaries

The current Remotion configuration expects a local `engine\remotion-binaries-nvenc\` directory.

```powershell
New-Item -ItemType Directory -Force .\engine\remotion-binaries-nvenc | Out-Null
Copy-Item .\engine\node_modules\@remotion\compositor-win32-x64-msvc\* .\engine\remotion-binaries-nvenc\ -Force
Copy-Item C:\path\to\nvenc\ffmpeg.exe .\engine\remotion-binaries-nvenc\ffmpeg.exe -Force
Copy-Item C:\path\to\nvenc\ffprobe.exe .\engine\remotion-binaries-nvenc\ffprobe.exe -Force
.\engine\remotion-binaries-nvenc\ffmpeg.exe -encoders | Select-String h264_nvenc
```

If the last command does not show `h264_nvenc`, replace the FFmpeg build with one that supports NVIDIA NVENC.

## 6. Build The Video Library

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
```

## 6a. Generate a Single YouTube Short

The `shorts` command chains topic selection, payload generation, validation, and optional rendering:

```powershell
python -m src.studio.cli shorts --topic-index 42
python -m src.studio.cli shorts --random
python -m src.studio.cli shorts --topic-index 42 --render
```

## 7. Build SVG Assets

`build_assets.py` opens Inkscape automatically by default.

```powershell
python build_assets.py
```

Useful variations:

```powershell
python build_assets.py --asset CharacterHappy
python build_assets.py --no-view
python -m src.studio.cli assets build --asset BackgroundCyber --no-view
```

## 8. Render A Video

```powershell
python -m src.studio.cli render video_503
```

Optional thumbnail export:

```powershell
python -m src.studio.cli thumbnail video_503 --frame 150
```

Expected output locations:

- `output\video_503.mp4`
- `output\*.png` for thumbnails when exported

## 9. Save An Example Copy

If you want a stable example copy in the repository, copy the final render into `examples\video\`:

```powershell
New-Item -ItemType Directory -Force .\examples\video | Out-Null
Copy-Item .\output\video_503.mp4 .\examples\video\combined_features_video_503_latest.mp4 -Force
```

## Troubleshooting

### `inkscape` not found

Make sure Inkscape is installed and available on `PATH`, or install it into the default Windows location under `C:\Program Files\Inkscape\`.

### `Unknown encoder 'h264_nvenc'`

Your active FFmpeg binary does not support NVIDIA NVENC. Replace `engine\remotion-binaries-nvenc\ffmpeg.exe` and `ffprobe.exe` with a compatible build.

### `npx.cmd` not found

Reopen PowerShell after installing Node.js. If it still fails, confirm `npm` and `npx.cmd` are on `PATH`.

### Virtual environment activation is blocked

Use the execution policy command from step 3.

### Renders fail immediately after cloning

The most likely cause is a missing `engine\remotion-binaries-nvenc\` directory. Recreate it locally before rendering.
