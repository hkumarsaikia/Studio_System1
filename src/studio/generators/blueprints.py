"""
FILE: blueprints.py
PURPOSE: Legacy storyboard scaffold helper for the profile-aware pipeline.

This module keeps a focused scaffold generator for all 500 production
storyboards. It is intentionally narrower than `topic_library.py` and exists
mainly for dry-run inspection and legacy blueprint experimentation.

Unlike the old flat-payload implementation, this module now targets:
  - `data/storyboards/video_001.json` → `video_500.json`
  - `data/videos/<profile_id>/video_001.json` → `video_500.json`
  - `data/video_manifest.json`
  - `engine/src/generated/videoManifest.js`

It still focuses specifically on:
  - Camera action assignment per scene
  - Person mood assignment
  - Category-specific palette embedding
  - Richer subtext generation
  - Dry-run mode for validation

USAGE:
  python -m src.studio.generators.blueprints              # Generate all 500
  python -m src.studio.generators.blueprints --dry-run    # Stats only, no files
"""
import argparse
import re

from src.studio.config import DATA_DIR, TOPICS_FILE, ensure_directories
from src.studio.contracts import DEFAULT_PROFILE_IDS
from src.studio.generators.topic_library import (
    build_metadata_hints,
    compile_storyboard_for_profile,
    create_storyboard_payload,
    write_engine_manifest,
    write_json,
)

# ── Path Configuration ──────────────────────────────────────────────
TOPICS_TXT = TOPICS_FILE
MANIFEST_PATH = DATA_DIR / 'video_manifest.json'

def parse_topics() -> list[dict]:
    """Parse Topics.txt into list of {index, topic}."""
    topics = []
    for line in TOPICS_TXT.read_text(encoding='utf-8').splitlines():
        match = re.match(r'^(\d+)\.\s+(.+?)\s*$', line)
        if match:
            topics.append({'index': int(match.group(1)), 'topic': match.group(2)})
    if len(topics) != 500:
        raise ValueError(f'Expected 500 topics but found {len(topics)}')
    return topics


def make_storyboard_payload(index: int, topic: str) -> dict:
    """Build the canonical storyboard JSON for one topic."""
    payload = create_storyboard_payload(index, topic)
    payload['metadataHints'] = build_metadata_hints(topic, payload['category'], payload['scenePlan'])
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate 500 production storyboards and profile-aware payloads')
    parser.add_argument('--dry-run', action='store_true', help='Print stats without writing files')
    args = parser.parse_args()

    ensure_directories()
    topics = parse_topics()

    manifest = {}
    action_counts = {}
    visual_counts = {}
    storyboard_count = 0
    profile_counts = {profile_id: 0 for profile_id in DEFAULT_PROFILE_IDS}

    for item in topics:
        storyboard = make_storyboard_payload(item['index'], item['topic'])
        video_id = storyboard['id']

        manifest[video_id] = {
            'title': storyboard['title'],
            'category': storyboard['category'],
            'templateFamily': storyboard['templateFamily'],
            'defaultProfiles': storyboard['defaultProfiles'],
            'sceneCount': len(storyboard['scenePlan']),
            'profiles': {},
        }

        for scene in storyboard['scenePlan']:
            action_counts[scene['cameraIntent']] = action_counts.get(scene['cameraIntent'], 0) + 1
            visual_counts[scene['visual']] = visual_counts.get(scene['visual'], 0) + 1

        if not args.dry_run:
            storyboard_path = DATA_DIR / 'storyboards' / f'{video_id}.json'
            write_json(storyboard_path, storyboard)
            storyboard_count += 1

            for profile_id in DEFAULT_PROFILE_IDS:
                compiled = compile_storyboard_for_profile(storyboard, profile_id)
                payload_path = DATA_DIR / 'videos' / profile_id / f'{video_id}.json'
                write_json(payload_path, compiled)
                profile_counts[profile_id] += 1
                manifest[video_id]['profiles'][profile_id] = {
                    'path': f'data/videos/{profile_id}/{video_id}.json',
                    'width': compiled['width'],
                    'height': compiled['height'],
                    'sceneCount': len(compiled['scenes']),
                    'template': compiled['template'],
                }

    if not args.dry_run:
        write_json(MANIFEST_PATH, manifest)
        write_engine_manifest(sorted(manifest.keys()))

    print(f'Processed {len(topics)} topics')
    print(f'Camera actions: {action_counts}')
    print(f'Visual types:   {visual_counts}')
    if not args.dry_run:
        print(f'Wrote {storyboard_count} storyboard files to {DATA_DIR / "storyboards"}')
        print(f'Wrote profile payloads: {profile_counts}')


if __name__ == '__main__':
    main()
