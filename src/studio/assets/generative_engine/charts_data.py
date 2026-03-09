"""
FILE: src/studio/assets/generative_engine/charts_data.py
PURPOSE: Procedural geometry builders for Charts & Data Visualization.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

def _draw_axes(canvas: ProceduralCanvas):
    canvas.draw_primitive_line((150, 650), (650, 650), stroke="#475569", stroke_width=6)
    canvas.draw_primitive_line((150, 650), (150, 150), stroke="#475569", stroke_width=6)

def build_line_chart_up(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    _draw_axes(canvas)
    canvas.draw_primitive_path("M 150 600 L 300 450 L 450 500 L 600 200", fill="none", stroke="#10b981", stroke_width=12)
    # Highlight end
    canvas.draw_primitive_circle(600, 200, 15, fill="#34d399", stroke="none")
    # Area under curve
    canvas.draw_primitive_path("M 150 650 L 150 600 L 300 450 L 450 500 L 600 200 L 600 650 Z", fill="#10b981", opacity=0.2, stroke="none")
    canvas.save()

def build_line_chart_down(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_axes(canvas)
    canvas.draw_primitive_path("M 150 200 L 300 350 L 450 300 L 600 600", fill="none", stroke="#ef4444", stroke_width=12)
    canvas.draw_primitive_circle(600, 600, 15, fill="#f87171", stroke="none")
    canvas.save()

def build_bar_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    _draw_axes(canvas)
    data = [120, 250, 180, 400]
    for i, h in enumerate(data):
        canvas.draw_primitive_rect(200 + i * 110, 650 - h, 60, h, fill=get_accent(2))
    canvas.save()

def build_pie_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Outer circle
    canvas.draw_primitive_circle(400, 400, 200, fill="none", stroke="#334155", stroke_width=40)
    # Wedge 1 (25%)
    canvas.draw_primitive_path("M 400 400 L 400 200 A 200 200 0 0 1 600 400 Z", fill="#8b5cf6", stroke="none")
    # Wedge 2 (25%)
    canvas.draw_primitive_path("M 400 400 L 600 400 A 200 200 0 0 1 400 600 Z", fill="#d946ef", stroke="none")
    # Pull-out Piece
    canvas.draw_primitive_path("M 380 380 L 380 180 A 200 200 0 0 0 180 380 Z", fill="#ec4899", stroke="none")
    canvas.save()

def build_inflation_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    _draw_axes(canvas)
    # Balloon inflating over time
    for i in range(4):
        cx = 250 + i * 100
        cy = 550 - i * 80
        r = 20 + i * 20
        canvas.draw_primitive_circle(cx, cy, r, fill="#fb923c", opacity=0.8, stroke="none")
    canvas.save()

def build_price_curve(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    _draw_axes(canvas)
    # Smooth bell curve
    canvas.draw_primitive_path("M 150 630 Q 400 150 650 630", fill="none", stroke="#0ea5e9", stroke_width=12)
    # Point at peak
    canvas.draw_primitive_circle(400, 390, 15, fill="#fcd34d", stroke="none")
    canvas.draw_primitive_line((400, 650), (400, 390), stroke="#475569", stroke_width=4, dasharray="10 10")
    canvas.save()

def build_demand_supply_graph(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    _draw_axes(canvas)
    canvas.draw_primitive_line((200, 200), (600, 600), stroke="#ef4444", stroke_width=10) # Demand
    canvas.draw_primitive_line((200, 600), (600, 200), stroke="#10b981", stroke_width=10) # Supply
    # Intersection Point
    canvas.draw_primitive_circle(400, 400, 20, fill="#fcd34d", stroke="none")
    canvas.save()

def build_economic_cycle_graph(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    _draw_axes(canvas)
    # Sine wave
    d = "M 150 400 C 250 150, 350 650, 450 400 S 550 150, 650 400"
    canvas.draw_primitive_path(d, fill="none", stroke=get_accent(1), stroke_width=12)
    canvas.save()

def build_bubble_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    _draw_axes(canvas)
    bubbles = [(250, 500, 40), (400, 350, 80), (550, 450, 60), (300, 250, 30), (500, 200, 50)]
    for cx, cy, r in bubbles:
        canvas.draw_primitive_circle(cx, cy, r, fill=get_accent(2), opacity=0.7)
    canvas.save()

def build_network_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    nodes = [(400, 400, 40), (250, 300, 30), (550, 300, 30), (250, 500, 30), (550, 500, 30)]
    # Connect edges
    for cx, cy, _ in nodes[1:]:
        canvas.draw_primitive_line((400,400), (cx,cy), stroke="#64748b", stroke_width=8)
    canvas.draw_primitive_line((250,300), (250,500), stroke="#64748b", stroke_width=8)
    canvas.draw_primitive_line((550,300), (550,500), stroke="#64748b", stroke_width=8)
    # Draw Nodes ON TOP
    for cx, cy, r in nodes:
        canvas.draw_primitive_circle(cx, cy, r, fill="#38bdf8")
    canvas.save()

def build_growth_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_path("M 200 600 L 500 300 L 500 450 M 500 300 L 350 300", fill="none", stroke="#10b981", stroke_width=40)
    canvas.save()

def build_decline_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_path("M 200 200 L 500 500 L 500 350 M 500 500 L 350 500", fill="none", stroke="#ef4444", stroke_width=40)
    canvas.save()

def build_trend_line(out_path: str):
    build_line_chart_up(out_path) # Alias
