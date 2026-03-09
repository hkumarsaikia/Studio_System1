from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from src.studio.assets.catalog import canonical_asset_id
from src.studio.config import (
    ASSET_COVERAGE_FILE,
    ASSET_REGISTRY_FILE,
    DATA_DIR,
    DEMOS_DIR,
    ROOT_DIR,
    STORYBOARDS_DIR,
    TOPIC_CATALOG_FILE,
)
from src.studio.contracts import (
    DEFAULT_PROFILE_ID,
    SCENE_ID_RE,
    SUPPORTED_VISUALS,
    compiled_payload_path,
    default_scene_count_for_profile,
    default_scene_duration_frames,
    default_scene_seconds_for_profile,
    get_render_profile,
    list_profile_ids,
    list_supported_profile_ids,
    scene_template_family_blueprint,
    supported_visual_grammars,
)
from src.studio.generators.topic_library import DEMO_MANIFEST_PATH, MANIFEST_PATH, build_topic_catalog, build_topics_index
from src.studio.utils.schema_validation import read_json, validate_with_schema

REQUIRED_DEMO_FIELDS = {'id', 'title', 'template', 'scenes'}


def _ensure_file(path: Path, message: str) -> None:
    if not path.exists():
        raise ValueError(message)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


class ValidationContext:
    def __init__(self, topic_catalog: dict[str, dict[str, object]], asset_registry: dict[str, dict[str, object]]) -> None:
        self.topic_catalog = topic_catalog
        self.asset_registry = asset_registry
        self.allowed_assets = set(asset_registry.keys())
        self.allowed_profiles = set(list_supported_profile_ids())
        self.allowed_grammars = supported_visual_grammars()

    def resolve_asset_ref(self, asset_id: object) -> str:
        raw_asset_id = str(asset_id)
        canonical = canonical_asset_id(raw_asset_id)
        if canonical in self.allowed_assets:
            return canonical
        return raw_asset_id

    def invalid_assets(self, asset_ids: list[object]) -> list[str]:
        return sorted(
            {
                str(asset_id)
                for asset_id in asset_ids
                if self.resolve_asset_ref(asset_id) not in self.allowed_assets
            }
        )

    def non_canonical_assets(self, asset_ids: list[object]) -> list[str]:
        return sorted(
            {
                str(asset_id)
                for asset_id in asset_ids
                if canonical_asset_id(str(asset_id)) != str(asset_id)
                and canonical_asset_id(str(asset_id)) in self.allowed_assets
            }
        )



def validate_topic_catalog_payload(catalog: dict[str, dict[str, object]], topics_index: dict[str, dict[str, object]]) -> None:
    validate_with_schema(catalog, 'topic_catalog', TOPIC_CATALOG_FILE.name)
    expected_catalog = build_topic_catalog(topics_index)
    if catalog != expected_catalog:
        raise ValueError('Topic catalog does not match the parsed Topics.txt source')



def validate_asset_registry_payload(asset_registry: dict[str, dict[str, object]]) -> None:
    validate_with_schema(asset_registry, 'asset_registry', ASSET_REGISTRY_FILE.name)
    for asset_id, entry in sorted(asset_registry.items()):
        if entry['id'] != asset_id:
            raise ValueError(f'asset_registry.json: {asset_id}: entry id mismatch')
        if entry['sourceType'] == 'svg_component':
            for field_name in ('svgSource', 'processedSvg', 'generatedComponent'):
                relative_path = entry.get(field_name)
                if not relative_path:
                    raise ValueError(f'asset_registry.json: {asset_id}: missing {field_name}')
                absolute_path = ROOT_DIR / str(relative_path)
                if not absolute_path.exists():
                    raise ValueError(f'asset_registry.json: {asset_id}: missing file {absolute_path}')
            if entry.get('status') != 'ready':
                raise ValueError(f"asset_registry.json: {asset_id}: svg_component status must be 'ready'")



