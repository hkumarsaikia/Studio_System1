"""
FILE: src/studio/assets/generative_engine/work_tech_social.py
PURPOSE: Procedural geometry builders for Work, Technology, and Social Media.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent
from src.studio.assets.generative_engine.charts_data import build_network_chart

# --- 7. Work & Productivity ---

def build_briefcase(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_rect(200, 350, 400, 250, fill=get_accent(0), rx=10)
    canvas.draw_primitive_rect(350, 300, 100, 50, fill="none", stroke="#94a3b8", stroke_width=15, rx=10)
    canvas.draw_primitive_rect(380, 450, 40, 50, fill="#334155")
    canvas.save()

def build_office_desk(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_line((200, 500), (600, 500), stroke="#94a3b8", stroke_width=20)
    canvas.draw_primitive_line((250, 500), (250, 650), stroke="#475569", stroke_width=15)
    canvas.draw_primitive_line((550, 500), (550, 650), stroke="#475569", stroke_width=15)
    # Monitor
    canvas.draw_primitive_rect(330, 350, 140, 100, fill="#1e293b", rx=5)
    canvas.draw_primitive_rect(390, 450, 20, 50, fill="#334155")
    canvas.save()

def build_laptop(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_rect(250, 300, 300, 200, fill="#1e293b", rx=10)
    canvas.draw_primitive_rect(200, 500, 400, 20, fill="#94a3b8", rx=10)
    canvas.draw_primitive_circle(400, 400, 30, fill="#38bdf8", stroke="none")
    canvas.save()

def build_email(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    canvas.draw_primitive_rect(200, 300, 400, 250, fill="#e2e8f0", stroke="#cbd5e1", stroke_width=10, rx=10)
    canvas.draw_primitive_path("M 200 300 L 400 450 L 600 300", fill="none", stroke="#94a3b8", stroke_width=10)
    canvas.save()

def build_meeting_table(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_ellipse((400, 450), (250, 80), fill="#64748b", stroke="none")
    # People around it
    for px, py in [(200, 450), (600, 450), (300, 350), (500, 350), (400, 550)]:
        canvas.draw_primitive_circle(px, py, 30, fill=get_accent(4), stroke="none")
    canvas.save()

def build_task_list(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_rect(250, 200, 300, 400, fill="#f8fafc", rx=10)
    for i in range(4):
        y = 280 + i * 80
        # Checkbox
        canvas.draw_primitive_rect(300, y, 30, 30, fill="none", stroke="#94a3b8", stroke_width=4)
        if i % 2 == 0:
            canvas.draw_primitive_path(f"M 305 {y+15} L 315 {y+25} L 335 {y+5}", fill="none", stroke="#22c55e", stroke_width=6)
        # Line
        canvas.draw_primitive_line((350, y+15), (500, y+15), stroke="#cbd5e1", stroke_width=15)
    canvas.save()

def build_calendar(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_rect(250, 250, 300, 300, fill="#f1f5f9", rx=15)
    canvas.draw_primitive_rect(250, 250, 300, 80, fill="#ef4444", rx=15)
    # Rings
    canvas.draw_primitive_line((300, 230), (300, 270), stroke="#94a3b8", stroke_width=15)
    canvas.draw_primitive_line((500, 230), (500, 270), stroke="#94a3b8", stroke_width=15)
    # Grid
    for r in range(3):
        for c in range(3):
            canvas.draw_primitive_rect(280 + c*80, 360 + r*60, 40, 30, fill="#cbd5e1" if (r+c)%2==0 else "#94a3b8")
    canvas.save()

def build_clock(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_circle(400, 400, 150, fill="#f8fafc", stroke="#334155", stroke_width=20)
    canvas.draw_primitive_line((400, 400), (400, 300), stroke="#ef4444", stroke_width=8)
    canvas.draw_primitive_line((400, 400), (480, 450), stroke="#334155", stroke_width=12)
    canvas.draw_primitive_circle(400, 400, 15, fill="#334155")
    canvas.save()

def build_overtime_clock(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_circle(400, 400, 150, fill="#f8fafc", stroke="#ef4444", stroke_width=20)
    canvas.draw_primitive_line((400, 400), (400, 300), stroke="#ef4444", stroke_width=8)
    canvas.draw_primitive_line((400, 400), (520, 400), stroke="#ef4444", stroke_width=12)
    # Speed lines
    for rot in range(0, 360, 45):
        canvas.dwg.add(canvas.dwg.line(start=(600, 400), end=(650, 400), stroke="#fcd34d", stroke_width=5, transform=f"rotate({rot} 400 400)"))
    canvas.save()

def build_career_ladder(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    canvas.draw_primitive_line((300, 650), (400, 200), stroke="#475569", stroke_width=15)
    canvas.draw_primitive_line((500, 650), (600, 200), stroke="#475569", stroke_width=15)
    for i in range(5):
        y = 600 - i * 80
        x_start = 300 + i * 20
        x_end = 500 + i * 20
        canvas.draw_primitive_line((x_start, y), (x_end, y), stroke="#94a3b8", stroke_width=10)
    canvas.save()

def build_promotion_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_path("M 400 600 L 400 300", stroke="#3b82f6", stroke_width=40)
    canvas.draw_primitive_path("M 300 350 L 400 200 L 500 350 Z", fill="#3b82f6", stroke="none")
    # Stars
    canvas.draw_primitive_circle(300, 250, 15, fill="#fcd34d")
    canvas.draw_primitive_circle(500, 250, 15, fill="#fcd34d")
    canvas.save()

def build_burnout_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_circle(400, 450, 80, fill="#f87171", stroke="none")
    # Flame on top
    d_flame = "M 400 250 Q 300 350 350 400 Q 400 380 400 420 Q 450 350 400 250"
    canvas.draw_primitive_path(d_flame, fill="#fcd34d", stroke="none")
    canvas.draw_primitive_path("M 350 420 L 450 480 M 350 480 L 450 420", stroke="#475569", stroke_width=10) # Dead eyes
    canvas.save()

# --- 8. Technology & Internet ---

def build_smartphone(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_rect(280, 200, 240, 450, rx=30, fill="#1e293b", stroke="#475569", stroke_width=10)
    canvas.draw_primitive_rect(300, 240, 200, 360, rx=10, fill="#0ea5e9", stroke="none")
    # Home button
    canvas.draw_primitive_circle(400, 625, 12, fill="#475569")
    canvas.save()

def build_app_grid(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    for r in range(3):
        for c in range(3):
            canvas.draw_primitive_rect(250 + c*110, 250 + r*110, 80, 80, rx=20, fill=get_accent((r+c)%6))
    canvas.save()

def build_notification_bell(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_path("M 300 450 Q 400 150 500 450 L 550 450 L 550 500 L 250 500 L 250 450 Z", fill="#fcd34d", stroke="none")
    canvas.draw_primitive_circle(400, 500, 30, fill="#f59e0b")
    # Notification dot
    canvas.draw_primitive_circle(520, 280, 30, fill="#ef4444", stroke="#fff", stroke_width=5)
    canvas.save()

def build_algorithm_symbol(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Brackets and gear
    canvas.draw_primitive_path("M 300 250 L 200 400 L 300 550", fill="none", stroke="#0ea5e9", stroke_width=20)
    canvas.draw_primitive_path("M 500 250 L 600 400 L 500 550", fill="none", stroke="#0ea5e9", stroke_width=20)
    canvas.draw_primitive_circle(400, 400, 50, fill="#1e293b", stroke="#94a3b8", stroke_width=15)
    canvas.save()

def build_ai_brain(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Abstract brain
    canvas.draw_primitive_path("M 400 250 C 250 250, 200 400, 400 550", fill="none", stroke="#d946ef", stroke_width=25)
    canvas.draw_primitive_path("M 400 250 C 550 250, 600 400, 400 550", fill="none", stroke="#d946ef", stroke_width=25)
    # Nodes attached
    for y in [300, 400, 500]:
        canvas.draw_primitive_circle(400, y, 15, fill="#fcd34d")
    canvas.save()

def build_robot(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_rect(300, 300, 200, 150, rx=30, fill="#475569")
    canvas.draw_primitive_rect(350, 450, 100, 80, rx=10, fill="#334155")
    # Eyes
    canvas.draw_primitive_circle(360, 380, 20, fill="#38bdf8")
    canvas.draw_primitive_circle(440, 380, 20, fill="#38bdf8")
    # Antenna
    canvas.draw_primitive_line((400, 300), (400, 220), stroke="#94a3b8", stroke_width=8)
    canvas.draw_primitive_circle(400, 220, 15, fill="#ef4444")
    canvas.save()

def build_data_cloud(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_circle(300, 450, 80, fill="#bae6fd", stroke="none")
    canvas.draw_primitive_circle(500, 450, 80, fill="#bae6fd", stroke="none")
    canvas.draw_primitive_circle(400, 350, 120, fill="#bae6fd", stroke="none")
    canvas.draw_primitive_rect(280, 400, 240, 130, fill="#bae6fd", stroke="none")
    # Nodes in cloud
    for x in [350, 400, 450]:
        canvas.draw_primitive_rect(x, 420, 10, 40, fill="#0284c7")
    canvas.save()

def build_server(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    for i in range(3):
        y = 300 + i*100
        canvas.draw_primitive_rect(250, y, 300, 60, rx=5, fill="#1e293b", stroke="#475569", stroke_width=5)
        canvas.draw_primitive_circle(280, y+30, 8, fill="#22c55e")
        canvas.draw_primitive_circle(310, y+30, 8, fill="#22c55e")
        canvas.draw_primitive_circle(340, y+30, 8, fill="#ef4444" if i==1 else "#22c55e")
    canvas.save()

def build_database(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    for i in range(3):
        y = 300 + i*80
        canvas.draw_primitive_ellipse((400, y+40), (150, 40), fill="#0f172a", stroke="none")
        canvas.draw_primitive_rect(250, y, 300, 40, fill="#475569", stroke="#94a3b8", stroke_width=4)
        canvas.draw_primitive_ellipse((400, y), (150, 40), fill="#94a3b8", stroke="none")
    canvas.save()

def build_internet_globe(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    canvas.draw_primitive_circle(400, 400, 200, fill="none", stroke="#0ea5e9", stroke_width=20)
    canvas.draw_primitive_ellipse((400, 400), (200, 80), fill="none", stroke="#0ea5e9", stroke_width=10)
    canvas.draw_primitive_ellipse((400, 400), (80, 200), fill="none", stroke="#0ea5e9", stroke_width=10)
    # Highlight
    canvas.draw_primitive_circle(300, 300, 20, fill="#bae6fd")
    canvas.save()

def build_wifi_signal(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_circle(400, 550, 30, fill=get_accent(4))
    for r in [120, 220, 320]:
        canvas.draw_primitive_path(f"M {400-r} {550-r} A {r*1.4} {r*1.4} 0 0 1 {400+r} {550-r}", fill="none", stroke=get_accent(4), stroke_width=25, stroke_linecap="round")
    canvas.save()

def build_cybersecurity_lock(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    # Shackle
    canvas.draw_primitive_path("M 300 350 L 300 250 A 100 100 0 0 1 500 250 L 500 350", fill="none", stroke="#94a3b8", stroke_width=30)
    # Body
    canvas.draw_primitive_rect(250, 350, 300, 200, rx=20, fill="#f59e0b")
    # Keyhole
    canvas.draw_primitive_circle(400, 420, 30, fill="#1e293b")
    canvas.draw_primitive_path("M 380 420 L 420 420 L 410 500 L 390 500 Z", fill="#1e293b", stroke="none")
    canvas.save()

def build_code_symbol(out_path: str):
    build_algorithm_symbol(out_path) # Alias

# --- 9. Social Media System ---

def build_like_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    # Thumbs up geometric
    canvas.draw_primitive_rect(250, 350, 80, 150, fill="#3b82f6", rx=10)
    canvas.draw_primitive_path("M 330 350 L 450 350 Q 500 350 500 300 Q 500 250 450 250 L 380 250 L 380 200 Q 380 150 330 150 Z", fill="#3b82f6", stroke="none")
    canvas.draw_primitive_rect(330, 380, 200, 120, fill="#3b82f6", rx=20)
    canvas.save()

def build_comment_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1), add_glow=False)
    canvas.draw_primitive_rect(250, 300, 300, 200, rx=40, fill="#4ade80")
    canvas.draw_primitive_path("M 300 500 L 250 550 L 250 450", fill="#4ade80", stroke="none")
    # Dots
    for x in [350, 400, 450]:
        canvas.draw_primitive_circle(x, 400, 15, fill="#fff", stroke="none")
    canvas.save()

def build_share_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2), add_glow=False)
    canvas.draw_primitive_line((300, 300), (500, 400), stroke="#94a3b8", stroke_width=15)
    canvas.draw_primitive_line((300, 500), (500, 400), stroke="#94a3b8", stroke_width=15)
    canvas.draw_primitive_circle(300, 300, 40, fill="#0ea5e9")
    canvas.draw_primitive_circle(300, 500, 40, fill="#0ea5e9")
    canvas.draw_primitive_circle(500, 400, 40, fill="#0ea5e9")
    canvas.save()

def build_follower_counter(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3), add_glow=False)
    # People + Shield/Badge
    canvas.draw_primitive_circle(350, 350, 40, fill="#8b5cf6")
    canvas.draw_primitive_path("M 250 500 Q 350 400 450 500 Z", fill="#8b5cf6", stroke="none")
    # Counter badge
    canvas.draw_primitive_rect(420, 280, 120, 60, rx=30, fill="#ef4444")
    canvas.draw_primitive_line((450, 310), (510, 310), stroke="#fff", stroke_width=10) # Dummy number
    canvas.save()

def build_social_network_graph(out_path: str):
    build_network_chart(out_path) # Alias

def build_hashtag_symbol(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4), add_glow=False)
    for x in [350, 450]:
        canvas.dwg.add(canvas.dwg.line(start=(x, 250), end=(x, 550), stroke="#1e293b", stroke_width=40, transform="skewX(-10)"))
    for y in [350, 450]:
        canvas.draw_primitive_line((250, y), (550, y), stroke="#1e293b", stroke_width=40)
    canvas.save()

def build_viral_arrow(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5), add_glow=False)
    # Huge zig zag
    canvas.draw_primitive_path("M 200 500 L 350 450 L 450 600 L 600 200", fill="none", stroke="#f59e0b", stroke_width=30)
    # Flame on tip
    canvas.draw_primitive_circle(600, 200, 40, fill="#ef4444")
    canvas.save()

def build_content_feed(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0), add_glow=False)
    for i in range(3):
        y = 200 + i*130
        canvas.draw_primitive_rect(300, y, 200, 100, rx=10, fill="#334155")
        canvas.draw_primitive_circle(330, y+30, 15, fill="#94a3b8")
        canvas.draw_primitive_line((360, y+30), (450, y+30), stroke="#94a3b8", stroke_width=8)
    canvas.save()

def build_notification_pop(out_path: str):
    build_notification_bell(out_path) # Alias

def build_creator_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1), add_glow=False)
    # Paint palette/digital creator
    canvas.draw_primitive_circle(400, 400, 150, fill="#d946ef")
    canvas.draw_primitive_circle(320, 350, 30, fill="#fff")
    canvas.draw_primitive_circle(400, 320, 30, fill="#fff")
    canvas.draw_primitive_circle(480, 380, 30, fill="#fff")
    canvas.draw_primitive_circle(380, 480, 25, fill="#b45309", stroke="#fff", stroke_width=5) # Thumb hole
    canvas.save()

def build_camera_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2), add_glow=False)
    canvas.draw_primitive_rect(250, 350, 300, 200, rx=20, fill="#1e293b")
    canvas.draw_primitive_rect(350, 300, 100, 50, rx=10, fill="#334155")
    canvas.draw_primitive_circle(400, 450, 60, fill="none", stroke="#0ea5e9", stroke_width=20)
    canvas.draw_primitive_circle(400, 450, 20, fill="#38bdf8")
    canvas.save()

def build_video_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3), add_glow=False)
    canvas.draw_primitive_rect(250, 300, 250, 200, rx=20, fill="#f43f5e")
    canvas.draw_primitive_path("M 530 350 L 600 300 L 600 500 L 530 450 Z", fill="#f43f5e", stroke="none")
    canvas.save()

def build_live_stream_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4), add_glow=False)
    canvas.draw_primitive_circle(400, 400, 40, fill="#ef4444")
    for r in [80, 120, 160]:
        canvas.draw_primitive_circle(400, 400, r, fill="none", stroke="#ef4444", stroke_width=8, dasharray="20 40")
    # "LIVE" box
    canvas.draw_primitive_rect(350, 480, 100, 40, rx=5, fill="#ef4444")
    canvas.save()

def build_trend_arrow(out_path: str):
    build_viral_arrow(out_path) # Alias
