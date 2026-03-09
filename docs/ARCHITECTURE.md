# Detailed Architecture

Studio_System1 is now a multi-format programmable media studio. The repository keeps one canonical semantic storyboard per production ID and derives profile-specific render payloads for multiple social outputs.

## System Summary

The system is organized into five layers:

1. topic source
2. canonical storyboard authoring
3. SVG and procedural asset registry
4. render-profile compilation
5. derived render, metadata, and manifest outputs

The current first-class render profiles are:

- `shorts_vertical` -> `1080x1920`, `9:16`
- `social_square` -> `1080x1080`, `1:1`
- `youtube_horizontal` -> `1920x1080`, `16:9`

An optional on-demand render profile is also supported:

- `shorts_vertical_30s` -> `1080x1920`, `9:16`, `30s`

The three default production profiles share the same 12-scene, 120-second narrative plan. The optional `30s` profile keeps the same 12 scenes but compresses them to `2.5` seconds each.

## Canonical Data Model

### Topic Source

`data/raw/Topics.txt` remains the human-maintained input list.

Derived outputs:

- `data/topic_catalog.json`
- `data/representative_topics.json`

`data/topic_catalog.json` is the normalized machine-readable source that the rest of the build pipeline uses.

### Canonical Storyboards

`data/storyboards/video_###.json` is the editable source of truth for production videos.

Top-level storyboard fields:

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

Each `scenePlan` item includes:

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

This means authoring is semantic first. The storyboard describes what the scene means, which grammar it uses, and which assets are needed. The build pipeline decides how that becomes a concrete render payload for a given profile.

### Render Profiles

`src/studio/contracts.py` defines the canonical profile registry. The same registry is also materialized to `data/render_profiles.json`.

Each profile defines:

- `width`
- `height`
- `fps`
- `aspectRatio`
- `timeline`
- `platforms`
- `layout`

The `layout` section is the key bridge into the Remotion engine. It controls:

- padding
- title scale
- subtitle scale
- category scale
- visual scale
- text max width
- text alignment

### Compiled Payloads

Compiled payloads are derived JSON artifacts under:

- `data/videos/shorts_vertical/`
- `data/videos/social_square/`
- `data/videos/youtube_horizontal/`

Default `build --materialize` writes those three production profiles. Optional profiles such as `shorts_vertical_30s` are materialized on demand by the render flow when the payload is missing.

Compiled payload fields include:

- `profileId`
- `dataset`
- `templateFamily`
- `template`
- `width`
- `height`
- `aspectRatio`
- `timeline`
- `sceneCount`
- `totalDurationSeconds`
- `platformTargets`
- `layoutProfile`
- `scenes`

Each compiled scene contains render-ready fields like:

- `segmentId`
- `text`
- `duration`
- `visual`
- `visualGrammar`
- `assetTags`
- `layout`
- `profileId`

### Production Manifest

`data/video_manifest.json` now maps each production video to all of its compiled profile outputs.

Each production manifest entry includes:

- title/topic/category/template family metadata
- storyboard path
- `defaultProfiles`
- per-profile compiled payload path, dimensions, fps, scene count, duration, and aspect ratio

### Demo Payloads

Demo payloads remain on a compatibility path under `data/demos/` and `data/demo_manifest.json`.

The long-term direction is to unify demos under the same profile-aware loader model, but that was not required for this delivery.

## Asset System

### Canonical Asset Registry

`data/asset_registry.json` is now authoritative.

Each asset entry records:

- logical ID
- source type
- asset family
- tags
- allowed scene roles
- render target
- raw SVG path
- processed SVG path
- generated React component path
- readiness status

`data/asset_library.json` is still produced as a grouped compatibility summary, but it is no longer the validation source of truth.

### Coverage Report

`data/asset_coverage.json` is derived during build and records:

- which videos use which assets
- which profiles use which assets
- scene references for each asset
- per-video profile asset coverage

### SVG Toolchain

`python build_assets.py` or `python -m src.studio.cli assets build` runs the asset toolchain.

Stages:

1. generate raw SVGs
2. normalize through Inkscape
3. optionally optimize with SVGO
4. transpile to React components in `engine/src/components/generated/`
5. regenerate the asset registry outputs

The build now ties the SVG pipeline directly to the authoritative asset registry.

## Python Layer

### `src/studio/generators/topic_library.py`

This is the production compiler.

Responsibilities:

- parse topics
- build the topic catalog
- choose representative topics
- migrate old storyboard files to the new canonical shape
- preserve authored storyboards unless forced
- compile one storyboard into multiple profile payloads
- write manifests and registry files
- refresh the generated engine manifest loader
- migrate demos from legacy payloads
- archive stale flat `data/videos/video_###.json` payloads

### `src/studio/utils/validate.py`

Validation is profile-aware.

It checks:

- topic catalog integrity against `Topics.txt`
- storyboard schema and `scenePlan` shape
- valid profile IDs in `defaultProfiles` and `profileOverrides`
- valid `visualGrammar` values
- valid `assetRefs`
- asset registry completeness and generated SVG component paths
- presence and correctness of all compiled profile payloads
- manifest/file consistency across production and demos

### `src/studio/generators/metadata.py`

Metadata is now written as one pack per video with per-profile variants under `profiles`.

### `src/studio/render/`

`render_single.py` renders:

- one production video in one profile
- one production video in all profiles
- one demo video

Production renders are written to:

- `output/<profile_id>/<video_id>.mp4`
- `output/segments/<profile_id>/<video_id>/segment_01.mp4`

`REMOTION_PROFILE_ID` is now part of the render environment.

## Remotion Layer

### Loader

`engine/src/Root.tsx` now selects data by:

- dataset
- `video_id`
- `profile_id`

It passes `layoutProfile` into the template stack and still supports:

- `MainComposition`
- `SegmentComposition`
- existing showcase/demo compositions

### Layout Adaptation

The profile-aware layout path is threaded through:

- `TemplateLoader`
- `SceneManager`
- `SceneBlock`
- `GenericScene`
- `CinematicText`

The same semantic scene now renders with profile-specific padding, text scale, max width, and visual scale.

### Generated Engine Manifest

`engine/src/generated/videoManifest.js` is refreshed by the Python build pipeline and now resolves production imports from `data/videos/<profile_id>/video_###.json`.

## Directory Map

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
|- engine/
|  \- src/
|     |- core/
|     |- overlays/
|     |- scenes/
|     |- templates/
|     |- types/
|     \- generated/
|- output/
|  |- metadata/
|  |- segments/
|  |  |- shorts_vertical/
|  |  |- shorts_vertical_30s/
|  |  |- social_square/
|  |  \- youtube_horizontal/
|  |- shorts_vertical_30s/
|  |- shorts_vertical/
|  |- social_square/
|  \- youtube_horizontal/
\- src/studio/
```

## Verification Performed

The current repository state was verified with:

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

The optional `shorts_vertical_30s` profile is available on demand and follows the same output layout under `output/shorts_vertical_30s/`.