def validate_storyboard_payload(
    storyboard: dict[str, object],
    context: ValidationContext,
    path: Path | None = None,
) -> None:
    context_name = path.name if path else str(storyboard.get('id', '<storyboard>'))
    validate_with_schema(storyboard, 'storyboard', context_name)

    video_id = str(storyboard['id'])
    topic_ref = str(storyboard['topicRef'])
    _assert(topic_ref in context.topic_catalog, f'{context_name}: topicRef {topic_ref!r} is not in topic catalog')
    expected_topic = str(context.topic_catalog[topic_ref]['topic'])
    _assert(str(storyboard['topic']) == expected_topic, f'{context_name}: topic mismatch. expected={expected_topic!r} actual={storyboard["topic"]!r}')

    template_family = str(storyboard['templateFamily'])
    scene_template_family_blueprint(template_family)

    default_profiles = [str(profile_id) for profile_id in storyboard.get('defaultProfiles', [])]
    _assert(default_profiles, f'{context_name}: defaultProfiles must not be empty')
    invalid_profiles = sorted(set(default_profiles) - context.allowed_profiles)
    _assert(not invalid_profiles, f'{context_name}: unsupported defaultProfiles {invalid_profiles}')

    scene_plan = list(storyboard.get('scenePlan', []))
    expected_scene_count = default_scene_count_for_profile(DEFAULT_PROFILE_ID)
    _assert(len(scene_plan) == expected_scene_count, f'{context_name}: expected {expected_scene_count} scenes in scenePlan, found {len(scene_plan)}')

    for index, scene in enumerate(scene_plan, start=1):
        expected_scene_id = f'scene_{index:02d}'
        _assert(str(scene['sceneId']) == expected_scene_id, f'{context_name}: sceneId mismatch at position {index}')
        _assert(str(scene['visualGrammar']) in context.allowed_grammars, f"{context_name}: unsupported visualGrammar {scene['visualGrammar']!r}")
        unknown_assets = context.invalid_assets(list(scene.get('assetRefs', [])))
        _assert(not unknown_assets, f'{context_name}: unknown assetRefs in {expected_scene_id}: {unknown_assets}')

        timing_hints = scene.get('timingHints') or {}
        if isinstance(timing_hints, dict):
            for field_name in ('baseSeconds', 'seconds'):
                if field_name in timing_hints:
                    _assert(float(timing_hints[field_name]) > 0, f'{context_name}: {expected_scene_id} timingHints.{field_name} must be positive')

        profile_overrides = scene.get('profileOverrides') or {}
        if isinstance(profile_overrides, dict):
            invalid_override_profiles = sorted(set(profile_overrides.keys()) - context.allowed_profiles)
            _assert(not invalid_override_profiles, f'{context_name}: invalid profileOverrides keys in {expected_scene_id}: {invalid_override_profiles}')
            for profile_id, override_payload in profile_overrides.items():
                if not isinstance(override_payload, dict):
                    raise ValueError(f'{context_name}: profileOverrides.{profile_id} for {expected_scene_id} must be an object')
                if 'visualGrammar' in override_payload:
                    override_grammar = str(override_payload['visualGrammar'])
                    _assert(override_grammar in context.allowed_grammars, f'{context_name}: invalid override visualGrammar {override_grammar!r} in {expected_scene_id}')
                if 'assetRefs' in override_payload:
                    override_assets = context.invalid_assets(list(override_payload['assetRefs']))
                    _assert(not override_assets, f'{context_name}: invalid override assetRefs in {expected_scene_id}: {override_assets}')



