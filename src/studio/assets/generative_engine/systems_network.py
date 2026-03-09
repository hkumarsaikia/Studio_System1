"""
FILE: src/studio/assets/generative_engine/systems_network.py
PURPOSE: Procedural geometry builders for Systems & Network Diagrams.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

def build_node(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_circle(400, 400, 150, fill="#1e293b", stroke=get_accent(0), stroke_width=20)
    canvas.draw_primitive_circle(400, 400, 80, fill=get_accent(0), stroke="none")
    # Rings
    canvas.draw_primitive_circle(400, 400, 220, fill="none", stroke="#334155", stroke_width=5, dasharray="20 20")
    canvas.draw_primitive_circle(400, 400, 260, fill="none", stroke="#1e293b", stroke_width=5, dasharray="10 30")
    canvas.save()

def build_network_nodes(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    nodes = [(400, 300, 60), (280, 500, 40), (520, 500, 40)]
    # Edges
    canvas.draw_primitive_line((400, 300), (280, 500), stroke="#475569", stroke_width=8)
    canvas.draw_primitive_line((400, 300), (520, 500), stroke="#475569", stroke_width=8)
    canvas.draw_primitive_line((280, 500), (520, 500), stroke="#475569", stroke_width=8)
    # Nodes
    for i, (cx, cy, r) in enumerate(nodes):
        canvas.draw_primitive_circle(cx, cy, r, fill="#1e293b", stroke=get_accent((1+i)%5), stroke_width=10)
    canvas.save()

def build_network_connections(out_path: str):
    build_network_nodes(out_path) # Alias

def build_flow_diagram(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Boxes
    canvas.draw_primitive_rect(200, 350, 100, 100, fill="#1e293b", stroke=get_accent(2), stroke_width=8, rx=10)
    canvas.draw_primitive_rect(500, 350, 100, 100, fill="#1e293b", stroke=get_accent(2), stroke_width=8, rx=10)
    # Connecting Arrows
    canvas.draw_primitive_path("M 320 380 L 480 380 L 460 360 M 480 380 L 460 400", fill="none", stroke="#475569", stroke_width=8)
    canvas.draw_primitive_path("M 480 420 L 320 420 L 340 400 M 320 420 L 340 440", fill="none", stroke="#475569", stroke_width=8)
    canvas.save()

def build_system_loop(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Infinite loop / infinity sign
    d = "M 400 400 C 300 200, 100 200, 200 400 C 300 600, 500 200, 600 400 C 700 600, 500 600, 400 400"
    canvas.draw_primitive_path(d, fill="none", stroke=get_accent(3), stroke_width=20)
    canvas.save()

def build_feedback_loop(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Circle with two arrows chasing
    canvas.draw_primitive_path("M 300 300 A 150 150 0 0 1 500 300 L 470 270 M 500 300 L 470 330", fill="none", stroke=get_accent(4), stroke_width=15)
    canvas.draw_primitive_path("M 500 500 A 150 150 0 0 1 300 500 L 330 530 M 300 500 L 330 470", fill="none", stroke="#475569", stroke_width=15)
    canvas.save()

def build_circular_flow(out_path: str):
    build_feedback_loop(out_path) # Alias

def build_supply_chain(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    nodes = [(200, 400), (400, 400), (600, 400)]
    for i in range(2):
        # Arrows
        x1, y1 = nodes[i]
        x2, y2 = nodes[i+1]
        canvas.draw_primitive_path(f"M {x1+50} {y1} L {x2-50} {y2} L {x2-70} {y2-20} M {x2-50} {y2} L {x2-70} {y2+20}", fill="none", stroke="#475569", stroke_width=8)
    # Boxes (Factory, Truck, Store abstractions)
    canvas.draw_primitive_rect(150, 350, 100, 100, fill=get_accent(5))
    canvas.draw_primitive_rect(350, 360, 100, 80, fill=get_accent(5), rx=10)
    canvas.draw_primitive_rect(550, 330, 100, 120, fill=get_accent(5))
    canvas.save()

def build_hierarchy_pyramid(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_path("M 400 200 L 600 550 L 200 550 Z", fill="none", stroke="#475569", stroke_width=10)
    canvas.draw_primitive_line((315, 400), (485, 400), stroke="#475569", stroke_width=10)
    canvas.draw_primitive_line((260, 500), (540, 500), stroke="#475569", stroke_width=10)
    # Nodes in pyramid
    canvas.draw_primitive_circle(400, 200, 30, fill=get_accent(0))
    canvas.draw_primitive_circle(400, 400, 25, fill="#94a3b8")
    canvas.draw_primitive_circle(315, 550, 20, fill="#cbd5e1")
    canvas.draw_primitive_circle(485, 550, 20, fill="#cbd5e1")
    canvas.save()

def build_decision_tree(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_line((400, 200), (400, 300), stroke="#475569", stroke_width=8)
    canvas.draw_primitive_line((400, 300), (250, 450), stroke="#475569", stroke_width=8)
    canvas.draw_primitive_line((400, 300), (550, 450), stroke="#475569", stroke_width=8)
    
    # Diamond root
    canvas.draw_primitive_path("M 400 150 L 450 200 L 400 250 L 350 200 Z", fill=get_accent(1))
    # Leaf boxes
    canvas.draw_primitive_rect(200, 450, 100, 60, fill="#94a3b8")
    canvas.draw_primitive_rect(500, 450, 100, 60, fill="#94a3b8")
    canvas.save()

def build_domino_chain(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Falling
    canvas.draw_primitive_path("M 200 500 L 250 350 L 300 360 L 250 510 Z", fill="#3b82f6", stroke="#1d4ed8", stroke_width=4)
    canvas.draw_primitive_path("M 300 500 L 370 360 L 420 380 L 350 520 Z", fill="#3b82f6", stroke="#1d4ed8", stroke_width=4)
    # Hit
    canvas.draw_primitive_path("M 430 500 L 520 400 L 570 430 L 480 530 Z", fill="#f43f5e", stroke="#be123c", stroke_width=8)
    # Standing
    canvas.draw_primitive_rect(580, 380, 60, 150, fill="#94a3b8", stroke="#475569", stroke_width=4)
    canvas.save()
