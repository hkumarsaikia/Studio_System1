# Studio_System1 Architecture

This is the short architecture summary. The detailed reference is in `docs/ARCHITECTURE.md`.

## End-To-End Flow

1. `python -m src.studio.cli build --materialize` parses `data/raw/Topics.txt`.
2. The build writes `data/topic_catalog.json` and `data/representative_topics.json`.
3. `data/storyboards/` is preserved or migrated into the canonical `scenePlan` contract.
4. Production storyboards are compiled into `data/videos/<profile_id>/video_###.json` for the default production profiles.
5. `data/video_manifest.json` maps each production video ID to its per-profile compiled payloads.
6. `python build_assets.py` refreshes SVG assets and `data/asset_registry.json`.
7. `python -m src.studio.cli render <video_id> --profile <profile_id>` renders profile-aware MP4 output and materializes optional profiles on demand.
8. `python -m src.studio.cli metadata <video_id>` writes one metadata pack per video.

## Core Layers

### Topic Source

- `data/raw/Topics.txt`
- `data/topic_catalog.json`
- `data/representative_topics.json`

### Canonical Storyboards

- `data/storyboards/video_###.json`
- semantic `scenePlan`
- `profileOverrides` for format-specific adjustments

### Asset Registry

- `data/asset_registry.json` is authoritative
- `data/asset_library.json` is derived compatibility output
- `data/asset_coverage.json` tracks which videos and profiles use which assets

### Render Profiles

- `shorts_vertical`
- `social_square`
- `youtube_horizontal`

Optional on-demand profile:

- `shorts_vertical_30s`

Each profile defines dimensions, aspect ratio, timeline, platforms, and layout rules.

### Derived Outputs

- `data/videos/<profile_id>/video_###.json`
- `output/<profile_id>/<video_id>.mp4`
- `output/segments/<profile_id>/<video_id>/`
- `output/metadata/<video_id>.json`

## Current Production Rules

- Production namespace: `video_001` through `video_500`
- Demo namespace: `demo_*`
- Current v1 timeline: `12` scenes, `10` seconds each, `120` seconds total
- `shorts_vertical_30s` uses the same `12` scenes at `2.5` seconds each and is materialized on demand
- Narration is stored as text only in v1
- Production renders are muted in v1

## Main Commands

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
python .\scripts\generate_repo_knowledge_graph.py
python -m src.studio.cli render video_002 --profile social_square
python -m src.studio.cli render video_010 --profile shorts_vertical_30s
python -m src.studio.cli render video_002 --all-profiles
python -m src.studio.cli metadata video_002
python build_assets.py --no-view
```
