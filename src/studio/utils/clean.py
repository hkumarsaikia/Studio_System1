"""
FILE: clean_output.py
PURPOSE: Workspace cleanup — purges temporary files to prevent disk bloat.

Two main cleanup targets:
  1. output/     → Rendered videos, thumbnails, metadata JSON files
  2. engine/tmp/ → Remotion's temporary frame data (can be 500MB+ per video)

Supports selective cleanup via flags:
  --output-only → Only clean output/ (keep tmp for debugging)
  --tmp-only    → Only clean engine/tmp/ (keep rendered videos)

Default (no flags) cleans both directories.

USAGE:
  python scripts/clean_output.py              # Clean everything
  python scripts/clean_output.py --output-only
  python scripts/clean_output.py --tmp-only
"""
import argparse
import shutil

from src.studio.config import ENGINE_DIR, OUTPUT_DIR

# ── Path Configuration ──────────────────────────────────────────────
ENGINE_TMP = ENGINE_DIR / 'tmp'


def clean_output() -> None:
    """
    Remove all files and subdirectories inside output/.
    Preserves the output/ directory itself so renders can immediately
    start writing to it without needing to mkdir first.
    """
    if OUTPUT_DIR.exists():
        for item in OUTPUT_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item)     # Remove subdirectories (metadata/, thumbnails/)
            else:
                item.unlink()           # Remove individual files (video_001.mp4, etc.)
        print(f'Cleaned: {OUTPUT_DIR}')
    else:
        print('No output directory found.')


def clean_engine_tmp() -> None:
    """
    Remove engine/tmp to free disk from temporary Remotion frame data.
    Remotion stores decoded frames here during rendering; a 2-minute
    video at 1080×1920 can use ~500MB of tmp space.
    """
    if ENGINE_TMP.exists():
        shutil.rmtree(ENGINE_TMP, ignore_errors=True)
        print(f'Cleaned: {ENGINE_TMP}')
    else:
        print('No engine/tmp directory found.')


def main() -> None:
    parser = argparse.ArgumentParser(description='Clean temporary and output files')
    parser.add_argument('--output-only', action='store_true', help='Only clean output/')
    parser.add_argument('--tmp-only', action='store_true', help='Only clean engine/tmp/')
    args = parser.parse_args()

    if args.output_only:
        clean_output()
    elif args.tmp_only:
        clean_engine_tmp()
    else:
        # Default: clean everything
        clean_output()
        clean_engine_tmp()
        print('Full cleanup complete.')


if __name__ == '__main__':
    main()
