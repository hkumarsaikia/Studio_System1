from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.studio.assets.catalog import asset_catalog_entry, canonical_asset_id, list_catalog_asset_ids
from src.studio.assets.toolchain import ASSET_SPECS
from src.studio.config import ASSET_REGISTRY_FILE, DATA_DIR, PROCESSED_ASSETS_DIR, RAW_ASSETS_DIR, REACT_COMPONENTS_DIR
from src.studio.contracts import CATEGORY_ASSET_TAGS

ASSET_LIBRARY_PATH = DATA_DIR / 'asset_library.json'


def _relative(path: Path) -> str:
    return path.relative_to(DATA_DIR.parent).as_posix()


def _paths_for_component(component_name: str) -> tuple[Path, Path, Path]:
    raw_path = RAW_ASSETS_DIR / f'{component_name}.svg'
    processed_path = PROCESSED_ASSETS_DIR / f'{component_name}.svg'
    generated_path = REACT_COMPONENTS_DIR / f'{component_name}.tsx'
    return raw_path, processed_path, generated_path


def _status(raw_path: Path, processed_path: Path, generated_path: Path) -> str:
    return 'ready' if raw_path.exists() and processed_path.exists() and generated_path.exists() else 'missing'


def _catalog_svg_component_entry(asset_id: str) -> dict[str, Any]:
    catalog_entry = asset_catalog_entry(asset_id)
    component_name = str(catalog_entry['componentName'])
    raw_path, processed_path, generated_path = _paths_for_component(component_name)
    return {
        'id': asset_id,
        'sourceType': 'svg_component',
        'family': catalog_entry['family'],
        'tags': list(catalog_entry['tags']),
        'allowedSceneRoles': list(catalog_entry['allowedSceneRoles']),
        'renderTarget': 'GeneratedReactComponent',
        'svgSource': _relative(raw_path),
        'processedSvg': _relative(processed_path),
        'generatedComponent': _relative(generated_path),
        'status': _status(raw_path, processed_path, generated_path),
        'aliases': list(catalog_entry['aliases']),
        'componentName': component_name,
        'catalogKind': catalog_entry['catalogKind'],
        'styleVariant': catalog_entry['styleVariant'],
    }


def _generated_component_entry(component_name: str) -> dict[str, Any]:
    raw_path, processed_path, generated_path = _paths_for_component(component_name)
    return {
        'id': component_name,
        'sourceType': 'svg_component',
        'family': 'generatedComponents',
        'tags': ['generated', 'svg', 'component'],
        'allowedSceneRoles': ['hook', 'real_world_example', 'takeaway'],
        'renderTarget': 'GeneratedReactComponent',
        'svgSource': _relative(raw_path),
        'processedSvg': _relative(processed_path),
        'generatedComponent': _relative(generated_path),
        'status': _status(raw_path, processed_path, generated_path),
        'aliases': [],
        'componentName': component_name,
        'catalogKind': 'generated',
        'styleVariant': 'illustration',
    }


def build_asset_registry() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}

    for asset_id in list_catalog_asset_ids(include_compatibility=True):
        registry[asset_id] = _catalog_svg_component_entry(asset_id)

    for spec in ASSET_SPECS:
        if spec.asset_id:
            continue
        registry[spec.component_name] = _generated_component_entry(spec.component_name)

    for category, asset_ids in CATEGORY_ASSET_TAGS.items():
        category_tag = category.lower().replace(' & ', '_').replace(' ', '_')
        for asset_id in asset_ids:
            resolved = canonical_asset_id(asset_id)
            if resolved in registry:
                tags = list(registry[resolved]['tags'])
                registry[resolved]['tags'] = sorted(set(tags + [category_tag]))

    return dict(sorted(registry.items()))


def build_asset_library_summary(asset_registry: dict[str, dict[str, Any]] | None = None) -> dict[str, list[str]]:
    registry = asset_registry or build_asset_registry()
    summary: dict[str, list[str]] = {}
    for asset_id, entry in registry.items():
        family = str(entry['family'])
        summary.setdefault(family, []).append(asset_id)
    return {family: sorted(asset_ids) for family, asset_ids in sorted(summary.items())}


def write_asset_registry_files() -> dict[str, dict[str, Any]]:
    registry = build_asset_registry()
    ASSET_REGISTRY_FILE.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    ASSET_LIBRARY_PATH.write_text(json.dumps(build_asset_library_summary(registry), indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return registry
