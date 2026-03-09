from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from src.studio.assets.catalog import canonical_asset_id
from src.studio.assets.registry import build_asset_registry, write_asset_registry_files
from src.studio.config import (
    ARCHIVE_DIR,
    ASSET_COVERAGE_FILE,
    DATA_DIR,
    DEMOS_DIR,
    ENGINE_DIR,
    RENDER_PROFILES_FILE,
    REPRESENTATIVE_TOPICS_FILE,
    SCENE_GRAMMAR_FILE,
    STORYBOARDS_DIR,
    TOPIC_CATALOG_FILE,
    TOPICS_FILE,
    VIDEOS_DIR,
    ensure_directories,
)
from src.studio.contracts import (
    CATEGORIES,
    CATEGORY_ASSET_TAGS,
    DEFAULT_PROFILE_ID,
    DEFAULT_PROFILE_IDS,
    RENDER_PROFILES,
    SCENE_GRAMMAR_REGISTRY,
    compiled_payload_path,
    default_scene_seconds_for_profile,
    default_template_family_for_index,
    default_template_for_index,
    get_render_profile,
    infer_category,
    is_production_video_id,
    list_supported_profile_ids,
    resolve_template_for_profile,
    scene_template_family_blueprint,
)
from src.studio.generators.narrative_engine import NarrativeEngine

TOPIC_LINE_RE = re.compile(r"^(\d+)\.\s+(.+?)\s*$")
MANIFEST_PATH = DATA_DIR / "video_manifest.json"
DEMO_MANIFEST_PATH = DATA_DIR / "demo_manifest.json"
ENGINE_MANIFEST_PATH = ENGINE_DIR / "src" / "generated" / "videoManifest.js"
ASSET_REQUIREMENTS_COMPAT_PATH = DATA_DIR / "asset_requirements_500.json"
LEGACY_ARCHIVE_DIR = ARCHIVE_DIR / "legacy_payloads"
LEGACY_ROOT_VIDEO_DIR = ARCHIVE_DIR / "legacy_flat_payloads"

LEGACY_DEMO_SOURCES = {
    "demo_graphics_showcase_v1": "video_500.json",
    "demo_combined_features_30s": "video_501.json",
    "demo_combined_features_30s_60fps": "video_502.json",
    "demo_graphics_showcase_v2": "video_503.json",
}


def parse_topics() -> list[dict[str, object]]:
    topics: list[dict[str, object]] = []
    for line in TOPICS_FILE.read_text(encoding="utf-8").splitlines():
        match = TOPIC_LINE_RE.match(line)
        if not match:
            continue
        index = int(match.group(1))
        topic = match.group(2)
        video_id = f"video_{index:03d}"
        topics.append(
            {
                "id": video_id,
                "index": index,
                "topic": topic,
                "title": topic,
                "category": infer_category(index),
                "source": "data/raw/Topics.txt",
            }
        )
    if len(topics) != 500:
        raise ValueError(f"Expected 500 topics but found {len(topics)}")
    return topics


def build_topics_index() -> dict[str, dict[str, object]]:
    return {str(item["id"]): item for item in parse_topics()}


