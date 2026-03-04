import os
from src.studio.assets.styles.theme_loader import THEME

def build_character(output_path, skin_index=0, shirt_index=0, mood="happy", accessory="none", hair="short"):
    """
    Expanded Programmatic Character Design System.
    Builds a vector graphic by composing XML strings (Graphics as Code).
    """
    colors = THEME["colors"]
    skin = colors["skinVariations"][skin_index % len(colors["skinVariations"])]
    shirt = colors["clothingPrimary"][shirt_index % len(colors["clothingPrimary"])]
    hair_color = colors["hairColors"][skin_index % len(colors["hairColors"])] # tie hair to skin for now
    stroke = colors["darkOutline"]
    stroke_w = THEME["dimensions"]["strokeWidth"]
    
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400">
    <g id="CharacterGroup">
        <!-- Body -->
        <rect x="70" y="150" width="60" height="120" rx="30" fill="{shirt}" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <!-- Dynamic Belt -->
        <rect x="70" y="240" width="60" height="10" fill="#1e293b"/>
        
        <!-- Arms -->
        <path d="M70,180 C40,200 40,250 50,280" fill="none" stroke="{shirt}" stroke-width="20" stroke-linecap="round"/>
        <path d="M130,180 C160,200 160,250 150,280" fill="none" stroke="{shirt}" stroke-width="20" stroke-linecap="round"/>
        
        <!-- Hands -->
        <circle cx="50" cy="280" r="15" fill="{skin}" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <circle cx="150" cy="280" r="15" fill="{skin}" stroke="{stroke}" stroke-width="{stroke_w}"/>
        
        <!-- Legs -->
        <rect x="80" y="270" width="15" height="100" rx="7.5" fill="{skin}" stroke="{stroke}" stroke-width="{stroke_w}"/>
        <rect x="105" y="270" width="15" height="100" rx="7.5" fill="{skin}" stroke="{stroke}" stroke-width="{stroke_w}"/>
        
        <!-- Feet -->
        <path d="M70,370 L95,370 C95,360 85,355 70,360 Z" fill="#2d2d2d"/>
        <path d="M105,370 L130,370 C130,360 120,355 105,360 Z" fill="#2d2d2d"/>
        
        <!-- Head -->
        <circle cx="100" cy="100" r="45" fill="{skin}" stroke="{stroke}" stroke-width="{stroke_w}"/>
"""

    if hair == "short":
        svg_content += f"""
        <!-- Hair Short -->
        <path d="M 55 100 A 45 45 0 0 1 145 100 C 145 70 120 45 100 45 C 80 45 55 70 55 100 Z" fill="{hair_color}" stroke="{stroke}" stroke-width="{stroke_w}"/>
"""
    elif hair == "long":
        svg_content += f"""
        <!-- Hair Long -->
        <path d="M 55 100 A 45 45 0 0 1 145 100 L 150 160 C 120 180 80 180 50 160 Z" fill="{hair_color}" stroke="{stroke}" stroke-width="{stroke_w}"/>
"""
    elif hair == "spiky":
        svg_content += f"""
        <!-- Hair Spiky -->
        <path d="M 55 90 L 60 50 L 75 70 L 90 30 L 110 70 L 125 40 L 140 80 A 45 45 0 0 0 55 90 Z" fill="{hair_color}" stroke="{stroke}" stroke-width="{stroke_w}"/>
"""

    # Expressions
    if mood == "happy":
        svg_content += f"""
        <!-- Eyes -->
        <path d="M85,95 Q90,85 95,95" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
        <path d="M105,95 Q110,85 115,95" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
        <!-- Mouth -->
        <path d="M90,115 Q100,130 110,115" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
"""
    elif mood == "sad":
        svg_content += f"""
        <!-- Eyes -->
        <circle cx="85" cy="95" r="3" fill="#000"/>
        <circle cx="115" cy="95" r="3" fill="#000"/>
        <!-- Mouth -->
        <path d="M90,120 Q100,110 110,120" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
"""
    elif mood == "surprised":
        svg_content += f"""
        <!-- Eyes -->
        <circle cx="85" cy="95" r="5" fill="#000"/>
        <circle cx="115" cy="95" r="5" fill="#000"/>
        <!-- Mouth -->
        <circle cx="100" cy="120" r="8" fill="#000"/>
"""
    elif mood == "angry":
        svg_content += f"""
        <!-- Eyes -->
        <line x1="80" y1="90" x2="95" y2="95" stroke="#000" stroke-width="3" stroke-linecap="round"/>
        <circle cx="88" cy="100" r="3" fill="#000"/>
        <line x1="120" y1="90" x2="105" y2="95" stroke="#000" stroke-width="3" stroke-linecap="round"/>
        <circle cx="112" cy="100" r="3" fill="#000"/>
        <!-- Mouth -->
        <path d="M90,120 L110,120" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
"""

    # Accessories
    if accessory == "glasses":
        svg_content += f"""
        <!-- Glasses -->
        <rect x="75" y="85" width="20" height="15" rx="3" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="105" y="85" width="20" height="15" rx="3" fill="none" stroke="#000" stroke-width="3"/>
        <line x1="95" y1="92" x2="105" y2="92" stroke="#000" stroke-width="2"/>
        <line x1="75" y1="92" x2="55" y2="92" stroke="#000" stroke-width="2"/>
        <line x1="125" y1="92" x2="145" y2="92" stroke="#000" stroke-width="2"/>
"""

    svg_content += """
    </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(svg_content)
    print(f"[{os.path.basename(__file__)}] Generated raw character SVG: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw", "TestCharacter.svg")
    build_character(out)
