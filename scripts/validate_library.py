"""
FILE: validate_library.py
PURPOSE: Pre-render validation — ensures all 500 video JSONs are correct.

Run this script BEFORE starting a batch render to catch data issues early.
It validates:
  1. Exactly 500 video files exist in data/videos/
  2. The manifest has exactly 500 entries
  3. Asset planning files exist (asset_library.json, asset_requirements_500.json)
  4. Every video has exactly 12 scenes
  5. Every video has a top-level category
  6. Every scene has the required keys: text, duration, visual
  7. Prints a distribution of visual types across all 6,000 scenes

USAGE:
  python scripts/validate_library.py

EXIT CODES:
  0 = All validations passed
  1 = Validation error (details printed to console)
"""
import json
from pathlib import Path

# ── Path Configuration ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
VIDEOS_DIR = ROOT / 'data' / 'videos'
MANIFEST_PATH = ROOT / 'data' / 'video_manifest.json'
ASSET_LIBRARY_PATH = ROOT / 'data' / 'asset_library.json'
ASSET_REQUIREMENTS_PATH = ROOT / 'data' / 'asset_requirements_500.json'

# Every scene MUST have these keys to render correctly
REQUIRED_SCENE_KEYS = {'text', 'duration', 'visual'}


def validate() -> None:
    """
    Run all validation checks. Raises ValueError with a descriptive
    message on the first failure found.
    """
    # ── Check 1: Exactly 500 video files ────────────────────────────
    files = sorted(VIDEOS_DIR.glob('video_*.json'))
    if len(files) != 500:
        raise ValueError(f'Expected 500 video files, found {len(files)}')

    # ── Check 2: Manifest has 500 entries ───────────────────────────
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    if len(manifest) != 500:
        raise ValueError(f'Expected 500 manifest entries, found {len(manifest)}')

    # ── Check 3: Asset planning files exist ─────────────────────────
    if not ASSET_LIBRARY_PATH.exists() or not ASSET_REQUIREMENTS_PATH.exists():
        raise ValueError('Asset planning files are missing. Run build_topic_library.py')

    # ── Check 4-6: Per-video validation ─────────────────────────────
    visual_counts = {}  # Track how many times each visual type is used
    for path in files:
        payload = json.loads(path.read_text(encoding='utf-8'))
        scenes = payload.get('scenes', [])

        # Check 4: Every video must have exactly 12 scenes
        if len(scenes) != 12:
            raise ValueError(f'{path.name} does not contain 12 scenes')

        # Check 5: Every video must have a category
        if not payload.get('category'):
            raise ValueError(f'{path.name} missing top-level category')

        # Check 6: Every scene must have required keys
        for scene in scenes:
            missing = REQUIRED_SCENE_KEYS - set(scene.keys())
            if missing:
                raise ValueError(f'{path.name} scene missing keys: {missing}')

            # Count visual type usage for the distribution report
            visual = scene['visual']
            visual_counts[visual] = visual_counts.get(visual, 0) + 1

    # ── All checks passed ───────────────────────────────────────────
    print('Library validation passed')
    print(f'Visual distribution: {visual_counts}')


if __name__ == '__main__':
    validate()
