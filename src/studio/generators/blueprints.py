"""
FILE: generate_blueprints.py
PURPOSE: Standalone blueprint generator — alternative to build_topic_library.py.

This script provides a focused, standalone approach to generating all 500
video blueprints. It's an enhanced version that focuses specifically on:
  - Camera action assignment per scene
  - Person mood assignment
  - Category-specific palette embedding
  - Richer subtext generation
  - Dry-run mode for validation

Unlike build_topic_library.py (which also writes asset files), this script
focuses solely on video JSONs and manifests.

OUTPUT FILES:
  - data/videos/video_001.json → video_500.json
  - data/video_manifest.json
  - engine/src/generated/videoManifest.js

USAGE:
  python scripts/generate_blueprints.py              # Generate all 500
  python scripts/generate_blueprints.py --dry-run    # Stats only, no files
"""
import argparse
import json
import re
import sys
from pathlib import Path

from src.studio.config import TOPICS_FILE, VIDEOS_DIR, ensure_directories, ROOT_DIR, ENGINE_DIR, DATA_DIR
from src.studio.generators.narrative_engine import NarrativeEngine

# ── Path Configuration ──────────────────────────────────────────────
TOPICS_TXT = TOPICS_FILE
MANIFEST_PATH = DATA_DIR / 'video_manifest.json'
ENGINE_MANIFEST_PATH = ENGINE_DIR / 'src' / 'generated' / 'videoManifest.js'

# ── Camera Actions ──────────────────────────────────────────────────
# All 7 available camera movements from Camera.jsx.
# Each scene in SCENE_BLUEPRINT references one of these.
CAMERA_ACTIONS = [
    'slow_zoom_in',
    'pan_right',
    'static_focus',
    'dramatic_pull_back',
    'pan_left',
    'slow_pan_up',
    'slow_pan_down',
]

# ── Category Definitions ────────────────────────────────────────────
# Same 5-category system as build_topic_library.py.
# Accent colors and palettes define the visual identity per category.
CATEGORIES = {
    'EVERYDAY SYSTEMS':     {'accent': '#38bdf8', 'palette': {'background': '#0f172a', 'secondary': '#1e293b'}},
    'MONEY & ECONOMICS':    {'accent': '#22c55e', 'palette': {'background': '#052e16', 'secondary': '#14532d'}},
    'INFORMATION SYSTEMS':  {'accent': '#f472b6', 'palette': {'background': '#1a0524', 'secondary': '#3b0764'}},
    'POWER & INSTITUTIONS': {'accent': '#a78bfa', 'palette': {'background': '#1e1b4b', 'secondary': '#312e81'}},
    'FUTURE SYSTEMS':       {'accent': '#14b8a6', 'palette': {'background': '#042f2e', 'secondary': '#134e4a'}},
}

# Category-specific icon sets for 'icons' visual scenes
CATEGORY_ASSET_TAGS = {
    'EVERYDAY SYSTEMS':     ['home', 'cart', 'transport', 'people', 'factory'],
    'MONEY & ECONOMICS':    ['bank', 'coin', 'chart', 'factory', 'globe'],
    'INFORMATION SYSTEMS':  ['media', 'cloud', 'ai', 'network', 'algorithm'],
    'POWER & INSTITUTIONS': ['law', 'shield', 'scale', 'people', 'book'],
    'FUTURE SYSTEMS':       ['ai', 'gear', 'lightning', 'globe', 'wave'],
}

# ── Scene Blueprint ─────────────────────────────────────────────────
# The canonical 12-scene structure that every video follows.
# This defines the narrative arc: Hook → Investigation → Data → Conclusion.
VISUAL_TYPES = {
    'everyday': ['crowd', 'flow', 'icons'],
    'money': ['bars', 'network', 'city', 'math_equation'],
    'info': ['network', 'flow', 'icons', 'earth', 'lattice', 'neural_core'],
    'power': ['city', 'network', 'crowd', 'math_equation'],
    'future': ['landscape', 'animals', 'earth', 'lattice', 'neural_core']
}
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

# Subtext templates — {topic} is replaced with the actual topic name
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
    """Parse Topics.txt into list of {index, topic}."""
    topics = []
    for line in TOPICS_TXT.read_text(encoding='utf-8').splitlines():
        match = re.match(r'^(\d+)\.\s+(.+?)\s*$', line)
        if match:
            topics.append({'index': int(match.group(1)), 'topic': match.group(2)})
    if len(topics) != 500:
        raise ValueError(f'Expected 500 topics but found {len(topics)}')
    return topics


def infer_category(index: int) -> str:
    """Determine category from topic index (100 per category)."""
    if index <= 100:
        return 'EVERYDAY SYSTEMS'
    if index <= 200:
        return 'MONEY & ECONOMICS'
    if index <= 300:
        return 'INFORMATION SYSTEMS'
    if index <= 400:
        return 'POWER & INSTITUTIONS'
    return 'FUTURE SYSTEMS'


