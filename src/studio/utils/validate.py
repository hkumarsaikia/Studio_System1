from __future__ import annotations

import json
from pathlib import Path

from src.studio.config import DATA_DIR, DEMOS_DIR, STORYBOARDS_DIR, VIDEOS_DIR
from src.studio.contracts import (
    DEFAULT_SCENE_DURATION,
    PRODUCTION_SEGMENT_COUNT,
    PRODUCTION_SEGMENT_SECONDS,
    SUPPORTED_VISUALS,
    flatten_asset_library,
)
from src.studio.generators.topic_library import build_topics_index
from src.studio.utils.schema_validation import read_json, validate_with_schema

MANIFEST_PATH = DATA_DIR / 'video_manifest.json'
DEMO_MANIFEST_PATH = DATA_DIR / 'demo_manifest.json'
ASSET_LIBRARY_PATH = DATA_DIR / 'asset_library.json'
ASSET_REQUIREMENTS_PATH = DATA_DIR / 'asset_requirements_500.json'


REQUIRED_DEMO_FIELDS = {'id', 'title', 'template', 'scenes'}


def validate_storyboard(path: Path, expected_topic: str, allowed_assets: set[str]) -> None:
    storyboard = read_json(path)
    validate_with_schema(storyboard, 'storyboard', path.name)

    if storyboard['topic'] != expected_topic:
        raise ValueError(f'{path.name}: topic mismatch. expected={expected_topic!r} actual={storyboard["topic"]!r}')

    segments = storyboard['segments']
    if int(storyboard['segmentCount']) != PRODUCTION_SEGMENT_COUNT or len(segments) != PRODUCTION_SEGMENT_COUNT:
        raise ValueError(f'{path.name}: expected {PRODUCTION_SEGMENT_COUNT} segments')
    if int(storyboard['segmentSeconds']) != PRODUCTION_SEGMENT_SECONDS:
        raise ValueError(f'{path.name}: segmentSeconds must equal {PRODUCTION_SEGMENT_SECONDS}')

    for index, segment in enumerate(segments, start=1):
        if int(segment['index']) != index:
            raise ValueError(f'{path.name}: segment index mismatch at position {index}')
        if segment['segmentId'] != f'segment_{index:02d}':
            raise ValueError(f'{path.name}: segmentId mismatch at position {index}')
        unknown_assets = sorted(set(segment.get('assetRefs', [])) - allowed_assets)
        if unknown_assets:
            raise ValueError(f'{path.name}: unknown assetRefs in {segment["segmentId"]}: {unknown_assets}')
        if segment['visual'] not in SUPPORTED_VISUALS:
            raise ValueError(f'{path.name}: unsupported visual {segment["visual"]}')


def validate_compiled_video(path: Path, expected_topic: str, allowed_assets: set[str]) -> None:
    payload = read_json(path)
    validate_with_schema(payload, 'video', path.name)

    if payload['topic'] != expected_topic:
        raise ValueError(f'{path.name}: compiled topic mismatch. expected={expected_topic!r} actual={payload["topic"]!r}')

    scenes = payload['scenes']
    if int(payload['segmentCount']) != PRODUCTION_SEGMENT_COUNT or len(scenes) != PRODUCTION_SEGMENT_COUNT:
        raise ValueError(f'{path.name}: expected {PRODUCTION_SEGMENT_COUNT} compiled scenes')
    if int(payload['segmentSeconds']) != PRODUCTION_SEGMENT_SECONDS:
        raise ValueError(f'{path.name}: segmentSeconds must equal {PRODUCTION_SEGMENT_SECONDS}')

    for index, scene in enumerate(scenes, start=1):
        if scene['segmentId'] != f'segment_{index:02d}':
            raise ValueError(f'{path.name}: compiled segmentId mismatch at position {index}')
        if int(scene['duration']) != DEFAULT_SCENE_DURATION:
            raise ValueError(f'{path.name}: scene {scene["segmentId"]} duration must equal {DEFAULT_SCENE_DURATION}')
        if scene['visual'] not in SUPPORTED_VISUALS:
            raise ValueError(f'{path.name}: unsupported visual {scene["visual"]}')
        unknown_assets = sorted(set(scene.get('assetTags', [])) - allowed_assets)
        if unknown_assets:
            raise ValueError(f'{path.name}: unknown assetTags in {scene["segmentId"]}: {unknown_assets}')


def validate_demo_payload(path: Path) -> None:
    payload = read_json(path)
    missing = REQUIRED_DEMO_FIELDS - set(payload.keys())
    if missing:
        raise ValueError(f'{path.name}: missing demo fields {sorted(missing)}')
    scenes = payload.get('scenes', [])
    if not scenes:
        raise ValueError(f'{path.name}: demo payload must include at least one scene')
    for scene in scenes:
        if scene.get('visual') not in SUPPORTED_VISUALS:
            raise ValueError(f'{path.name}: unsupported demo visual {scene.get("visual")}')


