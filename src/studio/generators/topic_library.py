from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Iterable

from src.studio.config import ARCHIVE_DIR, DATA_DIR, DEMOS_DIR, ENGINE_DIR, STORYBOARDS_DIR, TOPICS_FILE, VIDEOS_DIR, ensure_directories
from src.studio.contracts import (
    BASE_ASSET_LIBRARY,
    CATEGORIES,
    CATEGORY_ASSET_TAGS,
    DEFAULT_FPS,
    DEFAULT_HEIGHT,
    DEFAULT_ON_SCREEN_TEXT,
    DEFAULT_OVERLAYS,
    DEFAULT_SCENE_DURATION,
    DEFAULT_WIDTH,
    PRODUCTION_SEGMENT_COUNT,
    PRODUCTION_SEGMENT_SECONDS,
    SUPPORTED_VISUALS,
    default_template_for_index,
    infer_category,
)
from src.studio.generators.narrative_engine import NarrativeEngine

TOPIC_LINE_RE = re.compile(r'^(\d+)\.\s+(.+?)\s*$')
MANIFEST_PATH = DATA_DIR / 'video_manifest.json'
DEMO_MANIFEST_PATH = DATA_DIR / 'demo_manifest.json'
ENGINE_MANIFEST_PATH = ENGINE_DIR / 'src' / 'generated' / 'videoManifest.js'
ASSET_LIBRARY_PATH = DATA_DIR / 'asset_library.json'
ASSET_REQUIREMENTS_PATH = DATA_DIR / 'asset_requirements_500.json'
LEGACY_ARCHIVE_DIR = ARCHIVE_DIR / 'legacy_payloads'

LEGACY_DEMO_SOURCES = {
    'demo_graphics_showcase_v1': 'video_500.json',
    'demo_combined_features_30s': 'video_501.json',
    'demo_combined_features_30s_60fps': 'video_502.json',
    'demo_graphics_showcase_v2': 'video_503.json',
}

SEGMENT_BLUEPRINT = (
    {
        'label': 'Topic frame',
        'visual': 'crowd',
        'cameraAction': 'slow_zoom_in',
        'mood': 'neutral',
        'visualDirection': 'Open on people and motion to make the topic feel immediate and human.',
    },
    {
        'label': 'Hook',
        'visual': 'icons',
        'cameraAction': 'pan_right',
        'mood': 'stressed',
        'visualDirection': 'Use a dense icon field that quickly frames the pressure point or conflict.',
    },
    {
        'label': 'System boundary',
        'visual': 'network',
        'cameraAction': 'static_focus',
        'mood': 'thinking',
        'visualDirection': 'Show the system as connected nodes so the audience sees where the edges are.',
    },
    {
        'label': 'Cause layer 1',
        'visual': 'math_equation',
        'cameraAction': 'slow_zoom_in',
        'mood': 'neutral',
        'visualDirection': 'Present the first causal layer as a simple abstract mechanism or formula.',
    },
    {
        'label': 'Cause layer 2',
        'visual': 'flow',
        'cameraAction': 'pan_left',
        'mood': 'neutral',
        'visualDirection': 'Turn the mechanism into directional movement so cause and effect read instantly.',
    },
    {
        'label': 'Cause layer 3',
        'visual': 'lattice',
        'cameraAction': 'dramatic_pull_back',
        'mood': 'stressed',
        'visualDirection': 'Reveal the deeper feedback structure with denser motion and higher visual complexity.',
    },
    {
        'label': 'Data lens',
        'visual': 'neural_core',
        'cameraAction': 'slow_pan_up',
        'mood': 'thinking',
        'visualDirection': 'Shift to a data-centric visual that feels analytical and system-wide.',
    },
    {
        'label': 'Real world scene',
        'visual': 'city',
        'cameraAction': 'pan_right',
        'mood': 'neutral',
        'visualDirection': 'Bring the abstract explanation back to a concrete everyday environment.',
    },
    {
        'label': 'Ecology/externalities',
        'visual': 'animals',
        'cameraAction': 'slow_zoom_in',
        'mood': 'neutral',
        'visualDirection': 'Show hidden side effects with ecological or externality imagery.',
    },
    {
        'label': 'Macro trend',
        'visual': 'earth',
        'cameraAction': 'slow_pan_down',
        'mood': 'thinking',
        'visualDirection': 'Zoom outward and frame the topic as part of a wider long-range pattern.',
    },
    {
        'label': 'Actionable takeaway',
        'visual': 'icons',
        'cameraAction': 'dramatic_pull_back',
        'mood': 'happy',
        'visualDirection': 'Return to a clear icon-driven summary that points toward action.',
    },
    {
        'label': 'Closing',
        'visual': 'crowd',
        'cameraAction': 'slow_zoom_in',
        'mood': 'happy',
        'visualDirection': 'Close on people again so the system explanation resolves back to human consequence.',
    },
)


