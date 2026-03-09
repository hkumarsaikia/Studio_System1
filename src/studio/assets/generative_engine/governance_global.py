"""
FILE: src/studio/assets/generative_engine/governance_global.py
PURPOSE: Procedural geometry builders for Governance, Law, and Global Trade.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

# --- 10. Law & Governance ---

def build_gavel(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Handle
    for rot in [45]:
        canvas.dwg.add(canvas.dwg.rect(insert=(250, 400), size=(300, 30), fill="#78350f", rx=15, transform=f"rotate({rot} 400 400)"))
    # Head
    for rot in [45]:
        canvas.dwg.add(canvas.dwg.rect(insert=(450, 250), size=(60, 150), fill="#92400e", rx=10, transform=f"rotate({rot} 480 325)"))
    # Block
    canvas.draw_primitive_rect(150, 500, 150, 40, rx=5, fill="#b45309")
    canvas.draw_primitive_rect(170, 540, 110, 20, fill="#78350f")
    canvas.save()

def build_law_scales(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    # Base and pillar
    canvas.draw_primitive_rect(350, 600, 100, 20, fill="#d4d4d8")
    canvas.draw_primitive_rect(390, 200, 20, 400, fill="#d4d4d8")
    canvas.draw_primitive_circle(400, 200, 30, fill="#fcd34d")
    # Crossbeam
    canvas.draw_primitive_rect(200, 250, 400, 15, fill="#d4d4d8")
    canvas.draw_primitive_circle(200, 257, 10, fill="#fcd34d")
    canvas.draw_primitive_circle(600, 257, 10, fill="#fcd34d")
    # Bowls
    for x in [200, 600]:
        canvas.draw_primitive_path(f"M {x-60} 450 A 60 40 0 0 0 {x+60} 450 Z", fill="#fcd34d", stroke="none")
        canvas.draw_primitive_line((x, 250), (x-60, 450), stroke="#94a3b8", stroke_width=4)
        canvas.draw_primitive_line((x, 250), (x+60, 450), stroke="#94a3b8", stroke_width=4)
    canvas.save()

def build_justice_symbol(out_path: str):
    build_law_scales(out_path) # Alias

def build_document_contract(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_rect(250, 200, 300, 400, fill="#f8fafc", rx=10)
    for i in range(5):
        canvas.draw_primitive_rect(300, 280 + i*40, 200 if i%2==0 else 150, 10, fill="#cbd5e1")
    # Pen
    canvas.dwg.add(canvas.dwg.path("M 500 550 L 530 520 L 560 550 L 510 600 Z", fill="#475569", stroke="none", transform="rotate(-30 500 550)"))
    canvas.save()

def build_shield(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Police/Security style badge
    canvas.draw_primitive_path("M 400 200 L 550 250 L 550 450 Q 400 650 400 700 Q 250 650 250 450 L 250 250 Z", fill="#1e293b", stroke=get_accent(3), stroke_width=20, stroke_linejoin="round")
    # Star inside
    d_star = "M 400 300 L 430 380 L 500 400 L 440 440 L 460 520 L 400 480 L 340 520 L 360 440 L 300 400 L 370 380 Z"
    canvas.draw_primitive_path(d_star, fill="#fcd34d", stroke="none")
    canvas.save()

def build_police_badge(out_path: str):
    build_shield(out_path) # Alias

def build_prison_bars(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4), add_glow=False)
    canvas.draw_primitive_rect(200, 200, 400, 400, fill="#0f172a") # Dark background
    for x in range(250, 600, 60):
        canvas.draw_primitive_rect(x, 200, 30, 400, fill="#94a3b8")
    canvas.draw_primitive_rect(180, 250, 440, 40, fill="#475569")
    canvas.draw_primitive_rect(180, 500, 440, 40, fill="#475569")
    canvas.save()

def build_handcuffs(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5), add_glow=False)
    # Cuff 1
    canvas.draw_primitive_circle(300, 400, 80, fill="none", stroke="#cbd5e1", stroke_width=20)
    canvas.draw_primitive_path("M 260 400 L 340 400", fill="none", stroke="#475569", stroke_width=8) # Teeth
    # Cuff 2
    canvas.draw_primitive_circle(500, 400, 80, fill="none", stroke="#cbd5e1", stroke_width=20)
    canvas.draw_primitive_path("M 460 400 L 540 400", fill="none", stroke="#475569", stroke_width=8)
    # Chain
    canvas.draw_primitive_path("M 380 400 Q 400 450 420 400", fill="none", stroke="#94a3b8", stroke_width=10)
    canvas.draw_primitive_path("M 370 410 Q 400 350 430 410", fill="none", stroke="#94a3b8", stroke_width=10)
    canvas.save()

def build_ballot_box(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Box
    canvas.draw_primitive_rect(250, 350, 300, 250, fill="#f8fafc", stroke=get_accent(0), stroke_width=10, rx=10)
    canvas.draw_primitive_rect(350, 450, 100, 10, fill="#0f172a")
    # Paper sliding in
    canvas.draw_primitive_rect(360, 250, 80, 120, fill="#e2e8f0")
    # Checkmark on paper
    canvas.draw_primitive_path("M 380 300 L 390 310 L 420 280", fill="none", stroke="#22c55e", stroke_width=8)
    # Re-draw front slice of box to overlap paper
    canvas.draw_primitive_rect(250, 350, 300, 100, fill="#f8fafc", stroke=get_accent(0), stroke_width=10, rx=10)
    canvas.save()

# --- 11. Global & Trade ---

def build_globe(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_circle(400, 400, 200, fill="#0284c7")
    # Continents (abstract blobs)
    d1 = "M 300 250 Q 400 200 400 300 Q 300 400 250 350 Z"
    d2 = "M 450 350 Q 550 300 550 450 Q 500 550 400 500 Q 450 450 450 350 Z"
    canvas.draw_primitive_path(d1, fill="#22c55e", stroke="none")
    canvas.draw_primitive_path(d2, fill="#22c55e", stroke="none")
    # Grid lines
    canvas.draw_primitive_ellipse((400, 400), (200, 80), fill="none", stroke="#bae6fd", stroke_width=4, opacity=0.5)
    canvas.draw_primitive_ellipse((400, 400), (80, 200), fill="none", stroke="#bae6fd", stroke_width=4, opacity=0.5)
    canvas.save()

def build_international_flags(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    for cx, cy, rot, color in [(300, 400, -20, "#ef4444"), (500, 400, 20, "#3b82f6"), (400, 350, 0, "#22c55e")]:
        canvas.dwg.add(canvas.dwg.line(start=(cx, cy), end=(cx, cy+150), stroke="#94a3b8", stroke_width=10, stroke_linecap="round", transform=f"rotate({rot} {cx} {cy+150})"))
        canvas.dwg.add(canvas.dwg.rect(insert=(cx, cy), size=(80, 50), fill=color, transform=f"rotate({rot} {cx} {cy+150})"))
    canvas.save()

def build_cargo_ship(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Hull
    canvas.draw_primitive_path("M 150 450 L 650 450 L 600 550 L 250 550 Z", fill="#1e293b", stroke="none")
    # Cargo Boxes
    colors = ["#f43f5e", "#0ea5e9", "#fcd34d", "#22c55e"]
    for i in range(4):
        canvas.draw_primitive_rect(280 + i*70, 380, 60, 70, fill=colors[i], rx=2)
    for i in range(3):
        canvas.draw_primitive_rect(315 + i*70, 310, 60, 70, fill=colors[3-i], rx=2)
    # Bridge
    canvas.draw_primitive_rect(180, 350, 60, 100, fill="#f8fafc")
    canvas.draw_primitive_rect(200, 300, 20, 50, fill="#fcd34d")
    canvas.save()

def build_container(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Big 3D looking container box
    canvas.draw_primitive_rect(200, 300, 400, 200, fill="#f43f5e", stroke="#be123c", stroke_width=10)
    # Corrugation lines
    for x in range(230, 580, 40):
        canvas.draw_primitive_rect(x, 300, 20, 200, fill="#be123c", stroke="none")
    canvas.save()

def build_airplane(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.dwg.add(canvas.dwg.path("M 200 450 Q 500 450 600 400 Q 650 380 600 420 Q 500 480 200 500 Z", fill="#cbd5e1", stroke="none", transform="rotate(-15 400 400)"))
    # Main Fuselage
    canvas.dwg.add(canvas.dwg.path("M 150 400 Q 600 400 650 400 Q 700 400 650 450 L 200 450 Z", fill="#f8fafc", stroke="none", transform="rotate(-15 400 400)"))
    # Tail
    canvas.dwg.add(canvas.dwg.path("M 200 400 L 250 300 L 300 400 Z", fill="#f8fafc", stroke="none", transform="rotate(-15 400 400)"))
    canvas.save()

def build_truck(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Trailer
    canvas.draw_primitive_rect(200, 350, 280, 150, fill="#475569", rx=10)
    # Cab
    canvas.draw_primitive_rect(490, 400, 100, 100, fill="#f43f5e", rx=10)
    canvas.draw_primitive_rect(540, 410, 40, 40, fill="#bae6fd")
    # Wheels
    canvas.draw_primitive_circle(250, 520, 30, fill="#0f172a", stroke="#475569", stroke_width=10)
    canvas.draw_primitive_circle(330, 520, 30, fill="#0f172a", stroke="#475569", stroke_width=10)
    canvas.draw_primitive_circle(540, 520, 30, fill="#0f172a", stroke="#475569", stroke_width=10)
    canvas.save()

def build_handshake(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_path("M 200 450 L 350 400 Q 400 380 450 400 Q 400 450 350 450 L 200 500 Z", fill="#e2e8f0", stroke="#cbd5e1", stroke_width=5)
    canvas.draw_primitive_path("M 600 450 L 450 400 Q 400 380 350 400 Q 400 450 450 450 L 600 500 Z", fill="#64748b", stroke="#475569", stroke_width=5)
    # Sleeves
    canvas.draw_primitive_path("M 150 400 L 250 380 L 250 500 L 150 480 Z", fill="#1e293b", stroke="none")
    canvas.draw_primitive_path("M 650 400 L 550 380 L 550 500 L 650 480 Z", fill="#1e293b", stroke="none")
    canvas.save()

def build_satellite(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Panels
    canvas.dwg.add(canvas.dwg.rect(insert=(200, 350), size=(150, 100), fill="#0284c7", stroke="#fff", stroke_width=4, transform="skewY(-15)"))
    canvas.dwg.add(canvas.dwg.rect(insert=(450, 350), size=(150, 100), fill="#0284c7", stroke="#fff", stroke_width=4, transform="skewY(15)"))
    # Core
    canvas.draw_primitive_rect(370, 300, 60, 200, fill="#94a3b8", rx=20)
    # Dish
    canvas.draw_primitive_path("M 350 250 Q 400 150 450 250 Z", fill="#f1f5f9", stroke="none")
    # Signal waves
    for r in [40, 60, 80]:
        canvas.draw_primitive_path(f"M {400-r} {150-r} A {r*1.2} {r*1.2} 0 0 1 {400+r} {150-r}", fill="none", stroke="#fcd34d", stroke_width=6)
    canvas.save()
    
def build_customs_stamp(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Outer ring
    canvas.draw_primitive_circle(400, 400, 150, fill="none", stroke="#ef4444", stroke_width=20)
    canvas.draw_primitive_circle(400, 400, 130, fill="none", stroke="#ef4444", stroke_width=5)
    # Inner APPROVED text block (geometric rep)
    canvas.draw_primitive_rect(280, 370, 240, 60, fill="#ef4444", rx=5)
    # Abstract star
    canvas.draw_primitive_path("M 400 280 L 420 320 L 460 320 L 430 340 L 440 380 L 400 360 L 360 380 L 370 340 L 340 320 L 380 320 Z", fill="#ef4444", stroke="none")
    canvas.save()

def build_oil_barrel(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_ellipse((400, 300), (120, 30), fill="#334155", stroke="none")
    canvas.draw_primitive_rect(280, 300, 240, 300, fill="#1e293b", stroke="#0f172a", stroke_width=5)
    canvas.draw_primitive_ellipse((400, 600), (120, 30), fill="#1e293b", stroke="none")
    # Rings
    canvas.draw_primitive_ellipse((400, 400), (120, 30), fill="none", stroke="#0f172a", stroke_width=10)
    canvas.draw_primitive_ellipse((400, 500), (120, 30), fill="none", stroke="#0f172a", stroke_width=10)
    # Drop symbol
    canvas.draw_primitive_path("M 400 420 Q 420 460 400 480 Q 380 460 400 420 Z", fill="#f59e0b", stroke="none")
    canvas.save()
