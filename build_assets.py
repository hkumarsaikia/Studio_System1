import os
import argparse
from assets.toolchain import process_svg
from assets.react_transpiler import transpile_to_react
from assets.src.character_builder import build_character
from assets.src.background_builder import build_background
from assets.src.props_builder import build_prop
from assets.src.declarative_builder import build_declarative_prop

def main():
    print("="*60)
    print(" Studio System — Asset Compilation Pipeline")
    print("="*60)
    
    # 1. Define Paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(root_dir, "assets", "raw")
    processed_dir = os.path.join(root_dir, "assets", "processed")
    react_out_dir = os.path.join(root_dir, "engine", "src", "components", "generated")
    
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(react_out_dir, exist_ok=True)
    
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
    
    process_svg(char_a_raw, char_a_proc, optimize=True)
    process_svg(char_b_raw, char_b_proc, optimize=True)
    process_svg(bg_sunset_raw, bg_sunset_proc, optimize=True)
    process_svg(prop_server_raw, prop_server_proc, optimize=True)
    process_svg(prop_telescope_raw, prop_telescope_proc, optimize=True, open_gui=False) # Skip telescope to avoid too many windows
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
