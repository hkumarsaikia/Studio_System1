import os
import subprocess
from pathlib import Path

# --- Configuration ---
# Calculates the absolute path of the Studio_System folder 
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- Helper Function ---
def get_commented_content(file_path, description):
    """Wraps the description in the correct comment syntax based on file type."""
    ext = Path(file_path).suffix
    if ext in ['.js', '.jsx', '.css']:
        return f"/*\n * FILE: {Path(file_path).name}\n * DESCRIPTION: {description}\n */\n"
    elif ext in ['.py', '.yml', '.env']:
        return f"# FILE: {Path(file_path).name}\n# DESCRIPTION: {description}\n"
    elif ext == '.json':
        return f'{{\n  "_file": "{Path(file_path).name}",\n  "_description": "{description}"\n}}\n'
    else:
        return f"# {Path(file_path).name}\n\n{description}\n"

def create_file(relative_path, description):
    """Creates a file and its parent directories, then writes the description."""
    file_path = ROOT_DIR / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = get_commented_content(relative_path, description)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created/Updated: {relative_path}")

# --- File Contents Definition ---
# Dictionary mapping file paths to their descriptions.

FILE_DESCRIPTIONS = {
    # ROOT DOCS & CI
    ".env": "Environment configuration. Add API keys here.",
    ".github/workflows/render.yml": "GitHub Actions auto-render pipeline.",
    "README.md": "Professional documentation. Explains how to use the Studio System.",
    "ARCHITECTURE.md": "System explanation. Details the architecture, components, and data flow.",
    ".gitignore": "Specifies intentionally untracked files to ignore.",

    # AUTOMATION
    "automation/metadata_generator.py": "Generates SEO-optimized titles, descriptions, and tags for YouTube uploads.",
    "automation/thumbnail_template.jsx": "Specifically designed React component to render YouTube thumbnails.",
    "automation/clean_output.py": "Auto-clean output folder to save disk space before a new batch.",
    "automation/render.py": "Main orchestration script to trigger headless renders.",
    "automation/export_thumbnail.py": "Extracts high-quality PNG thumbnails from the rendered timeline.",

    # DATA & PRESETS
    "data/schema.json": "JSON validation schema for incoming video configurations.",
    "data/video_001.json": "Data file for video 1 containing scenes, text overlays, and audio paths.",
    "data/video_002.json": "Data file for video 2 containing scenes, text overlays, and audio paths.",
    "presets/youtube_2k.json": "Configuration preset for horizontal 2K rendering.",
    "presets/shorts_vertical.json": "Configuration preset for vertical Shorts rendering.",

    # ENGINE CONFIGURATIONS
    "engine/package.json": "Node.js dependencies, package definitions, and project scripts.",
    "engine/remotion.config.js": "Advanced render configuration for headless Chromium.",
    
    # ENGINE CORE FILES
    "engine/src/index.js": "Main entry point for the Remotion Engine.",
    "engine/src/Root.jsx": "Universal Root Loader that sets up the main composition.",
    "engine/src/core/TemplateLoader.jsx": "Dynamically loads template based on JSON.",
    "engine/src/core/SceneManager.jsx": "Orchestrates the timeline and maps over the scenes array.",
    "engine/src/core/Camera.jsx": "Wraps children in a cinematic zoom/pan effect.",
    "engine/src/core/MotionLayer.jsx": "Wraps components in cinematic motion blur.",

    # ENGINE UTILS
    "engine/src/utils/audioSync.js": "Scene audio alignment. Calculates exact frame offsets.",
    "engine/src/utils/dataParser.js": "Normalize input data. Ensures fallback values exist.",
    "engine/src/utils/propsValidator.js": "Validate scene props inside React before rendering.",
    "engine/src/utils/sceneTiming.js": "Central timing logic. Standardizes 10-second scenes at 30fps.",
    "engine/src/utils/sceneTransitions.js": "Standardized interpolation curves for smooth crossfades between scenes.",

    # ENGINE STYLES
    "engine/src/styles/global.css": "Global design system. Defines base CSS and fonts.",
    "engine/src/styles/theme.js": "Brand color system. Centralized color tokens.",
    "engine/src/styles/typography.js": "Typography scale. Centralized font sizes.",

    # ENGINE COMPONENTS & OVERLAYS
    "engine/src/components/Background.jsx": "Universal background component.",
    "engine/src/components/SceneAudio.jsx": "Wraps Remotion's Audio tag to safely handle missing files.",
    "engine/src/components/Person.jsx": "Modular SVG Vector Person component.",
    "engine/src/components/Crowd.jsx": "Procedural Crowd Generator component.",
    "engine/src/overlays/CinematicText.jsx": "Cinematic text overlay with animations.",

    # ENGINE SCENES
    "engine/src/scenes/GenericScene.jsx": "Universal Fallback Scene renderer.",
    "engine/src/scenes/SceneBlock.jsx": "Universal 10s scene renderer. Assembles background, audio, text, and vector actions.",
    "engine/src/scenes/SceneFactory.jsx": "Creates scenes from JSON type. Routes to specific scene blocks.",

    # ENGINE TEMPLATES
    "engine/src/templates/ProtestCinematic.jsx": "Protest style cinematic template.",
    "engine/src/templates/ExplainerCinematic.jsx": "Explainer style template.",
    "engine/src/templates/ShortsVertical.jsx": "Vertical Shorts template.",
    "engine/src/templates/DataInfographic.jsx": "Data visualization template."
}

# --- Empty Directories to ensure existence ---
EMPTY_DIRECTORIES = [
    "output/logs",         # Render logs storage
    "engine/public/music", # Background music storage
    "engine/public/audio"  # Voiceover audio storage
]

def build_architecture():
    print(f"\n🚀 Initiating Studio Architecture Build in: {ROOT_DIR}\n")
    
    # 1. Create Directories
    for d in EMPTY_DIRECTORIES:
        dir_path = ROOT_DIR / d
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create a .gitkeep so git tracks the empty folder
        (dir_path / ".gitkeep").touch()
        print(f"📁 Created Directory: {d}")
        
    print("-" * 40)
    
    # 2. Create Files with Descriptions
    for relative_path, description in FILE_DESCRIPTIONS.items():
        create_file(relative_path, description)
        
    print("\n✅ Build Complete! All descriptive files generated successfully.")

def push_to_github():
    print("\n🔄 Syncing updates to GitHub...")
    try:
        # Check if git is initialized
        if not (ROOT_DIR / ".git").exists():
            subprocess.run(["git", "init"], cwd=ROOT_DIR, check=True)
            print("Initialized empty Git repository.")

        # Add, Commit, Push
        subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Architectural Update: Generated File Descriptions"], cwd=ROOT_DIR)
        
        result = subprocess.run(["git", "push"], cwd=ROOT_DIR, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Successfully pushed to GitHub!")
        else:
            print("⚠️ Committed locally, but couldn't push. (No remote set up or authentication needed).")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git operation failed. Error: {e}")
    except FileNotFoundError:
        print("⚠️ Git is not installed or not found in PATH.")

if __name__ == "__main__":
    build_architecture()
    push_to_github()