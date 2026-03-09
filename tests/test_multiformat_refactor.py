from __future__ import annotations

import copy

import pytest

from src.studio.assets.registry import build_asset_registry
from src.studio.contracts import DEFAULT_PROFILE_ID, default_scene_duration_frames, get_render_profile, list_profile_ids
from src.studio.generators.topic_library import (
    build_topic_catalog,
    build_topics_index,
    compile_storyboard_for_profile,
    create_storyboard_payload,
    migrate_storyboard_payload,
)
from src.studio.utils.validate import (
    ValidationContext,
    validate_asset_registry_payload,
    validate_compiled_payload,
    validate_storyboard_payload,
)


@pytest.fixture(scope='module')
def topics_index() -> dict[str, dict[str, object]]:
    return build_topics_index()


@pytest.fixture(scope='module')
def validation_context(topics_index: dict[str, dict[str, object]]) -> ValidationContext:
    return ValidationContext(build_topic_catalog(topics_index), build_asset_registry())


def test_migrate_legacy_storyboard_to_scene_plan(topics_index: dict[str, dict[str, object]]) -> None:
    legacy_payload = {
        'id': 'video_001',
        'topic': topics_index['video_001']['topic'],
        'title': topics_index['video_001']['topic'],
        'category': topics_index['video_001']['category'],
        'template': 'explainer',
        'segmentCount': 12,
        'segmentSeconds': 10,
        'segments': [
            {
                'index': 1,
                'segmentId': 'segment_01',
                'label': 'Topic frame',
                'narrationText': 'Legacy narration survives migration.',
                'onScreenText': 'Legacy title',
                'subtext': 'Legacy subtitle',
                'visual': 'crowd',
                'visualGrammar': 'hook_tension',
                'assetRefs': ['CharacterHappy'],
                'cameraAction': 'slow_zoom_in',
            }
        ],
    }

    migrated = migrate_storyboard_payload(legacy_payload, topics_index)

    assert migrated['id'] == 'video_001'
    assert migrated['defaultProfiles'] == ['shorts_vertical', 'social_square', 'youtube_horizontal']
    assert len(migrated['scenePlan']) == 12
    assert migrated['scenePlan'][0]['sceneId'] == 'scene_01'
    assert migrated['scenePlan'][0]['narrationText'] == 'Legacy narration survives migration.'
    assert migrated['scenePlan'][0]['onScreenText'] == 'Legacy title'


def test_invalid_visual_grammar_is_rejected(
    validation_context: ValidationContext,
    topics_index: dict[str, dict[str, object]],
) -> None:
    storyboard = create_storyboard_payload(1, str(topics_index['video_001']['topic']))
    storyboard['scenePlan'][0]['visualGrammar'] = 'not_a_real_grammar'

    with pytest.raises(ValueError, match='visualGrammar'):
        validate_storyboard_payload(storyboard, validation_context)


def test_invalid_profile_id_is_rejected(
    validation_context: ValidationContext,
    topics_index: dict[str, dict[str, object]],
) -> None:
    storyboard = create_storyboard_payload(1, str(topics_index['video_001']['topic']))
    storyboard['defaultProfiles'] = ['not_a_real_profile']

    with pytest.raises(ValueError, match='defaultProfiles'):
        validate_storyboard_payload(storyboard, validation_context)


def test_unknown_asset_refs_are_rejected(
    validation_context: ValidationContext,
    topics_index: dict[str, dict[str, object]],
) -> None:
    storyboard = create_storyboard_payload(1, str(topics_index['video_001']['topic']))
    storyboard['scenePlan'][0]['assetRefs'] = ['missing_asset']

    with pytest.raises(ValueError, match='unknown assetRefs'):
        validate_storyboard_payload(storyboard, validation_context)


def test_legacy_alias_asset_refs_are_accepted(
    validation_context: ValidationContext,
    topics_index: dict[str, dict[str, object]],
) -> None:
    storyboard = create_storyboard_payload(1, str(topics_index['video_001']['topic']))
    storyboard['scenePlan'][0]['assetRefs'] = ['home', 'cart', 'CharacterHappy', 'PropServer', 'globe']

    validate_storyboard_payload(storyboard, validation_context)


def test_missing_generated_component_path_is_rejected() -> None:
    registry = build_asset_registry()
    broken_registry = copy.deepcopy(registry)
    broken_registry['BackgroundCyber']['generatedComponent'] = 'engine/src/components/generated/__missing__.tsx'

    with pytest.raises(ValueError, match='missing file'):
        validate_asset_registry_payload(broken_registry)


def test_compile_dimensions_for_all_profiles(topics_index: dict[str, dict[str, object]]) -> None:
    storyboard = create_storyboard_payload(2, str(topics_index['video_002']['topic']))

    for profile_id in list_profile_ids():
        compiled = compile_storyboard_for_profile(storyboard, profile_id)
        profile = get_render_profile(profile_id)
        assert compiled['profileId'] == profile_id
        assert compiled['width'] == profile['width']
        assert compiled['height'] == profile['height']
        assert compiled['aspectRatio'] == profile['aspectRatio']
        assert len(compiled['scenes']) == profile['timeline']['sceneCount']
        assert compiled['scenes'][0]['duration'] == default_scene_duration_frames(profile_id)


def test_compile_canonicalizes_legacy_asset_refs(topics_index: dict[str, dict[str, object]]) -> None:
    storyboard = create_storyboard_payload(3, str(topics_index['video_003']['topic']))
    storyboard['scenePlan'][0]['assetRefs'] = ['home', 'cart', 'CharacterHappy', 'PropServer', 'globe', 'home']

    compiled = compile_storyboard_for_profile(storyboard, DEFAULT_PROFILE_ID)
    scene = compiled['scenes'][0]

    assert scene['assetTags'] == ['house', 'shopping_cart', 'person', 'server', 'earth_globe']


def test_compiled_payload_rejects_non_canonical_asset_tags(
    validation_context: ValidationContext,
    topics_index: dict[str, dict[str, object]],
) -> None:
    storyboard = create_storyboard_payload(4, str(topics_index['video_004']['topic']))
    compiled = compile_storyboard_for_profile(storyboard, DEFAULT_PROFILE_ID)
    compiled['scenes'][0]['assetTags'][0] = 'home'

    with pytest.raises(ValueError, match='must be canonical ids'):
        validate_compiled_payload(compiled, validation_context, DEFAULT_PROFILE_ID)