def build_scene(topic: str, index: int, step: int, blueprint: dict, category: str) -> dict:
    """
    Build a single scene's JSON payload.

    Combines the static blueprint with dynamic, per-video parametric data
    to create a scene that's unique but consistent with the video's category.
    """
    cat = CATEGORIES[category]
    seed = (index % 9) + step  # Creates subtle variation between videos

    label = blueprint['label']
    mood = blueprint['mood']

    subtext = NarrativeEngine.generate_subtext(topic, label, category, mood)

    # Base scene structure
    scene = {
        'text': topic if label == 'Topic frame' else label,
        'subtext': subtext,
        'duration': 300,                         # 10 seconds at 30fps
        'visual': blueprint['visual'],
        'action': blueprint['action'],           # Camera movement
        'category': category,
        'accentColor': cat['accent'],
        'palette': cat['palette'],
        'assetTags': CATEGORY_ASSET_TAGS[category],
    }

    # ── Visual-specific parametric data ─────────────────────────────
    visual = blueprint['visual']

    # ── Advanced WebGL Payloads ─────────────────────────────────
    # Dynamically inject 3D Terrain backgrounds for Future or Eco topics
    if category == 'FUTURE SYSTEMS' or visual == 'earth':
        scene['backgroundMode'] = 'terrain'

    # Inject PixiJS Weather Systems if the scene mood is stressed
    if mood == 'stressed':
        scene['weather'] = 'rain'
    elif category == 'EVERYDAY SYSTEMS' and mood == 'thinking':
        scene['weather'] = 'snow'
    elif visual == 'lattice' or visual == 'network':
        # Add techy grid modes to other types
        scene['backgroundMode'] = 'mesh'

    if visual == 'crowd':
        scene['crowdCount'] = 10 + (index % 8)
        scene['mood'] = blueprint['mood']

    if visual == 'bars':
        scene['barValues'] = [18 + seed, 26 + seed, 36 + seed, 47 + seed, 58 + seed]

    if visual == 'flow':
        scene['flowLabels'] = (
            ['Trigger', 'Mechanism', 'Outcome'] if step == 5
            else ['Input', 'System', 'Output']
        )

    if visual == 'network':
        scene['networkNodes'] = (
            ['State', 'Market', 'Labor', 'Capital', 'Public'] if step == 3
            else ['Policy', 'Price', 'Behavior', 'Risk', 'Feedback']
        )

    if visual == 'icons':
        # Add our newly generated declarative SVGs to the standard icons mix randomly
        scene['icons'] = CATEGORY_ASSET_TAGS[category][:3] + ['bank', 'factory', 'home', 'PropDeclarativeRobot', 'PropServer', 'PropDeclarativeSaturn']

    if visual == 'animals':
        scene['animals'] = (
            ['bird', 'turtle', 'deer'] if category == 'FUTURE SYSTEMS'
            else ['bird', 'fish', 'bee']
        )

    return scene


def make_video_payload(index: int, topic: str) -> dict:
    """Build the complete video JSON for one topic."""
    video_id = f'video_{index:03d}'
    category = infer_category(index)
    cat = CATEGORIES[category]

    scenes = []
    for step, blueprint in enumerate(SCENE_BLUEPRINT, start=1):
        scenes.append(build_scene(topic, index, step, blueprint, category))

    return {
        'id': video_id,
        'title': topic,
        'template': 'explainer' if index % 3 == 0 else 'protest',
        'fps': 30,
        'width': 1080,
        'height': 1920,
        'category': category,
        'accentColor': cat['accent'],
        'scenes': scenes,
    }


def write_engine_manifest(video_ids: list[str]) -> None:
    """Generate the JavaScript manifest for Remotion's dynamic imports."""
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


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate 500 video blueprints with camera actions and palettes')
    parser.add_argument('--dry-run', action='store_true', help='Print stats without writing files')
    args = parser.parse_args()

    topics = parse_topics()
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {}
    action_counts = {}     # Track camera action usage across all scenes
    visual_counts = {}     # Track visual type usage across all scenes

    # ── Process all 500 topics ──────────────────────────────────────
    for item in topics:
        payload = make_video_payload(item['index'], item['topic'])
        video_id = payload['id']

        manifest[video_id] = {
            'title': payload['title'],
            'template': payload['template'],
            'category': payload['category'],
            'sceneCount': len(payload['scenes']),
        }

        # Count action and visual usage for the distribution report
        for scene in payload['scenes']:
            action_counts[scene['action']] = action_counts.get(scene['action'], 0) + 1
            visual_counts[scene['visual']] = visual_counts.get(scene['visual'], 0) + 1

        # Write individual video JSON (unless dry-run)
        if not args.dry_run:
            (VIDEOS_DIR / f'{video_id}.json').write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8',
            )

    # Write manifest files (unless dry-run)
    if not args.dry_run:
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8',
        )
        write_engine_manifest(sorted(manifest.keys()))

    # ── Distribution report ─────────────────────────────────────────
    print(f'Processed {len(topics)} topics')
    print(f'Camera actions: {action_counts}')
    print(f'Visual types:   {visual_counts}')
    if not args.dry_run:
        print(f'Wrote {len(manifest)} video files to {VIDEOS_DIR}')


if __name__ == '__main__':
    main()
