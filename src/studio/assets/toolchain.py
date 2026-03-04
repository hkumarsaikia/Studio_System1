import os
import shutil
import subprocess

from src.studio.assets.transpiler import transpile_to_react
from src.studio.assets.character_builder import build_character
from src.studio.assets.background_builder import build_background
from src.studio.assets.props_builder import build_prop
from src.studio.assets.declarative_builder import build_declarative_prop
from src.studio.config import RAW_ASSETS_DIR, PROCESSED_ASSETS_DIR, REACT_COMPONENTS_DIR, ensure_directories

def find_inkscape():
    """Locate the Inkscape executable on Windows."""
    ink_path = shutil.which("inkscape")
    if ink_path:
        return ink_path
    
    fallbacks = [
        r"C:\Program Files\Inkscape\bin\inkscape.exe",
        r"C:\Program Files\Inkscape\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\inkscape.exe"
    ]
    for path in fallbacks:
        if os.path.exists(path):
            return path
            
    raise RuntimeError("Inkscape executable not found. Please ensure Inkscape is installed.")

def process_svg(input_path: str, output_path: str, optimize=True, open_gui=True):
    """
    Run an SVG through Inkscape's command line to normalize it,
    then optionally run SVGO to optimize it.
    Can also launch the Inkscape GUI for user review.
    """
    inkscape_exe = find_inkscape()
    
    print(f"[{os.path.basename(__file__)}] Processing {os.path.basename(input_path)} via Inkscape CLI...")
    
    # 1. Background processing (text-to-path, plain SVG export)
    cmd = [
        inkscape_exe,
        input_path,
        f"--export-filename={output_path}",
        "--export-plain-svg",
        "--export-text-to-path"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Inkscape Error: {result.stderr}")
        raise RuntimeError("Inkscape processing failed.")
        
    # 2. SVGO Optimization
    if optimize:
        print(f"[{os.path.basename(__file__)}] Optimizing via SVGO...")
        svgo_cmd = ["npx", "svgo", output_path, "--multipass"]
        if shutil.which("npx"):
            subprocess.run(svgo_cmd, capture_output=True, shell=True)
        else:
            print("npx not found, skipping SVGO optimization.")
            
    print(f"[{os.path.basename(__file__)}] Successfully built: {output_path}")

    # 3. GUI Launch
    if open_gui:
        print(f"[{os.path.basename(__file__)}] Launching Inkscape GUI for {os.path.basename(output_path)}...")
        # We use subprocess.Popen so we don't block the Python script while Inkscape is open
        subprocess.Popen([inkscape_exe, output_path])

def main():
    print("="*60)
    print(" Studio System — Asset Compilation Pipeline")
    print("="*60)
    
    # 1. Define Paths & Ensure Exists
    ensure_directories()
    raw_dir = str(RAW_ASSETS_DIR)
    processed_dir = str(PROCESSED_ASSETS_DIR)
    react_out_dir = str(REACT_COMPONENTS_DIR)
    
    # 2. Generate Graphics as Code (Raw XML)
    print("\n[1/3] Generating Raw SVGs via Python Builders...")
    
    char_a_raw = os.path.join(raw_dir, "CharacterGeek.svg")
    char_b_raw = os.path.join(raw_dir, "CharacterAngry.svg")
    bg_sunset_raw = os.path.join(raw_dir, "BackgroundSunset.svg")
    prop_server_raw = os.path.join(raw_dir, "PropServer.svg")
    prop_telescope_raw = os.path.join(raw_dir, "PropTelescope.svg")
    prop_declarative_robot_raw = os.path.join(raw_dir, "PropDeclarativeRobot.svg")
    prop_declarative_saturn_raw = os.path.join(raw_dir, "PropDeclarativeSaturn.svg")
    
    build_character(char_a_raw, skin_index=1, shirt_index=0, mood="happy", accessory="glasses", hair="spiky")
    build_character(char_b_raw, skin_index=4, shirt_index=3, mood="angry", hair="long")
    build_background(bg_sunset_raw, palette="sunset")
    build_prop(prop_server_raw, prop_type="server_rack", accent_index=2)
    build_prop(prop_telescope_raw, prop_type="telescope", accent_index=1)
    
    # NEW: Declarative Geometry Builders
    build_declarative_prop(prop_declarative_robot_raw, prop_type="Robot")
    build_declarative_prop(prop_declarative_saturn_raw, prop_type="Saturn")
    
    # 3. Process via Inkscape CLI
    print("\n[2/3] Processing SVGs via Inkscape CLI...")
    
    char_a_proc = os.path.join(processed_dir, "CharacterGeek.svg")
    char_b_proc = os.path.join(processed_dir, "CharacterAngry.svg")
    bg_sunset_proc = os.path.join(processed_dir, "BackgroundSunset.svg")
    prop_server_proc = os.path.join(processed_dir, "PropServer.svg")
    prop_telescope_proc = os.path.join(processed_dir, "PropTelescope.svg")
    prop_robot_proc = os.path.join(processed_dir, "PropDeclarativeRobot.svg")
    prop_saturn_proc = os.path.join(processed_dir, "PropDeclarativeSaturn.svg")
    
    process_svg(char_a_raw, char_a_proc, optimize=True, open_gui=False)
    process_svg(char_b_raw, char_b_proc, optimize=True, open_gui=False)
    process_svg(bg_sunset_raw, bg_sunset_proc, optimize=True, open_gui=False)
    process_svg(prop_server_raw, prop_server_proc, optimize=True, open_gui=False)
    process_svg(prop_telescope_raw, prop_telescope_proc, optimize=True, open_gui=False)
    process_svg(prop_declarative_robot_raw, prop_robot_proc, optimize=True, open_gui=False) 
    process_svg(prop_declarative_saturn_raw, prop_saturn_proc, optimize=True, open_gui=False) 
    
    # 4. Transpile to React
    print("\n[3/3] Transpiling to React Components...")
    
    transpile_to_react(char_a_proc, "CharacterGeek", react_out_dir)
    transpile_to_react(char_b_proc, "CharacterAngry", react_out_dir)
    transpile_to_react(bg_sunset_proc, "BackgroundSunset", react_out_dir)
    transpile_to_react(prop_server_proc, "PropServer", react_out_dir)
    transpile_to_react(prop_telescope_proc, "PropTelescope", react_out_dir)
    transpile_to_react(prop_robot_proc, "PropDeclarativeRobot", react_out_dir)
    transpile_to_react(prop_saturn_proc, "PropDeclarativeSaturn", react_out_dir)
    
    print("\n[DONE] Asset Pipeline Complete!")
    print(f"Components ready in: {react_out_dir}")

if __name__ == "__main__":
    main()
