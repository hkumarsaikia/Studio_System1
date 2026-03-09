from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from src.studio.config import PROCESSED_ASSETS_DIR, RAW_ASSETS_DIR, REACT_COMPONENTS_DIR, VIDEOS_DIR

PRODUCTION_VIDEO_COUNT = 500
DEFAULT_FPS = 30
DEFAULT_PROFILE_ID = 'shorts_vertical'
DEFAULT_PROFILE_IDS = ('shorts_vertical', 'social_square', 'youtube_horizontal')
OPTIONAL_PROFILE_IDS = ('shorts_vertical_30s',)
DEFAULT_TEMPLATE_FAMILY = 'systems_explainer'
SUPPORTED_TEMPLATES = ('shorts', 'explainer', 'infographic', 'protest')
SUPPORTED_TEMPLATE_FAMILIES = (DEFAULT_TEMPLATE_FAMILY,)

PRODUCTION_ID_RE = re.compile(r'^video_[0-9]{3}$')
DEMO_ID_RE = re.compile(r'^demo_[a-z0-9_]+$')
SCENE_ID_RE = re.compile(r'^scene_[0-9]{2}$')

import inspect
from src.studio.assets.generative_engine import (
    people_society,
    buildings_infra,
    money_economy,
    charts_data,
    systems_network,
    arrows_flow,
    work_tech_social,
    governance_global,
    crisis_environment_future,
)

_PROCEDURAL_KEYS = []
for mod in [people_society, buildings_infra, money_economy, charts_data, systems_network, arrows_flow, work_tech_social, governance_global, crisis_environment_future]:
    for name, func in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith("build_"):
            comp_name = "Icon" + "".join(word.capitalize() for word in name[6:].split("_"))
            _PROCEDURAL_KEYS.append(comp_name)
_PROCEDURAL_KEYS = tuple(_PROCEDURAL_KEYS)

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
) + _PROCEDURAL_KEYS

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
) + _PROCEDURAL_KEYS

RENDER_PROFILES: dict[str, dict[str, Any]] = {
    'shorts_vertical': {
        'id': 'shorts_vertical',
        'label': 'Shorts Vertical',
        'platforms': ['YouTube Shorts', 'Instagram Reels'],
        'width': 1080,
        'height': 1920,
        'fps': 30,
        'aspectRatio': '9:16',
        'timeline': {
            'mode': 'segmented',
            'sceneCount': 12,
            'sceneDurationSeconds': 10,
            'totalSeconds': 120,
        },
        'layout': {
            'padding': 80,
            'titleScale': 1.0,
            'subtitleScale': 1.0,
            'categoryScale': 1.0,
            'visualScale': 1.0,
            'textMaxWidth': 920,
            'textAlign': 'center',
        },
    },
    'shorts_vertical_30s': {
        'id': 'shorts_vertical_30s',
        'label': 'Shorts Vertical 30s',
        'platforms': ['YouTube Shorts', 'Instagram Reels'],
        'width': 1080,
        'height': 1920,
        'fps': 30,
        'aspectRatio': '9:16',
        'timeline': {
            'mode': 'segmented',
            'sceneCount': 12,
            'sceneDurationSeconds': 2.5,
            'totalSeconds': 30,
        },
        'layout': {
            'padding': 80,
            'titleScale': 1.0,
            'subtitleScale': 1.0,
            'categoryScale': 1.0,
            'visualScale': 1.0,
            'textMaxWidth': 920,
            'textAlign': 'center',
        },
    },
    'social_square': {
        'id': 'social_square',
        'label': 'Social Square',
        'platforms': ['Instagram Feed', 'LinkedIn', 'X'],
        'width': 1080,
        'height': 1080,
        'fps': 30,
        'aspectRatio': '1:1',
        'timeline': {
            'mode': 'segmented',
            'sceneCount': 12,
            'sceneDurationSeconds': 10,
            'totalSeconds': 120,
        },
        'layout': {
            'padding': 72,
            'titleScale': 0.86,
            'subtitleScale': 0.92,
            'categoryScale': 0.92,
            'visualScale': 0.9,
            'textMaxWidth': 760,
            'textAlign': 'center',
        },
    },
    'youtube_horizontal': {
        'id': 'youtube_horizontal',
        'label': 'YouTube Horizontal',
        'platforms': ['YouTube', 'Presentations'],
        'width': 1920,
        'height': 1080,
        'fps': 30,
        'aspectRatio': '16:9',
        'timeline': {
            'mode': 'segmented',
            'sceneCount': 12,
            'sceneDurationSeconds': 10,
            'totalSeconds': 120,
        },
        'layout': {
            'padding': 120,
            'titleScale': 0.78,
            'subtitleScale': 0.84,
            'categoryScale': 0.9,
            'visualScale': 0.82,
            'textMaxWidth': 1120,
            'textAlign': 'center',
        },
    },
}

