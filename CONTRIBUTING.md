# Contributing To Studio_System1

Use this guide when you are changing the Python pipeline, the SVG asset toolchain, or the Remotion engine.

## Before You Start

Read these files first:

- `README.md`
- `docs\SETUP_GUIDE.md`
- `docs\ARCHITECTURE.md`
- `docs\ASSET_PRODUCTION_GUIDE.md`

## Local Setup

Follow `docs\SETUP_GUIDE.md` for the supported Windows setup. Contributors are expected to work from the repository root in PowerShell.

## Repository Structure

The most important areas are:

- `src\studio\` - Python CLI, data generators, asset builders, render adapters, and utilities.
- `data\assets\` - raw and processed SVG assets.
- `engine\src\` - Remotion, React, scene logic, generated asset wrappers, and effect components.
- `docs\` - operational and architecture documentation.

## Contributor Workflow

1. Branch from `main`.
2. Make the source changes.
3. Regenerate any derived files that belong to those changes.
4. Run the relevant verification steps.
5. Commit the source and generated outputs together when they are part of the feature.

## Verification Checklist

Run the checks that match your change:

```powershell
python -m src.studio.cli validate
python build_assets.py --no-view
Set-Location .\engine
npx tsc --noEmit
Set-Location ..
```

If you changed render behavior, also run a representative render such as:

```powershell
python -m src.studio.cli render video_503
```

## Rules For Asset Changes

When you add or change an SVG-backed asset:

1. Update the relevant builder in `src\studio\assets\`.
2. Register the asset in `src\studio\assets\toolchain.py` if it is a new asset.
3. Regenerate the raw SVG, processed SVG, and generated React component.
4. Confirm `engine\src\components\generated\index.ts` exports the component.

## Rules For Render Changes

- Keep Windows paths relative to the repository root through `src\studio\config.py` or local Node path utilities.
- Do not hardcode machine-specific absolute paths into tracked source files.
- Document any new local dependency or manual setup step in `README.md` and `docs\SETUP_GUIDE.md`.

## Git Hygiene

- Do not commit machine-specific secrets.
- Do not add `engine\remotion-binaries-nvenc\` to Git. It is intentionally local-only.
- Do not add `engine\build\` to Git.
- Keep example videos only when they are intentional artifacts for the repository.

## Code Style

### Python

- Keep path handling centralized through `pathlib` and `src\studio\config.py`.
- Prefer clear module boundaries over ad hoc scripts.
- Keep command-line behavior aligned with `python -m src.studio.cli` and `python build_assets.py`.

### TypeScript And React

- Keep generated components in `engine\src\components\generated\` machine-generated.
- Keep reusable scene and effect logic in dedicated engine modules instead of one-off inline code.
- Run `npx tsc --noEmit` after TypeScript changes.

## Pull Requests

A good pull request should include:

- what changed
- why the change was needed
- which commands were used to verify it
- any new setup requirement if the workflow changed
