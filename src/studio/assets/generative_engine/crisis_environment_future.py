"""
FILE: src/studio/assets/generative_engine/crisis_environment_future.py
PURPOSE: Procedural geometry builders for Crisis, Environment, and Future concepts.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent
from src.studio.assets.generative_engine.governance_global import build_law_scales, build_globe
from src.studio.assets.generative_engine.work_tech_social import build_cybersecurity_lock, build_wifi_signal

# --- 12. Conflict & Crisis ---

def build_warning_sign(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_path("M 400 200 L 600 550 L 200 550 Z", fill="#f59e0b", stroke="#b45309", stroke_width=20, stroke_linejoin="round")
    canvas.draw_primitive_line((400, 300), (400, 450), stroke="#1e293b", stroke_width=25)
    canvas.draw_primitive_circle(400, 500, 15, fill="#1e293b")
    canvas.save()

def build_skull(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_circle(400, 350, 120, fill="#f8fafc")
    canvas.draw_primitive_rect(340, 420, 120, 80, rx=10, fill="#f8fafc")
    canvas.draw_primitive_circle(350, 350, 30, fill="#0f172a")
    canvas.draw_primitive_circle(450, 350, 30, fill="#0f172a")
    canvas.draw_primitive_path("M 400 400 L 380 430 L 420 430 Z", fill="#0f172a", stroke="none") # nose
    for x in [360, 380, 400, 420, 440]:
        canvas.draw_primitive_line((x, 470), (x, 500), stroke="#0f172a", stroke_width=5)
    canvas.save()

def build_bomb(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_circle(400, 450, 120, fill="#1e293b")
    canvas.draw_primitive_rect(370, 300, 60, 40, rx=5, fill="#334155")
    # Fuse sparking
    canvas.draw_primitive_path("M 400 300 Q 380 250 450 200", fill="none", stroke="#f59e0b", stroke_width=10)
    for rot in range(0, 360, 45):
        canvas.dwg.add(canvas.dwg.line(start=(460, 200), end=(480, 200), stroke="#ef4444", stroke_width=5, transform=f"rotate({rot} 450 200)"))
    canvas.save()

def build_broken_shield(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Left half
    canvas.draw_primitive_path("M 400 200 L 250 250 L 250 450 Q 250 650 380 700 L 380 500 L 420 400 L 380 300 Z", fill="#ef4444", stroke="none")
    # Right half
    canvas.draw_primitive_path("M 420 200 L 550 250 L 550 450 Q 550 650 420 700 L 420 500 L 460 400 L 420 300 Z", fill="#f43f5e", stroke="none")
    # Crack down middle
    canvas.draw_primitive_path("M 390 200 L 430 300 L 390 400 L 430 500 L 390 700", fill="none", stroke="#0f172a", stroke_width=15, stroke_linejoin="miter")
    canvas.save()

def build_broken_chain(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_rect(200, 350, 150, 80, rx=40, fill="none", stroke="#94a3b8", stroke_width=25)
    canvas.draw_primitive_rect(450, 350, 150, 80, rx=40, fill="none", stroke="#94a3b8", stroke_width=25)
    # Broken middle link
    canvas.draw_primitive_path("M 380 350 C 350 300, 450 300, 420 350", fill="none", stroke="#cbd5e1", stroke_width=25, stroke_linecap="round")
    canvas.draw_primitive_path("M 380 430 C 350 480, 450 480, 420 430", fill="none", stroke="#cbd5e1", stroke_width=25, stroke_linecap="round")
    # Impact lines
    for rot in [45, -45, 135, -135]:
        canvas.dwg.add(canvas.dwg.line(start=(410, 390), end=(450, 390), stroke="#ef4444", stroke_width=6, stroke_linecap="round", transform=f"rotate({rot} 400 390)"))
    canvas.save()

def build_riot_shield(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_rect(300, 200, 200, 400, rx=20, fill="#1e293b", stroke="#475569", stroke_width=15)
    canvas.draw_primitive_rect(330, 250, 140, 50, rx=10, fill="#0f172a") # Viewport
    # Baton behind
    canvas.draw_primitive_line((200, 600), (600, 200), stroke="#475569", stroke_width=20)
    canvas.draw_primitive_line((530, 270), (550, 290), stroke="#f8fafc", stroke_width=20)
    canvas.save()

def build_protest_fist(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_circle(400, 350, 80, fill="#ef4444")
    # Fingers
    for i in range(4):
        canvas.draw_primitive_rect(320, 250 + i*40, 100, 35, rx=17, fill="#be123c")
    # Thumb
    canvas.draw_primitive_path("M 400 400 C 480 400, 500 350, 450 300 C 400 250, 400 250, 400 250", fill="none", stroke="#be123c", stroke_width=35, stroke_linecap="round")
    # Wrist
    canvas.draw_primitive_rect(360, 420, 80, 150, fill="#ef4444")
    canvas.save()

# --- 13. Environment & Nature ---

def build_leaf(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_path("M 400 550 C 650 550, 650 250, 400 200 C 150 250, 150 550, 400 550", fill="#22c55e", stroke="none")
    # Stem / Vein
    canvas.draw_primitive_line((400, 650), (400, 250), stroke="#166534", stroke_width=10)
    canvas.draw_primitive_line((400, 450), (480, 380), stroke="#166534", stroke_width=8)
    canvas.draw_primitive_line((400, 400), (320, 330), stroke="#166534", stroke_width=8)
    canvas.draw_primitive_line((400, 350), (450, 300), stroke="#166534", stroke_width=8)
    canvas.save()

def build_tree(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_rect(370, 400, 60, 200, fill="#78350f") # Trunk
    # Leaves layered
    canvas.draw_primitive_circle(400, 300, 120, fill="#22c55e")
    canvas.draw_primitive_circle(300, 350, 90, fill="#166534")
    canvas.draw_primitive_circle(500, 350, 90, fill="#15803d")
    canvas.draw_primitive_circle(400, 200, 80, fill="#4ade80")
    canvas.save()

def build_sun(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    canvas.draw_primitive_circle(400, 400, 100, fill="#fcd34d")
    for rot in range(0, 360, 45):
        canvas.dwg.add(canvas.dwg.line(start=(400, 250), end=(400, 180), stroke="#fcd34d", stroke_width=15, stroke_linecap="round", transform=f"rotate({rot} 400 400)"))
    canvas.save()

def build_water_drop(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_path("M 400 200 Q 550 450 550 500 A 150 150 0 0 1 250 500 Q 250 450 400 200 Z", fill="#0ea5e9", stroke="none")
    # Highlight
    canvas.draw_primitive_path("M 350 450 A 80 80 0 0 1 300 500", fill="none", stroke="#bae6fd", stroke_width=12, stroke_linecap="round")
    canvas.save()

def build_fire(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_path("M 400 600 C 650 600, 600 350, 400 200 C 380 300, 450 350, 380 400 C 350 380, 200 450, 200 600 C 200 700, 600 700, 400 600", fill="#ef4444", stroke="none")
    canvas.draw_primitive_path("M 400 550 C 550 550, 500 400, 400 350 C 390 400, 420 420, 380 450 C 360 440, 300 480, 300 550 C 300 600, 500 600, 400 550", fill="#fcd34d", stroke="none")
    canvas.save()

def build_wind(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    canvas.draw_primitive_path("M 150 300 L 450 300 C 550 300, 550 200, 450 200", fill="none", stroke="#94a3b8", stroke_width=20, stroke_linecap="round")
    canvas.draw_primitive_path("M 250 400 L 550 400 C 650 400, 650 500, 550 500", fill="none", stroke="#cbd5e1", stroke_width=15, stroke_linecap="round")
    canvas.draw_primitive_path("M 350 500 L 600 500 C 680 500, 680 600, 600 600", fill="none", stroke="#94a3b8", stroke_width=10, stroke_linecap="round")
    canvas.save()

def build_earth_globe(out_path: str):
    build_globe(out_path) # Alias

# --- 14. Abstractions & Utilities ---

def build_check_mark(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1), add_glow=False)
    canvas.draw_primitive_path("M 250 450 L 350 550 L 600 250", fill="none", stroke="#22c55e", stroke_width=50, stroke_linecap="round", stroke_linejoin="round")
    canvas.save()

def build_cross_mark(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2), add_glow=False)
    canvas.draw_primitive_line((250, 250), (550, 550), stroke="#ef4444", stroke_width=50)
    canvas.draw_primitive_line((250, 550), (550, 250), stroke="#ef4444", stroke_width=50)
    canvas.save()

def build_question_mark(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3), add_glow=False)
    canvas.draw_primitive_path("M 300 300 C 300 150, 500 150, 500 300 C 500 400, 400 400, 400 500", fill="none", stroke="#38bdf8", stroke_width=40, stroke_linecap="round")
    canvas.draw_primitive_circle(400, 600, 20, fill="#38bdf8")
    canvas.save()

def build_exclamation_mark(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4), add_glow=False)
    canvas.draw_primitive_path("M 400 150 L 400 450", fill="none", stroke="#f59e0b", stroke_width=50, stroke_linecap="round")
    canvas.draw_primitive_circle(400, 600, 25, fill="#f59e0b")
    canvas.save()

def build_target(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5), add_glow=False)
    for i, r in enumerate([200, 150, 100, 50]):
        color = "#ef4444" if i % 2 == 0 else "#fff"
        canvas.draw_primitive_circle(400, 400, r, fill=color)
    # Dart
    canvas.dwg.add(canvas.dwg.path("M 500 300 L 420 380", stroke="#334155", stroke_width=10, transform="rotate(20 400 400)"))
    canvas.dwg.add(canvas.dwg.path("M 500 300 L 530 270 M 500 300 L 520 290 M 500 300 L 510 280", stroke="#3b82f6", stroke_width=10, transform="rotate(20 400 400)"))
    canvas.save()

def build_magnet(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    canvas.draw_primitive_path("M 300 500 L 300 400 A 100 100 0 0 1 500 400 L 500 500 L 450 500 L 450 400 A 50 50 0 0 0 350 400 L 350 500 Z", fill="#ef4444", stroke="none")
    # Poles
    canvas.draw_primitive_rect(300, 500, 50, 50, fill="#d4d4d8")
    canvas.draw_primitive_rect(450, 500, 50, 50, fill="#d4d4d8")
    # Magnetic waves
    canvas.draw_primitive_path("M 250 630 A 150 150 0 0 1 550 630", fill="none", stroke="#38bdf8", stroke_width=8, stroke_linecap="round")
    canvas.draw_primitive_path("M 200 680 A 200 200 0 0 1 600 680", fill="none", stroke="#38bdf8", stroke_width=8, stroke_linecap="round")
    canvas.save()

def build_chain(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1), add_glow=False)
    for rot in [-20]:
        canvas.dwg.add(canvas.dwg.rect(insert=(250, 350), size=(150, 80), rx=40, fill="none", stroke="#94a3b8", stroke_width=25, transform=f"rotate({rot} 400 400)"))
        canvas.dwg.add(canvas.dwg.rect(insert=(350, 350), size=(150, 80), rx=40, fill="none", stroke="#94a3b8", stroke_width=25, transform=f"rotate({rot} 400 400)"))
        canvas.dwg.add(canvas.dwg.rect(insert=(450, 350), size=(150, 80), rx=40, fill="none", stroke="#94a3b8", stroke_width=25, transform=f"rotate({rot} 400 400)"))
    canvas.save()

def build_key(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2), add_glow=False)
    canvas.draw_primitive_circle(250, 400, 60, fill="none", stroke="#f59e0b", stroke_width=30)
    canvas.draw_primitive_line((310, 400), (600, 400), stroke="#f59e0b", stroke_width=30)
    canvas.draw_primitive_line((500, 400), (500, 450), stroke="#f59e0b", stroke_width=25)
    canvas.draw_primitive_line((570, 400), (570, 470), stroke="#f59e0b", stroke_width=25)
    canvas.save()

def build_lock(out_path: str):
    build_cybersecurity_lock(out_path) # Alias

def build_search_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3), add_glow=False)
    canvas.draw_primitive_circle(350, 350, 100, fill="none", stroke="#38bdf8", stroke_width=30)
    canvas.draw_primitive_line((430, 430), (550, 550), stroke="#38bdf8", stroke_width=40)
    canvas.save()

def build_signal_wave(out_path: str):
    build_wifi_signal(out_path) # Alias

def build_balance_scale(out_path: str):
    build_law_scales(out_path) # Alias

def build_magic_wand(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.dwg.add(canvas.dwg.line(start=(250, 550), end=(450, 350), stroke="#334155", stroke_width=20, stroke_linecap="round", transform="skewX(-10)"))
    canvas.dwg.add(canvas.dwg.line(start=(450, 350), end=(500, 300), stroke="#fcd34d", stroke_width=20, stroke_linecap="round", transform="skewX(-10)"))
    
    for px, py in [(550, 250), (450, 200), (600, 350)]:
        canvas.draw_primitive_path(f"M {px} {py-15} Q {px} {py} {px+15} {py} Q {px} {py} {px} {py+15} Q {px} {py} {px-15} {py} Q {px} {py} {px} {py-15}", fill="#fcd34d", stroke="none")
    canvas.save()

def build_lightbulb(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5), add_glow=False)
    canvas.draw_primitive_path("M 400 200 C 500 200, 550 300, 500 400 C 480 440, 440 460, 440 500 L 360 500 C 360 460, 320 440, 300 400 C 250 300, 300 200, 400 200 Z", fill="#fcd34d", stroke="#faba05", stroke_width=10)
    canvas.draw_primitive_rect(360, 500, 80, 40, rx=5, fill="#94a3b8")
    canvas.draw_primitive_rect(380, 540, 40, 20, rx=2, fill="#475569")
    # Filament
    canvas.draw_primitive_line((370, 480), (380, 400), stroke="#ea580c", stroke_width=5)
    canvas.draw_primitive_line((430, 480), (420, 400), stroke="#ea580c", stroke_width=5)
    canvas.draw_primitive_line((380, 400), (420, 400), stroke="#ea580c", stroke_width=5)
    # Glow rays
    for rot in [0, 45, -45, 90, -90]:
        canvas.dwg.add(canvas.dwg.line(start=(400, 150), end=(400, 100), stroke="#fcd34d", stroke_width=8, stroke_linecap="round", transform=f"rotate({rot} 400 350)"))
    canvas.save()

def build_hourglass(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    canvas.draw_primitive_path("M 300 200 L 500 200 L 420 400 L 500 600 L 300 600 L 380 400 Z", fill="none", stroke="#38bdf8", stroke_width=20, stroke_linejoin="round")
    canvas.draw_primitive_line((250, 200), (550, 200), stroke="#78350f", stroke_width=20, stroke_linecap="round")
    canvas.draw_primitive_line((250, 600), (550, 600), stroke="#78350f", stroke_width=20, stroke_linecap="round")
    # Sand
    canvas.draw_primitive_path("M 300 600 L 500 600 L 400 450 Z", fill="#fcd34d", stroke="none")
    canvas.draw_primitive_path("M 400 400 L 450 280 L 350 280 Z", fill="#fcd34d", stroke="none")
    # Falling
    canvas.draw_primitive_line((400, 400), (400, 450), stroke="#fcd34d", stroke_width=6)
    canvas.save()

def build_puzzle_piece(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    # Approximation of a puzzle piece
    d = "M 300 300 L 380 300 A 40 40 0 1 1 420 300 L 500 300 L 500 380 A 40 40 0 1 1 500 420 L 500 500 L 420 500 A 40 40 0 1 0 380 500 L 300 500 L 300 420 A 40 40 0 1 0 300 380 Z"
    canvas.draw_primitive_path(d, fill="#d946ef", stroke="#86198f", stroke_width=10)
    canvas.save()