def validate_compiled_payload(
    payload: dict[str, object],
    context: ValidationContext,
    profile_id: str,
    path: Path | None = None,
) -> None:
    context_name = path.name if path else f"{payload.get('id', '<video>')}[{profile_id}]"
    validate_with_schema(payload, 'video', context_name)

    profile = get_render_profile(profile_id)
    video_id = str(payload['id'])
    topic_ref = str(payload['topicRef'])
    _assert(str(payload['profileId']) == profile_id, f'{context_name}: profileId mismatch')
    _assert(str(payload['dataset']) == 'production', f'{context_name}: dataset must be production')
    _assert(topic_ref in context.topic_catalog, f'{context_name}: topicRef {topic_ref!r} missing from topic catalog')
    expected_topic = str(context.topic_catalog[topic_ref]['topic'])
    _assert(str(payload['topic']) == expected_topic, f'{context_name}: topic mismatch. expected={expected_topic!r} actual={payload["topic"]!r}')

    _assert(int(payload['width']) == int(profile['width']), f'{context_name}: width mismatch for {profile_id}')
    _assert(int(payload['height']) == int(profile['height']), f'{context_name}: height mismatch for {profile_id}')
    _assert(int(payload['fps']) == int(profile['fps']), f'{context_name}: fps mismatch for {profile_id}')
    _assert(str(payload['aspectRatio']) == str(profile['aspectRatio']), f'{context_name}: aspectRatio mismatch for {profile_id}')
    _assert(payload['timeline'] == profile['timeline'], f'{context_name}: timeline mismatch for {profile_id}')
    _assert(payload['layoutProfile'] == profile['layout'], f'{context_name}: layoutProfile mismatch for {profile_id}')

    expected_scene_count = default_scene_count_for_profile(profile_id)
    expected_duration = default_scene_duration_frames(profile_id)
    expected_total_seconds = expected_scene_count * default_scene_seconds_for_profile(profile_id)

    scenes = list(payload.get('scenes', []))
    _assert(int(payload['sceneCount']) == expected_scene_count, f'{context_name}: expected {expected_scene_count} scenes')
    _assert(len(scenes) == expected_scene_count, f'{context_name}: scenes length mismatch')
    _assert(math.isclose(float(payload['totalDurationSeconds']), float(expected_total_seconds), rel_tol=0.0, abs_tol=0.001), f'{context_name}: totalDurationSeconds mismatch')

    for index, scene in enumerate(scenes, start=1):
        expected_scene_id = f'scene_{index:02d}'
        expected_segment_id = f'segment_{index:02d}' if profile['timeline']['mode'] == 'segmented' else expected_scene_id
        _assert(str(scene['sceneId']) == expected_scene_id, f'{context_name}: sceneId mismatch at position {index}')
        _assert(str(scene['segmentId']) == expected_segment_id, f'{context_name}: segmentId mismatch at position {index}')
        _assert(int(scene['duration']) == expected_duration, f'{context_name}: duration mismatch in {expected_scene_id}')
        _assert(str(scene['visual']) in SUPPORTED_VISUALS, f"{context_name}: unsupported visual {scene['visual']!r}")
        _assert(str(scene['visualGrammar']) in context.allowed_grammars, f"{context_name}: unsupported visualGrammar {scene['visualGrammar']!r}")
        scene_asset_tags = list(scene.get('assetTags', []))
        unknown_assets = context.invalid_assets(scene_asset_tags)
        _assert(not unknown_assets, f'{context_name}: unknown assetTags in {expected_scene_id}: {unknown_assets}')
        non_canonical_assets = context.non_canonical_assets(scene_asset_tags)
        _assert(not non_canonical_assets, f'{context_name}: assetTags in {expected_scene_id} must be canonical ids: {non_canonical_assets}')
        if str(scene['visual']) == 'icons':
            icon_assets = list(scene.get('icons', []))
            unknown_icon_assets = context.invalid_assets(icon_assets)
            _assert(not unknown_icon_assets, f'{context_name}: unknown icons in {expected_scene_id}: {unknown_icon_assets}')
            non_canonical_icons = context.non_canonical_assets(icon_assets)
            _assert(not non_canonical_icons, f'{context_name}: icons in {expected_scene_id} must be canonical ids: {non_canonical_icons}')
            _assert([str(item) for item in icon_assets] == [str(item) for item in scene_asset_tags], f'{context_name}: icons must match assetTags in {expected_scene_id}')
        _assert(str(scene['profileId']) == profile_id, f'{context_name}: scene profileId mismatch in {expected_scene_id}')
        _assert(scene['layout'] == profile['layout'], f'{context_name}: scene layout mismatch in {expected_scene_id}')



