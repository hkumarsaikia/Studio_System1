# Final Task Initiation Plan

## Intent inferred from `data/*.txt`

The text corpus in `data/` shows a consistent direction:

1. Build a **systems explainer media engine** (not random animation content).
2. Focus on **high-level vector graphics**, flat 2D, moving slides, cinematic pacing.
3. Use **scene-by-scene production** (10 seconds each, total ~2 minutes).
4. Keep the pipeline **automation-first** (JSON data + scriptable rendering).
5. Run a channel around **economic/social/system topics** from `data/Topics.txt`.

## Direct final-task implementation strategy

Instead of incremental milestone demos, the repository should move as one integrated system:

### 1) Production data contract
- Keep one JSON per video in `data/video_XXX.json`.
- Each scene must include at minimum:
  - `text`
  - `duration`
- Optional:
  - `subtext`
  - `audio`
  - `visual`
  - `palette`

### 2) Visual runtime for high-level vector graphics
- Render vector-first scenes through reusable components:
  - `Background.jsx`: animated gradient motion.
  - `Person.jsx` + `Crowd.jsx`: procedural character blocks.
  - `CinematicText.jsx`: title/subtitle animation.
  - `GenericScene.jsx`: orchestration of vector layers.

### 3) Template routing
- `TemplateLoader.jsx` routes between channel styles:
  - `shorts`
  - `explainer`
  - `infographic`
  - `protest`

### 4) Immediate content launch format
- Start with one topic from `Topics.txt` and produce a 12-scene script.
- `data/video_002.json` is now the direct “final-task style” seed that can be duplicated for future topics.

## File-by-file coding guide for next expansion

### `automation/render.py`
- Add `video_id`-aware loading so render target can switch compositions/data without manual edits.
- Add output naming by title slug.

### `data/video_*.json`
- Store finalized 12-scene scripts from your topic list.
- Keep schema consistent for automation.

### `engine/src/core/*`
- `SceneManager.jsx`: add transitions + per-scene entry/exit timing.
- `TemplateLoader.jsx`: keep templates opinionated by content style.

### `engine/src/scenes/*`
- `GenericScene.jsx`: central scene renderer for text + visuals.
- `SceneBlock.jsx`: per-scene wrappers (audio + scene payload).
- `SceneFactory.jsx`: extend to select different scene components by `visual` type.

### `engine/src/components/*`
- Expand visual primitives:
  - economy icons, flow arrows, bar charts, currency stacks.
  - still vector + motion transform approach.

### `engine/src/overlays/*`
- Add hook captions, lower-thirds, and CTA overlays.

### `engine/src/utils/*`
- implement:
  - duration normalization
  - audio sync guards
  - scene payload validation

### `automation/metadata_generator.py`
- derive SEO title/description/hashtags from `video_XXX.json` topic.

### `automation/export_thumbnail.py`
- generate branded text-first thumbnails from scene 1 data.

## Final-task mindset

You can now proceed directly with full production:

1. pick topic from `Topics.txt`
2. write 12-scene JSON
3. attach scene audio files
4. render with Remotion
5. generate metadata + thumbnail
6. publish

This is the scalable factory architecture you were aiming for.
