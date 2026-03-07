from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from src.studio.config import DATA_DIR

SCHEMA_FILE_MAP = {
    'storyboard': DATA_DIR / 'storyboard.schema.json',
    'video': DATA_DIR / 'video.schema.json',
    'production_manifest': DATA_DIR / 'production-manifest.schema.json',
    'demo_manifest': DATA_DIR / 'demo-manifest.schema.json',
}


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = SCHEMA_FILE_MAP[schema_name]
    return json.loads(schema_path.read_text(encoding='utf-8'))


@lru_cache(maxsize=None)
def get_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def validate_with_schema(data: Any, schema_name: str, context: str) -> None:
    validator = get_validator(schema_name)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    if not errors:
        return

    formatted: list[str] = []
    for error in errors[:10]:
        location = '.'.join(str(part) for part in error.absolute_path) or '<root>'
        formatted.append(f'{context}: {location}: {error.message}')

    if len(errors) > 10:
        formatted.append(f'{context}: ... {len(errors) - 10} additional schema errors suppressed')

    raise ValueError('\n'.join(formatted))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))