def validate_demo_payload(path: Path) -> None:
    payload = read_json(path)
    missing = REQUIRED_DEMO_FIELDS - set(payload.keys())
    if missing:
        raise ValueError(f'{path.name}: missing demo fields {sorted(missing)}')
    scenes = payload.get('scenes', [])
    if not scenes:
        raise ValueError(f'{path.name}: demo payload must include at least one scene')
    for scene in scenes:
        visual = scene.get('visual')
        if visual and visual not in SUPPORTED_VISUALS:
            raise ValueError(f'{path.name}: unsupported demo visual {visual!r}')



def validate_manifest_consistency(
    production_manifest: dict[str, dict[str, object]],
    demo_manifest: dict[str, dict[str, object]],
    storyboard_map: dict[str, dict[str, object]],
    compiled_by_profile: dict[str, dict[str, dict[str, object]]],
) -> None:
    storyboard_ids = set(storyboard_map.keys())
    manifest_ids = set(production_manifest.keys())
    if manifest_ids != storyboard_ids:
        raise ValueError('Production manifest ids do not exactly match storyboard ids')

    demo_paths = sorted(DEMOS_DIR.glob('demo_*.json'))
    demo_ids = {path.stem for path in demo_paths}
    if set(demo_manifest.keys()) != demo_ids:
        raise ValueError('Demo manifest ids do not exactly match demo payload ids')
    collisions = storyboard_ids & demo_ids
    if collisions:
        raise ValueError(f'Production/demo id collisions detected: {sorted(collisions)}')

    for video_id, manifest_entry in production_manifest.items():
        storyboard = storyboard_map[video_id]
        if manifest_entry['title'] != storyboard['title']:
            raise ValueError(f'{video_id}: manifest title mismatch')
        if manifest_entry['topicRef'] != storyboard['topicRef']:
            raise ValueError(f'{video_id}: manifest topicRef mismatch')
        if manifest_entry['topic'] != storyboard['topic']:
            raise ValueError(f'{video_id}: manifest topic mismatch')
        if manifest_entry['category'] != storyboard['category']:
            raise ValueError(f'{video_id}: manifest category mismatch')
        if manifest_entry['templateFamily'] != storyboard['templateFamily']:
            raise ValueError(f'{video_id}: manifest templateFamily mismatch')
        if set(manifest_entry['defaultProfiles']) != set(storyboard['defaultProfiles']):
            raise ValueError(f'{video_id}: manifest defaultProfiles mismatch')
        expected_storyboard_path = f'data/storyboards/{video_id}.json'
        if manifest_entry['storyboard'] != expected_storyboard_path:
            raise ValueError(f'{video_id}: manifest storyboard path mismatch')

        manifest_profiles = manifest_entry.get('profiles', {})
        if set(manifest_profiles.keys()) != set(storyboard['defaultProfiles']):
            raise ValueError(f'{video_id}: manifest profiles do not match storyboard defaultProfiles')

        for profile_id, profile_entry in manifest_profiles.items():
            payload = compiled_by_profile[profile_id][video_id]
            expected_path = f'data/videos/{profile_id}/{video_id}.json'
            if profile_entry['path'] != expected_path:
                raise ValueError(f'{video_id}[{profile_id}]: manifest payload path mismatch')
            if profile_entry['width'] != payload['width'] or profile_entry['height'] != payload['height']:
                raise ValueError(f'{video_id}[{profile_id}]: manifest dimensions mismatch')
            if profile_entry['fps'] != payload['fps']:
                raise ValueError(f'{video_id}[{profile_id}]: manifest fps mismatch')
            if profile_entry['sceneCount'] != payload['sceneCount']:
                raise ValueError(f'{video_id}[{profile_id}]: manifest sceneCount mismatch')
            if not math.isclose(float(profile_entry['totalDurationSeconds']), float(payload['totalDurationSeconds']), rel_tol=0.0, abs_tol=0.001):
                raise ValueError(f'{video_id}[{profile_id}]: manifest duration mismatch')
            if profile_entry['aspectRatio'] != payload['aspectRatio']:
                raise ValueError(f'{video_id}[{profile_id}]: manifest aspect ratio mismatch')

    demo_payload_map = {path.stem: read_json(path) for path in demo_paths}
    for demo_id, entry in demo_manifest.items():
        payload = demo_payload_map[demo_id]
        if entry['title'] != payload['title']:
            raise ValueError(f'{demo_id}: demo manifest title mismatch')
        if entry['category'] != payload.get('category', 'DEMO'):
            raise ValueError(f'{demo_id}: demo manifest category mismatch')
        if entry['template'] != payload.get('template', 'explainer'):
            raise ValueError(f'{demo_id}: demo manifest template mismatch')
        if entry['sceneCount'] != len(payload.get('scenes', [])):
            raise ValueError(f'{demo_id}: demo manifest sceneCount mismatch')



