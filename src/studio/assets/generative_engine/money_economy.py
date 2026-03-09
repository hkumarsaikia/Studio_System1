"""
FILE: src/studio/assets/generative_engine/money_economy.py
PURPOSE: Procedural geometry builders for Money & Economy.
"""

from src.studio.assets.generative_engine.core import ProceduralCanvas
from src.studio.assets.generative_engine.theme_utils import get_accent

def _draw_coin(canvas: ProceduralCanvas, cx: int, cy: int, r: int, color: str):
    """Draw a 3D-ish coin using ellipses."""
    # Edge
    canvas.draw_primitive_circle(cx, cy + 5, r, fill="#ca8a04", stroke="none")
    # Face
    canvas.draw_primitive_circle(cx, cy, r, fill=color, stroke="none")
    # Inner ring
    canvas.draw_primitive_circle(cx, cy, r - 10, fill="none", stroke="#fef08a", stroke_width=2)

def build_money_coins(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Stack 1
    for i in range(5):
        _draw_coin(canvas, 300, 480 - i*20, 40, "#fcd34d")
    # Stack 2
    for i in range(3):
        _draw_coin(canvas, 420, 480 - i*20, 40, "#fcd34d")
    # Stack 3
    for i in range(7):
        _draw_coin(canvas, 500, 480 - i*20, 40, "#fcd34d")
    canvas.save()

def build_money_stack(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    for i in range(4):
        y = 450 - i * 30
        canvas.draw_primitive_rect(250, y, 300, 60, fill="#166534", rx=5, stroke="#4ade80", stroke_width=2)
        canvas.draw_primitive_rect(280, y+10, 240, 40, fill="#15803d", rx=2, stroke="none")
        canvas.draw_primitive_circle(400, y+30, 15, fill="#86efac", stroke="none")
    canvas.save()

def build_banknote(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Outer bill
    canvas.draw_primitive_rect(200, 300, 400, 200, fill="#166534", rx=10)
    # Inner decorative rect
    canvas.draw_primitive_rect(220, 320, 360, 160, fill="#15803d", rx=5)
    # Presidential portrait oval
    canvas.draw_primitive_circle(400, 400, 50, fill="#22c55e", stroke="none")
    canvas.draw_primitive_rect(400-20, 400-30, 40, 60, fill="#0f172a", rx=20)
    # Value markers
    for pos in [(250, 350), (550, 350), (250, 450), (550, 450)]:
        canvas.draw_primitive_circle(pos[0], pos[1], 15, fill="none", stroke="#4ade80", stroke_width=2)
    canvas.save()

def build_money_bag(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Tie/top
    canvas.draw_primitive_path("M 350 250 L 450 250 L 420 300 L 380 300 Z", fill="#b45309", stroke="none")
    # Base Bag
    canvas.draw_primitive_path("M 380 300 Q 200 450 300 550 L 500 550 Q 600 450 420 300 Z", fill="#f59e0b", stroke="none")
    # Dollar sign
    canvas.draw_primitive_path("M 400 380 L 400 480", stroke="#78350f", stroke_width=6)
    canvas.draw_primitive_path("M 420 400 Q 380 380 380 430 Q 420 430 420 450 Q 420 480 380 460", fill="none", stroke="#78350f", stroke_width=6)
    canvas.save()

def build_credit_card(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_rect(200, 300, 400, 240, rx=20, fill="#0ea5e9")
    # Chip
    canvas.draw_primitive_rect(250, 380, 60, 45, rx=5, fill="#fcd34d")
    # Lines for chip
    canvas.draw_primitive_line((250, 400), (270, 400), stroke="#b45309", stroke_width=2)
    canvas.draw_primitive_line((290, 400), (310, 400), stroke="#b45309", stroke_width=2)
    # Card Number
    for i in range(4):
        canvas.draw_primitive_rect(250 + i*90, 460, 60, 15, fill="#38bdf8", stroke="none")
    canvas.save()

def build_debit_card(out_path: str):
    build_credit_card(out_path) # Alias

def build_digital_payment(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_rect(300, 250, 200, 350, rx=20, fill="#475569")
    canvas.draw_primitive_rect(320, 270, 160, 280, rx=10, fill="#0f172a", stroke="none")
    # Pay wave
    canvas.draw_primitive_path("M 360 400 Q 400 360 440 400", fill="none", stroke="#10b981", stroke_width=6)
    canvas.draw_primitive_path("M 380 430 Q 400 410 420 430", fill="none", stroke="#10b981", stroke_width=6)
    canvas.save()

def build_interest_symbol(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    canvas.draw_primitive_line((250, 550), (550, 250), stroke=get_accent(0), stroke_width=20)
    canvas.draw_primitive_circle(300, 300, 50, fill="none", stroke=get_accent(0), stroke_width=20)
    canvas.draw_primitive_circle(500, 500, 50, fill="none", stroke=get_accent(0), stroke_width=20)
    canvas.save()

def build_loan_document(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_rect(250, 200, 300, 400, fill="#e2e8f0", stroke="#94a3b8", stroke_width=4)
    # Text lines
    for i in range(5):
        canvas.draw_primitive_rect(280, 260 + i*40, 240 if i%2==0 else 180, 10, fill="#94a3b8", stroke="none")
    # Stamp / Seal
    canvas.draw_primitive_circle(450, 500, 40, fill="#ef4444", stroke="#b91c1c", stroke_width=4)
    canvas.draw_primitive_path("M 430 490 L 470 510 M 470 490 L 430 510", stroke="#fff", stroke_width=4)
    canvas.save()

def build_debt_chain(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Chain Links
    for x in [250, 400, 550]:
        canvas.draw_primitive_rect(x, 350, 120, 60, rx=30, fill="none", stroke="#64748b", stroke_width=20)
    # Heavy Weight
    canvas.draw_primitive_path("M 300 410 L 400 550 L 500 410 Z", fill="#334155", stroke="none")
    canvas.draw_primitive_circle(400, 450, 15, fill="#94a3b8", stroke="none")
    canvas.save()

def build_tax_symbol(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Scissors cutting a bill
    canvas.draw_primitive_rect(300, 350, 300, 150, fill="#22c55e", rx=5, stroke="none")
    # Scissor blades
    canvas.draw_primitive_line((150, 300), (450, 450), stroke="#94a3b8", stroke_width=15)
    canvas.draw_primitive_line((150, 450), (450, 300), stroke="#94a3b8", stroke_width=15)
    canvas.draw_primitive_circle(200, 320, 40, fill="none", stroke="#ef4444", stroke_width=15)
    canvas.draw_primitive_circle(200, 430, 40, fill="none", stroke="#ef4444", stroke_width=15)
    canvas.save()

def build_cash_register(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    canvas.draw_primitive_rect(250, 400, 300, 150, fill="#475569")
    canvas.draw_primitive_rect(300, 250, 200, 150, fill="#334155")
    # Display
    canvas.draw_primitive_rect(320, 270, 160, 40, fill="#0ea5e9", stroke="none")
    canvas.draw_primitive_path("M 350 300 L 400 280 L 450 300 L 400 290 Z", stroke="#fff", stroke_width=2)
    # Buttons
    for r in range(2):
        for c in range(4):
            canvas.draw_primitive_rect(320 + c*40, 330 + r*30, 20, 15, fill="#94a3b8", stroke="none")
    # Drawer
    canvas.draw_primitive_rect(280, 450, 240, 50, fill="#1e293b", rx=5)
    canvas.save()

def build_price_tag(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    canvas.draw_primitive_path("M 400 200 L 550 300 L 400 550 L 250 450 Z", fill=get_accent(5), stroke="none")
    canvas.draw_primitive_circle(400, 260, 20, fill="#334155", stroke="none")
    # String
    canvas.draw_primitive_path("M 400 260 Q 300 150 450 100", fill="none", stroke="#94a3b8", stroke_width=4)
    canvas.save()

def build_shopping_cart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Basket
    canvas.draw_primitive_path("M 250 250 L 550 250 L 500 450 L 300 450 Z", fill="none", stroke="#0ea5e9", stroke_width=10)
    for i in range(1, 4):
        canvas.draw_primitive_line((250 + i*75, 250), (300 + i*50, 450), stroke="#0ea5e9", stroke_width=5)
        canvas.draw_primitive_line((260, 250 + i*50), (530, 250 + i*50), stroke="#0ea5e9", stroke_width=5)
    # Wheels
    canvas.draw_primitive_circle(320, 500, 30, fill="#475569")
    canvas.draw_primitive_circle(480, 500, 30, fill="#475569")
    # Handle
    canvas.draw_primitive_path("M 250 250 L 200 180 L 150 180", fill="none", stroke="#0ea5e9", stroke_width=10)
    canvas.save()

def build_wallet(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_rect(200, 300, 400, 200, rx=20, fill="#92400e", stroke="none")
    canvas.draw_primitive_rect(450, 350, 150, 100, rx=10, fill="#78350f", stroke="none")
    # Money sticking out
    canvas.draw_primitive_rect(250, 250, 200, 100, fill="#22c55e", rx=5, stroke="none")
    canvas.save()

def build_investment_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    canvas.draw_primitive_line((200, 600), (600, 600), stroke="#94a3b8", stroke_width=8)
    canvas.draw_primitive_line((200, 600), (200, 200), stroke="#94a3b8", stroke_width=8)
    canvas.draw_primitive_path("M 200 550 L 300 450 L 400 500 L 550 250", fill="none", stroke="#3b82f6", stroke_width=12)
    # Arrow head
    canvas.draw_primitive_path("M 530 250 L 550 250 L 550 270", fill="none", stroke="#3b82f6", stroke_width=12)
    canvas.save()

def build_wealth_pyramid(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Bottom
    canvas.draw_primitive_path("M 200 550 L 600 550 L 500 450 L 300 450 Z", fill="#0f172a", stroke="#334155", stroke_width=4)
    # Middle
    canvas.draw_primitive_path("M 300 450 L 500 450 L 430 350 L 370 350 Z", fill="#1e293b", stroke="#334155", stroke_width=4)
    # Top
    canvas.draw_primitive_path("M 370 350 L 430 350 L 400 250 Z", fill="#f59e0b", stroke="#b45309", stroke_width=4)
    canvas.save()

def build_income_arrow(out_path: str):
    build_investment_chart(out_path) # Alias

def build_salary_icon(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(4))
    # Envelope
    canvas.draw_primitive_rect(200, 350, 400, 200, fill="#e2e8f0", stroke="#cbd5e1", stroke_width=6)
    canvas.draw_primitive_path("M 200 350 L 400 500 L 600 350 Z", fill="#f1f5f9", stroke="#cbd5e1", stroke_width=6)
    # Cash
    canvas.draw_primitive_rect(300, 300, 200, 100, fill="#22c55e", rx=5, stroke="none")
    canvas.draw_primitive_circle(400, 350, 20, fill="#166534", stroke="none")
    canvas.save()

def build_stock_market(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(5))
    # Building columns
    for x in [300, 360, 420, 480]:
        canvas.draw_primitive_rect(x, 400, 30, 150, fill="#cbd5e1", stroke="none")
    canvas.draw_primitive_rect(250, 550, 300, 20, fill="#94a3b8", stroke="none")
    # Classical roof
    canvas.draw_primitive_path("M 220 400 L 400 300 L 580 400 Z", fill="#475569", stroke="none")
    # Red/Green Up/Down arrows overlaid
    canvas.draw_primitive_path("M 350 350 L 380 280 L 400 320", fill="none", stroke="#22c55e", stroke_width=8)
    canvas.save()

def build_stock_chart(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(0))
    # Candlesticks
    def candlestick(x, y, h, is_up):
        color = "#22c55e" if is_up else "#ef4444"
        canvas.draw_primitive_line((x, y-20), (x, y+h+20), stroke=color, stroke_width=4)
        canvas.draw_primitive_rect(x-15, y, 30, h, fill=color, stroke="none")
        
    candlestick(250, 400, 100, True)
    candlestick(350, 300, 150, True)
    candlestick(450, 350, 120, False)
    candlestick(550, 200, 180, True)
    canvas.save()

def build_gold_bar(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(1))
    canvas.draw_primitive_path("M 250 450 L 550 450 L 600 350 L 200 350 Z", fill="#f59e0b", stroke="#b45309", stroke_width=4)
    canvas.draw_primitive_path("M 250 450 L 200 350 L 250 350 Z", fill="#d97706", stroke="none") # Shadow side
    canvas.draw_primitive_path("M 550 450 L 600 350 L 550 350 Z", fill="#fbbf24", stroke="none") # Highlight side
    canvas.draw_primitive_path("M 250 350 L 550 350 L 500 280 L 300 280 Z", fill="#fcd34d", stroke="#b45309", stroke_width=4) # Top
    canvas.save()

def build_crypto_coin(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(2))
    # Outer coin
    canvas.draw_primitive_circle(400, 400, 150, fill="#f59e0b", stroke="#b45309", stroke_width=10)
    canvas.draw_primitive_circle(400, 400, 130, fill="#fcd34d", stroke="#d97706", stroke_width=5)
    # B Symbol
    canvas.draw_primitive_path("M 350 300 L 350 500 M 350 300 Q 450 300 450 400 Q 350 400 350 400 M 350 400 Q 480 400 480 500 Q 350 500 350 500", fill="none", stroke="#b45309", stroke_width=20)
    canvas.draw_primitive_line((370, 270), (370, 530), stroke="#b45309", stroke_width=10)
    canvas.draw_primitive_line((410, 270), (410, 530), stroke="#b45309", stroke_width=10)
    canvas.save()

def build_blockchain_symbol(out_path: str):
    canvas = ProceduralCanvas(out_path, get_accent(3))
    # Three connected blocks
    def block(x, y):
        canvas.draw_primitive_rect(x, y, 80, 80, fill="#0284c7", rx=10, stroke="#38bdf8", stroke_width=4)
        canvas.draw_primitive_circle(x+40, y+40, 20, fill="#bae6fd", stroke="none")
        
    block(250, 360)
    block(460, 250)
    block(460, 470)
    
    # Connecting chains
    canvas.draw_primitive_line((330, 400), (460, 290), stroke="#94a3b8", stroke_width=10)
    canvas.draw_primitive_line((330, 400), (460, 510), stroke="#94a3b8", stroke_width=10)
    canvas.save()
