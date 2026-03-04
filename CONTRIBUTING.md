# Contributing to Studio_System1

First off, thank you for considering contributing to Studio_System1! This pipeline powers a highly scalable automated rendering engine. We welcome contributions that improve stability, extend component libraries, or optimize render times.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, make one! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

## 2. Setting up your environment

Please refer to `docs/SETUP_GUIDE.md` for a complete environment setup. You will need Node.js, Python 3.12+, and FFmpeg.

## 3. Architecture Overview

Before contributing code, please read `docs/ARCHITECTURE.md`. The project is divided into:
- **`studio.py`**: The unified CLI.
- **`scripts/`**: Python logistics (building payloads, triggering renders).
- **`engine/`**: The Remotion React-based rendering engine.

## 4. Submitting Changes

1. Fork the repo and create your branch from `main`.
2. Do not use hardcoded absolute system paths (e.g. `C:\tools\ffmpeg`). Use `shutil.which` or rely on the `PATH` environment variable.
3. Ensure no unneeded files are tracked (respect `.gitignore`).
4. Issue that pull request!

## 5. Coding Conventions

- **Python**: Standard library only where possible. Automation should run natively without complex pip dependencies.
- **Node/React/Remotion**: Strict functional components. Components in `engine/src/components/` must be highly reusable, parametric SVG components. No heavy external visual assets unless required.
- **JSON**: Modifications to the video schemas must be verified against `scripts/templates/master_schema.json`.
