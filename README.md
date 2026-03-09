# Studio_System1

Studio_System1 is a programmable media studio for code-driven explainers. Python owns the production pipeline, Remotion owns the visual engine, and SVG assets are managed through an Inkscape-backed toolchain.

The current delivery is profile-aware from the start:

- `shorts_vertical` -> `1080x1920` (`9:16`)
- `social_square` -> `1080x1080` (`1:1`)
- `youtube_horizontal` -> `1920x1080` (`16:9`)

An optional on-demand render profile is also available:

- `shorts_vertical_30s` -> `1080x1920` (`9:16`, `30s`)

Each production video remains a 2-minute, 12-scene systems explainer in v1. The authoring surface is now semantic and canonical, while profile-specific render payloads are derived artifacts.

## Operating Model

The repository now runs on five layers:

1. Topic source: `data/raw/Topics.txt`
2. Topic catalog: `data/topic_catalog.json`
3. Canonical storyboard: `data/storyboards/video_###.json`
4. Asset registry: `data/asset_registry.json`
5. Profile-specific compiled payloads: `data/videos/<profile_id>/video_###.json`

Demo payloads stay separate under `data/demos/`.

## Production Namespace

- `video_001` through `video_500` are production IDs.
- `demo_*` is the demo namespace.
- Production and demo IDs must not collide.

## What The Pipeline Does

- Parses `data/raw/Topics.txt` into `data/topic_catalog.json`.
- Writes `data/representative_topics.json` for engine/asset coverage planning.
- Preserves or migrates existing storyboards into the canonical `scenePlan` contract.
- Compiles each production storyboard into three default profile-specific payloads.
- Materializes optional profiles such as `shorts_vertical_30s` on demand during render.
- Writes a profile-aware production manifest to `data/video_manifest.json`.
- Writes `data/render_profiles.json` and `data/scene_grammar_registry.json`.
- Writes `data/asset_registry.json`, `data/asset_library.json`, and `data/asset_coverage.json`.
- Renders production videos segment-first and stitches the final MP4.
- Generates metadata packs in `output/metadata/`.

## Core Commands

Build and materialize the full library:

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
```

Limit build compilation to one profile when needed:

```powershell
python -m src.studio.cli build --materialize --profile social_square
```

Render one production video in one profile:

```powershell
python -m src.studio.cli render video_002 --profile social_square
python -m src.studio.cli render video_010 --profile shorts_vertical_30s
```

Render the full social matrix from one storyboard:

```powershell
python -m src.studio.cli render video_002 --all-profiles
```

Batch render production videos:

```powershell
python -m src.studio.cli render --all --profile shorts_vertical
python -m src.studio.cli render --all --all-profiles
```

Generate metadata packs:

```powershell
python -m src.studio.cli metadata video_002
python -m src.studio.cli metadata --all
```

Refresh the repository knowledge graph:

```powershell
python .\scripts\generate_repo_knowledge_graph.py
```

Build or refresh SVG assets:

```powershell
python build_assets.py
python build_assets.py --asset BackgroundCyber --no-optimize
python -m src.studio.cli assets build --asset CharacterHappy --no-view
```

Export thumbnails:

```powershell
python -m src.studio.cli thumbnail video_002 --profile shorts_vertical
python -m src.studio.cli thumbnail video_002 --all-profiles
```

## Repository Layout

```text
Studio_System1/
|- data/
|  |- archive/
|  |- assets/
|  |- demos/
|  |- raw/
|  |  \- Topics.txt
|  |- storyboards/
|  |- videos/
|  |  |- shorts_vertical/
|  |  |- social_square/
|  |  \- youtube_horizontal/
|  |- asset_coverage.json
|  |- asset_library.json
|  |- asset_registry.json
|  |- render_profiles.json
|  |- representative_topics.json
|  |- scene_grammar_registry.json
|  |- topic_catalog.json
|  \- video_manifest.json
|- docs/
|- engine/
|- examples/
|- output/
|  |- metadata/
|  |- segments/
|  |  |- shorts_vertical/
|  |  |- social_square/
|  |  \- youtube_horizontal/
|  |- shorts_vertical/
|  |- social_square/
|  \- youtube_horizontal/
\- src/studio/
```

`output/shorts_vertical_30s/` and `output/segments/shorts_vertical_30s/` appear on demand after the first `30s` render.

## Canonical Storyboard Shape

Each production storyboard contains:

- `id`
- `topicRef`
- `topic`
- `title`
- `category`
- `templateFamily`
- `defaultProfiles`
- `metadataHints`
- `audioMode`
- `scenePlan`

Each `scenePlan` entry contains:

- `sceneId`
- `label`
- `purpose`
- `narrationText`
- `onScreenText`
- `subtext`
- `visualGrammar`
- `assetRefs`
- `cameraIntent`
- `motion`
- `timingHints`
- `profileOverrides`

## Current Output Model

Compiled production payloads are profile-aware and include:

- `profileId`
- `width`
- `height`
- `aspectRatio`
- `timeline`
- `layoutProfile`
- `platformTargets`
- `scenes`

Rendered files are written to:

- `output/<profile_id>/<video_id>.mp4`
- `output/segments/<profile_id>/<video_id>/segment_01.mp4`
- `output/metadata/<video_id>.json`

## Asset System

The canonical asset catalog is now `data/asset_registry.json`.

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

The derived summary file `data/asset_library.json` remains available for compatibility, but validation now treats `data/asset_registry.json` as authoritative.

## Requirements

- Windows 10 or Windows 11
- Python 3.12+
- Node.js 20+
- Inkscape
- Git
- Python packages from `requirements.txt`
- JavaScript packages from `engine/package.json`
- Optional for stitching/perf: `ffmpeg.exe` and `ffprobe.exe`

## Verification Status

The current repository state has been verified with:

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli metadata video_002
python build_assets.py --no-view
python .\scripts\generate_repo_knowledge_graph.py
python -m src.studio.cli validate
python -m pytest tests\test_multiformat_refactor.py
Set-Location .\engine
npx tsc --noEmit
Set-Location ..
python -m src.studio.cli render video_001 --profile shorts_vertical
```

Verified render outputs:

- `output/shorts_vertical/video_001.mp4`

`shorts_vertical_30s` remains available as an on-demand render profile when you explicitly need a `30s` vertical cut.

## Docs Map

- `README.md` - overview and operator commands
- `ARCHITECTURE.md` - short architecture summary
- `docs/ARCHITECTURE.md` - full system reference
- `docs/ASSET_PRODUCTION_GUIDE.md` - SVG and registry workflow
- `docs/SETUP_GUIDE.md` - Windows setup
- `docs/KNOWLEDGE_GRAPH.md` - repository graph datasets and dashboard
