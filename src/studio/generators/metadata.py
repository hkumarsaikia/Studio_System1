from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from src.studio.config import DEMOS_DIR, METADATA_OUTPUT_DIR, STORYBOARDS_DIR, ensure_directories
from src.studio.contracts import DEFAULT_PROFILE_IDS, RENDER_PROFILES, is_demo_video_id, is_production_video_id
from src.studio.generators.topic_library import load_demo_payload

WORD_RE = re.compile(r"[A-Za-z0-9']+")
CATEGORY_HASHTAGS = {
    'EVERYDAY SYSTEMS': ['#EverydaySystems', '#DailyLife', '#SystemsThinking'],
    'MONEY & ECONOMICS': ['#Economics', '#Money', '#SystemsThinking'],
    'INFORMATION SYSTEMS': ['#InformationSystems', '#Tech', '#SystemsThinking'],
    'POWER & INSTITUTIONS': ['#Institutions', '#Power', '#SystemsThinking'],
    'FUTURE SYSTEMS': ['#FutureSystems', '#Innovation', '#SystemsThinking'],
}
PROFILE_HASHTAGS = {
    'shorts_vertical': ['#YouTubeShorts', '#Shorts'],
    'social_square': ['#SocialVideo', '#SquareVideo'],
    'youtube_horizontal': ['#YouTube', '#ExplainerVideo'],
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



def build_keywords(title: str, category: str, scenes: list[dict[str, object]]) -> list[str]:
    seen: set[str] = set()
    keywords: list[str] = []
    for token in tokenize(title) + tokenize(category):
        if len(token) < 3 or token in seen:
            continue
        seen.add(token)
        keywords.append(token)
    for scene in scenes:
        for field_name in ('label', 'purpose', 'onScreenText'):
            for token in tokenize(str(scene.get(field_name, ''))):
                if len(token) < 3 or token in seen:
                    continue
                seen.add(token)
                keywords.append(token)
    return keywords[:20]



def build_hashtags(title: str, category: str, profile_id: str | None = None) -> list[str]:
    tags = list(CATEGORY_HASHTAGS.get(category, ['#SystemsThinking']))
    if profile_id:
        for tag in PROFILE_HASHTAGS.get(profile_id, []):
            if tag not in tags:
                tags.append(tag)
    for token in WORD_RE.findall(title):
        if len(token) < 4:
            continue
        hashtag = '#' + ''.join(part.capitalize() for part in re.split(r'[^A-Za-z0-9]+', token) if part)
        if hashtag not in tags:
            tags.append(hashtag)
        if len(tags) >= 10:
            break
    return tags[:10]



def build_description(title: str, category: str, narration_lines: list[str], profile_id: str | None = None) -> str:
    intro = f'{title} explained as a programmable systems video.'
    profile_label = RENDER_PROFILES[profile_id]['label'] if profile_id in RENDER_PROFILES else 'Canonical Pack'
    body = ' '.join(line.strip() for line in narration_lines[:4])
    closing = f'Category: {category}. Profile: {profile_label}.'
    return f'{intro} {body} {closing}'.strip()[:700]



def build_profile_pack(
    profile_id: str,
    title: str,
    category: str,
    keywords: list[str],
    narration_lines: list[str],
) -> dict[str, object]:
    profile = RENDER_PROFILES[profile_id]
    return {
        'profileId': profile_id,
        'label': profile['label'],
        'platformTargets': profile['platforms'],
        'aspectRatio': profile['aspectRatio'],
        'width': profile['width'],
        'height': profile['height'],
        'fps': profile['fps'],
        'durationSeconds': profile['timeline']['totalSeconds'],
        'title': title,
        'description': build_description(title, category, narration_lines, profile_id),
        'hashtags': build_hashtags(title, category, profile_id),
        'keywords': keywords,
    }



def generate_metadata(video_id: str) -> dict[str, object]:
    if is_production_video_id(video_id):
        storyboard = load_storyboard(video_id)
        title = str(storyboard['title'])
        category = str(storyboard.get('category', 'SYSTEMS'))
        scenes = list(storyboard.get('scenePlan', []))
        narration_lines = [str(scene.get('narrationText', '')) for scene in scenes]
        summary_scenes = [
            {
                'sceneId': scene['sceneId'],
                'label': scene['label'],
                'purpose': scene.get('purpose', ''),
                'onScreenText': scene.get('onScreenText', ''),
                'narrationText': scene.get('narrationText', ''),
            }
            for scene in scenes
        ]
        keywords = build_keywords(title, category, summary_scenes)
        profile_ids = [
            profile_id
            for profile_id in storyboard.get('defaultProfiles', list(DEFAULT_PROFILE_IDS))
            if profile_id in RENDER_PROFILES
        ]
        metadata = {
            'id': video_id,
            'dataset': 'production',
            'title': title,
            'category': category,
            'templateFamily': storyboard.get('templateFamily', 'systems_explainer'),
            'audioMode': storyboard.get('audioMode', 'text_only'),
            'description': build_description(title, category, narration_lines),
            'hashtags': build_hashtags(title, category),
            'keywords': keywords,
            'metadataHints': storyboard.get('metadataHints', {}),
            'profiles': {
                profile_id: build_profile_pack(profile_id, title, category, keywords, narration_lines)
                for profile_id in profile_ids
            },
            'scenePlan': summary_scenes,
        }
        return metadata

    if is_demo_video_id(video_id):
        payload = load_demo_payload(video_id)
        title = str(payload['title'])
        category = str(payload.get('category', 'DEMO'))
        scenes = list(payload.get('scenes', []))
        narration_lines = [str(scene.get('narrationText') or scene.get('subtext') or scene.get('text', '')) for scene in scenes]
        summary_scenes = [
            {
                'sceneId': scene.get('sceneId', f'scene_{index + 1:02d}'),
                'label': scene.get('label', scene.get('text', f'Scene {index + 1}')),
                'narrationText': scene.get('narrationText') or scene.get('subtext') or scene.get('text', ''),
            }
            for index, scene in enumerate(scenes)
        ]
        keywords = build_keywords(title, category, summary_scenes)
        return {
            'id': video_id,
            'dataset': 'demo',
            'title': title,
            'category': category,
            'description': build_description(title, category, narration_lines),
            'hashtags': build_hashtags(title, category),
            'keywords': keywords,
            'profiles': {
                'demo': {
                    'profileId': 'demo',
                    'label': 'Demo Payload',
                    'platformTargets': ['Preview'],
                    'durationSeconds': sum(int(scene.get('duration', 0)) for scene in scenes) / 30 if scenes else 0,
                    'title': title,
                    'description': build_description(title, category, narration_lines),
                    'hashtags': build_hashtags(title, category),
                    'keywords': keywords,
                }
            },
            'scenePlan': summary_scenes,
        }

    raise ValueError(f'Unsupported id for metadata: {video_id}')



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
