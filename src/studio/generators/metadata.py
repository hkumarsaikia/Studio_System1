from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from src.studio.config import DEMOS_DIR, METADATA_OUTPUT_DIR, STORYBOARDS_DIR, ensure_directories
from src.studio.contracts import is_demo_video_id, is_production_video_id
from src.studio.generators.topic_library import load_demo_payload

WORD_RE = re.compile(r"[A-Za-z0-9']+")
CATEGORY_HASHTAGS = {
    'EVERYDAY SYSTEMS': ['#EverydaySystems', '#DailyLife', '#SystemsThinking'],
    'MONEY & ECONOMICS': ['#Economics', '#Money', '#SystemsThinking'],
    'INFORMATION SYSTEMS': ['#InformationSystems', '#Tech', '#SystemsThinking'],
    'POWER & INSTITUTIONS': ['#Institutions', '#Power', '#SystemsThinking'],
    'FUTURE SYSTEMS': ['#FutureSystems', '#Innovation', '#SystemsThinking'],
}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding='utf-8'))


def load_storyboard(video_id: str) -> dict[str, object]:
    storyboard_path = STORYBOARDS_DIR / f'{video_id}.json'
    if not storyboard_path.exists():
        raise FileNotFoundError(f'Storyboard not found: {storyboard_path}')
    return read_json(storyboard_path)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in WORD_RE.findall(text)]


def build_keywords(title: str, category: str, segments: list[dict[str, object]]) -> list[str]:
    seen: set[str] = set()
    keywords: list[str] = []
    for token in tokenize(title) + tokenize(category):
        if len(token) < 3 or token in seen:
            continue
        seen.add(token)
        keywords.append(token)
    for segment in segments:
        for token in tokenize(str(segment.get('label', ''))):
            if len(token) < 3 or token in seen:
                continue
            seen.add(token)
            keywords.append(token)
    return keywords[:16]


def build_hashtags(title: str, category: str) -> list[str]:
    tags = list(CATEGORY_HASHTAGS.get(category, ['#SystemsThinking']))
    for token in WORD_RE.findall(title):
        if len(token) < 4:
            continue
        hashtag = '#' + ''.join(part.capitalize() for part in re.split(r'[^A-Za-z0-9]+', token) if part)
        if hashtag not in tags:
            tags.append(hashtag)
        if len(tags) >= 8:
            break
    if '#YouTubeShorts' not in tags:
        tags.append('#YouTubeShorts')
    return tags[:8]


def build_description(title: str, category: str, narration_lines: list[str]) -> str:
    intro = f'{title} explained as a 12-segment systems short.'
    body = ' '.join(line.strip() for line in narration_lines[:4])
    closing = f'Category: {category}.'
    description = f'{intro} {body} {closing}'.strip()
    return description[:600]


def generate_metadata(video_id: str) -> dict[str, object]:
    if is_production_video_id(video_id):
        storyboard = load_storyboard(video_id)
        title = str(storyboard['title'])
        category = str(storyboard.get('category', 'SYSTEMS'))
        segments = list(storyboard.get('segments', []))
        narration_lines = [str(segment.get('narrationText', '')) for segment in segments]
        summary_segments = [
            {
                'segmentId': segment['segmentId'],
                'label': segment['label'],
                'narrationText': segment['narrationText'],
            }
            for segment in segments
        ]
        dataset = 'production'
    elif is_demo_video_id(video_id):
        payload = load_demo_payload(video_id)
        title = str(payload['title'])
        category = str(payload.get('category', 'DEMO'))
        scenes = list(payload.get('scenes', []))
        narration_lines = [str(scene.get('narrationText') or scene.get('subtext') or scene.get('text', '')) for scene in scenes]
        summary_segments = [
            {
                'segmentId': scene.get('segmentId', f'scene_{index + 1:02d}'),
                'label': scene.get('label', scene.get('text', f'Scene {index + 1}')),
                'narrationText': scene.get('narrationText') or scene.get('subtext') or scene.get('text', ''),
            }
            for index, scene in enumerate(scenes)
        ]
        dataset = 'demo'
    else:
        raise ValueError(f'Unsupported id for metadata: {video_id}')

    metadata = {
        'id': video_id,
        'dataset': dataset,
        'title': title,
        'description': build_description(title, category, narration_lines),
        'hashtags': build_hashtags(title, category),
        'keywords': build_keywords(title, category, summary_segments),
        'category': category,
        'segments': summary_segments,
    }
    return metadata


def write_metadata(video_id: str) -> Path:
    ensure_directories()
    METADATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metadata = generate_metadata(video_id)
    output_path = METADATA_OUTPUT_DIR / f'{video_id}.json'
    output_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote metadata: {output_path}')
    return output_path


def batch_metadata() -> None:
    for path in sorted(STORYBOARDS_DIR.glob('video_*.json')):
        write_metadata(path.stem)


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate metadata JSON from storyboards or demo payloads')
    parser.add_argument('--video-id', type=str, default=None, help='Single video or demo id')
    parser.add_argument('--all', action='store_true', help='Generate metadata for all production storyboards')
    args = parser.parse_args()

    if args.all:
        batch_metadata()
    elif args.video_id:
        write_metadata(args.video_id)
    else:
        raise SystemExit('Provide --video-id or --all')


if __name__ == '__main__':
    main()
