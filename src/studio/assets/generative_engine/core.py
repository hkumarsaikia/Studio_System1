"""
FILE: src/studio/assets/generative_engine/core.py
PURPOSE: The core procedural geometry builder. Wraps svgwrite 
to provide high-level drawing primitives with automatic Studio THEME styling.
"""

import svgwrite
from src.studio.assets.generative_engine.theme_utils import (
    get_bg_gradient_stops,
    get_canvas_size,
    get_stroke,
    get_stroke_width,
)

class ProceduralCanvas:
    def __init__(self, output_path: str, accent_color: str, add_glow: bool = True):
        self.w, self.h = get_canvas_size()
        self.dwg = svgwrite.Drawing(output_path, size=(self.w, self.h), profile='full')
        self.dwg.viewbox(width=self.w, height=self.h)
        self.accent_color = accent_color
        self.stroke_color = get_stroke()
        self.stroke_width = get_stroke_width()
        
        # 1. Base Tile Gradient (Diagonal Glass Style)
        self.base_grad = self.dwg.linearGradient(id="baseGrad", start=(0, 0), end=(1, 1))
        bg_start, bg_end = get_bg_gradient_stops()
        self.base_grad.add_stop_color(0.0, bg_start)
        self.base_grad.add_stop_color(0.6, bg_start)
        self.base_grad.add_stop_color(1.0, bg_end)
        self.dwg.defs.add(self.base_grad)

        # 1b. Metallic/Glass Rim Gradient for all geometry
        self.stroke_grad = self.dwg.linearGradient(id="strokeGrad", start=(0, 0), end=(1, 1))
        self.stroke_grad.add_stop_color(0.0, "#ffffff", opacity=0.9)
        self.stroke_grad.add_stop_color(0.5, self.stroke_color, opacity=0.6)
        self.stroke_grad.add_stop_color(1.0, self.stroke_color, opacity=0.2)
        self.dwg.defs.add(self.stroke_grad)
        
        # Override baseline stroke color to use the new metallic gradient
        self.stroke_color = "url(#strokeGrad)"

        # 2. Accent Glow Gradient (Radial)
        self.glow_grad = self.dwg.radialGradient(id="glowGrad", center=(0.5, 0.5), r=0.5)
        self.glow_grad.add_stop_color(0.0, self.accent_color, opacity=0.4)
        self.glow_grad.add_stop_color(1.0, self.accent_color, opacity=0.0)
        self.dwg.defs.add(self.glow_grad)

        # 3. Soft Drop Shadow for all main items (SVG 1.1 compatible)
        self.drop_shadow = self.dwg.filter(id="dropShadow", x="-30%", y="-30%", width="160%", height="160%")
        self.drop_shadow.feGaussianBlur(in_="SourceAlpha", stdDeviation=25, result="blur")
        self.drop_shadow.feOffset(in_="blur", dx=0, dy=20, result="offsetBlur")
        self.drop_shadow.feFlood(flood_color="#000000", flood_opacity=0.6, result="shadowColor")
        self.drop_shadow.feComposite(in_="shadowColor", in2="offsetBlur", operator="in", result="shadow")
        self.drop_shadow.feMerge(["shadow", "SourceGraphic"])
        self.dwg.defs.add(self.drop_shadow)

        # 4. Dot Grid Pattern for tech aesthetic
        self.grid_pattern = self.dwg.pattern(id="dotGrid", width=40, height=40, patternUnits="userSpaceOnUse")
        self.grid_pattern.add(self.dwg.circle(center=(20, 20), r=2, fill="#ffffff", opacity=0.08))
        self.dwg.defs.add(self.grid_pattern)

        # Draw the standard background tile
        self._draw_background_tile(add_glow)

    def _draw_background_tile(self, add_glow: bool):
        # 1. Deep Glow (moved further back, wider radius)
        if add_glow:
            glow = self.dwg.circle(
                center=(400, 400), 
                r=380, 
                fill="url(#glowGrad)"
            )
            self.dwg.add(glow)

        # 2. Cyber/Tech Orbit Rings (more complex layered arrays)
        for r, op, dash, w in [(240, 0.15, "", 1.5), (320, 0.25, "8 16", 2), (400, 0.08, "2 8", 4)]:
            kwargs = {
                "center": (400, 400), "r": r, "fill": "none", 
                "stroke": self.accent_color, "stroke_width": w, "opacity": op
            }
            if dash:
                kwargs["stroke_dasharray"] = dash
            self.dwg.add(self.dwg.circle(**kwargs))

        # 3. Floating Rounded Tile
        tile_base = self.dwg.rect(
            insert=(100, 100), 
            size=(600, 600), 
            rx=120, 
            fill="url(#baseGrad)", 
            stroke="url(#strokeGrad)", 
            stroke_width=self.stroke_width,
            filter="url(#dropShadow)"
        )
        self.dwg.add(tile_base)

        # 4. Inset Tech Border (HUD aesthetic)
        inset_rect = self.dwg.rect(
            insert=(130, 130),
            size=(540, 540),
            rx=90,
            fill="none",
            stroke=self.accent_color,
            stroke_width=1.5,
            opacity=0.3,
            stroke_dasharray="4 8"
        )
        self.dwg.add(inset_rect)

        # 5. Corner HUD Crosshairs
        for cx, cy in [(130, 130), (670, 130), (130, 670), (670, 670)]:
            self.dwg.add(self.dwg.circle(center=(cx, cy), r=5, fill=self.accent_color, opacity=0.9))
            self.dwg.add(self.dwg.path(d=f"M {cx-18} {cy} L {cx+18} {cy} M {cx} {cy-18} L {cx} {cy+18}", 
                                       stroke=self.accent_color, stroke_width=2, opacity=0.6))

        # 6. Grid Overlay on the tile
        tile_grid = self.dwg.rect(
            insert=(100, 100),
            size=(600, 600),
            rx=120,
            fill="url(#dotGrid)"
        )
        self.dwg.add(tile_grid)

        # 7. Abstract Floating Geometric Data Nodes (Neural Network accents)
        node_group = self.dwg.g(opacity=0.5)
        for d in [
            "M 200 250 L 280 200 L 350 280 Z",
            "M 600 550 L 520 600 L 450 520 Z"
        ]:
            node_group.add(self.dwg.path(d=d, fill="none", stroke=self.accent_color, stroke_width=1.5, stroke_dasharray="4 4"))
        for cx, cy in [(200, 250), (280, 200), (350, 280), (600, 550), (520, 600), (450, 520)]:
            node_group.add(self.dwg.circle(center=(cx, cy), r=6, fill="url(#baseGrad)", stroke=self.accent_color, stroke_width=2))
        self.dwg.add(node_group)

        # 8. Glassmorphism top highlight simulating glass curve
        highlight_d = "M 100 220 Q 400 -20 700 220 L 700 300 Q 400 80 100 300 Z"
        glass_highlight = self.dwg.path(d=highlight_d, fill="#ffffff", opacity=0.06)
        self.dwg.add(glass_highlight)

        # Setup main group for items with the drop shadow applied so all geometry pops out
        self.main_group = self.dwg.g(id="ProceduralItems", filter="url(#dropShadow)")
        self.dwg.add(self.main_group)

    def _process_kwargs(self, kwargs):
        if "dasharray" in kwargs:
            kwargs["stroke_dasharray"] = kwargs.pop("dasharray")
        return kwargs

    def draw_primitive_rect(self, x, y, w, h, rx=0, fill="none", stroke=None, stroke_width=None, **kwargs):
        """Draw a styled rectangle."""
        kwargs = self._process_kwargs(kwargs)
        rect = self.dwg.rect(
            insert=(x, y), 
            size=(w, h), 
            rx=rx, 
            fill=fill,
            stroke=stroke or self.stroke_color,
            stroke_width=stroke_width or self.stroke_width,
            **kwargs
        )
        self.main_group.add(rect)
        return rect

    def draw_primitive_circle(self, cx, cy, r, fill="none", stroke=None, stroke_width=None, **kwargs):
        """Draw a styled circle."""
        kwargs = self._process_kwargs(kwargs)
        circle = self.dwg.circle(
            center=(cx, cy), 
            r=r, 
            fill=fill,
            stroke=stroke or self.stroke_color,
            stroke_width=stroke_width or self.stroke_width,
            **kwargs
        )
        self.main_group.add(circle)
        return circle

    def draw_primitive_ellipse(self, center, r, fill="none", stroke=None, stroke_width=None, **kwargs):
        """Draw a styled ellipse."""
        kwargs = self._process_kwargs(kwargs)
        ellipse = self.dwg.ellipse(
            center=center, 
            r=r, 
            fill=fill,
            stroke=stroke or self.stroke_color,
            stroke_width=stroke_width or self.stroke_width,
            **kwargs
        )
        self.main_group.add(ellipse)
        return ellipse

    def draw_primitive_line(self, start, end, stroke=None, stroke_width=None, dasharray=None, **kwargs):
        """Draw a styled line."""
        line_kwargs = {
            "stroke": stroke or self.stroke_color,
            "stroke_width": stroke_width or self.stroke_width,
            "stroke_linecap": "round",
            "stroke_linejoin": "round"
        }
        if dasharray:
            line_kwargs["stroke_dasharray"] = dasharray
        line_kwargs.update(self._process_kwargs(kwargs))
            
        line = self.dwg.line(start=start, end=end, **line_kwargs)
        self.main_group.add(line)
        return line

    def draw_primitive_path(self, d, fill="none", stroke=None, stroke_width=None, **kwargs):
        """Draw a styled custom path."""
        path_kwargs = {
            "fill": fill,
            "stroke": stroke or self.stroke_color,
            "stroke_width": stroke_width or self.stroke_width,
            "stroke_linecap": "round",
            "stroke_linejoin": "round"
        }
        path_kwargs.update(self._process_kwargs(kwargs))
        
        path = self.dwg.path(d=d, **path_kwargs)
        self.main_group.add(path)
        return path

    def save(self):
        self.dwg.save()
