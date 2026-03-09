"""Export thumbnails from Remotion compositions."""
from __future__ import annotations

import argparse
import os
import subprocess
from shutil import which
from pathlib import Path

from src.studio.config import OUTPUT_DIR as BASE_OUTPUT_DIR, ROOT_DIR
from src.studio.contracts import DEFAULT_PROFILE_ID, is_demo_video_id, is_production_video_id, list_profile_ids
from src.studio.generators.topic_library import load_demo_payload, load_production_payload, materialize_production_video
from src.studio.render.render_single import _build_env

OUTPUT_DIR = BASE_OUTPUT_DIR / 'thumbnails'



def _resolve_npx() -> str:
    npx_name = 'npx.cmd' if os.name == 'nt' else 'npx'
    npx_cmd = which(npx_name)
    if npx_cmd is None:
        raise EnvironmentError(f"'{npx_name}' not found. Please ensure Node.js is installed and in your system PATH.")
    return npx_cmd



def thumbnail_output_path(video_id: str, profile_id: str | None = None, dataset: str = 'production') -> Path:
    if dataset == 'demo':
        return OUTPUT_DIR / 'demos' / f'{video_id}.png'
    safe_profile = profile_id or DEFAULT_PROFILE_ID
    return OUTPUT_DIR / safe_profile / f'{video_id}.png'



def export_thumbnail(video_id: str, frame: int = 150, profile_id: str = DEFAULT_PROFILE_ID) -> Path:
    if is_production_video_id(video_id):
        try:
            load_production_payload(video_id, profile_id)
        except FileNotFoundError:
            materialize_production_video(video_id, profile_id)
        dataset = 'production'
        output_file = thumbnail_output_path(video_id, profile_id=profile_id, dataset=dataset)
        env = _build_env(video_id, dataset=dataset, profile_id=profile_id)
    elif is_demo_video_id(video_id):
        load_demo_payload(video_id)
        dataset = 'demo'
        output_file = thumbnail_output_path(video_id, dataset=dataset)
        env = _build_env(video_id, dataset=dataset, profile_id=None)
    else:
        raise FileNotFoundError(f'Unknown video id: {video_id}')

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists():
        print(f'Thumbnail exists, skipping: {output_file}')
        return output_file

    command = [
        _resolve_npx(),
        'remotion',
        'still',
        'src/index.ts',
        'MainComposition',
        str(output_file),
        '--frame',
        str(frame),
    ]

    try:
        subprocess.run(command, cwd=ROOT_DIR / 'engine', check=True, env=env)
        print(f'Exported thumbnail: {output_file}')
        return output_file
    except subprocess.CalledProcessError as exc:
        print(f'WARNING: Thumbnail export failed for {video_id}: {exc}')
        raise



def batch_export(limit: int | None = None, profile_ids: list[str] | None = None) -> None:
    files = sorted((ROOT_DIR / 'data' / 'storyboards').glob('video_*.json'))
    if limit:
        files = files[:limit]

    selected_profiles = profile_ids or [DEFAULT_PROFILE_ID]
    successes = 0
    failures: list[tuple[str, str]] = []
    for path in files:
        video_id = path.stem
        for profile_id in selected_profiles:
            try:
                export_thumbnail(video_id, profile_id=profile_id)
                successes += 1
            except Exception as exc:  # noqa: BLE001
                failures.append((f'{video_id}[{profile_id}]', str(exc)))

    print(f'Thumbnails exported: {successes}/{len(files) * len(selected_profiles)}')
    if failures:
        for vid, err in failures:
            print(f'  FAILED: {vid} -> {err}')



def main() -> None:
    parser = argparse.ArgumentParser(description='Export thumbnail PNGs from video compositions')
    parser.add_argument('video_id', nargs='?', default=None, help='Single video ID (e.g. video_001)')
    parser.add_argument('--frame', type=int, default=150, help='Frame to capture (default: 150)')
    parser.add_argument('--all', action='store_true', help='Export thumbnails for all production videos')
    parser.add_argument('--limit', type=int, default=None, help='Limit batch to first N videos')
    parser.add_argument('--profile', type=str, default=DEFAULT_PROFILE_ID, help='Production profile id')
    parser.add_argument('--all-profiles', action='store_true', help='Export production thumbnails for every supported profile')
    args = parser.parse_args()

    if args.all:
        batch_export(args.limit, profile_ids=list_profile_ids() if args.all_profiles else [args.profile])
    elif args.video_id:
        if is_demo_video_id(args.video_id):
            export_thumbnail(args.video_id, args.frame)
        elif args.all_profiles:
            for profile_id in list_profile_ids():
                export_thumbnail(args.video_id, args.frame, profile_id=profile_id)
        else:
            export_thumbnail(args.video_id, args.frame, profile_id=args.profile)
    else:
        raise SystemExit('Provide a video_id or --all')


if __name__ == '__main__':
    main()