def parse_topics() -> list[dict[str, object]]:
    topics: list[dict[str, object]] = []
    for line in TOPICS_FILE.read_text(encoding='utf-8').splitlines():
        match = TOPIC_LINE_RE.match(line)
        if match:
            topics.append({'index': int(match.group(1)), 'topic': match.group(2)})
    if len(topics) != 500:
        raise ValueError(f'Expected 500 topics but found {len(topics)}')
    return topics


def build_topics_index() -> dict[str, dict[str, object]]:
    index: dict[str, dict[str, object]] = {}
    for item in parse_topics():
        video_id = f"video_{int(item['index']):03d}"
        index[video_id] = item
    return index


def derive_on_screen_text(topic: str, label: str) -> str:
    token = DEFAULT_ON_SCREEN_TEXT[label]
    return topic if token == 'topic' else token


def default_background_mode(category: str, visual: str) -> str:
    if visual == 'earth' or category == 'FUTURE SYSTEMS':
        return 'terrain'
    if visual in {'network', 'lattice', 'neural_core', 'math_equation'}:
        return 'mesh'
    return 'gradient'


def default_motion(visual: str) -> str:
    if visual in {'earth', 'lattice', 'neural_core'}:
        return 'drift'
    return 'pan'


def default_overlays(visual: str) -> list[str]:
    overlays = list(DEFAULT_OVERLAYS)
    if visual in {'network', 'lattice', 'neural_core', 'earth'}:
        overlays.append('scanlines')
    return overlays


def default_asset_refs(category: str, visual: str, step: int) -> list[str]:
    category_refs = CATEGORY_ASSET_TAGS[category]
    if visual == 'crowd':
        return ['CharacterHappy', 'CharacterSad', 'CharacterGeek']
    if visual == 'icons':
        return category_refs[:3] + ['PropDeclarativeRobot', 'PropServer', 'PropDeclarativeSaturn']
    if visual == 'animals':
        return ['bird', 'turtle', 'deer'] if category == 'FUTURE SYSTEMS' else ['bird', 'fish', 'bee']
    if visual == 'network':
        return category_refs[:3] + ['network', 'arrow']
    if visual == 'flow':
        return ['arrow', 'loop'] + category_refs[:2]
    if visual == 'math_equation':
        return ['chart', 'arrow', 'gear'] + category_refs[:2]
    if visual == 'neural_core':
        return ['ai', 'network', 'cloud'] + category_refs[:2]
    if visual == 'earth':
        return ['globe', 'cloud', 'wave'] + category_refs[:2]
    if visual == 'city':
        return ['home', 'transport', 'factory']
    if visual == 'lattice':
        return ['network', 'gear', 'algorithm'] + category_refs[:2]
    return category_refs


