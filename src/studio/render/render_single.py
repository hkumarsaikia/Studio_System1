from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from src.studio.config import ENGINE_DIR, OUTPUT_DIR, SEGMENTS_OUTPUT_DIR, VIDEOS_DIR
from src.studio.contracts import DEFAULT_SCENE_DURATION, is_demo_video_id, is_production_video_id
from src.studio.generators.topic_library import load_demo_payload, materialize_production_video


def _cleanup_temp_files() -> None:
    temp_dir = tempfile.gettempdir()
    engine_tmp = ENGINE_DIR / 'tmp'
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
                pass

    if engine_tmp.exists():
        shutil.rmtree(engine_tmp, ignore_errors=True)
        cleaned_count += 1

    if cleaned_count > 0:
        print(f'[cleanup] Removed {cleaned_count} temp file(s)/folder(s)')


def _resolve_npx() -> str:
    npx_name = 'npx.cmd' if os.name == 'nt' else 'npx'
    npx_cmd = shutil.which(npx_name)
    if npx_cmd is None:
        raise EnvironmentError(f"'{npx_name}' not found. Please ensure Node.js is installed and in your system PATH.")
    return npx_cmd


def _resolve_ffmpeg() -> str:
    local_binaries = ENGINE_DIR / 'remotion-binaries-nvenc' / 'ffmpeg.exe'
    if local_binaries.exists():
        return str(local_binaries)

    ffmpeg_cmd = shutil.which('ffmpeg.exe') or shutil.which('ffmpeg')
    if ffmpeg_cmd is None:
        raise EnvironmentError("'ffmpeg' not found. Please ensure FFmpeg is installed or available in engine\\remotion-binaries-nvenc.")
    return ffmpeg_cmd


def _build_env(video_id: str, dataset: str = 'production', segment_index: int | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env['REMOTION_VIDEO_ID'] = video_id
    env['REMOTION_DATASET'] = dataset
    env['NODE_OPTIONS'] = '--max-old-space-size=14336'
    if segment_index is None:
        env.pop('REMOTION_SEGMENT_INDEX', None)
    else:
        env['REMOTION_SEGMENT_INDEX'] = str(segment_index)
    return env


def _render_composition(
    video_id: str,
    dataset: str,
    composition_id: str,
    output_file: Path,
    quality: int,
    segment_index: int | None = None,
) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    command = [
        _resolve_npx(),
        'remotion',
        'render',
        'src/index.ts',
        composition_id,
        str(output_file),
        '--crf',
        str(quality),
        '--concurrency',
        '10',
        '--overwrite',
    ]
    env = _build_env(video_id, dataset=dataset, segment_index=segment_index)
    try:
        subprocess.run(command, cwd=ENGINE_DIR, check=True, env=env)
    finally:
        _cleanup_temp_files()


def _stitch_segments(segment_files: list[Path], output_file: Path) -> None:
    ffmpeg_cmd = _resolve_ffmpeg()
    concat_list = output_file.parent / f'{output_file.stem}_segments.txt'
    lines = []
    for segment_file in segment_files:
        normalized = segment_file.resolve().as_posix().replace("'", "'\\''")
        lines.append(f"file '{normalized}'")
    concat_list.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    command = [
        ffmpeg_cmd,
        '-y',
        '-f',
        'concat',
        '-safe',
        '0',
        '-i',
        str(concat_list),
        '-c',
        'copy',
        str(output_file),
    ]
    try:
        subprocess.run(command, cwd=ENGINE_DIR, check=True)
    finally:
        concat_list.unlink(missing_ok=True)


def render_production_video(video_id: str, quality: int = 20) -> Path:
    compiled_payload = materialize_production_video(video_id)
    scenes = compiled_payload.get('scenes', [])
    if len(scenes) == 0:
        raise ValueError(f'No scenes compiled for {video_id}')

    segment_dir = SEGMENTS_OUTPUT_DIR / video_id
    segment_dir.mkdir(parents=True, exist_ok=True)
    segment_files: list[Path] = []

    for segment_index, _scene in enumerate(scenes, start=1):
        segment_file = segment_dir / f'segment_{segment_index:02d}.mp4'
        print(f'[render] Rendering {video_id} segment {segment_index:02d}/{len(scenes):02d}')
        _render_composition(
            video_id,
            dataset='production',
            composition_id='SegmentComposition',
            output_file=segment_file,
            quality=quality,
            segment_index=segment_index,
        )
        segment_files.append(segment_file)

    output_file = OUTPUT_DIR / f'{video_id}.mp4'
    _stitch_segments(segment_files, output_file)
    print(f'[render] Stitched final output: {output_file}')
    return output_file


def render_demo_video(video_id: str, quality: int = 20) -> Path:
    load_demo_payload(video_id)
    output_file = OUTPUT_DIR / f'{video_id}.mp4'
    print(f'[render] Rendering demo payload: {video_id}')
    _render_composition(
        video_id,
        dataset='demo',
        composition_id='MainComposition',
        output_file=output_file,
        quality=quality,
        segment_index=None,
    )
    return output_file


def render_video(video_id: str, quality: int = 20) -> Path:
    if is_demo_video_id(video_id):
        return render_demo_video(video_id, quality)
    if is_production_video_id(video_id):
        return render_production_video(video_id, quality)
    raise ValueError(f'Unsupported video id: {video_id}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Render one video from storyboards or demos')
    parser.add_argument('video_id', help='Example: video_001 or demo_graphics_showcase_v2')
    parser.add_argument('--crf', type=int, default=20, help='Output quality (lower = better quality, larger file)')
    args = parser.parse_args()

    render_video(args.video_id, args.crf)


if __name__ == '__main__':
    main()
