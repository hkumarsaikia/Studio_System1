from __future__ import annotations

import argparse
import json
import shutil

from src.studio.config import DATA_DIR, OUTPUT_DIR, ENGINE_DIR, LOGS_DIR
from src.studio.generators.topic_library import build_library
from src.studio.render.render_single import render_video

MANIFEST_PATH = DATA_DIR / 'video_manifest.json'
ENGINE_TMP = ENGINE_DIR / 'tmp'


def load_video_ids(limit: int | None = None) -> list[str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
    ids = sorted(manifest.keys())
    return ids[:limit] if limit else ids


def clean_tmp() -> None:
    if ENGINE_TMP.exists():
        shutil.rmtree(ENGINE_TMP, ignore_errors=True)
        ENGINE_TMP.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description='Batch render all production Shorts with resume support')
    parser.add_argument('--limit', type=int, default=None, help='Render only first N videos')
    parser.add_argument('--start-from', type=str, default=None, help='Resume from a given production video id')
    parser.add_argument('--crf', type=int, default=20, help='Output quality (lower = better)')
    parser.add_argument('--clean-every', type=int, default=10, help='Clean tmp after every N renders')
    parser.add_argument('--force', action='store_true', help='Re-render even if output exists')
    args = parser.parse_args()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / 'render_batch.log'

    print('[build] Syncing storyboards, compiled production payloads, and manifests before batch render...')
    build_library(materialize=True, force_storyboards=False, refresh_manifests=True)

    video_ids = load_video_ids(args.limit)
    if args.start_from:
        video_ids = [vid for vid in video_ids if vid >= args.start_from]

    rendered = 0
    skipped = 0
    failures: list[tuple[str, str]] = []

    for idx, video_id in enumerate(video_ids, start=1):
        output_file = OUTPUT_DIR / f'{video_id}.mp4'
        if output_file.exists() and not args.force:
            print(f'[{idx}/{len(video_ids)}] SKIP (exists): {video_id}')
            skipped += 1
            continue

        print(f'[{idx}/{len(video_ids)}] Rendering {video_id}')
        try:
            render_video(video_id, args.crf)
            rendered += 1
        except Exception as exc:  # noqa: BLE001
            failures.append((video_id, str(exc)))
            print(f'FAILED: {video_id} -> {exc}')

        if rendered > 0 and rendered % args.clean_every == 0:
            print(f'[Cleanup] Purging engine/tmp after {rendered} renders...')
            clean_tmp()

    summary = (
        f'\n=== Batch Render Complete ===\n'
        f'Rendered: {rendered}\n'
        f'Skipped:  {skipped}\n'
        f'Failed:   {len(failures)}\n'
        f'Total:    {len(video_ids)}\n'
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
