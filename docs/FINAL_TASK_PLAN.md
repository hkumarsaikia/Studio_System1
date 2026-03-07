# Current State And Next Steps

This file replaces the earlier bootstrap plan with the current repository state.

## Current State

The repository already implements the core production loop:

- materialized video payload generation through `python -m src.studio.cli build --materialize`
- validation through `python -m src.studio.cli validate`
- SVG generation through `python build_assets.py`
- Inkscape normalization and visual inspection
- generated React SVG components under `engine\src\components\generated\`
- Remotion-based rendering with local NVENC support
- example outputs saved in `output\` and `examples\video\`

## Recommended Working Loop

1. Update or generate the data payloads.
2. Build or refresh SVG assets.
3. Render the target video ID.
4. Copy the finished output into `examples\video\` when you want a stable showcase artifact.
5. Commit both the source changes and the generated assets that belong to them.

## Current Showcase Targets

- `video_503` is the current graphics-heavy showcase payload.
- The repository already contains full example renders for `video_503` in `output\` and `examples\video\`.

## Current Gaps Worth Tracking

- The CLI still exposes a `metadata` command, but the backing `src\studio\generators\metadata.py` module is not present in the current tree.
- Automated tests for the Python layer and render pipeline are still minimal.
- Local NVENC binaries must be recreated on each new Windows machine because they are intentionally not tracked in Git.

## Recommended Next Improvements

1. Add more assets to `ASSET_SPECS` and wire them into more scenes.
2. Restore or implement the metadata generator behind the CLI `metadata` entrypoint.
3. Add small automated checks around asset generation and render configuration.
4. Add more documented example render IDs and output naming conventions.