def build_storyboard_segment(topic: str, index: int, step: int, blueprint: dict[str, str], category: str) -> dict[str, object]:
    label = blueprint['label']
    visual = blueprint['visual']
    mood = blueprint['mood']
    category_meta = CATEGORIES[category]
    return {
        'index': step,
        'segmentId': f'segment_{step:02d}',
        'label': label,
        'narrationText': NarrativeEngine.generate_narration(topic, label, category, mood),
        'onScreenText': derive_on_screen_text(topic, label),
        'subtext': NarrativeEngine.generate_subtext(topic, label, category, mood),
        'visual': visual,
        'visualDirection': blueprint['visualDirection'],
        'assetRefs': default_asset_refs(category, visual, step),
        'cameraAction': blueprint['cameraAction'],
        'palette': category_meta['palette'],
        'backgroundMode': default_background_mode(category, visual),
        'motion': default_motion(visual),
        'overlays': default_overlays(visual),
        'mood': mood,
    }


def create_storyboard_payload(index: int, topic: str) -> dict[str, object]:
    video_id = f'video_{index:03d}'
    category = infer_category(index)
    category_meta = CATEGORIES[category]
    segments = [
        build_storyboard_segment(topic, index, step, blueprint, category)
        for step, blueprint in enumerate(SEGMENT_BLUEPRINT, start=1)
    ]
    return {
        'id': video_id,
        'topic': topic,
        'title': topic,
        'template': default_template_for_index(index),
        'fps': DEFAULT_FPS,
        'width': DEFAULT_WIDTH,
        'height': DEFAULT_HEIGHT,
        'segmentCount': PRODUCTION_SEGMENT_COUNT,
        'segmentSeconds': PRODUCTION_SEGMENT_SECONDS,
        'category': category,
        'accentColor': category_meta['accent'],
        'segments': segments,
    }


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def ensure_storyboards(
    topics_index: dict[str, dict[str, object]],
    only_video_ids: Iterable[str] | None = None,
    force_storyboards: bool = False,
    materialize: bool = True,
) -> tuple[list[dict[str, object]], int, int]:
    storyboard_payloads: list[dict[str, object]] = []
    created = 0
    preserved = 0
    selected_ids = list(only_video_ids) if only_video_ids is not None else sorted(topics_index.keys())

    for video_id in selected_ids:
        topic_entry = topics_index.get(video_id)
        if topic_entry is None:
            raise ValueError(f'Unknown production video id: {video_id}')

        storyboard_path = STORYBOARDS_DIR / f'{video_id}.json'
        if storyboard_path.exists() and not force_storyboards:
            storyboard_payloads.append(read_json(storyboard_path))
            preserved += 1
            continue

        storyboard = create_storyboard_payload(int(topic_entry['index']), str(topic_entry['topic']))
        if materialize:
            write_json(storyboard_path, storyboard)
        storyboard_payloads.append(storyboard)
        created += 1

    return storyboard_payloads, created, preserved


def compile_segment(storyboard: dict[str, object], segment: dict[str, object]) -> dict[str, object]:
    video_id = str(storyboard['id'])
    video_index = int(video_id.split('_')[1])
    step = int(segment['index'])
    category = str(storyboard.get('category') or infer_category(video_index))
    category_meta = CATEGORIES[category]
    accent_color = str(storyboard.get('accentColor') or category_meta['accent'])
    visual = str(segment['visual'])
    mood = str(segment.get('mood') or 'neutral')
    asset_refs = [str(item) for item in segment.get('assetRefs', [])]

    payload: dict[str, object] = {
        'segmentId': segment['segmentId'],
        'label': segment['label'],
        'narrationText': segment['narrationText'],
        'text': segment['onScreenText'],
        'subtext': segment['subtext'],
        'duration': int(storyboard.get('segmentSeconds', PRODUCTION_SEGMENT_SECONDS)) * int(storyboard.get('fps', DEFAULT_FPS)),
        'visual': visual,
        'action': segment['cameraAction'],
        'category': category,
        'accentColor': accent_color,
        'palette': segment['palette'],
        'assetTags': asset_refs,
        'visualDirection': segment['visualDirection'],
        'backgroundMode': segment.get('backgroundMode') or default_background_mode(category, visual),
        'motion': segment.get('motion') or default_motion(visual),
        'overlays': segment.get('overlays') or default_overlays(visual),
        'mood': mood,
    }

    seed = (video_index % 9) + step
    if mood == 'stressed':
        payload['weather'] = 'rain'
    elif category == 'EVERYDAY SYSTEMS' and mood == 'thinking':
        payload['weather'] = 'snow'

    if visual == 'crowd':
        payload['crowdCount'] = 10 + (video_index % 8)

    if visual == 'bars':
        payload['barValues'] = [18 + seed, 26 + seed, 36 + seed, 47 + seed, 58 + seed]

    if visual == 'flow':
        payload['flowLabels'] = ['Trigger', 'Mechanism', 'Outcome'] if step == 5 else ['Input', 'System', 'Output']

    if visual == 'network':
        payload['networkNodes'] = ['State', 'Market', 'Labor', 'Capital', 'Public'] if step == 3 else ['Policy', 'Price', 'Behavior', 'Risk', 'Feedback']

    if visual == 'icons':
        payload['icons'] = asset_refs or default_asset_refs(category, visual, step)

    if visual == 'animals':
        payload['animals'] = asset_refs or default_asset_refs(category, visual, step)

    return payload


