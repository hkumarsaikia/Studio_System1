from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from src.studio.config import ENGINE_DIR, LOGS_DIR, OUTPUT_DIR
from src.studio.contracts import DEFAULT_PROFILE_ID, list_profile_ids
from src.studio.generators.topic_library import MANIFEST_PATH, build_library
from src.studio.render.render_single import production_output_file, render_production_video

ENGINE_TMP = ENGINE_DIR / 'tmp'



def load_video_ids(limit: int | None = None) -> list[str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    ids = sorted(manifest.keys())
    return ids[:limit] if limit else ids



def clean_tmp() -> None:
    if ENGINE_TMP.exists():
        shutil.rmtree(ENGINE_TMP, ignore_errors=True)
        ENGINE_TMP.mkdir(parents=True, exist_ok=True)



def output_exists(video_id: str, profile_ids: list[str]) -> bool:
    return all(production_output_file(video_id, profile_id).exists() for profile_id in profile_ids)



def main() -> None:
    parser = argparse.ArgumentParser(description='Batch render production videos with resume support')
    parser.add_argument('--limit', type=int, default=None, help='Render only first N videos')
    parser.add_argument('--start-from', type=str, default=None, help='Resume from a given production video id')
    parser.add_argument('--crf', type=int, default=20, help='Output quality (lower = better)')
    parser.add_argument('--clean-every', type=int, default=10, help='Clean tmp after every N video groups')
    parser.add_argument('--force', action='store_true', help='Re-render even if the output file exists')
    parser.add_argument('--profile', type=str, default=None, help='Render only the selected profile')
    parser.add_argument('--all-profiles', action='store_true', help='Render every supported profile for each production video')
    args = parser.parse_args()

    profile_ids = list_profile_ids() if args.all_profiles else [args.profile or DEFAULT_PROFILE_ID]

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / 'render_batch.log'

    print('[build] Syncing topic catalog, storyboards, registries, manifests, and compiled payloads before batch render...')
    build_library(materialize=True, force_storyboards=False, refresh_manifests=True, profile_ids=profile_ids)

    video_ids = load_video_ids(args.limit)
    if args.start_from:
        video_ids = [vid for vid in video_ids if vid >= args.start_from]

    rendered = 0
    skipped = 0
    failures: list[tuple[str, str]] = []

    for idx, video_id in enumerate(video_ids, start=1):
        if output_exists(video_id, profile_ids) and not args.force:
            print(f'[{idx}/{len(video_ids)}] SKIP (exists): {video_id} -> {", ".join(profile_ids)}')
            skipped += 1
            continue

        print(f'[{idx}/{len(video_ids)}] Rendering {video_id} -> {", ".join(profile_ids)}')
        try:
            for profile_id in profile_ids:
                render_production_video(video_id, profile_id=profile_id, quality=args.crf)
            rendered += 1
        except Exception as exc:  # noqa: BLE001
            failures.append((video_id, str(exc)))
            print(f'FAILED: {video_id} -> {exc}')

        if rendered > 0 and rendered % args.clean_every == 0:
            print(f'[Cleanup] Purging engine/tmp after {rendered} rendered video groups...')
            clean_tmp()

    summary = (
        f'\n=== Batch Render Complete ===\n'
        f'Rendered: {rendered}\n'
        f'Skipped:  {skipped}\n'
        f'Failed:   {len(failures)}\n'
        f'Total:    {len(video_ids)}\n'
        f'Profiles: {", ".join(profile_ids)}\n'
    )
    print(summary)

    with log_file.open('a', encoding='utf-8') as handle:
        handle.write(summary)
        if failures:
            handle.write('Failures:\n')
            for video_id, error in failures:
                handle.write(f'  - {video_id}: {error}\n')

    if failures:
        print('Failures:')
        for video_id, error in failures:
            print(f'  - {video_id}: {error}')


if __name__ == '__main__':
    main()
