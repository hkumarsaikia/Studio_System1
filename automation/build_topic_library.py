"""
FILE: build_topic_library.py
PURPOSE: Master builder for the 500-video data layer.

This is the most important automation script — it reads Topics.txt (500 topics)
and generates the entire data layer that the Remotion engine consumes:

OUTPUT FILES:
  - data/videos/video_001.json → video_500.json (individual video blueprints)
  - data/video_manifest.json (lookup index for all 500 videos)
  - engine/src/generated/videoManifest.js (JS manifest for Remotion imports)
  - data/asset_library.json (available SVG assets/icons)
  - data/asset_requirements_500.json (per-video asset requirements)

FEATURES:
  - Camera action assignment per scene (7 action types)
  - Category-specific color palettes (5 categories × unique colors)
  - Person mood per crowd scene (neutral, stressed, happy, thinking)
  - Parametric visual data (bar values, flow labels, network nodes, etc.)
  - Richer subtexts templated from scene labels

CATEGORY SYSTEM (100 topics each):
  1-100:   EVERYDAY SYSTEMS     → Sky blue accent
  101-200: MONEY & ECONOMICS    → Green accent
  201-300: INFORMATION SYSTEMS  → Pink accent
  301-400: POWER & INSTITUTIONS → Purple accent
  401-500: FUTURE SYSTEMS       → Teal accent

USAGE:
  python automation/build_topic_library.py                  # Build manifest only
  python automation/build_topic_library.py --materialize    # Write all 500 JSON files
"""
import argparse
import json
import re
from pathlib import Path

# ── Path Configuration ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
TOPICS_TXT = ROOT / 'data' / 'Topics.txt'
VIDEOS_DIR = ROOT / 'data' / 'videos'
MANIFEST_PATH = ROOT / 'data' / 'video_manifest.json'
ENGINE_MANIFEST_PATH = ROOT / 'engine' / 'src' / 'generated' / 'videoManifest.js'
ASSET_LIBRARY_PATH = ROOT / 'data' / 'asset_library.json'
ASSET_REQUIREMENTS_PATH = ROOT / 'data' / 'asset_requirements_500.json'

# ── Asset Library ───────────────────────────────────────────────────
# Defines all available SVG assets that scenes can reference.
# This is saved as data/asset_library.json for external tools.
BASE_ASSET_LIBRARY = {
    'humans': ['person_adult_female', 'person_adult_male', 'person_youth', 'person_senior', 'crowd_group_8', 'crowd_group_16'],
    'animals': ['bird', 'fish', 'deer', 'cow', 'bee', 'turtle'],
    'objects': ['coin', 'bank', 'factory', 'house', 'cart', 'briefcase', 'microphone', 'cloud', 'chip', 'gavel'],
    'icons': ['bank', 'factory', 'home', 'cart', 'hospital', 'school', 'transport', 'energy', 'law', 'media', 'cloud', 'ai',
              'algorithm', 'pollution', 'coin', 'shield', 'globe', 'lightning', 'gear', 'people', 'chart', 'arrow',
              'loop', 'scale', 'network', 'lock', 'book', 'wave'],
    'backdrops': ['gradient_system', 'city_street', 'landscape_sunrise'],
    'charts': ['bars', 'flow', 'network'],
}

# ── Category Definitions ────────────────────────────────────────────
# Each category has a unique accent color and dark palette for backgrounds.
# Topics 1-100 get EVERYDAY SYSTEMS colors, 101-200 get MONEY colors, etc.
CATEGORIES = {
    'EVERYDAY SYSTEMS':     {'accent': '#38bdf8', 'palette': {'background': '#0f172a', 'secondary': '#1e293b'}},
    'MONEY & ECONOMICS':    {'accent': '#22c55e', 'palette': {'background': '#052e16', 'secondary': '#14532d'}},
    'INFORMATION SYSTEMS':  {'accent': '#f472b6', 'palette': {'background': '#1a0524', 'secondary': '#3b0764'}},
    'POWER & INSTITUTIONS': {'accent': '#a78bfa', 'palette': {'background': '#1e1b4b', 'secondary': '#312e81'}},
    'FUTURE SYSTEMS':       {'accent': '#14b8a6', 'palette': {'background': '#042f2e', 'secondary': '#134e4a'}},
}

