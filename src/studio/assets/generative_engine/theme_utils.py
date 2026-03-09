"""
FILE: src/studio/assets/generative_engine/theme_utils.py
PURPOSE: Utility functions to expose Studio System theme colors
for procedural SVGs.
"""

from src.studio.assets.styles.theme_loader import THEME

def get_accent(index: int) -> str:
    """Get an accent color from the clothingPrimary array."""
    colors = THEME["colors"]["clothingPrimary"]
    return colors[index % len(colors)]

def get_stroke() -> str:
    """Get the standard dark outline color."""
    return THEME["colors"]["darkOutline"]

def get_stroke_width() -> int:
    """Get the standard stroke width."""
    return THEME["dimensions"]["strokeWidth"]

def get_bg_gradient_stops() -> tuple[str, str]:
    """Get the standard background dark gradient."""
    return ("#334155", "#0f172a")

def get_canvas_size() -> tuple[int, int]:
    """Get the standard generative canvas size."""
    return (800, 800)