def validate() -> None:
    _ensure_file(TOPIC_CATALOG_FILE, 'Topic catalog is missing. Run python -m src.studio.cli build --materialize')
    _ensure_file(ASSET_REGISTRY_FILE, 'Asset registry is missing. Run python build_assets.py or python -m src.studio.cli build --materialize')
    _ensure_file(ASSET_COVERAGE_FILE, 'Asset coverage report is missing. Run python -m src.studio.cli build --materialize')
    _ensure_file(MANIFEST_PATH, 'Production manifest is missing. Run python -m src.studio.cli build --materialize')
    _ensure_file(DEMO_MANIFEST_PATH, 'Demo manifest is missing. Run python -m src.studio.cli build --materialize')

    topics_index = build_topics_index()
    topic_catalog = read_json(TOPIC_CATALOG_FILE)
    validate_topic_catalog_payload(topic_catalog, topics_index)

    asset_registry = read_json(ASSET_REGISTRY_FILE)
    validate_asset_registry_payload(asset_registry)

    context = ValidationContext(topic_catalog, asset_registry)

    storyboard_paths = sorted(STORYBOARDS_DIR.glob('video_*.json'))
    if len(storyboard_paths) != 500:
        raise ValueError(f'Expected 500 storyboard files, found {len(storyboard_paths)}')

    storyboard_map: dict[str, dict[str, object]] = {}
    for path in storyboard_paths:
        storyboard = read_json(path)
        validate_storyboard_payload(storyboard, context, path)
        storyboard_map[path.stem] = storyboard

    compiled_by_profile: dict[str, dict[str, dict[str, object]]] = {}
    for profile_id in list_profile_ids():
        profile_dir = DATA_DIR / 'videos' / profile_id
        if not profile_dir.exists():
            raise ValueError(f'Missing compiled payload directory: {profile_dir}')
        payload_paths = sorted(profile_dir.glob('video_*.json'))
        if len(payload_paths) != 500:
            raise ValueError(f'Expected 500 compiled production videos for {profile_id}, found {len(payload_paths)}')
        compiled_by_profile[profile_id] = {}
        for path in payload_paths:
            payload = read_json(path)
            validate_compiled_payload(payload, context, profile_id, path)
            compiled_by_profile[profile_id][path.stem] = payload

    production_manifest = read_json(MANIFEST_PATH)
    demo_manifest = read_json(DEMO_MANIFEST_PATH)
    validate_with_schema(production_manifest, 'production_manifest', MANIFEST_PATH.name)
    validate_with_schema(demo_manifest, 'demo_manifest', DEMO_MANIFEST_PATH.name)
    validate_manifest_consistency(production_manifest, demo_manifest, storyboard_map, compiled_by_profile)

    demo_paths = sorted(DEMOS_DIR.glob('demo_*.json'))
    for path in demo_paths:
        validate_demo_payload(path)

    print('Profile-aware library validation passed')
    print(f'Production storyboards: {len(storyboard_paths)}')
    for profile_id in list_profile_ids():
        print(f'Compiled production videos [{profile_id}]: {len(compiled_by_profile[profile_id])}')
    print(f'Demo payloads: {len(demo_paths)}')


if __name__ == '__main__':
    validate()
