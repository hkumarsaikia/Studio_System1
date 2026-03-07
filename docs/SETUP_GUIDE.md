# Windows Setup Guide

This guide describes the supported Windows setup for the storyboard-first version of Studio_System1.

## 1. Install Required Software

Open Windows PowerShell and install the base tools:

```powershell
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements
winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
winget install --id OpenJS.NodeJS.LTS -e --accept-package-agreements --accept-source-agreements
winget install --id Inkscape.Inkscape -e --accept-package-agreements --accept-source-agreements
```

Optional tools:

- GitHub CLI
- an FFmpeg build with `h264_nvenc`

Reopen PowerShell after installation so `git`, `python`, `npm`, and `inkscape` are available on `PATH`.

## 2. Clone The Repository On Windows

```powershell
Set-Location C:\Users\hkuma
git clone https://github.com/hkumarsaikia/Studio_System1.git
Set-Location .\Studio_System1
```

If you prefer the mirror:

```powershell
git clone https://github.com/hkumarsaikia/Codex.git
```

## 3. Create And Activate A Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If script execution is blocked:

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

The FFmpeg stitch step can use the local `engine/remotion-binaries-nvenc/` directory when you want NVIDIA GPU encoding.

```powershell
New-Item -ItemType Directory -Force .\engine\remotion-binaries-nvenc | Out-Null
Copy-Item .\engine\node_modules\@remotion\compositor-win32-x64-msvc\* .\engine\remotion-binaries-nvenc\ -Force
Copy-Item C:\path\to\nvenc\ffmpeg.exe .\engine\remotion-binaries-nvenc\ffmpeg.exe -Force
Copy-Item C:\path\to\nvenc\ffprobe.exe .\engine\remotion-binaries-nvenc\ffprobe.exe -Force
.\engine\remotion-binaries-nvenc\ffmpeg.exe -encoders | Select-String h264_nvenc
```

If the encoder list does not contain `h264_nvenc`, replace the FFmpeg build.

## 6. Materialize The Storyboard Library

```powershell
python -m src.studio.cli build --materialize
```

What this does:

- reads `data/raw/Topics.txt`
- creates missing storyboards in `data/storyboards/`
- compiles production payloads into `data/videos/`
- refreshes manifests and asset requirement files
- preserves existing storyboard files by default

If you intentionally want to regenerate storyboard skeletons:

```powershell
python -m src.studio.cli build --materialize --force-storyboards
```

## 7. Validate The Library

```powershell
python -m src.studio.cli validate
```

This checks:

- `500` production storyboards
- `500` compiled production payloads
- segment/frame rules
- visuals and asset references
- production/demo separation
- manifest consistency

## 8. Build SVG Assets

`build_assets.py` opens Inkscape automatically by default.

```powershell
python build_assets.py
```

Useful variants:

```powershell
python build_assets.py --asset CharacterHappy
python build_assets.py --no-view
python -m src.studio.cli assets build --asset BackgroundCyber --no-view
```

## 9. Generate Metadata

```powershell
python -m src.studio.cli metadata video_002
python -m src.studio.cli metadata --all
```

Outputs are written to `output/metadata/`.

## 10. Render A Production Short

```powershell
python -m src.studio.cli render video_002
```

Production behavior:

- renders `12` segment MP4 files into `output/segments/video_002/`
- stitches them into `output/video_002.mp4`

## 11. Render A Demo Payload

```powershell
python -m src.studio.cli render demo_graphics_showcase_v2
```

Demo payloads render directly from `data/demos/` and do not go through the production segment directory.

## 12. Export A Thumbnail

```powershell
python -m src.studio.cli thumbnail video_002 --frame 150
```

## 13. Save An Example Copy

If you want a stable example artifact inside the repository:

```powershell
New-Item -ItemType Directory -Force .\examples\video | Out-Null
Copy-Item .\output\video_002.mp4 .\examples\video\video_002_example.mp4 -Force
```

## Troubleshooting

### `inkscape` not found

Make sure Inkscape is installed and either on `PATH` or in the default Windows install location under `C:\Program Files\Inkscape\`.

### `Unknown encoder 'h264_nvenc'`

Your active FFmpeg binary does not support NVIDIA NVENC. Replace `engine/remotion-binaries-nvenc/ffmpeg.exe` and `ffprobe.exe` with a compatible build.

### `npx.cmd` not found

Reopen PowerShell after installing Node.js. If it still fails, confirm `npm` and `npx.cmd` are on `PATH`.

### Storyboards were not regenerated

That is expected. The build preserves existing storyboard files by default. Use `--force-storyboards` only when you intentionally want to replace them.

### A production render fails validation

Run `python -m src.studio.cli validate` and fix the storyboard or manifest issue before rendering again.
