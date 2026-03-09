"""
FILE: src/studio/assets/generative_engine/people_society.py
PURPOSE: Procedural geometry builders for People & Society symbols.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

def _draw_person_base(canvas: ProceduralCanvas, cx: int, cy: int, scale: float = 1.0, accent_idx: int = 0, is_active: bool = False):
    """Internal helper to draw a simple geometric person figure."""
    color = get_accent(accent_idx) if is_active else "#94a3b8"
    
    # Head
    canvas.draw_primitive_circle(cx, cy - 40 * scale, 30 * scale, fill=color, stroke="none")
    # Body
    d = f"M {cx - 40 * scale} {cy + 20 * scale} Q {cx} {cy - 10 * scale} {cx + 40 * scale} {cy + 20 * scale} L {cx + 40 * scale} {cy + 80 * scale} Q {cx} {cy + 100 * scale} {cx - 40 * scale} {cy + 80 * scale} Z"
    canvas.draw_primitive_path(d=d, fill=color, stroke="none")

# --- Exported Builder Functions ---

def build_person(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=0, is_active=True)
    canvas.save()

def build_person_group(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_person_base(canvas, 300, 420, scale=1.2, accent_idx=1, is_active=False)
    _draw_person_base(canvas, 500, 420, scale=1.2, accent_idx=1, is_active=False)
    _draw_person_base(canvas, 400, 380, scale=1.4, accent_idx=1, is_active=True)
    canvas.save()

def build_crowd(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Draw 5 people in a V formation
    _draw_person_base(canvas, 250, 450, scale=1.0, accent_idx=0, is_active=False)
    _draw_person_base(canvas, 550, 450, scale=1.0, accent_idx=0, is_active=False)
    _draw_person_base(canvas, 320, 410, scale=1.1, accent_idx=1, is_active=False)
    _draw_person_base(canvas, 480, 410, scale=1.1, accent_idx=1, is_active=False)
    _draw_person_base(canvas, 400, 360, scale=1.3, accent_idx=2, is_active=True)
    canvas.save()

def build_worker(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=3, is_active=True)
    # Hard Hat
    d_hat = "M 350 340 Q 400 300 450 340 L 460 350 L 340 350 Z"
    canvas.draw_primitive_path(d=d_hat, fill="#f59e0b", stroke="none")
    canvas.save()

def build_office_worker(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=4, is_active=True)
    # Tie
    d_tie = "M 390 430 L 410 430 L 405 500 L 400 520 L 395 500 Z"
    canvas.draw_primitive_path(d=d_tie, fill="#334155", stroke="none")
    canvas.save()

def build_manager(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    _draw_person_base(canvas, 400, 380, scale=1.2, accent_idx=5, is_active=True)
    # Desk
    canvas.draw_primitive_rect(280, 470, 240, 20, fill="#cbd5e1", rx=5)
    canvas.save()

def build_business_person(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=0, is_active=True)
    # Briefcase next to body
    canvas.draw_primitive_rect(440, 460, 60, 40, rx=5, fill="#475569")
    canvas.draw_primitive_rect(460, 450, 20, 10, fill="none", stroke="#475569", stroke_width=4)
    canvas.save()

def build_consumer(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=1, is_active=True)
    # Shopping bag
    canvas.draw_primitive_rect(440, 460, 50, 60, rx=2, fill="#f43f5e")
    canvas.draw_primitive_path("M 450 460 Q 465 430 480 460", fill="none", stroke="#f43f5e", stroke_width=4)
    canvas.save()

def build_customer(out_path: str):
    build_consumer(out_path) # Alias

def build_citizen(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=2, is_active=True)
    # Vote card
    canvas.draw_primitive_rect(440, 440, 40, 60, fill="#fff", stroke=canvas.stroke_color, stroke_width=2)
    canvas.save()

def build_voter(out_path: str):
    build_citizen(out_path) # Alias

def build_student(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=3, is_active=True)
    # Graduation Cap
    canvas.draw_primitive_path("M 350 330 L 400 310 L 450 330 L 400 350 Z", fill="#1e293b", stroke="none")
    canvas.draw_primitive_path("M 430 340 L 430 380", stroke="#1e293b", stroke_width=4)
    canvas.save()

def build_teacher(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    _draw_person_base(canvas, 350, 420, scale=1.3, accent_idx=4, is_active=True)
    # Chalkboard
    canvas.draw_primitive_rect(420, 300, 150, 100, fill="#166534", stroke="#854d0e", stroke_width=8)
    # Pointer Stick
    canvas.draw_primitive_line((380, 450), (450, 350), stroke="#854d0e", stroke_width=4)
    canvas.save()

def build_doctor(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=5, is_active=True)
    # Stethoscope (white v-shape with dots)
    canvas.draw_primitive_path("M 370 420 Q 400 480 430 420", fill="none", stroke="#e2e8f0", stroke_width=6)
    canvas.draw_primitive_circle(370, 415, 6, fill="#cbd5e1", stroke="none")
    canvas.draw_primitive_circle(430, 415, 6, fill="#cbd5e1", stroke="none")
    canvas.save()

def build_family(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Adult 1
    _draw_person_base(canvas, 340, 400, scale=1.4, accent_idx=0, is_active=True)
    # Adult 2
    _draw_person_base(canvas, 460, 400, scale=1.3, accent_idx=0, is_active=True)
    # Child
    _draw_person_base(canvas, 400, 460, scale=0.8, accent_idx=0, is_active=True)
    canvas.save()

def build_child(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_person_base(canvas, 400, 440, scale=1.0, accent_idx=1, is_active=True)
    # Toy block
    canvas.draw_primitive_rect(430, 480, 30, 30, fill="#ef4444")
    canvas.save()

def build_elderly_person(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=2, is_active=True)
    # Cane
    canvas.draw_primitive_path("M 450 440 Q 470 440 470 460 L 470 540", fill="none", stroke="#78350f", stroke_width=6)
    canvas.save()

def build_entrepreneur(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=3, is_active=True)
    # Rocket icon in hand
    d_rocket = "M 440 480 L 450 440 L 460 480 Z"
    canvas.draw_primitive_path(d=d_rocket, fill="#3b82f6", stroke="none")
    canvas.save()

def build_influencer(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    _draw_person_base(canvas, 400, 400, scale=1.5, accent_idx=4, is_active=True)
    # Sparkles
    for x, y in [(320, 320), (480, 350), (350, 480)]:
        canvas.draw_primitive_path(f"M {x} {y-10} Q {x} {y} {x+10} {y} Q {x} {y} {x} {y+10} Q {x} {y} {x-10} {y} Q {x} {y} {x} {y-10}", fill="#fcd34d", stroke="none")
    canvas.save()

def build_politician(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    _draw_person_base(canvas, 400, 380, scale=1.3, accent_idx=5, is_active=True)
    # Podium
    canvas.draw_primitive_rect(350, 450, 100, 120, fill="#78350f")
    canvas.draw_primitive_rect(330, 440, 140, 10, fill="#92400e")
    canvas.save()

def build_protester(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    _draw_person_base(canvas, 400, 410, scale=1.4, accent_idx=0, is_active=True)
    # Protest Sign
    canvas.draw_primitive_rect(420, 280, 80, 60, fill="#fecaca", stroke="#dc2626", stroke_width=4)
    canvas.draw_primitive_line((460, 340), (460, 480), stroke="#78350f", stroke_width=6)
    canvas.save()
