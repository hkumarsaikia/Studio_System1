# Asset Production Guide

This guide describes the current SVG production workflow in Studio_System1.

## Source Of Truth

The source of truth for generated SVG assets is the Python toolchain under `src\studio\assets\`. The repository does not treat hand-authored static SVG files as the primary asset system.

## Entrypoints

Use either of these commands from the repository root:

```powershell
python build_assets.py
python -m src.studio.cli assets build
```

`build_assets.py` is the direct entrypoint and is the simplest command when you are actively iterating on SVGs.

## What The Pipeline Does

For each asset in `ASSET_SPECS`, the pipeline:

1. Builds a raw SVG with Python.
2. Saves the raw file to `data\assets\raw\`.
3. Runs Inkscape CLI to normalize the SVG.
4. Saves the processed file to `data\assets\processed\`.
5. Optionally runs SVGO through `npx svgo`.
6. Transpiles the processed SVG into a React component in `engine\src\components\generated\`.
7. Regenerates `engine\src\components\generated\index.ts`.

## Inkscape Behavior

Inkscape opens automatically after each processed SVG is written. That is the default behavior on purpose so the generated result is immediately visible while you are working.

Use `--no-view` only when you want a headless run:

```powershell
python build_assets.py --no-view
```

## Current Asset Catalog

The active assets registered in `src\studio\assets\toolchain.py` are:

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

## Useful Commands

Build everything and open Inkscape for each asset:

```powershell
python build_assets.py
```

Build only one asset:

```powershell
python build_assets.py --asset CharacterHappy
```

Build multiple named assets:

```powershell
python build_assets.py --asset BackgroundCyber --asset PropServer
```

Skip the SVGO pass:

```powershell
python build_assets.py --no-optimize
```

Use the unified CLI form instead:

```powershell
python -m src.studio.cli assets build --asset BackgroundCyber --no-view
```

## Output Directories

- `data\assets\raw\` - raw Python-generated SVG files.
- `data\assets\processed\` - Inkscape-normalized SVG files.
- `engine\src\components\generated\` - React components generated from processed SVGs.

## Adding A New SVG Asset

1. Decide whether the asset fits an existing builder or needs a new builder.
2. Add or update the builder under `src\studio\assets\`.
3. Register the asset in `ASSET_SPECS` inside `src\studio\assets\toolchain.py`.
4. Run `python build_assets.py --asset YourAssetName`.
5. Confirm the raw SVG, processed SVG, and generated React component were all produced.
6. Use the generated component from `engine\src\components\generated\` inside a scene or showcase component.

## Validation Checklist

After generating or changing assets, verify:

- the raw SVG exists in `data\assets\raw\`
- the processed SVG exists in `data\assets\processed\`
- the React wrapper exists in `engine\src\components\generated\`
- `index.ts` exports the new component
- the asset renders correctly inside the target video or showcase scene

## Operational Notes

- Inkscape must be installed locally for the pipeline to work.
- The toolchain searches `PATH` first and then common Windows install paths.
- The generated React component directory is part of the repository, so asset generation changes should be committed together with the corresponding source changes.
