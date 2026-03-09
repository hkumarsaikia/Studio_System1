# Current State And Next Steps

This file captures the implemented storyboard-first platform model and the next improvements that still make sense.

## Current State

The repository now implements the intended production architecture:

- `data/storyboards/` is the canonical editable source of truth
- `data/videos/<profile_id>/` contains compiled production payloads for the default profiles
- `data/demos/` contains demo payloads only
- `video_001` through `video_500` are reserved for production Shorts
- every production Short is `12` segments of `10` seconds each
- `shorts_vertical_30s` is available as an optional on-demand `30s` profile
- production renders are segment-first and then stitched into the final MP4
- metadata generation is implemented and deterministic
- JSON-schema-backed validation protects storyboards, payloads, and manifests
- SVG assets are generated through the Inkscape-backed pipeline and exposed as stable asset refs
- A completely procedural Math-to-SVG engine generates ~230 graphics using `svgwrite`
- Advanced SVG aesthetics are integrated (Glassmorphism, SVG Shadows, Glows, HUD Crosshairs)
- repository graph outputs are regenerated into `data/knowledge-graph/` and summarized in `docs/KNOWLEDGE_GRAPH.md`

## Verified Commands

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

Verified result:

- `video_001` renders `12` segment MP4 files under `output/segments/shorts_vertical/video_001/`
- the final stitched file is `output/shorts_vertical/video_001.mp4`
- the optional `shorts_vertical_30s` profile is still available on demand under `output/segments/shorts_vertical_30s/` and `output/shorts_vertical_30s/`

## Recommended Working Loop

1. update or curate storyboards in `data/storyboards/`
2. run `python -m src.studio.cli build --materialize`
3. run `python -m src.studio.cli validate`
4. build or refresh SVG assets if needed
5. generate metadata
6. refresh the knowledge graph when code or dependency structure changes
7. render the target production ID or demo ID
8. copy the final render into `examples/video/` when you want a stable repository example

## Current Gaps Worth Tracking

- narration text is stored in the storyboard but there is still no TTS or audio mix pipeline in v1
- automated tests are still light compared with the amount of generated data
- local NVENC binaries still need to be recreated on new machines because they are intentionally not tracked in Git

## Recommended Next Improvements

1. add automated tests for negative validation cases and manifest generation
2. add more storyboard templates beyond the current scaffold presets
3. add optional narration generation and audio stitching in a later version
4. continue expanding the procedural scene vocabulary in `src/studio/assets/generative_engine/`
