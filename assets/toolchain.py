import os
import shutil
import subprocess

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
