# Current State And Next Steps

This file captures the implemented storyboard-first platform model and the next improvements that still make sense.

## Current State

The repository now implements the intended production architecture:

- `data/storyboards/` is the canonical editable source of truth
- `data/videos/` contains compiled production payloads only
- `data/demos/` contains demo payloads only
- `video_001` through `video_500` are reserved for production Shorts
- every production Short is `12` segments of `10` seconds each
- production renders are segment-first and then stitched into the final MP4
- metadata generation is implemented and deterministic
- JSON-schema-backed validation protects storyboards, payloads, and manifests
- SVG assets are generated through the Inkscape-backed pipeline and exposed as stable asset refs

## Verified Commands

```powershell
python -m src.studio.cli build --materialize
python -m src.studio.cli validate
python -m src.studio.cli metadata video_002
Set-Location .\engine
npx tsc --noEmit
Set-Location ..
python -m src.studio.cli render video_002
```

Verified result:

- `video_002` renders `12` segment MP4 files under `output/segments/video_002/`
- the final stitched file is `output/video_002.mp4`
- `ffprobe` reports `120.000000` seconds for the final output

## Recommended Working Loop

1. update or curate storyboards in `data/storyboards/`
2. run `python -m src.studio.cli build --materialize`
3. run `python -m src.studio.cli validate`
4. build or refresh SVG assets if needed
5. generate metadata
6. render the target production ID or demo ID
7. copy the final render into `examples/video/` when you want a stable repository example

## Current Gaps Worth Tracking

- narration text is stored in the storyboard but there is still no TTS or audio mix pipeline in v1
- automated tests are still light compared with the amount of generated data
- local NVENC binaries still need to be recreated on new machines because they are intentionally not tracked in Git

## Recommended Next Improvements

1. add automated tests for negative validation cases and manifest generation
2. add more storyboard templates beyond the current scaffold presets
3. add optional narration generation and audio stitching in a later version
4. expand the reusable SVG asset catalog and scene vocabulary
