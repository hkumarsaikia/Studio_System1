# Asset Production Guide for 500 Systems Videos

This repository now supports **template-based asset reuse** so you do not build 500 videos one-by-one manually.

## Core idea

You build a reusable asset library once, then every topic JSON references those assets by tags and visual types.

## 1) Asset families to create once

- Humans
  - modular people heads, bodies, skin tones, hairstyles, glasses, beard, clothing palettes
  - crowd bundles (8/16/24 variants)
- Objects/icons
  - economy, policy, education, healthcare, media, transport, housing, energy, AI
- Data graphics
  - bars, flow diagrams, network diagrams, icon grids
- Backdrops
  - city street, abstract gradient, landscape sunrise, office, factory, classroom
- Animals/ecology
  - bird, fish, deer, bee, turtle, cow (for climate/ecology/system externalities)

## 2) Scene blueprint used for all topics

All videos use a fixed 12-scene blueprint, each scene mapped to a visual type:
- crowd
- icons
- network
- bars
- flow
- city
- animals
- landscape

This keeps production scalable and consistent.

## 3) How to regenerate everything

```bash
python automation/build_topic_library.py --materialize
```

Generates:
- `data/videos/video_001.json` ... `video_500.json`
- `data/video_manifest.json`
- `data/asset_library.json`
- `data/asset_requirements_500.json`

## 4) Asset planning outputs

- `data/asset_library.json`: reusable master asset families.
- `data/asset_requirements_500.json`: per-video required asset tags and visuals.

Use these files as your production checklist with designers/illustrators.

## 5) Render process

```bash
python automation/validate_library.py
python automation/render.py video_001
python automation/render_all.py --start-from video_001
```

## 6) Practical recommendation

Create SVG master packs first:
- `humans_pack.svg`
- `icons_pack.svg`
- `animals_pack.svg`
- `backdrops_pack.svg`

Then map pack symbols into React components progressively.
