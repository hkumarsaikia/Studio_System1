"""
FILE: src/studio/shorts_pipeline.py
PURPOSE: Single-command orchestrator for generating one YouTube Short.

This module implements the `shorts` CLI command. It chains:
  1. Topic selection from Topics.txt (by index or randomly)
  2. Single video JSON generation with the 12-segment structure
  3. Validation of the generated payload
  4. Optional render to MP4

USAGE (via CLI):
  python -m src.studio.cli shorts --topic-index 42
  python -m src.studio.cli shorts --random
  python -m src.studio.cli shorts --topic-index 1 --render
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

from src.studio.config import TOPICS_FILE, VIDEOS_DIR, OUTPUT_DIR, ensure_directories
from src.studio.generators.topic_library import make_video_payload, parse_topics
from src.studio.render.render_single import render_video


def select_topic(topic_index: int | None = None, use_random: bool = False) -> dict:
    """Select a topic from Topics.txt by index or randomly."""
    topics = parse_topics()

    if use_random:
        item = random.choice(topics)
    elif topic_index is not None:
        matches = [t for t in topics if t['index'] == topic_index]
        if not matches:
            print(f'[shorts] ERROR: Topic index {topic_index} not found in Topics.txt')
            sys.exit(1)
        item = matches[0]
    else:
        item = topics[0]  # Default to first topic

    return item


def print_segment_summary(payload: dict) -> None:
    """Print a formatted summary of all 12 segments before rendering."""
    print()
    print(f'+==================================================================+')
    print(f'|  YouTube Short: {payload["title"][:48]:<48} |')
    print(f'|  ID: {payload["id"]}  |  Duration: {payload["totalDurationSeconds"]}s  |  Segments: {len(payload["scenes"])}        |')
    print(f'+==================================================================+')

    for scene in payload['scenes']:
        idx = scene.get('segmentIndex', '?')
        text = scene['text'][:30]
        visual = scene['visual'][:15]
        narration = scene.get('narration', '')[:50]
        print(f'|  Seg {idx:>2} | {text:<30} | {visual:<15} |')
        print(f'         | >> {narration:<56} |')

    print(f'+==================================================================+')
    print()


def run_shorts_pipeline(
    topic_index: int | None = None,
    use_random: bool = False,
    do_render: bool = False,
    crf: int = 20,
) -> None:
    """Run the full shorts pipeline: select → generate → validate → (render)."""
    ensure_directories()

    # ── Step 1: Select topic ────────────────────────────────────────
    item = select_topic(topic_index, use_random)
    print(f'[shorts] Selected topic #{item["index"]}: {item["topic"]}')

    # ── Step 2: Generate the video payload ──────────────────────────
    payload = make_video_payload(item['index'], item['topic'])
    video_id = payload['id']

    # Write the JSON file
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    video_path = VIDEOS_DIR / f'{video_id}.json'
    video_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    print(f'[shorts] Generated {video_path}')

    # ── Step 3: Validate ────────────────────────────────────────────
    scenes = payload['scenes']
    errors = []
    if len(scenes) != 12:
        errors.append(f'Expected 12 scenes, found {len(scenes)}')
    for i, scene in enumerate(scenes, 1):
        if scene.get('duration') != 300:
            errors.append(f'Scene {i} duration is {scene.get("duration")}, expected 300')
        if not scene.get('narration'):
            errors.append(f'Scene {i} missing narration')
        if not scene.get('visualDirection'):
            errors.append(f'Scene {i} missing visualDirection')

    if errors:
        print('[shorts] VALIDATION ERRORS:')
        for e in errors:
            print(f'  X {e}')
        sys.exit(1)
    else:
        print(f'[shorts] OK Validation passed: 12 segments, 300 frames each, all fields present')

    # ── Step 4: Print summary ───────────────────────────────────────
    print_segment_summary(payload)

    # ── Step 5: Render (optional) ───────────────────────────────────
    if do_render:
        print(f'[shorts] Rendering {video_id} to MP4...')
        render_video(video_id, crf)
        print(f'[shorts] OK Render complete: {OUTPUT_DIR / f"{video_id}.mp4"}')
    else:
        print(f'[shorts] Skipping render. Use --render to generate MP4.')
        print(f'[shorts] Or run: python -m src.studio.cli render {video_id}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate a YouTube Short from a single topic')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--topic-index', type=int, help='Topic number from Topics.txt (1-500)')
    group.add_argument('--random', action='store_true', help='Pick a random topic')
    parser.add_argument('--render', action='store_true', help='Also render the video to MP4')
    parser.add_argument('--crf', type=int, default=20, help='Output quality for render (default: 20)')
    args = parser.parse_args()

    run_shorts_pipeline(
        topic_index=args.topic_index,
        use_random=args.random,
        do_render=args.render,
        crf=args.crf,
    )


if __name__ == '__main__':
    main()
