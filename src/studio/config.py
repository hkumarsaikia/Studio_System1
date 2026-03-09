import os
from pathlib import Path

# --- CORE DIRECTORY PATHS ---
# Natively calculate all paths relative to the root of the Git repo
# so there are zero hardcoded paths in the application.

# src/studio/config.py
STUDIO_DIR = Path(__file__).resolve().parent
SRC_DIR = STUDIO_DIR.parent
ROOT_DIR = SRC_DIR.parent

DATA_DIR = ROOT_DIR / "data"
VIDEOS_DIR = DATA_DIR / "videos"
STORYBOARDS_DIR = DATA_DIR / "storyboards"
DEMOS_DIR = DATA_DIR / "demos"
ARCHIVE_DIR = DATA_DIR / "archive"
KNOWLEDGE_GRAPH_DIR = DATA_DIR / "knowledge-graph"
ASSETS_DIR = DATA_DIR / "assets"
RAW_ASSETS_DIR = ASSETS_DIR / "raw"
PROCESSED_ASSETS_DIR = ASSETS_DIR / "processed"

ENGINE_DIR = ROOT_DIR / "engine"
PRESETS_DIR = ROOT_DIR / "presets"
LOGS_DIR = ROOT_DIR / "logs"
OUTPUT_DIR = ROOT_DIR / "output"
SEGMENTS_OUTPUT_DIR = OUTPUT_DIR / "segments"
METADATA_OUTPUT_DIR = OUTPUT_DIR / "metadata"

# Define important asset output constants
REACT_COMPONENTS_DIR = ENGINE_DIR / "src" / "components" / "generated"

# File Constants
TOPICS_FILE = DATA_DIR / 'raw' / 'Topics.txt'
TOPIC_CATALOG_FILE = DATA_DIR / 'topic_catalog.json'
REPRESENTATIVE_TOPICS_FILE = DATA_DIR / 'representative_topics.json'
RENDER_PROFILES_FILE = DATA_DIR / 'render_profiles.json'
SCENE_GRAMMAR_FILE = DATA_DIR / 'scene_grammar_registry.json'
ASSET_REGISTRY_FILE = DATA_DIR / 'asset_registry.json'
ASSET_COVERAGE_FILE = DATA_DIR / 'asset_coverage.json'

def ensure_directories():
    """Ensure that all data directories exist on startup."""
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    STORYBOARDS_DIR.mkdir(parents=True, exist_ok=True)
    DEMOS_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    RAW_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    REACT_COMPONENTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SEGMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
