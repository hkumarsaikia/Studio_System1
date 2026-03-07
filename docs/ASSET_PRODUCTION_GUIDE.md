# Asset Production Guide

This guide describes the SVG production workflow in the storyboard-first version of Studio_System1.

## Source Of Truth

The source of truth for generated SVG assets is the Python asset toolchain under `src/studio/assets/`. Storyboards reference stable `assetRefs`, and those references resolve against the generated asset library.

## Entrypoints

Use either of these commands from the repository root:

```powershell
python build_assets.py
python -m src.studio.cli assets build
```

`build_assets.py` is the direct asset entrypoint and is the simplest command when you are actively iterating on SVGs.

## What The Pipeline Does

For each asset in `ASSET_SPECS`, the pipeline:

1. builds a raw SVG with Python
2. writes the raw file to `data/assets/raw/`
3. runs Inkscape CLI to normalize the SVG
4. writes the processed file to `data/assets/processed/`
5. optionally runs SVGO through `npx svgo`
6. transpiles the processed SVG into a React component in `engine/src/components/generated/`
7. regenerates the generated component export index

## Inkscape Behavior

Inkscape opens automatically after each processed SVG is written. That is the default behavior on purpose so the generated result is immediately visible while you are working.

Use `--no-view` only when you want a headless run:

```powershell
python build_assets.py --no-view
```

## Current Asset Catalog

The active generated asset set includes:

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

The full resolved asset library for storyboard use is written to `data/asset_library.json`.

## Asset Refs In Storyboards

Production storyboard segments use `assetRefs` such as character, prop, or background IDs. The compiler validates those references against the known asset library before a render payload is produced.

That means the practical sequence is:

1. define or update the asset builder
2. build the SVG asset
3. confirm it appears in the generated asset library
4. reference it from storyboard `assetRefs`
5. rebuild and validate the production library

## Useful Commands

Build everything and open Inkscape for each asset:

```powershell
python build_assets.py
```

Build one asset:

```powershell
python build_assets.py --asset CharacterHappy
```

Build multiple assets:

```powershell
python build_assets.py --asset BackgroundCyber --asset PropServer
```

Skip the SVGO pass:

```powershell
python build_assets.py --no-optimize
```

Use the unified CLI form:

```powershell
python -m src.studio.cli assets build --asset BackgroundCyber --no-view
```

## Output Directories

- `data/assets/raw/` - raw Python-generated SVG files
- `data/assets/processed/` - Inkscape-normalized SVG files
- `engine/src/components/generated/` - generated React component wrappers
- `data/asset_library.json` - storyboard-facing asset ID catalog

## Adding A New SVG Asset

1. add or update the builder under `src/studio/assets/`
2. register the asset in `ASSET_SPECS` inside `src/studio/assets/toolchain.py`
3. run `python build_assets.py --asset YourAssetName`
4. confirm the raw SVG, processed SVG, and generated React component were all produced
5. confirm the asset is represented in `data/asset_library.json`
6. use the asset through storyboard `assetRefs` or scene props

## Validation Checklist

After generating or changing assets, verify:

- the raw SVG exists in `data/assets/raw/`
- the processed SVG exists in `data/assets/processed/`
- the React wrapper exists in `engine/src/components/generated/`
- `index.ts` exports the generated component
- `data/asset_library.json` reflects the asset set you expect
- `python -m src.studio.cli validate` still passes

## Operational Notes

- Inkscape must be installed locally.
- The toolchain searches `PATH` first and then common Windows install paths.
- Generated React components are repository artifacts and should be committed together with the corresponding source changes.