CATEGORIES = {
    'EVERYDAY SYSTEMS': {'accent': '#38bdf8', 'palette': {'background': '#0f172a', 'secondary': '#1e293b'}},
    'MONEY & ECONOMICS': {'accent': '#22c55e', 'palette': {'background': '#052e16', 'secondary': '#14532d'}},
    'INFORMATION SYSTEMS': {'accent': '#f472b6', 'palette': {'background': '#1a0524', 'secondary': '#3b0764'}},
    'POWER & INSTITUTIONS': {'accent': '#a78bfa', 'palette': {'background': '#1e1b4b', 'secondary': '#312e81'}},
    'FUTURE SYSTEMS': {'accent': '#14b8a6', 'palette': {'background': '#042f2e', 'secondary': '#134e4a'}},
}

CATEGORY_ASSET_TAGS = {
    'EVERYDAY SYSTEMS': ['house', 'shopping_cart', 'airplane', 'person_group', 'factory'],
    'MONEY & ECONOMICS': ['bank_building', 'money_coins', 'bar_chart', 'factory', 'earth_globe'],
    'INFORMATION SYSTEMS': ['video_icon', 'data_cloud', 'ai_brain', 'network_nodes', 'algorithm_symbol'],
    'POWER & INSTITUTIONS': ['law_document', 'shield', 'balance_scale', 'person_group', 'constitution_scroll'],
    'FUTURE SYSTEMS': ['ai_brain', 'gear', 'lightning', 'earth_globe', 'signal_wave'],
}

