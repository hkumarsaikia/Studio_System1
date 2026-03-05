import os
from src.studio.assets.styles.theme_loader import THEME

def build_prop(output_path, prop_type="server_rack", accent_index=0):
    """
    Programmatic Props Design System.
    Generates various objects in the minimalist style.
    """
    colors = THEME["colors"]
    accent = colors["clothingPrimary"][accent_index % len(colors["clothingPrimary"])]
    stroke = colors["darkOutline"]
    stroke_w = THEME["dimensions"]["strokeWidth"]
    
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400">
    <g id="PropGroup">
"""

    if prop_type == "server_rack":
        # A minimalist style server rack with glowing lights
        svg_content += f"""
        <!-- Base Cabinet -->
        <rect x="40" y="50" width="120" height="300" rx="10" fill="#334155" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <!-- Shadow -->
        <rect x="50" y="60" width="100" height="280" rx="5" fill="#1e293b"/>
        
        <!-- Server Units -->
        <rect x="55" y="70" width="90" height="40" rx="3" fill="#cbd5e1" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <rect x="55" y="120" width="90" height="40" rx="3" fill="#cbd5e1" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <rect x="55" y="170" width="90" height="40" rx="3" fill="#cbd5e1" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <rect x="55" y="220" width="90" height="40" rx="3" fill="#cbd5e1" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <rect x="55" y="270" width="90" height="40" rx="3" fill="#cbd5e1" stroke="{stroke}" stroke-width="{stroke_w}"/>
        
        <!-- Blinking Lights -->
        <circle cx="70" cy="90" r="5" fill="{accent}"/>
        <circle cx="90" cy="90" r="5" fill="#ef4444"/>
        
        <circle cx="70" cy="140" r="5" fill="{accent}"/>
        <circle cx="90" cy="140" r="5" fill="{accent}"/>
        
        <circle cx="70" cy="190" r="5" fill="#f59e0b"/>
        <circle cx="90" cy="190" r="5" fill="{accent}"/>
        
        <circle cx="70" cy="240" r="5" fill="{accent}"/>
        <circle cx="90" cy="240" r="5" fill="{accent}"/>
        
        <circle cx="70" cy="290" r="5" fill="{accent}"/>
        <circle cx="90" cy="290" r="5" fill="#ef4444"/>
"""
    elif prop_type == "telescope":
        svg_content += f"""
        <!-- Telescope Mount -->
        <path d="M 80 250 L 50 380 L 70 380 L 90 250 Z" fill="#64748b" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <path d="M 120 250 L 150 380 L 130 380 L 110 250 Z" fill="#64748b" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <circle cx="100" cy="250" r="20" fill="#334155" stroke="{stroke}" stroke-width="{stroke_w}"/>
        
        <!-- Telescope Body (Angled) -->
        <g transform="rotate(-30 100 250)">
            <rect x="60" y="100" width="80" height="200" rx="10" fill="#cbd5e1" stroke="{stroke}" stroke-width="{stroke_w}"/>
            <rect x="65" y="110" width="70" height="180" rx="5" fill="#f8fafc"/>
            
            <!-- Accents -->
            <rect x="60" y="130" width="80" height="20" fill="{accent}" stroke="{stroke}" stroke-width="{stroke_w}"/>
            <rect x="60" y="240" width="80" height="20" fill="{accent}" stroke="{stroke}" stroke-width="{stroke_w}"/>
            
            <!-- Lens -->
            <ellipse cx="100" cy="100" rx="40" ry="10" fill="#0ea5e9" stroke="{stroke}" stroke-width="{stroke_w}"/>
            <ellipse cx="100" cy="100" rx="20" ry="5" fill="#bae6fd"/>
            
            <!-- Eyepiece -->
            <rect x="85" y="300" width="30" height="20" rx="3" fill="#334155" stroke="{stroke}" stroke-width="{stroke_w}"/>
            <circle cx="100" cy="320" r="10" fill="#0ea5e9" stroke="{stroke}" stroke-width="{stroke_w}"/>
        </g>
"""

    svg_content += """
    </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(svg_content)
    print(f"[{os.path.basename(__file__)}] Generated raw prop SVG: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw", "TestProp.svg")
    build_prop(out)
