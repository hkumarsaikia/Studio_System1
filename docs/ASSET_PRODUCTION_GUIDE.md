# Asset Production Guide

This guide describes the asset system in the profile-aware Studio_System1 pipeline.

## Canonical Asset Files

The asset layer now has three important outputs:

- `data/asset_registry.json` - authoritative asset catalog
- `data/asset_library.json` - grouped compatibility summary
- `data/asset_coverage.json` - per-video and per-profile coverage report

When you author or update scene instructions, `assetRefs` should be chosen from `data/asset_registry.json`.

## What The Asset Registry Contains

Each asset entry records:

- logical asset ID
- source type (`procedural` or `svg_component`)
- asset family
- tags
- allowed scene roles
- render target
- raw SVG path
- processed SVG path
- generated React component path
- readiness status

This makes the asset registry the operational source of truth for both storyboards and validation.

## Entrypoints

Use one of these commands from the repository root:

```powershell
python build_assets.py
python -m src.studio.cli assets build
```

## SVG Pipeline

For each asset in `ASSET_SPECS`, the toolchain:

1. generates a raw SVG in `data/assets/raw/`
2. normalizes it through Inkscape into `data/assets/processed/`
3. optionally runs SVGO
4. transpiles it into a React component in `engine/src/components/generated/`
5. regenerates `engine/src/components/generated/index.ts`
6. refreshes `data/asset_registry.json` and `data/asset_library.json`

## Procedural Graphics Architecture

Rather than using manual Illustrator files or Lucide icons, all Studio System SVGs are built procedurally using Python (`svgwrite`) in `src/studio/assets/generative_engine/`. 
The `ProceduralCanvas` automatically injects the following global advanced aesthetics:
- **Glassmorphism Base Tiles:** Translucent curve overlays
- **Radial Glow Gradients:** Deep luminous backgrounds
- **Dot Matrix Grid Backings:** Hex/Dot grid patterns for technical scenes
- **SVG 1.1 Drop Shadows:** `feComposite` and `feGaussianBlur` filtering for 3D depth
- **HUD Crosshairs & Tech Rings:** Generative mathematical frames
- **Metallic Linear Gradients:** Angled SVG strokes for 3D neon appearance

## Inkscape Behavior

Inkscape opens automatically after each processed SVG is written.

Use `--no-view` only when you want a headless run:

```powershell
python build_assets.py --no-view
```

## Storyboard Asset Refs

Storyboards use `assetRefs` in `scenePlan` entries. Those values are validated against `data/asset_registry.json`.

That means the correct asset workflow is:

1. create or update the asset builder
2. run the asset build command
3. confirm the asset is present and `ready` in `data/asset_registry.json`
4. reference the asset ID from storyboard `assetRefs`
5. run `python -m src.studio.cli build --materialize`
6. run `python -m src.studio.cli validate`

## Coverage Report

`data/asset_coverage.json` is generated during the production build and answers two practical questions:

- which assets are used by each video/profile
- which videos/scenes require each asset

Use it when you want to identify missing coverage before expanding the visual engine.

## Useful Commands

Build all assets and open Inkscape:

```powershell
python build_assets.py
```

Build one asset and skip SVGO:

```powershell
python build_assets.py --asset BackgroundCyber --no-optimize
```

Build multiple assets without opening the GUI:

```powershell
python -m src.studio.cli assets build --asset CharacterHappy --asset PropServer --no-view
```

## Output Paths

- `data/assets/raw/` - raw generated SVG files
- `data/assets/processed/` - Inkscape-normalized SVG files
- `engine/src/components/generated/` - generated React wrappers
- `data/asset_registry.json` - authoritative asset catalog
- `data/asset_library.json` - grouped asset summary
- `data/asset_coverage.json` - asset usage report

## Current Generated SVG Components

The generated SVG component set now has two parts:

- the catalog-derived asset surface generated from `src/studio/assets/catalog.py`
- the legacy compatibility components such as `BackgroundCyber`, `BackgroundSunset`, `CharacterAngry`, `CharacterGeek`, `CharacterHappy`, `CharacterSad`, `PropDeclarativeRobot`, `PropDeclarativeSaturn`, `PropServer`, and `PropTelescope`

Use `engine/src/components/generated/index.ts` as the authoritative export surface. The directory now includes the large catalog-backed wrapper set in addition to the legacy compatibility components.

## Validation Rules

Validation fails if any of these are true:

- a storyboard references an unknown `assetRefs` value
- a generated SVG asset is missing its raw SVG
- a generated SVG asset is missing its processed SVG
- a generated SVG asset is missing its generated React component
- an asset registry entry reports the wrong readiness status

## Recommended Routine

```powershell
python build_assets.py --asset BackgroundCyber --no-optimize
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
```

That sequence keeps the SVG source, asset registry, compiled payloads, and validation state aligned.