def compile_storyboard(storyboard: dict[str, object]) -> dict[str, object]:
    video_id = str(storyboard['id'])
    video_index = int(video_id.split('_')[1])
    category = str(storyboard.get('category') or infer_category(video_index))
    category_meta = CATEGORIES[category]
    scenes = [compile_segment(storyboard, segment) for segment in storyboard['segments']]
    return {
        'id': video_id,
        'title': storyboard['title'],
        'topic': storyboard['topic'],
        'template': storyboard['template'],
        'fps': int(storyboard.get('fps', DEFAULT_FPS)),
        'width': int(storyboard.get('width', DEFAULT_WIDTH)),
        'height': int(storyboard.get('height', DEFAULT_HEIGHT)),
        'segmentCount': int(storyboard.get('segmentCount', PRODUCTION_SEGMENT_COUNT)),
        'segmentSeconds': int(storyboard.get('segmentSeconds', PRODUCTION_SEGMENT_SECONDS)),
        'category': category,
        'accentColor': str(storyboard.get('accentColor') or category_meta['accent']),
        'scenes': scenes,
    }


def compile_storyboards(storyboards: list[dict[str, object]], materialize: bool = True) -> list[dict[str, object]]:
    compiled_payloads: list[dict[str, object]] = []
    for storyboard in storyboards:
        compiled = compile_storyboard(storyboard)
        compiled_payloads.append(compiled)
        if materialize:
            write_json(VIDEOS_DIR / f"{compiled['id']}.json", compiled)
    return compiled_payloads


def write_production_manifest(storyboards: list[dict[str, object]], compiled_payloads: list[dict[str, object]]) -> None:
    manifest: dict[str, dict[str, object]] = {}
    storyboard_map = {str(item['id']): item for item in storyboards}
    for payload in compiled_payloads:
        video_id = str(payload['id'])
        storyboard = storyboard_map[video_id]
        manifest[video_id] = {
            'title': payload['title'],
            'topic': payload['topic'],
            'template': payload['template'],
            'category': payload['category'],
            'sceneCount': len(payload['scenes']),
            'segmentCount': int(storyboard.get('segmentCount', PRODUCTION_SEGMENT_COUNT)),
            'segmentSeconds': int(storyboard.get('segmentSeconds', PRODUCTION_SEGMENT_SECONDS)),
            'storyboard': f'data/storyboards/{video_id}.json',
        }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def write_demo_manifest(demo_payloads: list[dict[str, object]]) -> None:
    manifest: dict[str, dict[str, object]] = {}
    for payload in demo_payloads:
        demo_id = str(payload['id'])
        manifest[demo_id] = {
            'title': payload['title'],
            'template': payload.get('template', 'explainer'),
            'category': payload.get('category', 'DEMO'),
            'sceneCount': len(payload.get('scenes', [])),
        }
    DEMO_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def write_engine_manifest(production_ids: list[str], demo_ids: list[str]) -> None:
    demo_fallback = demo_ids[0] if demo_ids else None
    lines = [
        'export const productionVideoIds = ' + json.dumps(production_ids, ensure_ascii=False, indent=2) + ';',
        '',
        'export const demoVideoIds = ' + json.dumps(demo_ids, ensure_ascii=False, indent=2) + ';',
        '',
        'export const getVideoData = async (dataset, videoId) => {',
        "  const selectedDataset = dataset === 'demo' ? 'demo' : 'production';",
        '  if (selectedDataset === "demo") {',
        f'    const fallbackId = {json.dumps(demo_fallback)};',
        '    if (!fallbackId) {',
        '      throw new Error("No demo payloads are available.");',
        '    }',
        '    const safeId = demoVideoIds.includes(videoId) ? videoId : fallbackId;',
        '    const module = await import(`../../../data/demos/${safeId}.json`);',
        '    return module.default;',
        '  }',
        "  const id = videoId || 'video_001';",
        '  const safeId = productionVideoIds.includes(id) ? id : "video_001";',
        '  const module = await import(`../../../data/videos/${safeId}.json`);',
        '  return module.default;',
        '};',
        '',
    ]
    ENGINE_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENGINE_MANIFEST_PATH.write_text('\n'.join(lines), encoding='utf-8')


