"""
FILE: render_all.py
PURPOSE: Batch renderer — renders all 500 videos with resume support.

This is the main entry point for production rendering. It processes all
videos listed in the manifest and provides:

  - SKIP-EXISTING: Already-rendered videos are skipped (resume-friendly)
  - START-FROM:    Resume from a specific video ID after interruption
  - DISK CLEANUP:  Periodically purges engine/tmp to prevent disk bloat
  - LOGGING:       Writes results to logs/render_batch.log
  - FORCE MODE:    Re-render everything with --force

USAGE:
  python scripts/render_all.py                    # Render all, skip existing
  python scripts/render_all.py --limit 10         # Render first 10 only
  python scripts/render_all.py --start-from video_042  # Resume from video_042
  python scripts/render_all.py --force             # Force re-render all
  python scripts/render_all.py --crf 18            # Higher quality output
"""
import argparse
import json
import shutil

from src.studio.render.render_single import render_video
from src.studio.config import DATA_DIR, OUTPUT_DIR, ENGINE_DIR, LOGS_DIR

# ── Path Configuration ──────────────────────────────────────────────
MANIFEST_PATH = DATA_DIR / 'video_manifest.json'
ENGINE_TMP = ENGINE_DIR / 'tmp'       # Remotion's temporary frame data


def load_video_ids(limit: int | None = None) -> list[str]:
    """Load all video IDs from the manifest, optionally limited to first N."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    ids = sorted(manifest.keys())
    return ids[:limit] if limit else ids


def clean_tmp() -> None:
    """
    Purge engine/tmp to free disk space.

    Remotion stores temporary frame images in engine/tmp/ during rendering.
    A single video can use ~500MB of tmp space, so we periodically clean
    this to prevent the disk from filling up during batch renders.
    """
    if ENGINE_TMP.exists():
        shutil.rmtree(ENGINE_TMP, ignore_errors=True)
        ENGINE_TMP.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # ── CLI argument parsing ────────────────────────────────────────
    parser = argparse.ArgumentParser(description='Batch render all topic videos with resume support')
    parser.add_argument('--limit', type=int, default=None, help='Render only first N videos')
    parser.add_argument('--start-from', type=str, default=None, help='Resume from a given video id')
    parser.add_argument('--crf', type=int, default=20, help='Output quality (lower = better)')
    parser.add_argument('--clean-every', type=int, default=10, help='Clean tmp after every N renders')
    parser.add_argument('--force', action='store_true', help='Re-render even if output exists')
    args = parser.parse_args()

    # Ensure the logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / 'render_batch.log'

    # ── Load and filter video IDs ───────────────────────────────────
    video_ids = load_video_ids(args.limit)
    if args.start_from:
        # Keep only videos at or after the start-from ID (alphabetical order)
        video_ids = [vid for vid in video_ids if vid >= args.start_from]

    # ── Render loop ─────────────────────────────────────────────────
    rendered = 0       # Successfully rendered count
    skipped = 0        # Already-exists skipped count
    failures = []      # List of (video_id, error_message) tuples

    for idx, video_id in enumerate(video_ids, start=1):
        output_file = OUTPUT_DIR / f'{video_id}.mp4'

        # Skip existing renders unless --force flag is set
        if output_file.exists() and not args.force:
            print(f'[{idx}/{len(video_ids)}] SKIP (exists): {video_id}')
            skipped += 1
            continue

        print(f'[{idx}/{len(video_ids)}] Rendering {video_id}')
        try:
            render_video(video_id, args.crf)
            rendered += 1
        except Exception as exc:  # noqa: BLE001
            # Log the failure but continue with the next video
            failures.append((video_id, str(exc)))
            print(f'FAILED: {video_id} → {exc}')

        # Periodic disk cleanup — prevents tmp from eating all disk space
        if rendered > 0 and rendered % args.clean_every == 0:
            print(f'[Cleanup] Purging engine/tmp after {rendered} renders...')
            clean_tmp()

    # ── Final summary ───────────────────────────────────────────────
    summary = (
        f'\n=== Batch Render Complete ===\n'
        f'Rendered: {rendered}\n'
        f'Skipped:  {skipped}\n'
        f'Failed:   {len(failures)}\n'
        f'Total:    {len(video_ids)}\n'
    )
    print(summary)

    # Append results to the log file for historical tracking
    with log_file.open('a', encoding='utf-8') as f:
        f.write(summary)
        if failures:
            f.write('Failures:\n')
            for vid, err in failures:
                f.write(f'  - {vid}: {err}\n')

    # Print failures to console for immediate visibility
    if failures:
        print('Failures:')
        for vid, err in failures:
            print(f'  - {vid}: {err}')


if __name__ == '__main__':
    main()
