# Current State And Next Steps

This file describes the current repository state and recommended workflows for the YouTube Shorts animation engine.

## Current State

The repository implements the complete automated YouTube Shorts pipeline:

- **500 topics** stored in `data\raw\Topics.txt` as the content database.
- **12-segment structure**: every video has exactly 12 scenes of 10 seconds (300 frames at 30fps) = 120 seconds total.
- **Per-segment instructions**: each segment includes `narration` (script), `visualDirection` (animation notes), `subtext` (display text), `visual` (component type), and `action` (camera movement).
- **Shorts CLI**: `python -m src.studio.cli shorts` chains topic selection → payload generation → validation → optional rendering.
- **Full library build**: `python -m src.studio.cli build --materialize` generates all 500 video JSONs.
- **Validation**: `python -m src.studio.cli validate` checks data integrity.
- **SVG asset toolchain**: Python builders → Inkscape normalization → React component transpilation.
- **Remotion rendering**: 30+ visual components rendered at 1080×1920 with NVENC GPU support.
- **Reusable assets**: Characters, icons, backgrounds, and props available in `ASSET_SPECS`.

## Recommended Working Loop

### For a Single YouTube Short

1. Run `python -m src.studio.cli shorts --topic-index N` (or `--random`).
2. Review the 12-segment summary printed to the console.
3. Add `--render` to generate the MP4 when ready.
4. Copy the finished output into `examples\video\` for a stable showcase artifact.

### For Batch Operations

1. Run `python -m src.studio.cli build --materialize` to regenerate all 500 payloads.
2. Run `python -m src.studio.cli validate` to check integrity.
3. Build or refresh SVG assets with `python build_assets.py`.
4. Render individual videos with `python -m src.studio.cli render video_001`.
5. Commit both source changes and generated assets together.

## Current Showcase Targets

- Any `video_XXX` from the 500-video library can be rendered as a YouTube Short.
- Each video follows the same 12-segment narrative arc but with unique per-topic content.

## Current Gaps Worth Tracking

- The CLI still exposes a `metadata` command, but the backing `src\studio\generators\metadata.py` module is not present in the current tree.
- Automated tests for the Python layer and render pipeline are still minimal.
- Local NVENC binaries must be recreated on each new Windows machine because they are intentionally not tracked in Git.

## Recommended Next Improvements

1. Add more assets to `ASSET_SPECS` and wire them into more scene templates.
2. Restore or implement the metadata generator behind the CLI `metadata` entrypoint.
3. Add automated tests around segment validation, narrative generation, and render configuration.
4. Integrate audio/voiceover generation using the `narration` field in each segment.
5. Add a batch shorts mode to generate and render multiple Shorts in sequence.
