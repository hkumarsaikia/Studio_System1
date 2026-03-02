"""
FILE: render.py
PURPOSE: Single-video renderer — the fundamental render unit.

This script renders ONE video from its JSON data file by:
  1. Verifying the video JSON exists in data/videos/
  2. Setting the REMOTION_VIDEO_ID environment variable
  3. Calling `npx remotion render` with the correct arguments
  4. Saving the output MP4 to output/

Used directly for testing individual videos, and also imported by
render_all.py for batch rendering.

USAGE:
  python automation/render.py video_001
  python automation/render.py video_042 --crf 18
"""
import argparse
import os
import subprocess
from pathlib import Path

# Project root (one level above the automation/ directory)
ROOT = Path(__file__).resolve().parents[1]
VIDEOS_DIR = ROOT / 'data' / 'videos'
OUTPUT_DIR = ROOT / 'output'


def ensure_video_exists(video_id: str) -> None:
    """Verify the video JSON data file exists before attempting render."""
    candidate = VIDEOS_DIR / f'{video_id}.json'
    if not candidate.exists():
        raise FileNotFoundError(f'Video data not found: {candidate}')


def render_video(video_id: str, quality: int = 20) -> None:
    """
    Render a single video to MP4.

    This is the core render function used by both this script and render_all.py.
    It sets REMOTION_VIDEO_ID in the environment so Root.jsx picks up the
    correct video data, then invokes Remotion's CLI renderer.

    Args:
        video_id: E.g. "video_001" — must match a file in data/videos/
        quality:  CRF value (0-51). Lower = better quality, larger file.
                  Default 20 is a good balance for YouTube uploads.
    """
    ensure_video_exists(video_id)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f'{video_id}.mp4'

    # Pass the video ID to the Remotion engine via environment variable
    env = os.environ.copy()
    env['REMOTION_VIDEO_ID'] = video_id

    # Build the Remotion render command
    npx_cmd = 'npx.cmd' if os.name == 'nt' else 'npx'
    command = [
        npx_cmd,
        'remotion',
        'render',
        'src/index.js',          # Entry point for Remotion
        'MainComposition',       # Composition ID defined in Root.jsx
        str(output_file),        # Output file path
        '--crf',
        str(quality),            # Constant Rate Factor for quality
    ]

    # Run from the engine/ directory so Remotion can find its config
    subprocess.run(command, cwd=ROOT / 'engine', check=True, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description='Render one video from data/videos/video_XXX.json')
    parser.add_argument('video_id', help='Example: video_001')
    parser.add_argument('--crf', type=int, default=20, help='Output quality (lower = better quality, larger file)')
    args = parser.parse_args()

    render_video(args.video_id, args.crf)


if __name__ == '__main__':
    main()
