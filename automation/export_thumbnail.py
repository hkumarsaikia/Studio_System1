"""
FILE: export_thumbnail.py
PURPOSE: Thumbnail exporter — captures a still frame as PNG for each video.

Uses Remotion's `still` command to render a single frame from the video
composition as a PNG image. These thumbnails are used for YouTube upload.

FEATURES:
  - Default frame: 150 (middle of Scene 1, shows the topic frame)
  - Skip-existing: Won't re-export if the PNG already exists
  - Batch mode: --all flag processes the entire library
  - Error tolerant: Failures don't stop the batch

USAGE:
  python automation/export_thumbnail.py video_001
  python automation/export_thumbnail.py video_001 --frame 200
  python automation/export_thumbnail.py --all
  python automation/export_thumbnail.py --all --limit 50
"""
import argparse
import json
import os
import subprocess
from pathlib import Path

# ── Path Configuration ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / 'output' / 'thumbnails'
VIDEOS_DIR = ROOT / 'data' / 'videos'


def export_thumbnail(video_id: str, frame: int = 150) -> None:
    """
    Export a single thumbnail PNG from a video at the specified frame.

    Args:
        video_id: E.g. "video_001"
        frame:    Frame number to capture (default 150 = 5 seconds in,
                  typically shows the Topic Frame scene)
    """
    video_json = VIDEOS_DIR / f'{video_id}.json'
    if not video_json.exists():
        raise FileNotFoundError(f'Unknown video id: {video_id}')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f'{video_id}.png'

    # Skip if thumbnail already exists (idempotent — safe to re-run)
    if output_file.exists():
        print(f'Thumbnail exists, skipping: {output_file}')
        return

    # Use the robust environment builder from render.py so Node.js/ffmpeg are in PATH
    from render import _build_env
    env = _build_env(video_id)

    # Use robust npx resolution
    from shutil import which
    npx_name = 'npx.cmd' if os.name == 'nt' else 'npx'
    npx_cmd = which(npx_name)
    if npx_cmd is None:
        raise EnvironmentError(f"'{npx_name}' not found. Please ensure Node.js is installed and in your system PATH.")

    # Use Remotion's 'still' command to capture a single frame
    command = [
        npx_cmd,
        'remotion',
        'still',
        'src/index.ts',          # Remotion entry point (fixed from .js)
        'MainComposition',       # Composition ID
        str(output_file),        # Output PNG path
        '--frame',
        str(frame),              # Which frame to capture
    ]

    try:
        subprocess.run(command, cwd=ROOT / 'engine', check=True, env=env)
        print(f'Exported thumbnail: {output_file}')
    except subprocess.CalledProcessError as exc:
        # Log warning but don't crash — batch mode continues
        print(f'WARNING: Thumbnail export failed for {video_id}: {exc}')


def batch_export(limit: int | None = None) -> None:
    """
    Export thumbnails for all videos (or first N).
    Failures are collected and reported at the end.
    """
    files = sorted(VIDEOS_DIR.glob('video_*.json'))
    if limit:
        files = files[:limit]

    successes = 0
    failures = []
    for path in files:
        video_id = path.stem
        try:
            export_thumbnail(video_id)
            successes += 1
        except Exception as exc:  # noqa: BLE001
            failures.append((video_id, str(exc)))

    # Print final report
    print(f'Thumbnails exported: {successes}/{len(files)}')
    if failures:
        for vid, err in failures:
            print(f'  FAILED: {vid} → {err}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Export thumbnail PNGs from video compositions')
    parser.add_argument('video_id', nargs='?', default=None, help='Single video ID (e.g. video_001)')
    parser.add_argument('--frame', type=int, default=150, help='Frame to capture (default: 150)')
    parser.add_argument('--all', action='store_true', help='Export thumbnails for all videos')
    parser.add_argument('--limit', type=int, default=None, help='Limit batch to first N videos')
    args = parser.parse_args()

    if args.all:
        batch_export(args.limit)
    elif args.video_id:
        export_thumbnail(args.video_id, args.frame)
    else:
        raise SystemExit('Provide a video_id or --all')


if __name__ == '__main__':
    main()
