"""
FILE: src/studio/assets/generative_engine/buildings_infra.py
PURPOSE: Procedural geometry builders for Buildings & Infrastructure.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

def _draw_building_base(canvas: ProceduralCanvas, x: int, y: int, w: int, h: int, color: str, draw_windows: bool = True, window_cols: int = 3):
    """Internal helper for drawing a base block building."""
    canvas.draw_primitive_rect(x, y, w, h, fill=color, stroke="none")
    if draw_windows:
        win_w = w / (window_cols * 2)
        win_h = win_w * 1.5
        spacing_x = (w - (win_w * window_cols)) / (window_cols + 1)
        rows = int((h - 20) / (win_h + spacing_x))
        for r in range(rows):
            for c in range(window_cols):
                wx = x + spacing_x + c * (win_w + spacing_x)
                wy = y + 20 + r * (win_h + spacing_x)
                # Skip some windows randomly (pseudorandom based on coord)
                if (r * c + r + c) % 7 != 0:
                    canvas.draw_primitive_rect(wx, wy, win_w, win_h, fill="#0f172a", stroke="none")

# --- Exported Builder Functions ---

def build_house(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Base
    canvas.draw_primitive_rect(300, 400, 200, 150, fill=get_accent(0))
    # Roof
    canvas.draw_primitive_path("M 280 400 L 400 300 L 520 400 Z", fill="#334155", stroke="none")
    # Door
    canvas.draw_primitive_rect(380, 480, 40, 70, fill="#0f172a")
    canvas.save()

def build_apartment_building(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_building_base(canvas, 320, 250, 160, 300, get_accent(1), draw_windows=True, window_cols=4)
    # Door
    canvas.draw_primitive_rect(380, 500, 40, 50, fill="#334155")
    canvas.save()

def build_city_skyline(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    _draw_building_base(canvas, 200, 350, 100, 200, "#475569", draw_windows=True, window_cols=2)
    _draw_building_base(canvas, 300, 200, 120, 350, get_accent(2), draw_windows=True, window_cols=3)
    _draw_building_base(canvas, 420, 280, 140, 270, "#334155", draw_windows=True, window_cols=4)
    _draw_building_base(canvas, 560, 400, 80, 150, "#475569", draw_windows=False)
    canvas.save()

def build_skyscraper(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Core
    _draw_building_base(canvas, 350, 200, 100, 350, get_accent(3), draw_windows=True, window_cols=2)
    # Antenna
    canvas.draw_primitive_line((400, 200), (400, 100), stroke="#ffffff", stroke_width=6)
    canvas.draw_primitive_circle(400, 100, 8, fill="#ef4444", stroke="none")
    canvas.save()

def build_suburban_house(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Garage
    canvas.draw_primitive_rect(250, 450, 120, 100, fill="#475569")
    canvas.draw_primitive_rect(260, 470, 100, 80, fill="#1e293b", rx=5)
    # Main House
    canvas.draw_primitive_rect(370, 400, 160, 150, fill=get_accent(4))
    canvas.draw_primitive_path("M 350 400 L 450 320 L 550 400 Z", fill="#334155", stroke="none")
    canvas.save()

def build_luxury_house(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_rect(250, 400, 300, 150, fill=get_accent(5))
    # Modern flat roofs
    canvas.draw_primitive_rect(230, 380, 340, 20, fill="#ffffff")
    canvas.draw_primitive_rect(350, 300, 150, 80, fill="#475569")
    canvas.draw_primitive_rect(330, 280, 190, 20, fill="#ffffff")
    # Large glass windows
    canvas.draw_primitive_rect(280, 420, 80, 130, fill="#0ea5e9", opacity=0.3)
    canvas.draw_primitive_rect(440, 420, 80, 130, fill="#0ea5e9", opacity=0.3)
    canvas.save()

def build_empty_house(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    canvas.draw_primitive_rect(300, 400, 200, 150, fill="none", stroke="#475569", stroke_width=8, dasharray="10,10")
    canvas.draw_primitive_path("M 280 400 L 400 300 L 520 400 Z", fill="none", stroke="#475569", stroke_width=8, dasharray="10,10")
    canvas.save()

def build_office_building(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_building_base(canvas, 280, 300, 240, 250, get_accent(1), draw_windows=True, window_cols=5)
    canvas.save()

def build_corporate_headquarters(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Main tower
    _draw_building_base(canvas, 350, 250, 100, 300, get_accent(2), draw_windows=True, window_cols=2)
    # Side wings
    canvas.draw_primitive_path("M 250 550 Q 300 450 350 450 L 350 550 Z", fill="#475569", stroke="none")
    canvas.draw_primitive_path("M 550 550 Q 500 450 450 450 L 450 550 Z", fill="#475569", stroke="none")
    canvas.save()

def build_factory(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Building
    canvas.draw_primitive_rect(250, 400, 300, 150, fill=get_accent(3))
    # Sawtooth Roof
    canvas.draw_primitive_path("M 250 400 L 300 350 L 300 400 L 350 350 L 350 400 L 400 350 L 400 400", fill="none", stroke=get_accent(3), stroke_width=20)
    # Smokestacks
    canvas.draw_primitive_rect(450, 250, 30, 150, fill="#475569")
    canvas.draw_primitive_rect(500, 280, 30, 120, fill="#475569")
    # Smoke
    canvas.draw_primitive_circle(465, 200, 20, fill="#cbd5e1", opacity=0.5, stroke="none")
    canvas.draw_primitive_circle(450, 150, 30, fill="#cbd5e1", opacity=0.3, stroke="none")
    canvas.save()

def build_warehouse(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Building
    canvas.draw_primitive_rect(200, 450, 400, 100, fill=get_accent(4))
    # Curved roof
    canvas.draw_primitive_path("M 200 450 Q 400 380 600 450 Z", fill="#334155", stroke="none")
    # Loading docks
    canvas.draw_primitive_rect(250, 480, 80, 70, fill="#0f172a")
    canvas.draw_primitive_rect(470, 480, 80, 70, fill="#0f172a")
    canvas.save()

def build_bank_building(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    # Steps
    canvas.draw_primitive_rect(250, 480, 300, 20, fill="#475569")
    canvas.draw_primitive_rect(230, 500, 340, 20, fill="#334155")
    # Pillars
    for px in [280, 340, 400, 460]:
        canvas.draw_primitive_rect(px, 350, 20, 130, fill="#e2e8f0")
    # Roof
    canvas.draw_primitive_path("M 240 350 L 400 250 L 560 350 Z", fill=get_accent(5), stroke="none")
    # Pillar Base/Top
    canvas.draw_primitive_rect(260, 330, 240, 20, fill="#94a3b8")
    canvas.save()

def build_hospital(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Building
    _draw_building_base(canvas, 300, 250, 200, 300, "#475569", draw_windows=True, window_cols=4)
    # Cross sign
    canvas.draw_primitive_circle(400, 200, 40, fill="#ef4444", stroke="none")
    canvas.draw_primitive_rect(390, 175, 20, 50, fill="#ffffff", rx=2)
    canvas.draw_primitive_rect(375, 190, 50, 20, fill="#ffffff", rx=2)
    canvas.save()

def build_school(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_rect(280, 400, 240, 150, fill=get_accent(1))
    # Bell tower
    canvas.draw_primitive_rect(370, 250, 60, 150, fill="#475569")
    canvas.draw_primitive_path("M 360 250 L 400 180 L 440 250 Z", fill="#334155", stroke="none")
    canvas.draw_primitive_circle(400, 280, 15, fill="#fcd34d", stroke="none")
    canvas.save()

def build_university(out_path: str):
    build_bank_building(out_path) # Uses the classical columns look too

def build_government_building(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Dome
    canvas.draw_primitive_path("M 300 350 A 100 100 0 0 1 500 350", fill="#f8fafc", stroke="none")
    # Base building
    canvas.draw_primitive_rect(240, 350, 320, 200, fill=get_accent(2))
    # Columns
    for px in [260, 320, 380, 440, 500]:
        canvas.draw_primitive_rect(px, 380, 20, 150, fill="#e2e8f0")
    canvas.save()

def build_court_building(out_path: str):
    build_bank_building(out_path) # Alias for classical columns look

def build_data_center(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Base massive block
    canvas.draw_primitive_rect(250, 250, 300, 300, fill="#1e293b", rx=10)
    # Glowing server arrays inside
    for r in range(4):
        for c in range(3):
            canvas.draw_primitive_rect(280 + c*90, 280 + r*60, 60, 40, fill="#334155", rx=4)
            canvas.draw_primitive_circle(300 + c*90, 300 + r*60, 5, fill=get_accent(3), stroke="none")
    canvas.save()

def build_power_plant(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Reactor dome
    canvas.draw_primitive_path("M 250 550 A 100 100 0 0 1 450 550 Z", fill=get_accent(4), stroke="none")
    # Cooling tower
    canvas.draw_primitive_path("M 450 550 L 470 300 L 530 300 L 550 550 Z", fill="#475569", stroke="none")
    canvas.draw_primitive_ellipse((500, 300), (30, 10), fill="#334155", stroke="none")
    # Electricity bolt
    canvas.draw_primitive_path("M 350 480 L 330 510 L 350 510 L 340 540", fill="none", stroke="#fcd34d", stroke_width=6)
    canvas.save()

def build_airport(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_path("M 200 500 Q 400 450 600 500 L 600 550 L 200 550 Z", fill="#475569", stroke="none")
    # Control tower
    canvas.draw_primitive_rect(380, 250, 40, 250, fill=get_accent(5))
    canvas.draw_primitive_path("M 360 250 L 440 250 L 420 200 L 380 200 Z", fill="#0ea5e9", opacity=0.8, stroke="none")
    canvas.draw_primitive_circle(400, 180, 10, fill="#f43f5e", stroke="none")
    canvas.save()

def build_shopping_mall(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_rect(200, 400, 400, 150, fill="#475569")
    canvas.draw_primitive_rect(300, 350, 200, 50, fill=get_accent(0))
    canvas.draw_primitive_rect(350, 450, 100, 100, fill="#fff", stroke=canvas.stroke_color, stroke_width=4)
    # Glass entrance
    canvas.draw_primitive_line((400, 450), (400, 550), stroke="#475569", stroke_width=4)
    canvas.save()

def build_small_business_store(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_rect(300, 350, 200, 200, fill="#334155")
    # Awning
    canvas.draw_primitive_path("M 280 350 L 520 350 L 500 400 L 300 400 Z", fill=get_accent(1), stroke="none")
    # Stripes on Awning
    for x in range(300, 500, 40):
        canvas.draw_primitive_path(f"M {x} 350 L {x+20} 350 L {x+20} 400 L {x} 400 Z", fill="#ffffff", opacity=0.3, stroke="none")
    # Shop Window
    canvas.draw_primitive_rect(320, 430, 80, 80, fill="#0ea5e9", opacity=0.3)
    # Door
    canvas.draw_primitive_rect(420, 430, 60, 120, fill="#0ea5e9", opacity=0.3)
    canvas.save()

def build_restaurant(out_path: str):
    build_small_business_store(out_path) # Alias