def build_topic_catalog(topics_index: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    return {
        video_id: {
            "id": video_id,
            "index": int(item["index"]),
            "topic": str(item["topic"]),
            "title": str(item["title"]),
            "category": str(item["category"]),
            "source": str(item["source"]),
        }
        for video_id, item in sorted(topics_index.items())
    }


def build_representative_topics(topic_catalog: dict[str, dict[str, object]]) -> dict[str, object]:
    by_category: dict[str, list[dict[str, object]]] = defaultdict(list)
    for entry in topic_catalog.values():
        by_category[str(entry["category"])].append(entry)

    selected: list[dict[str, object]] = []
    offsets = (0, 20, 40, 60, 80)
    for category, entries in sorted(by_category.items()):
        ordered = sorted(entries, key=lambda item: int(item["index"]))
        for offset in offsets:
            if offset >= len(ordered):
                continue
            picked = ordered[offset]
            selected.append(
                {
                    "id": picked["id"],
                    "topic": picked["topic"],
                    "category": category,
                    "index": picked["index"],
                    "reason": "Deterministic representative sample for engine coverage and visual grammar review.",
                }
            )

    return {
        "selectionStrategy": "5 deterministic topics per category at 20-topic intervals",
        "count": len(selected),
        "topics": selected,
    }


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object] | list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tokenize_words(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9']+", text)]


def build_metadata_hints(topic: str, category: str, scenes: list[dict[str, object]]) -> dict[str, object]:
    keywords: list[str] = []
    seen: set[str] = set()
    for token in tokenize_words(topic) + tokenize_words(category):
        if len(token) < 3 or token in seen:
            continue
        keywords.append(token)
        seen.add(token)
    hashtags = ["#" + "".join(part.capitalize() for part in token.split()) for token in keywords[:6]]
    return {
        "summary": f"{topic} explained as a systems video.",
        "keywords": keywords[:16],
        "hashtags": hashtags[:8],
        "hook": scenes[0]["narrationText"] if scenes else topic,
    }


def derive_on_screen_text(topic: str, label: str) -> str:
    defaults = {
        "Topic frame": "topic",
        "Hook": "Why It Matters",
        "System boundary": "System Boundary",
        "Cause layer 1": "Root Cause",
        "Cause layer 2": "Mechanism",
        "Cause layer 3": "Feedback Loops",
        "Data lens": "Data Lens",
        "Real world scene": "Real World",
        "Ecology/externalities": "Hidden Costs",
        "Macro trend": "Macro Trend",
        "Actionable takeaway": "What To Do",
        "Closing": "Closing",
    }
    token = defaults.get(label, label)
    return topic if token == "topic" else token


def default_background_mode(category: str, visual: str) -> str:
    if visual == "earth" or category == "FUTURE SYSTEMS":
        return "terrain"
    if visual in {"network", "lattice", "neural_core", "math_equation"}:
        return "mesh"
    return "gradient"


def default_motion(visual: str) -> str:
    if visual in {"earth", "lattice", "neural_core"}:
        return "drift"
    return "pan"


def default_overlays(visual: str) -> list[str]:
    overlays = ["grain", "vignette"]
    if visual in {"network", "lattice", "neural_core", "earth"}:
        overlays.append("scanlines")
    return overlays


def default_asset_refs(category: str, visual: str, step: int) -> list[str]:
    category_refs = CATEGORY_ASSET_TAGS[category]
    if visual == "crowd":
        return ["person", "person_group", "crowd"]
    if visual == "icons":
        return category_refs[:3] + ["robot", "server", "satellite"]
    if visual == "animals":
        return ["bird", "turtle", "deer"] if category == "FUTURE SYSTEMS" else ["bird", "fish", "bee"]
    if visual == "network":
        return category_refs[:3] + ["network_nodes", "flow_arrow"]
    if visual == "flow":
        return ["flow_arrow", "loop_arrow"] + category_refs[:2]
    if visual == "math_equation":
        return ["bar_chart", "flow_arrow", "gear"] + category_refs[:2]
    if visual == "neural_core":
        return ["ai_brain", "network_nodes", "data_cloud"] + category_refs[:2]
    if visual == "earth":
        return ["earth_globe", "data_cloud", "signal_wave"] + category_refs[:2]
    if visual == "city":
        return ["house", "airplane", "factory"]
    if visual == "lattice":
        return ["network_nodes", "gear", "algorithm_symbol"] + category_refs[:2]
    _ = step
    return category_refs


def canonicalize_asset_refs(asset_refs: Iterable[object]) -> list[str]:
    resolved: list[str] = []
    seen: set[str] = set()
    for item in asset_refs:
        canonical = canonical_asset_id(str(item))
        if canonical in seen:
            continue
        resolved.append(canonical)
        seen.add(canonical)
    return resolved


def build_scene_plan_scene(topic: str, step: int, blueprint: dict[str, object], category: str) -> dict[str, object]:
    label = str(blueprint["label"])
    visual = str(blueprint["visual"])
    mood = str(blueprint["mood"])
    category_meta = CATEGORIES[category]
    return {
        "sceneId": f"scene_{step:02d}",
        "label": label,
        "purpose": str(blueprint["purpose"]),
        "narrationText": NarrativeEngine.generate_narration(topic, label, category, mood),
        "onScreenText": derive_on_screen_text(topic, label),
        "subtext": NarrativeEngine.generate_subtext(topic, label, category, mood),
        "visualGrammar": str(blueprint["visualGrammar"]),
        "visual": visual,
        "visualDirection": SCENE_GRAMMAR_REGISTRY[str(blueprint["visualGrammar"])]["visualDirection"],
        "assetRefs": default_asset_refs(category, visual, step),
        "cameraIntent": str(blueprint["cameraIntent"]),
        "motion": default_motion(visual),
        "backgroundMode": default_background_mode(category, visual),
        "overlays": default_overlays(visual),
        "palette": category_meta["palette"],
        "mood": mood,
        "timingHints": {"baseSeconds": default_scene_seconds_for_profile(DEFAULT_PROFILE_ID)},
        "profileOverrides": {},
    }


def create_storyboard_payload(index: int, topic: str) -> dict[str, object]:
    video_id = f"video_{index:03d}"
    category = infer_category(index)
    template_family = default_template_family_for_index(index)
    scene_plan = [
        build_scene_plan_scene(topic, step, blueprint, category)
        for step, blueprint in enumerate(scene_template_family_blueprint(template_family), start=1)
    ]
    return {
        "id": video_id,
        "topicRef": video_id,
        "topic": topic,
        "title": topic,
        "category": category,
        "accentColor": CATEGORIES[category]["accent"],
        "templateFamily": template_family,
        "templateHint": default_template_for_index(index),
        "defaultProfiles": list(DEFAULT_PROFILE_IDS),
        "metadataHints": build_metadata_hints(topic, category, scene_plan),
        "audioMode": "text_only",
        "scenePlan": scene_plan,
    }


def _merge_dicts(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def normalize_scene_plan(
    payload: dict[str, object],
    topic_entry: dict[str, object],
    category: str,
    template_family: str,
) -> list[dict[str, object]]:
    topic = str(payload.get("topic") or topic_entry["topic"])
    blueprint_family = scene_template_family_blueprint(template_family)

    if "scenePlan" in payload and isinstance(payload["scenePlan"], list):
        raw_scenes = list(payload["scenePlan"])
        normalized: list[dict[str, object]] = []
        for step, blueprint in enumerate(blueprint_family, start=1):
            raw = raw_scenes[step - 1] if step - 1 < len(raw_scenes) and isinstance(raw_scenes[step - 1], dict) else {}
            grammar_key = str(raw.get("visualGrammar") or blueprint["visualGrammar"])
            grammar = SCENE_GRAMMAR_REGISTRY[grammar_key]
            visual = str(raw.get("visual") or blueprint["visual"])
            mood = str(raw.get("mood") or blueprint["mood"])
            normalized.append(
                {
                    "sceneId": str(raw.get("sceneId") or f"scene_{step:02d}"),
                    "label": str(raw.get("label") or blueprint["label"]),
                    "purpose": str(raw.get("purpose") or blueprint["purpose"]),
                    "narrationText": str(
                        raw.get("narrationText")
                        or NarrativeEngine.generate_narration(topic, str(blueprint["label"]), category, mood)
                    ),
                    "onScreenText": str(raw.get("onScreenText") or derive_on_screen_text(topic, str(blueprint["label"]))),
                    "subtext": str(
                        raw.get("subtext")
                        or NarrativeEngine.generate_subtext(topic, str(blueprint["label"]), category, mood)
                    ),
                    "visualGrammar": grammar_key,
                    "visual": visual,
                    "visualDirection": str(raw.get("visualDirection") or grammar["visualDirection"]),
                    "assetRefs": [str(item) for item in raw.get("assetRefs", default_asset_refs(category, visual, step))],
                    "cameraIntent": str(raw.get("cameraIntent") or raw.get("cameraAction") or blueprint["cameraIntent"]),
                    "motion": str(raw.get("motion") or default_motion(visual)),
                    "backgroundMode": str(raw.get("backgroundMode") or default_background_mode(category, visual)),
                    "overlays": [str(item) for item in raw.get("overlays", default_overlays(visual))],
                    "palette": raw.get("palette") or CATEGORIES[category]["palette"],
                    "mood": mood,
                    "timingHints": raw.get("timingHints") or {"baseSeconds": default_scene_seconds_for_profile(DEFAULT_PROFILE_ID)},
                    "profileOverrides": raw.get("profileOverrides") or {},
                }
            )
        return normalized

    legacy_segments = list(payload.get("segments", []))
    normalized = []
    for step, blueprint in enumerate(blueprint_family, start=1):
        legacy = legacy_segments[step - 1] if step - 1 < len(legacy_segments) and isinstance(legacy_segments[step - 1], dict) else {}
        grammar_key = str(legacy.get("visualGrammar") or blueprint["visualGrammar"])
        grammar = SCENE_GRAMMAR_REGISTRY[grammar_key]
        visual = str(legacy.get("visual") or blueprint["visual"])
        mood = str(legacy.get("mood") or blueprint["mood"])
        normalized.append(
            {
                "sceneId": f"scene_{step:02d}",
                "label": str(legacy.get("label") or blueprint["label"]),
                "purpose": str(legacy.get("purpose") or blueprint["purpose"]),
                "narrationText": str(
                    legacy.get("narrationText")
                    or NarrativeEngine.generate_narration(topic, str(blueprint["label"]), category, mood)
                ),
                "onScreenText": str(legacy.get("onScreenText") or derive_on_screen_text(topic, str(blueprint["label"]))),
                "subtext": str(
                    legacy.get("subtext")
                    or NarrativeEngine.generate_subtext(topic, str(blueprint["label"]), category, mood)
                ),
                "visualGrammar": grammar_key,
                "visual": visual,
                "visualDirection": str(legacy.get("visualDirection") or grammar["visualDirection"]),
                "assetRefs": [str(item) for item in legacy.get("assetRefs", default_asset_refs(category, visual, step))],
                "cameraIntent": str(legacy.get("cameraIntent") or legacy.get("cameraAction") or blueprint["cameraIntent"]),
                "motion": str(legacy.get("motion") or default_motion(visual)),
                "backgroundMode": str(legacy.get("backgroundMode") or default_background_mode(category, visual)),
                "overlays": [str(item) for item in legacy.get("overlays", default_overlays(visual))],
                "palette": legacy.get("palette") or CATEGORIES[category]["palette"],
                "mood": mood,
                "timingHints": legacy.get("timingHints")
                or {"baseSeconds": int(payload.get("segmentSeconds", default_scene_seconds_for_profile(DEFAULT_PROFILE_ID)))},
                "profileOverrides": legacy.get("profileOverrides") or {},
            }
        )
    return normalized


def migrate_storyboard_payload(payload: dict[str, object], topics_index: dict[str, dict[str, object]]) -> dict[str, object]:
    video_id = str(payload.get("id") or "")
    if not is_production_video_id(video_id):
        raise ValueError(f"Unsupported storyboard id: {video_id}")
    topic_entry = topics_index[video_id]
    category = str(payload.get("category") or topic_entry["category"])
    template_family = str(payload.get("templateFamily") or default_template_family_for_index(int(topic_entry["index"])))
    scene_plan = normalize_scene_plan(payload, topic_entry, category, template_family)
    topic = str(payload.get("topic") or topic_entry["topic"])
    return {
        "id": video_id,
        "topicRef": str(payload.get("topicRef") or video_id),
        "topic": topic,
        "title": str(payload.get("title") or topic),
        "category": category,
        "accentColor": str(payload.get("accentColor") or CATEGORIES[category]["accent"]),
        "templateFamily": template_family,
        "templateHint": str(payload.get("templateHint") or payload.get("template") or default_template_for_index(int(topic_entry["index"]))),
        "defaultProfiles": [
            str(profile_id)
            for profile_id in payload.get("defaultProfiles", list(DEFAULT_PROFILE_IDS))
            if str(profile_id) in RENDER_PROFILES
        ]
        or list(DEFAULT_PROFILE_IDS),
        "metadataHints": payload.get("metadataHints") or build_metadata_hints(topic, category, scene_plan),
        "audioMode": str(payload.get("audioMode") or "text_only"),
        "scenePlan": scene_plan,
    }


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
            raise ValueError(f"Unknown production video id: {video_id}")

        storyboard_path = STORYBOARDS_DIR / f"{video_id}.json"
        if storyboard_path.exists() and not force_storyboards:
            existing = read_json(storyboard_path)
            migrated = migrate_storyboard_payload(existing, topics_index)
            if materialize and migrated != existing:
                write_json(storyboard_path, migrated)
            storyboard_payloads.append(migrated)
            preserved += 1
            continue

        storyboard = create_storyboard_payload(int(topic_entry["index"]), str(topic_entry["topic"]))
        if materialize:
            write_json(storyboard_path, storyboard)
        storyboard_payloads.append(storyboard)
        created += 1

    return storyboard_payloads, created, preserved


def _resolve_scene_for_profile(scene: dict[str, object], profile_id: str) -> dict[str, object]:
    profile_overrides = scene.get("profileOverrides") or {}
    if isinstance(profile_overrides, dict) and profile_id in profile_overrides and isinstance(profile_overrides[profile_id], dict):
        return _merge_dicts(scene, profile_overrides[profile_id])
    return dict(scene)


def compile_scene(storyboard: dict[str, object], scene: dict[str, object], profile_id: str, ordinal: int) -> dict[str, object]:
    profile = get_render_profile(profile_id)
    resolved = _resolve_scene_for_profile(scene, profile_id)
    category = str(storyboard["category"])
    accent_color = str(storyboard.get("accentColor") or CATEGORIES[category]["accent"])
    grammar_key = str(resolved["visualGrammar"])
    grammar = SCENE_GRAMMAR_REGISTRY[grammar_key]
    visual = str(resolved.get("visual") or grammar["defaultVisual"])
    timing_hints = resolved.get("timingHints") or {}
    if "seconds" in timing_hints:
        scene_seconds = float(timing_hints["seconds"])
    elif profile_id == DEFAULT_PROFILE_ID and "baseSeconds" in timing_hints:
        scene_seconds = float(timing_hints["baseSeconds"])
    else:
        scene_seconds = float(profile["timeline"]["sceneDurationSeconds"])
    duration = round(scene_seconds * int(profile["fps"]))
    asset_refs = canonicalize_asset_refs(resolved.get("assetRefs", default_asset_refs(category, visual, ordinal)))

    payload: dict[str, object] = {
        "sceneId": str(resolved.get("sceneId") or f"scene_{ordinal:02d}"),
        "segmentId": f"segment_{ordinal:02d}"
        if profile["timeline"]["mode"] == "segmented"
        else str(resolved.get("sceneId") or f"scene_{ordinal:02d}"),
        "label": str(resolved.get("label") or grammar["label"]),
        "purpose": str(resolved.get("purpose") or ""),
        "narrationText": str(resolved["narrationText"]),
        "text": str(resolved["onScreenText"]),
        "subtext": str(resolved.get("subtext") or ""),
        "duration": duration,
        "visual": visual,
        "visualGrammar": grammar_key,
        "action": str(resolved.get("cameraIntent") or grammar["defaultCameraIntent"]),
        "cameraIntent": str(resolved.get("cameraIntent") or grammar["defaultCameraIntent"]),
        "category": category,
        "accentColor": accent_color,
        "palette": resolved.get("palette") or CATEGORIES[category]["palette"],
        "assetTags": asset_refs,
        "visualDirection": str(resolved.get("visualDirection") or grammar["visualDirection"]),
        "backgroundMode": str(resolved.get("backgroundMode") or default_background_mode(category, visual)),
        "motion": str(resolved.get("motion") or default_motion(visual)),
        "overlays": [str(item) for item in resolved.get("overlays", default_overlays(visual))],
        "mood": str(resolved.get("mood") or grammar["defaultMood"]),
        "layout": profile["layout"],
        "profileId": profile_id,
    }

    video_id = str(storyboard["id"])
    video_index = int(video_id.split("_")[1])
    seed = (video_index % 9) + ordinal

    if payload["mood"] == "stressed":
        payload["weather"] = "rain"
    elif category == "EVERYDAY SYSTEMS" and payload["mood"] == "thinking":
        payload["weather"] = "snow"

    if visual == "crowd":
        payload["crowdCount"] = 10 + (video_index % 8)
    if visual == "bars":
        payload["barValues"] = [18 + seed, 26 + seed, 36 + seed, 47 + seed, 58 + seed]
    if visual == "flow":
        payload["flowLabels"] = ["Trigger", "Mechanism", "Outcome"] if ordinal == 5 else ["Input", "System", "Output"]
    if visual == "network":
        payload["networkNodes"] = (
            ["State", "Market", "Labor", "Capital", "Public"]
            if ordinal == 3
            else ["Policy", "Price", "Behavior", "Risk", "Feedback"]
        )
    if visual == "icons":
        payload["icons"] = asset_refs
    if visual == "animals":
        payload["animals"] = asset_refs

    return payload


def compile_storyboard_for_profile(storyboard: dict[str, object], profile_id: str) -> dict[str, object]:
    profile = get_render_profile(profile_id)
    video_id = str(storyboard["id"])
    video_index = int(video_id.split("_")[1])
    scenes = [
        compile_scene(storyboard, scene, profile_id, ordinal)
        for ordinal, scene in enumerate(storyboard["scenePlan"], start=1)
    ]
    total_duration_seconds = sum(int(scene["duration"]) for scene in scenes) / int(profile["fps"]) if scenes else 0
    return {
        "id": video_id,
        "topicRef": str(storyboard["topicRef"]),
        "profileId": profile_id,
        "dataset": "production",
        "title": str(storyboard["title"]),
        "topic": str(storyboard["topic"]),
        "templateFamily": str(storyboard["templateFamily"]),
        "template": str(
            storyboard.get("templateHint")
            or resolve_template_for_profile(str(storyboard["templateFamily"]), profile_id, video_index)
        ),
        "fps": int(profile["fps"]),
        "width": int(profile["width"]),
        "height": int(profile["height"]),
        "aspectRatio": str(profile["aspectRatio"]),
        "timeline": profile["timeline"],
        "sceneCount": len(scenes),
        "totalDurationSeconds": total_duration_seconds,
        "category": str(storyboard["category"]),
        "accentColor": str(storyboard.get("accentColor") or CATEGORIES[str(storyboard["category"])]["accent"]),
        "platformTargets": profile["platforms"],
        "layoutProfile": profile["layout"],
        "audioMode": str(storyboard.get("audioMode") or "text_only"),
        "metadataHints": storyboard.get("metadataHints") or {},
        "scenes": scenes,
    }


def compile_storyboards(
    storyboards: list[dict[str, object]],
    profile_ids: list[str],
    materialize: bool = True,
) -> dict[str, list[dict[str, object]]]:
    compiled_by_profile: dict[str, list[dict[str, object]]] = {profile_id: [] for profile_id in profile_ids}
    for storyboard in storyboards:
        for profile_id in profile_ids:
            compiled = compile_storyboard_for_profile(storyboard, profile_id)
            compiled_by_profile[profile_id].append(compiled)
            if materialize:
                write_json(compiled_payload_path(str(compiled["id"]), profile_id), compiled)
    return compiled_by_profile


def write_topic_outputs(topic_catalog: dict[str, dict[str, object]]) -> None:
    write_json(TOPIC_CATALOG_FILE, topic_catalog)
    write_json(REPRESENTATIVE_TOPICS_FILE, build_representative_topics(topic_catalog))


def write_registry_outputs() -> dict[str, dict[str, object]]:
    write_json(RENDER_PROFILES_FILE, RENDER_PROFILES)
    write_json(SCENE_GRAMMAR_FILE, SCENE_GRAMMAR_REGISTRY)
    return write_asset_registry_files()


def refresh_engine_manifest(profile_ids: list[str] | None = None) -> None:
    if MANIFEST_PATH.exists():
        production_manifest = read_json(MANIFEST_PATH)
        production_ids = sorted(str(video_id) for video_id in production_manifest.keys())
    else:
        production_ids = sorted(path.stem for path in STORYBOARDS_DIR.glob("video_*.json"))

    if DEMO_MANIFEST_PATH.exists():
        demo_manifest = read_json(DEMO_MANIFEST_PATH)
        demo_ids = sorted(str(video_id) for video_id in demo_manifest.keys())
    else:
        demo_ids = sorted(path.stem for path in DEMOS_DIR.glob("demo_*.json"))

    write_engine_manifest(production_ids, demo_ids, profile_ids or list_supported_profile_ids())


def write_production_manifest(
    storyboards: list[dict[str, object]],
    compiled_by_profile: dict[str, list[dict[str, object]]],
) -> None:
    manifest: dict[str, dict[str, object]] = {}
    storyboard_map = {str(item["id"]): item for item in storyboards}

    for video_id, storyboard in sorted(storyboard_map.items()):
        manifest_entry = {
            "title": storyboard["title"],
            "topicRef": storyboard["topicRef"],
            "topic": storyboard["topic"],
            "category": storyboard["category"],
            "templateFamily": storyboard["templateFamily"],
            "defaultProfiles": storyboard["defaultProfiles"],
            "storyboard": f"data/storyboards/{video_id}.json",
            "profiles": {},
        }
        for profile_id, payloads in compiled_by_profile.items():
            payload = next(item for item in payloads if str(item["id"]) == video_id)
            manifest_entry["profiles"][profile_id] = {
                "path": f"data/videos/{profile_id}/{video_id}.json",
                "width": payload["width"],
                "height": payload["height"],
                "fps": payload["fps"],
                "sceneCount": payload["sceneCount"],
                "totalDurationSeconds": payload["totalDurationSeconds"],
                "aspectRatio": payload["aspectRatio"],
            }
        manifest[video_id] = manifest_entry

    write_json(MANIFEST_PATH, manifest)


def write_demo_manifest(demo_payloads: list[dict[str, object]]) -> None:
    manifest: dict[str, dict[str, object]] = {}
    for payload in demo_payloads:
        demo_id = str(payload["id"])
        manifest[demo_id] = {
            "title": payload["title"],
            "template": payload.get("template", "explainer"),
            "category": payload.get("category", "DEMO"),
            "sceneCount": len(payload.get("scenes", [])),
        }
    write_json(DEMO_MANIFEST_PATH, manifest)


def write_engine_manifest(production_ids: list[str], demo_ids: list[str], profile_ids: list[str]) -> None:
    demo_fallback = demo_ids[0] if demo_ids else None
    lines = [
        "export const productionVideoIds = " + json.dumps(production_ids, ensure_ascii=False, indent=2) + ";",
        "",
        "export const demoVideoIds = " + json.dumps(demo_ids, ensure_ascii=False, indent=2) + ";",
        "",
        "export const productionProfileIds = " + json.dumps(profile_ids, ensure_ascii=False, indent=2) + ";",
        "",
        f"export const defaultProductionProfileId = {json.dumps(DEFAULT_PROFILE_ID)};",
        "",
        "export const getVideoData = async (dataset, videoId, profileId) => {",
        "  const selectedDataset = dataset === 'demo' ? 'demo' : 'production';",
        '  if (selectedDataset === "demo") {',
        f"    const fallbackId = {json.dumps(demo_fallback)};",
        "    if (!fallbackId) {",
        '      throw new Error("No demo payloads are available.");',
        "    }",
        "    const safeId = demoVideoIds.includes(videoId) ? videoId : fallbackId;",
        "    const module = await import(`../../../data/demos/${safeId}.json`);",
        "    return module.default;",
        "  }",
        "  const safeProfileId = profileId || defaultProductionProfileId;",
        "  const id = videoId || 'video_001';",
        '  const safeId = productionVideoIds.includes(id) ? id : "video_001";',
        "  const module = await import(`../../../data/videos/${safeProfileId}/${safeId}.json`);",
        "  return module.default;",
        "};",
        "",
    ]
    ENGINE_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENGINE_MANIFEST_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_asset_coverage(
    storyboards: list[dict[str, object]],
    compiled_by_profile: dict[str, list[dict[str, object]]],
    asset_registry: dict[str, dict[str, object]],
) -> None:
    coverage: dict[str, object] = {
        "summary": {
            "videoCount": len(storyboards),
            "profileCount": len(compiled_by_profile),
            "assetCount": len(asset_registry),
        },
        "assets": {},
        "videos": {},
    }

    for asset_id, entry in asset_registry.items():
        coverage["assets"][asset_id] = {
            "family": entry["family"],
            "sourceType": entry["sourceType"],
            "profiles": [],
            "videos": [],
            "sceneRefs": [],
        }

    for storyboard in storyboards:
        video_id = str(storyboard["id"])
        coverage["videos"][video_id] = {
            "title": storyboard["title"],
            "category": storyboard["category"],
            "profiles": {},
        }

    for profile_id, payloads in compiled_by_profile.items():
        for payload in payloads:
            video_id = str(payload["id"])
            asset_set: set[str] = set()
            scene_refs: list[str] = []
            for scene in payload["scenes"]:
                scene_id = str(scene["sceneId"])
                scene_refs.append(scene_id)
                for asset_id in scene.get("assetTags", []):
                    asset_key = str(asset_id)
                    asset_set.add(asset_key)
                    if asset_key not in coverage["assets"]:
                        continue
                    asset_entry = coverage["assets"][asset_key]
                    if video_id not in asset_entry["videos"]:
                        asset_entry["videos"].append(video_id)
                    if profile_id not in asset_entry["profiles"]:
                        asset_entry["profiles"].append(profile_id)
                    asset_entry["sceneRefs"].append(f"{video_id}:{profile_id}:{scene_id}")

            coverage["videos"][video_id]["profiles"][profile_id] = {
                "path": f"data/videos/{profile_id}/{video_id}.json",
                "assets": sorted(asset_set),
                "sceneRefs": scene_refs,
                "visuals": sorted({str(scene["visual"]) for scene in payload["scenes"]}),
            }

    write_json(ASSET_COVERAGE_FILE, coverage)
    compatibility = {
        "assetLibrary": {
            family: sorted([asset_id for asset_id, entry in asset_registry.items() if entry["family"] == family])
            for family in sorted({entry["family"] for entry in asset_registry.values()})
        },
        "videos": coverage["videos"],
    }
    write_json(ASSET_REQUIREMENTS_COMPAT_PATH, compatibility)


def archive_file(source: Path, target_name: str | None = None) -> Path:
    LEGACY_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    target = LEGACY_ARCHIVE_DIR / (target_name or source.name)
    target.parent.mkdir(parents=True, exist_ok=True)
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
        if source_name in {"video_501.json", "video_502.json", "video_503.json"}:
            return current
        payload = read_json(current)
        if len(payload.get("scenes", [])) != 12:
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

    legacy_overview = VIDEOS_DIR / "video_001.json"
    if legacy_overview.exists():
        payload = read_json(legacy_overview)
        if len(payload.get("scenes", [])) != 12:
            archive_file(legacy_overview, "video_001_legacy_showcase.json")

    legacy_backup = VIDEOS_DIR / "video_500_backup_20260305_211242.json"
    if legacy_backup.exists():
        archive_file(legacy_backup)

    for demo_id, source_name in LEGACY_DEMO_SOURCES.items():
        source = find_legacy_source(source_name)
        if source is None:
            continue
        payload = read_json(source)
        payload["id"] = demo_id
        demo_path = DEMOS_DIR / f"{demo_id}.json"
        write_json(demo_path, payload)
        if source.parent == VIDEOS_DIR:
            archive_file(source)

    for path in sorted(DEMOS_DIR.glob("demo_*.json")):
        demo_payloads.append(read_json(path))

    return demo_payloads


def cleanup_legacy_flat_payloads(materialize: bool = True) -> None:
    if not materialize:
        return
    LEGACY_ROOT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(VIDEOS_DIR.glob("video_*.json")):
        target = LEGACY_ROOT_VIDEO_DIR / path.name
        if target.exists():
            path.unlink(missing_ok=True)
            continue
        shutil.move(str(path), str(target))


def write_materialized_support_files(topic_catalog: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    write_topic_outputs(topic_catalog)
    return write_registry_outputs()


def build_library(
    materialize: bool,
    force_storyboards: bool = False,
    only_video_ids: list[str] | None = None,
    refresh_manifests: bool = True,
    profile_ids: list[str] | None = None,
) -> dict[str, object]:
    ensure_directories()
    topics_index = build_topics_index()
    selected_profile_ids = profile_ids or list(DEFAULT_PROFILE_IDS)

    topic_catalog = build_topic_catalog(topics_index)
    asset_registry = build_asset_registry()
    if materialize and refresh_manifests:
        asset_registry = write_materialized_support_files(topic_catalog)

    demo_payloads = migrate_legacy_payloads(materialize=materialize) if refresh_manifests else []
    storyboards, created_storyboards, preserved_storyboards = ensure_storyboards(
        topics_index,
        only_video_ids=only_video_ids,
        force_storyboards=force_storyboards,
        materialize=materialize,
    )
    compiled_by_profile = compile_storyboards(storyboards, selected_profile_ids, materialize=materialize)

    if materialize and refresh_manifests:
        write_production_manifest(storyboards, compiled_by_profile)
        write_demo_manifest(demo_payloads)
        write_engine_manifest(
            sorted(str(payload["id"]) for payload in compiled_by_profile[DEFAULT_PROFILE_ID]),
            sorted(str(payload["id"]) for payload in demo_payloads),
            list_supported_profile_ids(),
        )
        write_asset_coverage(storyboards, compiled_by_profile, asset_registry)
        cleanup_legacy_flat_payloads(materialize=True)

    return {
        "topic_catalog": topic_catalog,
        "storyboards": storyboards,
        "compiled_payloads_by_profile": compiled_by_profile,
        "compiled_payloads": compiled_by_profile.get(DEFAULT_PROFILE_ID, []),
        "demo_payloads": demo_payloads,
        "created_storyboards": created_storyboards,
        "preserved_storyboards": preserved_storyboards,
        "profile_ids": selected_profile_ids,
    }


def materialize_production_video(video_id: str, profile_id: str = DEFAULT_PROFILE_ID, force_storyboards: bool = False) -> dict[str, object]:
    summary = build_library(
        materialize=True,
        force_storyboards=force_storyboards,
        only_video_ids=[video_id],
        refresh_manifests=False,
        profile_ids=[profile_id],
    )
    compiled = summary["compiled_payloads_by_profile"].get(profile_id, [])
    if not compiled:
        raise ValueError(f"No compiled payload created for {video_id} [{profile_id}]")
    return compiled[0]


def load_production_payload(video_id: str, profile_id: str = DEFAULT_PROFILE_ID) -> dict[str, object]:
    payload_path = compiled_payload_path(video_id, profile_id)
    if not payload_path.exists():
        return materialize_production_video(video_id, profile_id)
    return read_json(payload_path)


def load_demo_payload(video_id: str) -> dict[str, object]:
    migrate_legacy_payloads(materialize=True)
    demo_path = DEMOS_DIR / f"{video_id}.json"
    if not demo_path.exists():
        raise FileNotFoundError(f"Demo payload not found: {demo_path}")
    return read_json(demo_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build profile-aware production payloads and manifests")
    parser.add_argument("--materialize", action="store_true", help="Write storyboards, compiled videos, manifests, and registries to disk")
    parser.add_argument("--force-storyboards", action="store_true", help="Regenerate storyboard skeletons even when files already exist")
    parser.add_argument("--profile", action="append", dest="profiles", help="Limit compilation to the selected profile id. Repeat for multiple profiles.")
    args = parser.parse_args()

    summary = build_library(
        materialize=args.materialize,
        force_storyboards=args.force_storyboards,
        profile_ids=args.profiles,
    )
    production_count = len(summary["storyboards"])
    profile_summary = ", ".join(
        f"{profile_id}:{len(summary['compiled_payloads_by_profile'].get(profile_id, []))}"
        for profile_id in summary["profile_ids"]
    )
    demo_count = len(summary["demo_payloads"])
    print(f"Production storyboards prepared: {production_count}")
    print(f"Created storyboards: {summary['created_storyboards']}")
    print(f"Preserved storyboards: {summary['preserved_storyboards']}")
    print(f"Compiled production payloads by profile: {profile_summary}")
    print(f"Demo payloads available: {demo_count}")
    if args.materialize:
        print(f"Materialized storyboards in: {STORYBOARDS_DIR}")
        print(f"Materialized production payloads in: {VIDEOS_DIR}")
        print(f"Materialized demo payloads in: {DEMOS_DIR}")


if __name__ == "__main__":
    main()