PROCEDURAL_ASSET_LIBRARY = {
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

SCENE_GRAMMAR_REGISTRY: dict[str, dict[str, Any]] = {
    'hook_tension': {
        'label': 'Hook / tension',
        'defaultVisual': 'crowd',
        'defaultCameraIntent': 'slow_zoom_in',
        'defaultMood': 'neutral',
        'visualDirection': 'Open on people and motion to make the topic feel immediate and human.',
    },
    'icon_pressure': {
        'label': 'Icon pressure',
        'defaultVisual': 'icons',
        'defaultCameraIntent': 'pan_right',
        'defaultMood': 'stressed',
        'visualDirection': 'Use a dense icon field that quickly frames the pressure point or conflict.',
    },
    'system_map': {
        'label': 'System map',
        'defaultVisual': 'network',
        'defaultCameraIntent': 'static_focus',
        'defaultMood': 'thinking',
        'visualDirection': 'Show the system as connected nodes so the audience sees where the edges are.',
    },
    'causal_chain': {
        'label': 'Causal chain',
        'defaultVisual': 'math_equation',
        'defaultCameraIntent': 'slow_zoom_in',
        'defaultMood': 'neutral',
        'visualDirection': 'Present the first causal layer as a simple abstract mechanism or formula.',
    },
    'process_flow': {
        'label': 'Process flow',
        'defaultVisual': 'flow',
        'defaultCameraIntent': 'pan_left',
        'defaultMood': 'neutral',
        'visualDirection': 'Turn the mechanism into directional movement so cause and effect read instantly.',
    },
    'feedback_loop': {
        'label': 'Feedback loop',
        'defaultVisual': 'lattice',
        'defaultCameraIntent': 'dramatic_pull_back',
        'defaultMood': 'stressed',
        'visualDirection': 'Reveal the deeper feedback structure with denser motion and higher visual complexity.',
    },
    'data_lens': {
        'label': 'Data lens',
        'defaultVisual': 'neural_core',
        'defaultCameraIntent': 'slow_pan_up',
        'defaultMood': 'thinking',
        'visualDirection': 'Shift to a data-centric visual that feels analytical and system-wide.',
    },
    'real_world_example': {
        'label': 'Real-world example',
        'defaultVisual': 'city',
        'defaultCameraIntent': 'pan_right',
        'defaultMood': 'neutral',
        'visualDirection': 'Bring the abstract explanation back to a concrete everyday environment.',
    },
    'externality': {
        'label': 'Externality',
        'defaultVisual': 'animals',
        'defaultCameraIntent': 'slow_zoom_in',
        'defaultMood': 'neutral',
        'visualDirection': 'Show hidden side effects with ecological or externality imagery.',
    },
    'macro_context': {
        'label': 'Macro context',
        'defaultVisual': 'earth',
        'defaultCameraIntent': 'slow_pan_down',
        'defaultMood': 'thinking',
        'visualDirection': 'Zoom outward and frame the topic as part of a wider long-range pattern.',
    },
    'takeaway': {
        'label': 'Takeaway',
        'defaultVisual': 'icons',
        'defaultCameraIntent': 'dramatic_pull_back',
        'defaultMood': 'happy',
        'visualDirection': 'Return to a clear icon-driven summary that points toward action.',
    },
    'conclusion': {
        'label': 'Conclusion',
        'defaultVisual': 'crowd',
        'defaultCameraIntent': 'slow_zoom_in',
        'defaultMood': 'happy',
        'visualDirection': 'Close on people again so the system explanation resolves back to human consequence.',
    },
}

SCENE_TEMPLATE_FAMILIES: dict[str, tuple[dict[str, Any], ...]] = {
    DEFAULT_TEMPLATE_FAMILY: (
        {
            'label': 'Topic frame',
            'purpose': 'hook',
            'visualGrammar': 'hook_tension',
            'visual': 'crowd',
            'cameraIntent': 'slow_zoom_in',
            'mood': 'neutral',
        },
        {
            'label': 'Hook',
            'purpose': 'tension',
            'visualGrammar': 'icon_pressure',
            'visual': 'icons',
            'cameraIntent': 'pan_right',
            'mood': 'stressed',
        },
        {
            'label': 'System boundary',
            'purpose': 'system_boundary',
            'visualGrammar': 'system_map',
            'visual': 'network',
            'cameraIntent': 'static_focus',
            'mood': 'thinking',
        },
        {
            'label': 'Cause layer 1',
            'purpose': 'root_cause',
            'visualGrammar': 'causal_chain',
            'visual': 'math_equation',
            'cameraIntent': 'slow_zoom_in',
            'mood': 'neutral',
        },
        {
            'label': 'Cause layer 2',
            'purpose': 'mechanism',
            'visualGrammar': 'process_flow',
            'visual': 'flow',
            'cameraIntent': 'pan_left',
            'mood': 'neutral',
        },
        {
            'label': 'Cause layer 3',
            'purpose': 'feedback_loop',
            'visualGrammar': 'feedback_loop',
            'visual': 'lattice',
            'cameraIntent': 'dramatic_pull_back',
            'mood': 'stressed',
        },
        {
            'label': 'Data lens',
            'purpose': 'data_lens',
            'visualGrammar': 'data_lens',
            'visual': 'neural_core',
            'cameraIntent': 'slow_pan_up',
            'mood': 'thinking',
        },
        {
            'label': 'Real world scene',
            'purpose': 'real_world_example',
            'visualGrammar': 'real_world_example',
            'visual': 'city',
            'cameraIntent': 'pan_right',
            'mood': 'neutral',
        },
        {
            'label': 'Ecology/externalities',
            'purpose': 'externality',
            'visualGrammar': 'externality',
            'visual': 'animals',
            'cameraIntent': 'slow_zoom_in',
            'mood': 'neutral',
        },
        {
            'label': 'Macro trend',
            'purpose': 'macro_context',
            'visualGrammar': 'macro_context',
            'visual': 'earth',
            'cameraIntent': 'slow_pan_down',
            'mood': 'thinking',
        },
        {
            'label': 'Actionable takeaway',
            'purpose': 'takeaway',
            'visualGrammar': 'takeaway',
            'visual': 'icons',
            'cameraIntent': 'dramatic_pull_back',
            'mood': 'happy',
        },
        {
            'label': 'Closing',
            'purpose': 'conclusion',
            'visualGrammar': 'conclusion',
            'visual': 'crowd',
            'cameraIntent': 'slow_zoom_in',
            'mood': 'happy',
        },
    ),
}


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



def default_template_family_for_index(index: int) -> str:
    _ = index
    return DEFAULT_TEMPLATE_FAMILY



def resolve_template_for_profile(template_family: str, profile_id: str, index: int) -> str:
    _ = profile_id
    if template_family not in SUPPORTED_TEMPLATE_FAMILIES:
        return default_template_for_index(index)
    return default_template_for_index(index)



def list_profile_ids() -> list[str]:
    return list(DEFAULT_PROFILE_IDS)


def list_supported_profile_ids() -> list[str]:
    return list(RENDER_PROFILES.keys())



def default_profile_ids() -> list[str]:
    return list(DEFAULT_PROFILE_IDS)



def get_render_profile(profile_id: str) -> dict[str, Any]:
    if profile_id not in RENDER_PROFILES:
        raise ValueError(f'Unsupported render profile: {profile_id}')
    return RENDER_PROFILES[profile_id]



def profile_video_dir(profile_id: str) -> Path:
    return VIDEOS_DIR / profile_id



def compiled_payload_path(video_id: str, profile_id: str) -> Path:
    return profile_video_dir(profile_id) / f'{video_id}.json'



def generated_asset_paths(component_name: str) -> dict[str, str]:
    return {
        'rawSvg': str((RAW_ASSETS_DIR / f'{component_name}.svg').relative_to(RAW_ASSETS_DIR.parent.parent.parent)),
        'processedSvg': str((PROCESSED_ASSETS_DIR / f'{component_name}.svg').relative_to(PROCESSED_ASSETS_DIR.parent.parent.parent)),
        'generatedComponent': str((REACT_COMPONENTS_DIR / f'{component_name}.tsx').relative_to(REACT_COMPONENTS_DIR.parent.parent.parent)),
    }



def flatten_asset_library(asset_registry: dict[str, dict[str, Any]] | None = None) -> set[str]:
    if asset_registry is not None:
        return set(asset_registry.keys())

    asset_names: set[str] = set()
    for values in PROCEDURAL_ASSET_LIBRARY.values():
        asset_names.update(values)
    for values in CATEGORY_ASSET_TAGS.values():
        asset_names.update(values)
    asset_names.update(GENERATED_ASSET_COMPONENTS)
    return asset_names



def supported_visual_grammars() -> set[str]:
    return set(SCENE_GRAMMAR_REGISTRY.keys())



def scene_template_family_blueprint(template_family: str) -> tuple[dict[str, Any], ...]:
    if template_family not in SCENE_TEMPLATE_FAMILIES:
        raise ValueError(f'Unsupported template family: {template_family}')
    return SCENE_TEMPLATE_FAMILIES[template_family]



def default_scene_count_for_profile(profile_id: str) -> int:
    return int(get_render_profile(profile_id)['timeline']['sceneCount'])



def default_scene_seconds_for_profile(profile_id: str) -> float:
    return float(get_render_profile(profile_id)['timeline']['sceneDurationSeconds'])



def default_scene_duration_frames(profile_id: str) -> int:
    profile = get_render_profile(profile_id)
    return round(float(profile['timeline']['sceneDurationSeconds']) * int(profile['fps']))
