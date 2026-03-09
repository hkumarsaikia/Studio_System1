"""
FILE: src/studio/assets/generative_engine/arrows_flow.py
PURPOSE: Procedural geometry builders for Arrows & Flow Indicators.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

def _draw_fat_arrow(canvas: ProceduralCanvas, x: int, y: int, rotation: int, color: str):
    # Base arrow pointing up before rotation
    d = "M 350 600 L 450 600 L 450 350 L 550 350 L 400 150 L 250 350 L 350 350 Z"
    canvas.dwg.add(canvas.dwg.path(d=d, fill=color, transform=f"rotate({rotation} 400 400)"))

def build_arrow_up(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    _draw_fat_arrow(canvas, 400, 400, 0, get_accent(0))
    canvas.save()

def build_arrow_down(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1), add_glow=False)
    _draw_fat_arrow(canvas, 400, 400, 180, get_accent(1))
    canvas.save()

def build_arrow_left(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2), add_glow=False)
    _draw_fat_arrow(canvas, 400, 400, -90, get_accent(2))
    canvas.save()

def build_arrow_right(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3), add_glow=False)
    _draw_fat_arrow(canvas, 400, 400, 90, get_accent(3))
    canvas.save()

def build_curved_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4), add_glow=False)
    canvas.draw_primitive_path("M 200 600 Q 200 300 500 300 M 500 300 L 450 250 M 500 300 L 450 350", fill="none", stroke=get_accent(4), stroke_width=40)
    canvas.save()

def build_loop_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5), add_glow=False)
    # Circle almost closing
    canvas.draw_primitive_path("M 400 200 A 200 200 0 1 1 250 250", fill="none", stroke=get_accent(5), stroke_width=40)
    # Arrow head
    canvas.draw_primitive_path("M 250 250 L 200 250 M 250 250 L 250 300", fill="none", stroke=get_accent(5), stroke_width=40)
    canvas.save()

def build_cycle_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    # Three arrows forming a circle (recycle style)
    for rot in [0, 120, 240]:
        canvas.dwg.add(canvas.dwg.path("M 400 150 A 250 250 0 0 1 600 250 L 550 220 M 600 250 L 630 200", fill="none", stroke=get_accent(0), stroke_width=25, transform=f"rotate({rot} 400 400)"))
    canvas.save()

def build_double_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1), add_glow=False)
    canvas.draw_primitive_path("M 200 400 L 600 400", stroke=get_accent(1), stroke_width=40)
    canvas.draw_primitive_path("M 200 400 L 250 350 M 200 400 L 250 450", fill="none", stroke=get_accent(1), stroke_width=40)
    canvas.draw_primitive_path("M 600 400 L 550 350 M 600 400 L 550 450", fill="none", stroke=get_accent(1), stroke_width=40)
    canvas.save()

def build_flow_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2), add_glow=False)
    canvas.draw_primitive_path("M 150 400 L 650 400 M 650 400 L 550 300 M 650 400 L 550 500", fill="none", stroke="#38bdf8", stroke_width=80, stroke_linejoin="miter", stroke_linecap="butt")
    canvas.save()

def build_timeline_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3), add_glow=False)
    canvas.draw_primitive_path("M 150 400 L 650 400 M 650 400 L 550 350 M 650 400 L 550 450", fill="none", stroke="#475569", stroke_width=30)
    # Timeline nodes
    for x in [250, 400, 550]:
        canvas.draw_primitive_circle(x, 400, 20, fill="#fcd34d", stroke="#fff", stroke_width=4)
    canvas.save()

def build_process_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4), add_glow=False)
    # Chevron style segments
    d1 = "M 150 300 L 350 300 L 450 400 L 350 500 L 150 500 L 250 400 Z"
    d2 = "M 400 300 L 600 300 L 700 400 L 600 500 L 400 500 L 500 400 Z"
    canvas.draw_primitive_path(d1, fill="#1e293b", stroke=get_accent(4), stroke_width=8)
    canvas.draw_primitive_path(d2, fill="#1e293b", stroke=get_accent(4), stroke_width=8)
    canvas.save()

def build_cause_effect_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5), add_glow=False)
    # Huge thick arrow hitting a wall
    canvas.draw_primitive_path("M 150 400 Q 300 200 550 400", fill="none", stroke="#ef4444", stroke_width=30)
    canvas.draw_primitive_path("M 550 400 L 480 380 M 550 400 L 530 330", fill="none", stroke="#ef4444", stroke_width=30)
    # Impact explosion
    for rot in range(0, 360, 45):
        canvas.dwg.add(canvas.dwg.line(start=(570, 400), end=(610, 400), stroke="#fcd34d", stroke_width=8, stroke_linecap="round", transform=f"rotate({rot} 550 400)"))
    canvas.save()
