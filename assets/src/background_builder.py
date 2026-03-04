import os
from assets.styles.theme_loader import THEME

def build_background(output_path, palette="cyber"):
    """
    Programmatic Background Design System.
    Builds a vector graphic backdrop (Graphics as Code).
    """
    # Define some palettes programmatically based on the theme
    bg_color = "#0f172a"
    grid_color = "#1e293b"
    accent = "#38bdf8"
    
    if palette == "sunset":
        bg_color = "#4c1d95"
        grid_color = "#7c3aed"
        accent = "#f472b6"
    elif palette == "neon":
        bg_color = "#020617"
        grid_color = "#0f766e"
        accent = "#22d3ee"

    stroke_w = THEME["dimensions"]["strokeWidth"]
    
    # SVG Assembly
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">
    <!-- Base Canvas -->
    <rect width="1920" height="1080" fill="{bg_color}"/>
    
    <!-- Horizon Glow -->
    <ellipse cx="960" cy="800" rx="1200" ry="400" fill="{accent}" opacity="0.15" filter="blur(100px)"/>
    
    <!-- Deep Grid -->
    <g stroke="{grid_color}" stroke-width="{stroke_w}" opacity="0.6">
        <!-- Horizontals -->
        <line x1="0" y1="500" x2="1920" y2="500"/>
        <line x1="0" y1="650" x2="1920" y2="650"/>
        <line x1="0" y1="850" x2="1920" y2="850"/>
        <line x1="0" y1="1080" x2="1920" y2="1080"/>
        
        <!-- Perspective Verticals -->
        <line x1="960" y1="400" x2="960" y2="1080"/>
        <line x1="960" y1="400" x2="500" y2="1080"/>
        <line x1="960" y1="400" x2="100" y2="1080"/>
        <line x1="960" y1="400" x2="-400" y2="1080"/>
        <line x1="960" y1="400" x2="1420" y2="1080"/>
        <line x1="960" y1="400" x2="1820" y2="1080"/>
        <line x1="960" y1="400" x2="2320" y2="1080"/>
    </g>
    
    <!-- Abstract Geometry overlay -->
    <circle cx="960" cy="300" r="150" fill="none" stroke="{accent}" stroke-width="4" opacity="0.8" stroke-dasharray="10 20"/>
    <circle cx="960" cy="300" r="180" fill="none" stroke="{accent}" stroke-width="1" opacity="0.4"/>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(svg_content)
    print(f"[{os.path.basename(__file__)}] Generated raw background SVG: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw", "TestBackground.svg")
    build_background(out)
