"""
FILE: src/studio/shorts_pipeline.py
PURPOSE: Single-command orchestrator for generating one YouTube Short.

This module implements the `shorts` CLI command. It chains:
  1. Topic selection from Topics.txt (by index or randomly)
  2. Storyboard generation with the 12-segment structure
  3. Compilation into a render-ready video JSON
  4. Validation of the generated payload
  5. Optional render to MP4

USAGE (via CLI):
  python -m src.studio.cli shorts --topic-index 42
  python -m src.studio.cli shorts --random
  python -m src.studio.cli shorts --topic-index 1 --render
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from src.studio.config import VIDEOS_DIR, OUTPUT_DIR, STORYBOARDS_DIR, ensure_directories
from src.studio.contracts import PRODUCTION_SEGMENT_COUNT, PRODUCTION_SEGMENT_SECONDS, DEFAULT_FPS
from src.studio.generators.topic_library import (
    parse_topics,
    create_storyboard_payload,
    compile_storyboard,
    write_json,
)
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
        item = topics[0]

    return item


def print_segment_summary(payload: dict) -> None:
    """Print a formatted summary of all 12 segments before rendering."""
    print()
    print('+==================================================================+')
    print(f'|  YouTube Short: {payload["title"][:48]:<48} |')
    seg_count = payload.get('segmentCount', len(payload.get('scenes', [])))
    seg_secs = payload.get('segmentSeconds', PRODUCTION_SEGMENT_SECONDS)
    print(f'|  ID: {payload["id"]}  |  Duration: {seg_count * seg_secs}s  |  Segments: {seg_count}        |')
    print('+==================================================================+')

    scenes = payload.get('scenes', [])
    for i, scene in enumerate(scenes, 1):
        text = str(scene.get('text', scene.get('label', '')))[:30]
        visual = str(scene.get('visual', ''))[:15]
        narration = str(scene.get('narrationText', scene.get('narration', '')))[:50]
        print(f'|  Seg {i:>2} | {text:<30} | {visual:<15} |')
        if narration:
            print(f'|         | >> {narration:<56} |')

    print('+==================================================================+')
    print()


def run_shorts_pipeline(
    topic_index: int | None = None,
    use_random: bool = False,
    do_render: bool = False,
    crf: int = 20,
) -> None:
    """Run the full shorts pipeline: select -> storyboard -> compile -> validate -> (render)."""
    ensure_directories()

    # Step 1: Select topic
    item = select_topic(topic_index, use_random)
    print(f'[shorts] Selected topic #{item["index"]}: {item["topic"]}')

    # Step 2: Generate storyboard
    storyboard = create_storyboard_payload(item['index'], item['topic'])
    video_id = str(storyboard['id'])

    storyboard_path = STORYBOARDS_DIR / f'{video_id}.json'
    write_json(storyboard_path, storyboard)
    print(f'[shorts] Generated storyboard: {storyboard_path}')

    # Step 3: Compile into render-ready video JSON
    compiled = compile_storyboard(storyboard)
    video_path = VIDEOS_DIR / f'{video_id}.json'
    write_json(video_path, compiled)
    print(f'[shorts] Compiled video: {video_path}')

    # Step 4: Validate
    scenes = compiled.get('scenes', [])
    expected_duration = PRODUCTION_SEGMENT_SECONDS * DEFAULT_FPS
    errors = []
    if len(scenes) != PRODUCTION_SEGMENT_COUNT:
        errors.append(f'Expected {PRODUCTION_SEGMENT_COUNT} scenes, found {len(scenes)}')
    for i, scene in enumerate(scenes, 1):
        if scene.get('duration') != expected_duration:
            errors.append(f'Scene {i} duration is {scene.get("duration")}, expected {expected_duration}')

    if errors:
        print('[shorts] VALIDATION ERRORS:')
        for e in errors:
            print(f'  X {e}')
        sys.exit(1)
    else:
        print(f'[shorts] OK Validation passed: {PRODUCTION_SEGMENT_COUNT} segments, {expected_duration} frames each')

    # Step 5: Print summary
    print_segment_summary(compiled)

    # Step 6: Render (optional)
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
