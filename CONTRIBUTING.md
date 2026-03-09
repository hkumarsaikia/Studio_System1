# Contributing To Studio_System1

Use this guide when you are changing the storyboard compiler, the SVG asset toolchain, or the Remotion engine.

## Before You Start

Read these files first:

- `README.md`
- `docs/SETUP_GUIDE.md`
- `docs/ARCHITECTURE.md`
- `docs/ASSET_PRODUCTION_GUIDE.md`

## Local Setup

Follow `docs/SETUP_GUIDE.md` for the supported Windows setup. Contributors are expected to work from the repository root in PowerShell.

## Repository Structure

The most important areas are:

- `src/studio/` - Python CLI, storyboard generation, validation, metadata, asset builders, and render adapters
- `data/storyboards/` - canonical production storyboard JSON
- `data/topic_catalog.json` - normalized topic catalog derived from `data/raw/Topics.txt`
- `data/asset_registry.json` - canonical SVG asset catalog and readiness map
- `data/videos/<profile_id>/` - compiled production payload JSON per render profile
- `data/demos/` - showcase/demo payload JSON
- `data/assets/` - raw and processed SVG assets
- `engine/src/` - Remotion, React, generated asset wrappers, scene logic, and effect components
- `docs/` - operational and architecture documentation

## Contributor Workflow

1. branch from `main`
2. make the source changes
3. regenerate any derived files that belong to the change
4. run the relevant verification steps
5. commit the source and generated outputs together when they are part of the feature

## Verification Checklist

Run the checks that match your change:

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
python build_assets.py --no-view
python .\scripts\generate_repo_knowledge_graph.py
Set-Location .\engine
npx tsc --noEmit
Set-Location ..
```

If you changed production render behavior, also run a representative render such as:

```powershell
python -m src.studio.cli render video_002 --profile shorts_vertical
python -m src.studio.cli render video_010 --profile shorts_vertical_30s
python -m src.studio.cli render video_002 --all-profiles
```

If you changed metadata generation, also verify:

```powershell
python -m src.studio.cli metadata video_002
```

## Rules For Storyboard And Data Changes

- Keep `data/storyboards/` as the canonical authoring source.
- Do not hand-edit `data/videos/<profile_id>/` unless you are deliberately debugging compiled output.
- Do not place demo payloads under `data/videos/`.
- Do not reuse production IDs for demo content.
- Use `--force-storyboards` only when you intentionally want to regenerate existing storyboard skeletons.
- Keep `data/topic_catalog.json`, `data/render_profiles.json`, `data/scene_grammar_registry.json`, `data/asset_registry.json`, and `data/asset_coverage.json` in sync with `build --materialize`.
- Default `build --materialize` writes the three primary production profiles; optional profiles such as `shorts_vertical_30s` are materialized on demand.

## Rules For Asset Changes

When you add or change an SVG-backed asset:

1. update the relevant builder in `src/studio/assets/`
2. register or classify the asset in `src/studio/assets/catalog.py` and `src/studio/assets/toolchain.py` if it is new
3. regenerate the raw SVG, processed SVG, and generated React component
4. confirm `engine/src/components/generated/index.ts` exports the component
5. confirm `data/asset_registry.json` and `data/asset_coverage.json` refresh and still validate against storyboard references

## Rules For Render Changes

- Keep path handling centralized through `src/studio/config.py` or local Node path utilities.
- Do not hardcode machine-specific absolute paths into tracked source files.
- Keep production rendering segment-first unless you are intentionally changing the architecture.
- Document any new local dependency or workflow change in `README.md` and `docs/SETUP_GUIDE.md`.

## Git Hygiene

- do not commit machine-specific secrets
- do not add `engine/remotion-binaries-nvenc/` to Git
- do not add `engine/build/` to Git
- keep example videos only when they are intentional repository artifacts

## Code Style

### Python

- keep shared production rules in `src/studio/contracts.py`
- keep path handling centralized through `pathlib` and `src/studio/config.py`
- prefer generation and validation logic in modules, not ad hoc scripts
- keep command behavior aligned with `python -m src.studio.cli`

### TypeScript And React

- keep generated components in `engine/src/components/generated/` machine-generated
- keep reusable scene and effect logic in dedicated modules instead of inline duplication
- run `npx tsc --noEmit` after engine changes

## Pull Requests

A good pull request should include:

- what changed
- why the change was needed
- which commands were used to verify it
- any new setup requirement if the workflow changed