def write_asset_library() -> None:
    ASSET_LIBRARY_PATH.write_text(json.dumps(BASE_ASSET_LIBRARY, indent=2) + '\n', encoding='utf-8')


def write_asset_requirements(all_payloads: list[dict[str, object]]) -> None:
    requirements: dict[str, object] = {
        'assetLibrary': BASE_ASSET_LIBRARY,
        'categoryAssetTags': CATEGORY_ASSET_TAGS,
        'sceneBlueprint': [[step['label'], step['visual'], step['cameraAction']] for step in SEGMENT_BLUEPRINT],
        'videos': {},
    }

    for payload in all_payloads:
        used_assets: set[str] = set()
        used_visuals: set[str] = set()
        used_actions: set[str] = set()
        for scene in payload['scenes']:
            used_visuals.add(str(scene['visual']))
            used_actions.add(str(scene['action']))
            for item in scene.get('assetTags', []):
                used_assets.add(str(item))
            for key in ('icons', 'animals', 'networkNodes', 'flowLabels'):
                for item in scene.get(key, []):
                    used_assets.add(str(item))
        requirements['videos'][str(payload['id'])] = {
            'title': payload['title'],
            'category': payload['category'],
            'visuals': sorted(used_visuals),
            'actions': sorted(used_actions),
            'assets': sorted(used_assets),
        }

    ASSET_REQUIREMENTS_PATH.write_text(json.dumps(requirements, indent=2) + '\n', encoding='utf-8')


def archive_file(source: Path, target_name: str | None = None) -> Path:
    LEGACY_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    target = LEGACY_ARCHIVE_DIR / (target_name or source.name)
    if source.resolve() == target.resolve():
        return target
    if target.exists():
        source.unlink(missing_ok=True)
        return target
    shutil.move(str(source), str(target))
    return target


def find_legacy_source(source_name: str) -> Path | None:
    current = VIDEOS_DIR / source_name
    if current.exists():
        if source_name in {'video_501.json', 'video_502.json', 'video_503.json'}:
            return current
        payload = read_json(current)
        if len(payload.get('scenes', [])) != PRODUCTION_SEGMENT_COUNT:
            return current
    archived = LEGACY_ARCHIVE_DIR / source_name
    if archived.exists():
        return archived
    return None