def validate_manifest_consistency(
    production_manifest: dict[str, dict[str, object]],
    demo_manifest: dict[str, dict[str, object]],
    storyboard_paths: list[Path],
    video_paths: list[Path],
    demo_paths: list[Path],
) -> None:
    storyboard_ids = {path.stem for path in storyboard_paths}
    video_ids = {path.stem for path in video_paths}
    demo_ids = {path.stem for path in demo_paths}

    if set(production_manifest.keys()) != storyboard_ids or set(production_manifest.keys()) != video_ids:
        raise ValueError('Production manifest ids do not exactly match storyboard ids and compiled video ids')

    if set(demo_manifest.keys()) != demo_ids:
        raise ValueError('Demo manifest ids do not exactly match demo payload ids')

    collisions = storyboard_ids & demo_ids
    if collisions:
        raise ValueError(f'Production/demo id collisions detected: {sorted(collisions)}')

    for video_id, entry in production_manifest.items():
        if entry['sceneCount'] != PRODUCTION_SEGMENT_COUNT:
            raise ValueError(f'{video_id}: manifest sceneCount must equal {PRODUCTION_SEGMENT_COUNT}')
        if entry['segmentCount'] != PRODUCTION_SEGMENT_COUNT:
            raise ValueError(f'{video_id}: manifest segmentCount must equal {PRODUCTION_SEGMENT_COUNT}')
        if entry['segmentSeconds'] != PRODUCTION_SEGMENT_SECONDS:
            raise ValueError(f'{video_id}: manifest segmentSeconds must equal {PRODUCTION_SEGMENT_SECONDS}')
        expected_storyboard = f'data/storyboards/{video_id}.json'
        if entry['storyboard'] != expected_storyboard:
            raise ValueError(f'{video_id}: manifest storyboard path mismatch')

    storyboard_map = {path.stem: read_json(path) for path in storyboard_paths}
    video_map = {path.stem: read_json(path) for path in video_paths}
    demo_map = {path.stem: read_json(path) for path in demo_paths}

    for video_id, entry in production_manifest.items():
        storyboard = storyboard_map[video_id]
        video = video_map[video_id]
        if entry['title'] != storyboard['title'] or entry['title'] != video['title']:
            raise ValueError(f'{video_id}: manifest title does not match storyboard/video title')
        if entry['topic'] != storyboard['topic'] or entry['topic'] != video['topic']:
            raise ValueError(f'{video_id}: manifest topic does not match storyboard/video topic')
        if entry['category'] != storyboard['category'] or entry['category'] != video['category']:
            raise ValueError(f'{video_id}: manifest category does not match storyboard/video category')
        if entry['template'] != storyboard['template'] or entry['template'] != video['template']:
            raise ValueError(f'{video_id}: manifest template does not match storyboard/video template')

    for demo_id, entry in demo_manifest.items():
        demo = demo_map[demo_id]
        if entry['title'] != demo['title']:
            raise ValueError(f'{demo_id}: demo manifest title does not match payload title')
        if entry['category'] != demo.get('category', 'DEMO'):
            raise ValueError(f'{demo_id}: demo manifest category does not match payload category')
        if entry['template'] != demo.get('template', 'explainer'):
            raise ValueError(f'{demo_id}: demo manifest template does not match payload template')
        if entry['sceneCount'] != len(demo.get('scenes', [])):
            raise ValueError(f'{demo_id}: demo manifest sceneCount does not match payload scene count')


def validate() -> None:
    storyboard_paths = sorted(STORYBOARDS_DIR.glob('video_*.json'))
    video_paths = sorted(VIDEOS_DIR.glob('video_*.json'))
    demo_paths = sorted(DEMOS_DIR.glob('demo_*.json'))
    topics_index = build_topics_index()

    if len(storyboard_paths) != 500:
        raise ValueError(f'Expected 500 storyboard files, found {len(storyboard_paths)}')
    if len(video_paths) != 500:
        raise ValueError(f'Expected 500 compiled production videos, found {len(video_paths)}')

    if not ASSET_LIBRARY_PATH.exists() or not ASSET_REQUIREMENTS_PATH.exists():
        raise ValueError('Asset planning files are missing. Run python -m src.studio.cli build --materialize')

    production_manifest = read_json(MANIFEST_PATH)
    demo_manifest = read_json(DEMO_MANIFEST_PATH)
    validate_with_schema(production_manifest, 'production_manifest', MANIFEST_PATH.name)
    validate_with_schema(demo_manifest, 'demo_manifest', DEMO_MANIFEST_PATH.name)

    if len(production_manifest) != 500:
        raise ValueError(f'Expected 500 production manifest entries, found {len(production_manifest)}')

    allowed_assets = flatten_asset_library(read_json(ASSET_LIBRARY_PATH))

    for path in storyboard_paths:
        expected_topic = str(topics_index[path.stem]['topic'])
        validate_storyboard(path, expected_topic, allowed_assets)

    for path in video_paths:
        expected_topic = str(topics_index[path.stem]['topic'])
        validate_compiled_video(path, expected_topic, allowed_assets)

    for path in demo_paths:
        validate_demo_payload(path)

    validate_manifest_consistency(production_manifest, demo_manifest, storyboard_paths, video_paths, demo_paths)

    print('Storyboard-first library validation passed')
    print(f'Production storyboards: {len(storyboard_paths)}')
    print(f'Compiled production videos: {len(video_paths)}')
    print(f'Demo payloads: {len(demo_paths)}')


if __name__ == '__main__':
    validate()
