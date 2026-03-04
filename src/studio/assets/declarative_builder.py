import os
import svgwrite
from svgwrite import cm, mm

def build_declarative_prop(output_path: str, prop_type: str = "Robot"):
    """
    Generates an SVG using a highly declarative, object-oriented approach
    via the svgwrite library, eliminating brittle string formatting.
    """
    # 1. Initialize the drawing object
    dwg = svgwrite.Drawing(output_path, size=(800, 800), profile='tiny')
    dwg.viewbox(width=800, height=800)

    # 2. Reusable style definitions (Gradients)
    metal_grad = dwg.linearGradient(id="metalGrad", start=(0, 0), end=(1, 1))
    metal_grad.add_stop_color(0.0, '#94a3b8')
    metal_grad.add_stop_color(1.0, '#475569')
    dwg.defs.add(metal_grad)

    glow_grad = dwg.radialGradient(id="glowGrad", center=(0.5, 0.5), r=0.5)
    glow_grad.add_stop_color(0.0, '#38bdf8')
    glow_grad.add_stop_color(1.0, '#0284c7')
    dwg.defs.add(glow_grad)

    if prop_type == "Robot":
        # Using SVGWrite groupings for modular architecture
        robot_group = dwg.g(id="robot")

        # Head / Base
        head = dwg.rect(insert=(250, 200), size=(300, 250), rx=40, fill="url(#metalGrad)")
        robot_group.add(head)

        # Antenna
        antenna_stem = dwg.line(start=(400, 200), end=(400, 100), stroke="#334155", stroke_width=10)
        robot_group.add(antenna_stem)
        
        antenna_bulb = dwg.circle(center=(400, 100), r=25, fill="url(#glowGrad)")
        robot_group.add(antenna_bulb)

        # Visor
        visor = dwg.rect(insert=(300, 250), size=(200, 80), rx=15, fill="#0f172a")
        robot_group.add(visor)

        # Eyes
        eye_left = dwg.circle(center=(350, 290), r=15, fill="#38bdf8")
        eye_right = dwg.circle(center=(450, 290), r=15, fill="#38bdf8")
        robot_group.add(eye_left)
        robot_group.add(eye_right)
        
        # Details
        vent = dwg.rect(insert=(350, 380), size=(100, 20), rx=5, fill="#334155")
        robot_group.add(vent)

        dwg.add(robot_group)

    elif prop_type == "Saturn":
        saturn_group = dwg.g(id="saturn")
        
        planet_grad = dwg.linearGradient(id="planetGrad", start=(0, 0), end=(1, 1))
        planet_grad.add_stop_color(0.0, '#fbbf24')
        planet_grad.add_stop_color(1.0, '#d97706')
        dwg.defs.add(planet_grad)

        planet = dwg.circle(center=(400, 400), r=200, fill="url(#planetGrad)")
        saturn_group.add(planet)

        # Elipse for ring
        ring_bg = dwg.ellipse(center=(400, 400), r=(350, 80), fill="none", stroke="#fcd34d", stroke_width=40)
        saturn_group.add(ring_bg)
        ring_fg = dwg.ellipse(center=(400, 400), r=(350, 80), fill="none", stroke="#f59e0b", stroke_width=15)
        saturn_group.add(ring_fg)

        dwg.add(saturn_group)

    # 3. Save the XML perfectly
    dwg.save()

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "raw_inkscape")
    os.makedirs(out_dir, exist_ok=True)
    
    path_robot = os.path.join(out_dir, "PropDeclarativeRobot.svg")
    build_declarative_prop(path_robot, prop_type="Robot")
    print(f"Generated Declarative Robot: {path_robot}")

    path_saturn = os.path.join(out_dir, "PropDeclarativeSaturn.svg")
    build_declarative_prop(path_saturn, prop_type="Saturn")
    print(f"Generated Declarative Saturn: {path_saturn}")