def migrate_legacy_payloads(materialize: bool = True) -> list[dict[str, object]]:
    demo_payloads: list[dict[str, object]] = []
    if not materialize:
        return demo_payloads

    LEGACY_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    legacy_overview = VIDEOS_DIR / 'video_001.json'
    if legacy_overview.exists():
        payload = read_json(legacy_overview)
        if len(payload.get('scenes', [])) != PRODUCTION_SEGMENT_COUNT:
            archive_file(legacy_overview, 'video_001_legacy_showcase.json')

    legacy_backup = VIDEOS_DIR / 'video_500_backup_20260305_211242.json'
    if legacy_backup.exists():
        archive_file(legacy_backup)

    for demo_id, source_name in LEGACY_DEMO_SOURCES.items():
        source = find_legacy_source(source_name)
        if source is None:
            continue
        payload = read_json(source)
        payload['id'] = demo_id
        demo_path = DEMOS_DIR / f'{demo_id}.json'
        write_json(demo_path, payload)
        if source.parent == VIDEOS_DIR:
            archive_file(source)

    for path in sorted(DEMOS_DIR.glob('demo_*.json')):
        demo_payloads.append(read_json(path))

    return demo_payloads


def build_library(
    materialize: bool,
    force_storyboards: bool = False,
    only_video_ids: list[str] | None = None,
    refresh_manifests: bool = True,
) -> dict[str, int | list[dict[str, object]]]:
    ensure_directories()
    topics_index = build_topics_index()

    demo_payloads = migrate_legacy_payloads(materialize=materialize) if refresh_manifests else []
    storyboards, created_storyboards, preserved_storyboards = ensure_storyboards(
        topics_index,
        only_video_ids=only_video_ids,
        force_storyboards=force_storyboards,
        materialize=materialize,
    )
    compiled_payloads = compile_storyboards(storyboards, materialize=materialize)

    if materialize and refresh_manifests:
        write_production_manifest(storyboards, compiled_payloads)
        write_demo_manifest(demo_payloads)
        write_engine_manifest(
            sorted(str(payload['id']) for payload in compiled_payloads),
            sorted(str(payload['id']) for payload in demo_payloads),
        )
        write_asset_library()
        write_asset_requirements(compiled_payloads)

    return {
        'storyboards': storyboards,
        'compiled_payloads': compiled_payloads,
        'demo_payloads': demo_payloads,
        'created_storyboards': created_storyboards,
        'preserved_storyboards': preserved_storyboards,
    }


def materialize_production_video(video_id: str, force_storyboards: bool = False) -> dict[str, object]:
    summary = build_library(
        materialize=True,
        force_storyboards=force_storyboards,
        only_video_ids=[video_id],
        refresh_manifests=False,
    )
    compiled = summary['compiled_payloads']
    if not compiled:
        raise ValueError(f'No compiled payload created for {video_id}')
    return compiled[0]


def load_demo_payload(video_id: str) -> dict[str, object]:
    migrate_legacy_payloads(materialize=True)
    demo_path = DEMOS_DIR / f'{video_id}.json'
    if not demo_path.exists():
        raise FileNotFoundError(f'Demo payload not found: {demo_path}')
    return read_json(demo_path)


def main() -> None:
    parser = argparse.ArgumentParser(description='Build storyboard-first production payloads and manifests')
    parser.add_argument('--materialize', action='store_true', help='Write storyboards, compiled videos, and manifests to disk')
    parser.add_argument('--force-storyboards', action='store_true', help='Regenerate storyboard skeletons even when files already exist')
    args = parser.parse_args()

    summary = build_library(materialize=args.materialize, force_storyboards=args.force_storyboards)
    production_count = len(summary['compiled_payloads'])
    demo_count = len(summary['demo_payloads'])
    print(f'Production storyboards prepared: {len(summary["storyboards"])}')
    print(f'Created storyboards: {summary["created_storyboards"]}')
    print(f'Preserved storyboards: {summary["preserved_storyboards"]}')
    print(f'Compiled production payloads: {production_count}')
    print(f'Demo payloads available: {demo_count}')
    if args.materialize:
        print(f'Materialized storyboards in: {STORYBOARDS_DIR}')
        print(f'Materialized production payloads in: {VIDEOS_DIR}')
        print(f'Materialized demo payloads in: {DEMOS_DIR}')


if __name__ == '__main__':
    main()