# Icons most relevant to each category (used in 'icons' visual scenes)
CATEGORY_ASSET_TAGS = {
    'EVERYDAY SYSTEMS':     ['home', 'cart', 'transport', 'people', 'factory'],
    'MONEY & ECONOMICS':    ['bank', 'coin', 'chart', 'factory', 'globe'],
    'INFORMATION SYSTEMS':  ['media', 'cloud', 'ai', 'network', 'algorithm'],
    'POWER & INSTITUTIONS': ['law', 'shield', 'scale', 'people', 'book'],
    'FUTURE SYSTEMS':       ['ai', 'gear', 'lightning', 'globe', 'wave'],
}

# ── Scene Blueprint ─────────────────────────────────────────────────
# Every video has exactly 12 scenes in this order. Each scene specifies:
#   label  → Human-readable scene name (used for text if not Topic frame)
#   visual → Component type from SceneFactory
#   action → Camera movement from Camera.jsx
#   mood   → Person mood for crowd scenes
SCENE_BLUEPRINT = [
    {'label': 'Topic frame',           'visual': 'crowd',     'action': 'slow_zoom_in',       'mood': 'neutral'},
    {'label': 'Hook',                  'visual': 'icons',     'action': 'pan_right',          'mood': 'stressed'},
    {'label': 'System boundary',       'visual': 'network',   'action': 'static_focus',       'mood': 'thinking'},
    {'label': 'Cause layer 1',         'visual': 'bars',      'action': 'slow_zoom_in',       'mood': 'neutral'},
    {'label': 'Cause layer 2',         'visual': 'flow',      'action': 'pan_left',           'mood': 'neutral'},
    {'label': 'Cause layer 3',         'visual': 'lattice',   'action': 'dramatic_pull_back', 'mood': 'stressed'},
    {'label': 'Data lens',             'visual': 'bars',      'action': 'slow_pan_up',        'mood': 'thinking'},
    {'label': 'Real world scene',      'visual': 'city',      'action': 'pan_right',          'mood': 'neutral'},
    {'label': 'Ecology/externalities', 'visual': 'animals',   'action': 'slow_zoom_in',       'mood': 'neutral'},
    {'label': 'Macro trend',           'visual': 'earth',     'action': 'slow_pan_down',      'mood': 'thinking'},
    {'label': 'Actionable takeaway',   'visual': 'icons',     'action': 'dramatic_pull_back', 'mood': 'happy'},
    {'label': 'Closing',               'visual': 'crowd',     'action': 'slow_zoom_in',       'mood': 'happy'},
]

# Template subtexts for each scene label. {topic} is replaced with the actual topic.
SCENE_SUBTEXTS = {
    'Topic frame':           'A systems explainer in 2 minutes.',
    'Hook':                  'Why this matters in daily life: {topic}',
    'System boundary':       'Where does the system begin and end?',
    'Cause layer 1':         'The primary driver behind {topic}.',
    'Cause layer 2':         'How mechanisms propagate through the system.',
    'Cause layer 3':         'Feedback loops that amplify or dampen effects.',
    'Data lens':             'What the numbers tell us about {topic}.',
    'Real world scene':      'How this plays out on the street.',
    'Ecology/externalities': 'The hidden costs no one talks about.',
    'Macro trend':           'Where this is headed in the next decade.',
    'Actionable takeaway':   'What you can actually do about it.',
    'Closing':               'Understand systems, predict outcomes, act early.',
}


