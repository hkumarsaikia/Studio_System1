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
  python scripts/render.py video_001
  python scripts/render.py video_042 --crf 18
"""
import argparse
import glob
import os
import shutil
import subprocess
import tempfile

from src.studio.config import ENGINE_DIR, OUTPUT_DIR, VIDEOS_DIR




def _cleanup_temp_files() -> None:
    """
    Delete all Remotion/Puppeteer temp files left behind after rendering.

    Remotion spawns headless Chrome via Puppeteer, which creates:
      - puppeteer_dev_chrome_profile-*  (Chrome user-data dirs)
      - chrome_chrome_url_fetcher_*     (download caches)
    in the system TEMP directory. It also may leave frames in engine/tmp.

    This function nukes all of them to reclaim disk space.
    """
    temp_dir = tempfile.gettempdir()
    engine_tmp = ENGINE_DIR / 'tmp'

    # Patterns to match in the system TEMP directory
    patterns = [
        os.path.join(temp_dir, 'puppeteer_dev_chrome_profile-*'),
        os.path.join(temp_dir, 'chrome_chrome_url_fetcher_*'),
        os.path.join(temp_dir, 'remotion-*'),
    ]

    cleaned_count = 0
    for pattern in patterns:
        for match in glob.glob(pattern):
            try:
                if os.path.isdir(match):
                    shutil.rmtree(match, ignore_errors=True)
                else:
                    os.remove(match)
                cleaned_count += 1
            except OSError:
                pass  # Best-effort cleanup

    # Clean engine/tmp if it exists
    if engine_tmp.exists():
        shutil.rmtree(engine_tmp, ignore_errors=True)
        cleaned_count += 1

    if cleaned_count > 0:
        print(f'[cleanup] Removed {cleaned_count} temp file(s)/folder(s)')


def _build_env(video_id: str) -> dict:
    """Build a subprocess environment. We rely on the system PATH for Node.js and ffmpeg."""
    env = os.environ.copy()
    env['REMOTION_VIDEO_ID'] = video_id
    return env


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

    env = _build_env(video_id)

    # Resolve npx executable
    npx_name = 'npx.cmd' if os.name == 'nt' else 'npx'
    npx_cmd = shutil.which(npx_name)
    if npx_cmd is None:
        raise EnvironmentError(f"'{npx_name}' not found. Please ensure Node.js is installed and in your system PATH.")

    # Build the Remotion render command
    command = [
        npx_cmd,
        'remotion',
        'render',
        'src/index.ts',          # Entry point for Remotion (TypeScript)
        'MainComposition',       # Composition ID defined in Root.tsx
        str(output_file),        # Output file path
        '--crf',
        str(quality),            # Constant Rate Factor for quality
    ]

    # Run from the engine/ directory so Remotion can find its config
    try:
        subprocess.run(command, cwd=ENGINE_DIR, check=True, env=env)
    finally:
        # Always clean up temp frames/files, even if the render fails
        _cleanup_temp_files()


def main() -> None:
    parser = argparse.ArgumentParser(description='Render one video from data/videos/video_XXX.json')
    parser.add_argument('video_id', help='Example: video_001')
    parser.add_argument('--crf', type=int, default=20, help='Output quality (lower = better quality, larger file)')
    args = parser.parse_args()

    render_video(args.video_id, args.crf)


if __name__ == '__main__':
    main()
