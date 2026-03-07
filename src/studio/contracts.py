from __future__ import annotations

import re

PRODUCTION_VIDEO_COUNT = 500
PRODUCTION_SEGMENT_COUNT = 12
PRODUCTION_SEGMENT_SECONDS = 10
DEFAULT_FPS = 30
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1920
DEFAULT_SCENE_DURATION = PRODUCTION_SEGMENT_SECONDS * DEFAULT_FPS
DEFAULT_OVERLAYS = ('grain', 'vignette')
SUPPORTED_TEMPLATES = ('shorts', 'explainer', 'infographic', 'protest')

PRODUCTION_ID_RE = re.compile(r'^video_[0-9]{3}$')
DEMO_ID_RE = re.compile(r'^demo_[a-z0-9_]+$')

GENERATED_ASSET_COMPONENTS = (
    'BackgroundCyber',
    'BackgroundSunset',
    'CharacterAngry',
    'CharacterGeek',
    'CharacterHappy',
    'CharacterSad',
    'PropDeclarativeRobot',
    'PropDeclarativeSaturn',
    'PropServer',
    'PropTelescope',
)

SUPPORTED_VISUALS = (
    'crowd',
    'bars',
    'flow',
    'network',
    'icons',
    'landscape',
    'city',
    'animals',
    'lattice',
    'neural_core',
    'math_equation',
    'earth',
    'matrix',
    'hud',
    'donut',
    'gradient_orb',
    'explosion',
    'radar',
    'glass_card',
    'pulse_grid',
    'timeline',
    'line_chart',
    'progress_ring',
    'aurora',
    'orbital_assembly',
    'prism_field',
    'constellation',
    'PropServer',
    'PropDeclarativeRobot',
    'PropDeclarativeSaturn',
)

BASE_ASSET_LIBRARY = {
    'humans': [
        'person_adult_female',
        'person_adult_male',
        'person_youth',
        'person_senior',
        'crowd_group_8',
        'crowd_group_16',
    ],
    'animals': ['bird', 'fish', 'deer', 'cow', 'bee', 'turtle'],
    'objects': ['coin', 'bank', 'factory', 'house', 'cart', 'briefcase', 'microphone', 'cloud', 'chip', 'gavel'],
    'icons': [
        'bank',
        'factory',
        'home',
        'cart',
        'hospital',
        'school',
        'transport',
        'energy',
        'law',
        'media',
        'cloud',
        'ai',
        'algorithm',
        'pollution',
        'coin',
        'shield',
        'globe',
        'lightning',
        'gear',
        'people',
        'chart',
        'arrow',
        'loop',
        'scale',
        'network',
        'lock',
        'book',
        'wave',
    ],
    'backdrops': ['gradient_system', 'city_street', 'landscape_sunrise'],
    'charts': ['bars', 'flow', 'network', 'donut', 'line_chart', 'progress_ring', 'timeline'],
    'generatedComponents': list(GENERATED_ASSET_COMPONENTS),
}

CATEGORIES = {
    'EVERYDAY SYSTEMS': {'accent': '#38bdf8', 'palette': {'background': '#0f172a', 'secondary': '#1e293b'}},
    'MONEY & ECONOMICS': {'accent': '#22c55e', 'palette': {'background': '#052e16', 'secondary': '#14532d'}},
    'INFORMATION SYSTEMS': {'accent': '#f472b6', 'palette': {'background': '#1a0524', 'secondary': '#3b0764'}},
    'POWER & INSTITUTIONS': {'accent': '#a78bfa', 'palette': {'background': '#1e1b4b', 'secondary': '#312e81'}},
    'FUTURE SYSTEMS': {'accent': '#14b8a6', 'palette': {'background': '#042f2e', 'secondary': '#134e4a'}},
}

CATEGORY_ASSET_TAGS = {
    'EVERYDAY SYSTEMS': ['home', 'cart', 'transport', 'people', 'factory'],
    'MONEY & ECONOMICS': ['bank', 'coin', 'chart', 'factory', 'globe'],
    'INFORMATION SYSTEMS': ['media', 'cloud', 'ai', 'network', 'algorithm'],
    'POWER & INSTITUTIONS': ['law', 'shield', 'scale', 'people', 'book'],
    'FUTURE SYSTEMS': ['ai', 'gear', 'lightning', 'globe', 'wave'],
}

DEFAULT_ON_SCREEN_TEXT = {
    'Topic frame': 'topic',
    'Hook': 'Why It Matters',
    'System boundary': 'System Boundary',
    'Cause layer 1': 'Root Cause',
    'Cause layer 2': 'Mechanism',
    'Cause layer 3': 'Feedback Loops',
    'Data lens': 'Data Lens',
    'Real world scene': 'Real World',
    'Ecology/externalities': 'Hidden Costs',
    'Macro trend': 'Macro Trend',
    'Actionable takeaway': 'What To Do',
    'Closing': 'Closing',
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


def is_production_video_id(video_id: str) -> bool:
    return bool(PRODUCTION_ID_RE.match(video_id))


def is_demo_video_id(video_id: str) -> bool:
    return bool(DEMO_ID_RE.match(video_id))


def infer_category(index: int) -> str:
    if index <= 100:
        return 'EVERYDAY SYSTEMS'
    if index <= 200:
        return 'MONEY & ECONOMICS'
    if index <= 300:
        return 'INFORMATION SYSTEMS'
    if index <= 400:
        return 'POWER & INSTITUTIONS'
    return 'FUTURE SYSTEMS'


def default_template_for_index(index: int) -> str:
    return 'explainer' if index % 3 == 0 else 'protest'


def flatten_asset_library(asset_library: dict[str, list[str]] | None = None) -> set[str]:
    library = asset_library or BASE_ASSET_LIBRARY
    asset_names: set[str] = set()
    for values in library.values():
        asset_names.update(values)
    for values in CATEGORY_ASSET_TAGS.values():
        asset_names.update(values)
    return asset_names