def parse_topics() -> list[dict]:
    """Parse Topics.txt into a list of {index, topic} dictionaries."""
    topics = []
    for line in TOPICS_TXT.read_text(encoding='utf-8').splitlines():
        # Match lines like "1. How Tax Systems Determine Wealth Distribution"
        match = re.match(r'^(\d+)\.\s+(.+?)\s*$', line)
        if match:
            topics.append({'index': int(match.group(1)), 'topic': match.group(2)})
    if len(topics) != 500:
        raise ValueError(f'Expected 500 topics but found {len(topics)}')
    return topics


def infer_category(index: int) -> str:
    """Determine category based on topic index (100 topics per category)."""
    if index <= 100:
        return 'EVERYDAY SYSTEMS'
    if index <= 200:
        return 'MONEY & ECONOMICS'
    if index <= 300:
        return 'INFORMATION SYSTEMS'
    if index <= 400:
        return 'POWER & INSTITUTIONS'
    return 'FUTURE SYSTEMS'


def scene_payload(topic: str, index: int, step: int, blueprint: dict, category: str) -> dict:
    """
    Build the JSON payload for a single scene.

    Combines the blueprint template with topic-specific data to create
    a complete scene object ready for the Remotion engine.
    """
    cat = CATEGORIES[category]
    # Seed creates slight variation between videos for parametric data
    seed = (index % 9) + step
    label = blueprint['label']

    # Build subtext from template, replacing {topic} placeholder
    subtext_tmpl = SCENE_SUBTEXTS.get(label, f'{label} for topic: {{topic}}')
    subtext = subtext_tmpl.format(topic=topic)

    # Scene title: use the topic name for the first scene, label for others
    if label == 'Topic frame':
        text = topic
    elif label == 'Hook':
        text = 'Hook'
    elif label == 'Closing':
        text = 'Closing'
    else:
        text = label

    # Base scene payload (every scene has these fields)
    payload = {
        'text': text,
        'subtext': subtext,
        'duration': 300,                         # 10 seconds at 30fps
        'visual': blueprint['visual'],
        'action': blueprint['action'],           # Camera movement type
        'category': category,
        'accentColor': cat['accent'],            # Category accent color
        'palette': cat['palette'],               # Background gradient colors
        'assetTags': CATEGORY_ASSET_TAGS[category],
    }

    # ── Visual-specific parametric data ─────────────────────────────
    # Each visual type has its own data fields that customize the rendering
    visual = blueprint['visual']

    if visual == 'crowd':
        payload['crowdCount'] = 10 + (index % 8)     # 10-17 people
        payload['mood'] = blueprint['mood']           # Facial expression

    if visual == 'bars':
        # Generate 5 bar values with slight per-video variation
        payload['barValues'] = [18 + seed, 26 + seed, 36 + seed, 47 + seed, 58 + seed]

    if visual == 'flow':
        # Different labels for Cause layer 2 vs other flow scenes
        payload['flowLabels'] = ['Trigger', 'Mechanism', 'Outcome'] if step == 5 else ['Input', 'System', 'Output']

    if visual == 'network':
        # Different node labels for System boundary vs Cause layer 3
        payload['networkNodes'] = ['State', 'Market', 'Labor', 'Capital', 'Public'] if step == 3 else ['Policy', 'Price', 'Behavior', 'Risk', 'Feedback']

    if visual == 'icons':
        # First 3 from category + 3 universal icons
        payload['icons'] = CATEGORY_ASSET_TAGS[category][:3] + ['bank', 'factory', 'home']

    if visual == 'animals':
        # Different animals by category for variety
        payload['animals'] = ['bird', 'turtle', 'deer'] if category == 'FUTURE SYSTEMS' else ['bird', 'fish', 'bee']

    return payload


def base_scenes(topic: str, index: int) -> list[dict]:
    """Build the full 12-scene array for a video."""
    category = infer_category(index)
    scenes = []
    for i, blueprint in enumerate(SCENE_BLUEPRINT, start=1):
        scenes.append(scene_payload(topic, index, i, blueprint, category))
    return scenes


