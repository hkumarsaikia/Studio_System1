# Contributing to Studio_System1

First off, thank you for considering contributing to Studio_System1! This pipeline powers a highly scalable automated rendering engine producing **minimalist-style** explainer videos. We welcome contributions that improve stability, extend component libraries, or optimize render times.

## 1. Where Do I Go From Here?

If you've noticed a bug or have a feature request, make one! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

## 2. Setting Up Your Environment

Please refer to `docs/SETUP_GUIDE.md` for a complete environment setup. You will need Node.js, Python 3.12+, and FFmpeg.

## 3. Architecture Overview

Before contributing code, please read `docs/ARCHITECTURE.md`. The project is divided into:
- **`studio.py`**: The unified CLI.
- **`scripts/`**: Python logistics (building payloads, triggering renders).
- **`engine/`**: The Remotion React/TypeScript rendering engine.

## 4. Submitting Changes

1. Fork the repo and create your branch from `main`.
2. Do not use hardcoded absolute system paths (e.g. `C:\tools\ffmpeg`). Use `shutil.which` or rely on the `PATH` environment variable.
3. Ensure no unneeded files are tracked (respect `.gitignore`).
4. Run `npx tsc --noEmit` inside `engine/` to verify zero TypeScript errors.
5. Run `python studio.py validate` from the project root.
6. Issue that pull request!

## 5. Coding Conventions

### Python
- Standard library only where possible. Scripts should run natively without `pip install`.
- All scripts in `scripts/` must have `__init__.py` files for package imports.
- Use `shutil.which()` to resolve external binaries — never hardcode paths.

### TypeScript / React / Remotion
- **Strict TypeScript** is enabled. All new files must be `.tsx`/`.ts`, not `.jsx`/`.js`.
- Use `@/` path aliases for imports (e.g., `import { Camera } from '@/core/Camera'`).
- Components in `engine/src/components/` must be parametric, reusable SVG components.
- New visual components should use `SvgDefs.tsx` filters (`#kurzDropShadow`, `#neonGlow`) for depth and glow effects.
- Use `polished` (`darken`, `lighten`, `transparentize`) for dynamic color manipulation instead of hardcoding shadow colors.
- Animations should use Remotion's `spring()` or the `useElasticAnim` hook for bouncy, elastic entrances.

### JSON
- Modifications to the video schemas must be verified against `scripts/templates/master_schema.json`.

## 6. Graphics Standards

To maintain the **minimalist** aesthetic:
- **Layer your SVGs**: Base shape → Shadow layer → Highlight layer.
- **Use gradients**: Radial for spherical objects, linear for metallic surfaces.
- **Apply drop shadows**: Every foreground element should use `filter="url(#kurzDropShadow)"`.
- **Avoid flat single-color shapes**: Use at least 2–3 tonal layers per element.
- **Animate with springs**: Prefer elastic pop-ins over linear fades.