def make_video_payload(index: int, topic: str) -> dict:
    """Build the complete video JSON structure for one topic."""
    video_id = f'video_{index:03d}'
    category = infer_category(index)
    cat = CATEGORIES[category]
    return {
        'id': video_id,
        'title': topic,
        'template': 'explainer' if index % 3 == 0 else 'protest',  # Alternate templates
        'fps': 30,
        'width': 1080,
        'height': 1920,       # 9:16 vertical format
        'category': category,
        'accentColor': cat['accent'],
        'scenes': base_scenes(topic, index),
    }


def write_engine_manifest(video_ids: list[str]) -> None:
    """
    Generate the JavaScript manifest that Remotion uses to import video data.
    This creates engine/src/generated/videoManifest.js with a dynamic import
    function that loads the correct JSON file at render time.
    """
    lines = [
        'export const videoIds = ' + json.dumps(video_ids, ensure_ascii=False, indent=2) + ';',
        '',
        'export const getVideoData = async (videoId) => {',
        "  const id = videoId || 'video_001';",
        '  const safeId = videoIds.includes(id) ? id : \"video_001\";',
        '  const module = await import(`../../../data/videos/${safeId}.json`);',
        '  return module.default;',
        '};',
        '',
    ]
    ENGINE_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENGINE_MANIFEST_PATH.write_text('\n'.join(lines), encoding='utf-8')


def write_asset_requirements(all_payloads: list[dict]) -> None:
    """
    Analyze all 500 video payloads and write:
      1. asset_library.json — the canonical list of available assets
      2. asset_requirements_500.json — which assets each video uses
    """
    requirements = {
        'assetLibrary': BASE_ASSET_LIBRARY,
        'categoryAssetTags': CATEGORY_ASSET_TAGS,
        'sceneBlueprint': [[b['label'], b['visual'], b['action']] for b in SCENE_BLUEPRINT],
        'videos': {},
    }

    for payload in all_payloads:
        # Collect all unique assets, visuals, and actions used by this video
        used_assets = set()
        used_visuals = set()
        used_actions = set()
        for scene in payload['scenes']:
            used_visuals.add(scene['visual'])
            used_actions.add(scene['action'])
            for tag in scene.get('assetTags', []):
                used_assets.add(tag)
            # Also collect items from parametric data fields
            for k in ['icons', 'animals', 'networkNodes', 'flowLabels']:
                for item in scene.get(k, []):
                    used_assets.add(str(item))

        requirements['videos'][payload['id']] = {
            'title': payload['title'],
            'category': payload['category'],
            'visuals': sorted(used_visuals),
            'actions': sorted(used_actions),
            'assets': sorted(used_assets),
        }

    ASSET_LIBRARY_PATH.write_text(json.dumps(BASE_ASSET_LIBRARY, indent=2) + '\n', encoding='utf-8')
    ASSET_REQUIREMENTS_PATH.write_text(json.dumps(requirements, indent=2), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Build topic library and video manifests')
    parser.add_argument('--materialize', action='store_true', help='Write all 500 video JSON files to data/videos')
    args = parser.parse_args()

    topics = parse_topics()
    manifest = {}
    all_payloads = []

    if args.materialize:
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Process all 500 topics ──────────────────────────────────────
    for item in topics:
        payload = make_video_payload(item['index'], item['topic'])
        all_payloads.append(payload)

        # Add to manifest index
        manifest[payload['id']] = {
            'title': payload['title'],
            'template': payload['template'],
            'category': payload['category'],
            'sceneCount': len(payload['scenes']),
        }

        # Write individual video JSON if materializing
        if args.materialize:
            (VIDEOS_DIR / f"{payload['id']}.json").write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8',
            )

    # ── Write manifests and asset files ─────────────────────────────
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    write_engine_manifest(sorted(manifest.keys()))
    write_asset_requirements(all_payloads)

    print(f'Built manifest for {len(manifest)} videos')
    if args.materialize:
        print(f'Materialized video files in: {VIDEOS_DIR}')


if __name__ == '__main__':
    main()
