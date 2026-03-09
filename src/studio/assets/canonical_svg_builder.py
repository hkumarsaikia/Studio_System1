from __future__ import annotations

import re
from pathlib import Path

from src.studio.assets.catalog import canonical_asset_id, family_for_asset

BASE = "#37506A"
ACCENT = "#38BDF8"
MUTED = "#D8E6F2"
STROKE = "#0F172A"
WHITE = "#FFFFFF"


def build_catalog_asset(output_path: str, asset_id: str) -> None:
    canonical = canonical_asset_id(asset_id)
    svg = render_catalog_asset(canonical)
    Path(output_path).write_text(svg, encoding="utf-8")


def render_catalog_asset(asset_id: str) -> str:
    family = family_for_asset(asset_id)
    renderer = FAMILY_RENDERERS.get(family, _render_fallback)
    elements = renderer(asset_id)
    return _svg_document(asset_id, family, elements)


def _flatten_elements(elements: list[str] | list[object]) -> list[str]:
    flattened: list[str] = []
    for element in elements:
        if isinstance(element, str):
            flattened.append(element)
            continue
        if isinstance(element, list | tuple):
            flattened.extend(_flatten_elements(list(element)))
            continue
        raise TypeError(f"Unsupported SVG element payload: {type(element)!r}")
    return flattened


def _svg_document(asset_id: str, family: str, elements: list[str]) -> str:
    flat_elements = _flatten_elements(elements)
    defs = _svg_defs()
    plate = _plate_for_family(family)
    shadow_group = _group([_shadowize(element) for element in flat_elements], transform="translate(0 3)", opacity=0.16)
    icon_group = _group(flat_elements, transform="translate(0 1)")
    ornaments = _foreground_ornaments(family)
    content = "\n    ".join([defs, *plate, shadow_group, icon_group, *ornaments])
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" aria-label="{asset_id}">\n'
        f"    {content}\n"
        "</svg>\n"
    )


def _svg_defs() -> str:
    return (
        "<defs>"
        '<linearGradient id="plate-fill" x1="12%" y1="10%" x2="88%" y2="92%">'
        f'<stop offset="0%" stop-color="{WHITE}" stop-opacity="0.94"/>'
        f'<stop offset="22%" stop-color="{MUTED}" stop-opacity="0.96"/>'
        f'<stop offset="68%" stop-color="{BASE}" stop-opacity="0.22"/>'
        f'<stop offset="100%" stop-color="{STROKE}" stop-opacity="0.08"/>'
        "</linearGradient>"
        '<linearGradient id="fill-base" x1="18%" y1="10%" x2="84%" y2="92%">'
        f'<stop offset="0%" stop-color="{MUTED}" stop-opacity="0.88"/>'
        f'<stop offset="28%" stop-color="{BASE}" stop-opacity="0.98"/>'
        f'<stop offset="100%" stop-color="{STROKE}" stop-opacity="0.92"/>'
        "</linearGradient>"
        '<linearGradient id="fill-accent" x1="10%" y1="8%" x2="88%" y2="94%">'
        f'<stop offset="0%" stop-color="{WHITE}" stop-opacity="0.9"/>'
        f'<stop offset="24%" stop-color="{MUTED}" stop-opacity="0.92"/>'
        f'<stop offset="100%" stop-color="{ACCENT}" stop-opacity="1"/>'
        "</linearGradient>"
        '<linearGradient id="fill-muted" x1="8%" y1="8%" x2="92%" y2="92%">'
        f'<stop offset="0%" stop-color="{WHITE}" stop-opacity="0.96"/>'
        f'<stop offset="100%" stop-color="{MUTED}" stop-opacity="0.94"/>'
        "</linearGradient>"
        '<radialGradient id="ambient-glow" cx="26%" cy="18%" r="84%">'
        f'<stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.22"/>'
        f'<stop offset="42%" stop-color="{MUTED}" stop-opacity="0.18"/>'
        f'<stop offset="100%" stop-color="{WHITE}" stop-opacity="0"/>'
        "</radialGradient>"
        "</defs>"
    )


def _plate_for_family(family: str) -> list[str]:
    if family in {"people_society", "social_media_system", "global_systems", "abstract_system_symbols"}:
        return [
            _circle(50, 54, 39, fill=STROKE, stroke=None, opacity=0.12),
            _circle(50, 50, 44, fill="url(#ambient-glow)", stroke=None),
            _circle(50, 50, 40, fill="url(#plate-fill)", stroke=STROKE, stroke_width=2.4, opacity=0.98),
            _circle(50, 50, 34, fill="none", stroke=WHITE, stroke_width=1.4, opacity=0.34),
            _path("M 28 31 Q 50 20 72 28", fill="none", stroke=WHITE, stroke_width=3, opacity=0.42),
        ]
    if family in {"charts_data_visualization", "systems_network_diagrams", "arrows_flow_indicators", "crisis_risk"}:
        return [
            _rect(12, 18, 76, 68, 24, fill=STROKE, stroke=None, opacity=0.12),
            _rect(10, 14, 80, 72, 24, fill="url(#ambient-glow)", stroke=None),
            _rect(10, 14, 80, 72, 24, fill="url(#plate-fill)", stroke=STROKE, stroke_width=2.4, opacity=0.98),
            _rect(16, 20, 68, 60, 18, fill="none", stroke=WHITE, stroke_width=1.4, opacity=0.28),
            _path("M 20 26 H 64", fill="none", stroke=WHITE, stroke_width=3, opacity=0.34),
        ]
    return [
        _rect(14, 16, 72, 72, 22, fill=STROKE, stroke=None, opacity=0.12),
        _rect(12, 12, 76, 76, 22, fill="url(#ambient-glow)", stroke=None),
        _rect(12, 12, 76, 76, 22, fill="url(#plate-fill)", stroke=STROKE, stroke_width=2.4, opacity=0.98),
        _rect(18, 18, 64, 64, 16, fill="none", stroke=WHITE, stroke_width=1.4, opacity=0.28),
        _path("M 22 24 H 64", fill="none", stroke=WHITE, stroke_width=3, opacity=0.34),
    ]


def _foreground_ornaments(family: str) -> list[str]:
    if family in {"people_society", "technology_internet", "future_technology", "social_media_system"}:
        return [
            _circle(74, 24, 3.5, fill=ACCENT, stroke=None, opacity=0.92),
            _circle(68, 30, 1.8, fill=WHITE, stroke=None, opacity=0.82),
        ]
    if family in {"money_economy", "charts_data_visualization", "crisis_risk"}:
        return [
            _path("M 70 78 Q 78 74 84 66", fill="none", stroke=ACCENT, stroke_width=3, opacity=0.5),
        ]
    return [
        _circle(76, 24, 2.8, fill=ACCENT, stroke=None, opacity=0.78),
    ]


def _resolve_fill(fill: str | None) -> str:
    if fill is None:
        return "none"
    if fill == BASE:
        return "url(#fill-base)"
    if fill == ACCENT:
        return "url(#fill-accent)"
    if fill == MUTED:
        return "url(#fill-muted)"
    return fill


def _group(elements: list[str], *, transform: str | None = None, opacity: float | None = None) -> str:
    attrs = []
    if transform:
        attrs.append(f'transform="{transform}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    prefix = f"<g {' '.join(attrs)}>" if attrs else "<g>"
    return prefix + "".join(elements) + "</g>"


def _shadowize(element: str) -> str:
    shadow = re.sub(r'fill="(?!none)[^"]+"', f'fill="{STROKE}"', element)
    shadow = re.sub(r'stroke="(?!none)[^"]+"', f'stroke="{STROKE}"', shadow)
    return shadow


def _style(fill: str | None = None, stroke: str | None = STROKE, width: float = 3, opacity: float | None = None) -> str:
    attrs = []
    attrs.append(f'fill="{_resolve_fill(fill)}"' if fill is not None else 'fill="none"')
    attrs.append(f'stroke="{stroke}"' if stroke is not None else 'stroke="none"')
    attrs.append(f'stroke-width="{width}"')
    attrs.append('stroke-linecap="round"')
    attrs.append('stroke-linejoin="round"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return " ".join(attrs)


def _rect(
    x: float,
    y: float,
    width: float,
    height: float,
    rx: float = 0,
    *,
    fill: str | None = None,
    stroke: str | None = STROKE,
    stroke_width: float = 3,
    opacity: float | None = None,
) -> str:
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'width="{width}"',
        f'height="{height}"',
    ]
    if rx:
        attrs.append(f'rx="{rx}"')
    attrs.append(_style(fill=fill, stroke=stroke, width=stroke_width, opacity=opacity))
    return f"<rect {' '.join(attrs)}/>"


def _circle(
    cx: float,
    cy: float,
    r: float,
    *,
    fill: str | None = None,
    stroke: str | None = STROKE,
    stroke_width: float = 3,
    opacity: float | None = None,
) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" {_style(fill=fill, stroke=stroke, width=stroke_width, opacity=opacity)}/>'


def _ellipse(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    *,
    fill: str | None = None,
    stroke: str | None = STROKE,
    stroke_width: float = 3,
    opacity: float | None = None,
) -> str:
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" {_style(fill=fill, stroke=stroke, width=stroke_width, opacity=opacity)}/>'


def _line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke: str = STROKE,
    stroke_width: float = 3,
    opacity: float | None = None,
) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {_style(fill="none", stroke=stroke, width=stroke_width, opacity=opacity)}/>'


def _polyline(points: str, *, fill: str | None = None, stroke: str | None = STROKE, stroke_width: float = 3, opacity: float | None = None) -> str:
    return f'<polyline points="{points}" {_style(fill=fill, stroke=stroke, width=stroke_width, opacity=opacity)}/>'


def _polygon(points: str, *, fill: str | None = None, stroke: str | None = STROKE, stroke_width: float = 3, opacity: float | None = None) -> str:
    return f'<polygon points="{points}" {_style(fill=fill, stroke=stroke, width=stroke_width, opacity=opacity)}/>'


def _path(d: str, *, fill: str | None = None, stroke: str | None = STROKE, stroke_width: float = 3, opacity: float | None = None) -> str:
    return f'<path d="{d}" {_style(fill=fill, stroke=stroke, width=stroke_width, opacity=opacity)}/>'


def _token_set(asset_id: str) -> set[str]:
    return set(asset_id.split("_"))


def _has(tokens: set[str], *names: str) -> bool:
    return any(name in tokens for name in names)


def _person(cx: float, cy: float, scale: float = 1.0, accessory: str | None = None) -> list[str]:
    head_r = 7 * scale
    torso_w = 18 * scale
    torso_h = 20 * scale
    body_x = cx - torso_w / 2
    head_y = cy - 18 * scale
    body_y = cy - 4 * scale
    limb_width = max(2.4, 3 * scale)
    elements = [
        _circle(cx, head_y + 1.5 * scale, head_r + 1.8 * scale, fill=ACCENT, stroke=None, opacity=0.18),
        _circle(cx, head_y, head_r, fill=BASE),
        _path(
            f"M {cx - 4.8 * scale} {head_y - 1.2 * scale} "
            f"Q {cx} {head_y - 6.2 * scale} {cx + 4.8 * scale} {head_y - 1.2 * scale} "
            f"Q {cx} {head_y + 1.8 * scale} {cx - 4.8 * scale} {head_y - 1.2 * scale} Z",
            fill=MUTED,
            stroke=None,
            opacity=0.42,
        ),
        _rect(body_x, body_y, torso_w, torso_h, 8 * scale, fill=ACCENT),
        _rect(body_x + 2.5 * scale, body_y + 3.4 * scale, torso_w - 5 * scale, 5 * scale, 2.6 * scale, fill=MUTED, stroke=None, opacity=0.54),
        _path(
            f"M {body_x + 2 * scale} {body_y + torso_h - 2 * scale} "
            f"Q {cx} {body_y + torso_h + 5 * scale} {body_x + torso_w - 2 * scale} {body_y + torso_h - 2 * scale}",
            fill="none",
            stroke=BASE,
            stroke_width=max(1.9, 2.5 * scale),
            opacity=0.52,
        ),
        _line(cx, body_y + torso_h, cx, body_y + torso_h + 10 * scale, stroke_width=limb_width),
        _line(cx - 8 * scale, body_y + 8 * scale, cx + 8 * scale, body_y + 8 * scale, stroke_width=limb_width),
        _line(cx, body_y + torso_h + 10 * scale, cx - 7 * scale, body_y + torso_h + 18 * scale, stroke_width=limb_width),
        _line(cx, body_y + torso_h + 10 * scale, cx + 7 * scale, body_y + torso_h + 18 * scale, stroke_width=limb_width),
        _ellipse(cx - 6 * scale, body_y + torso_h + 18.5 * scale, 3.2 * scale, 1.6 * scale, fill=BASE, stroke=None, opacity=0.92),
        _ellipse(cx + 6 * scale, body_y + torso_h + 18.5 * scale, 3.2 * scale, 1.6 * scale, fill=BASE, stroke=None, opacity=0.92),
    ]
    if accessory == "helmet":
        elements.append(_path(f"M {cx - 10 * scale} {head_y} Q {cx} {head_y - 12 * scale} {cx + 10 * scale} {head_y} L {cx + 10 * scale} {head_y + 4 * scale} L {cx - 10 * scale} {head_y + 4 * scale} Z", fill=ACCENT))
    elif accessory == "tie":
        elements.append(_polygon(f"{cx},{body_y + 4 * scale} {cx - 3 * scale},{body_y + 10 * scale} {cx},{body_y + 18 * scale} {cx + 3 * scale},{body_y + 10 * scale}", fill=BASE))
    elif accessory == "briefcase":
        elements.append(_rect(cx + 10 * scale, body_y + 8 * scale, 12 * scale, 10 * scale, 2 * scale, fill=BASE))
    elif accessory == "bag":
        elements.append(_path(f"M {cx + 11 * scale} {body_y + 12 * scale} Q {cx + 16 * scale} {body_y + 6 * scale} {cx + 21 * scale} {body_y + 12 * scale} L {cx + 21 * scale} {body_y + 24 * scale} L {cx + 11 * scale} {body_y + 24 * scale} Z", fill=BASE))
    elif accessory == "ballot":
        elements.append(_rect(cx + 10 * scale, body_y + 4 * scale, 14 * scale, 16 * scale, 3 * scale, fill=MUTED))
        elements.append(_line(cx + 13 * scale, body_y + 9 * scale, cx + 20 * scale, body_y + 9 * scale))
    elif accessory == "cap":
        elements.append(_polygon(f"{cx - 12 * scale},{head_y - 1 * scale} {cx},{head_y - 8 * scale} {cx + 12 * scale},{head_y - 1 * scale} {cx},{head_y + 5 * scale}", fill=ACCENT))
    elif accessory == "cross":
        elements.append(_rect(cx + 10 * scale, body_y + 7 * scale, 12 * scale, 12 * scale, 3 * scale, fill=MUTED))
        elements.append(_line(cx + 16 * scale, body_y + 10 * scale, cx + 16 * scale, body_y + 16 * scale))
        elements.append(_line(cx + 13 * scale, body_y + 13 * scale, cx + 19 * scale, body_y + 13 * scale))
    elif accessory == "cane":
        elements.append(_line(cx + 9 * scale, body_y + 8 * scale, cx + 11 * scale, body_y + 29 * scale))
        elements.append(_path(f"M {cx + 7 * scale} {body_y + 10 * scale} Q {cx + 12 * scale} {body_y + 4 * scale} {cx + 16 * scale} {body_y + 10 * scale}", fill="none"))
    elif accessory == "megaphone":
        elements.append(_polygon(f"{cx + 10 * scale},{body_y + 8 * scale} {cx + 23 * scale},{body_y + 12 * scale} {cx + 10 * scale},{body_y + 18 * scale}", fill=BASE))
    elif accessory == "camera":
        elements.append(_rect(cx + 10 * scale, body_y + 8 * scale, 14 * scale, 10 * scale, 3 * scale, fill=BASE))
        elements.append(_circle(cx + 17 * scale, body_y + 13 * scale, 3 * scale, fill=MUTED))
    elif accessory == "podium":
        elements.append(_rect(cx - 12 * scale, body_y + 14 * scale, 24 * scale, 13 * scale, 4 * scale, fill=BASE))
    elif accessory == "laptop":
        elements.append(_rect(cx + 8 * scale, body_y + 8 * scale, 16 * scale, 11 * scale, 2 * scale, fill=MUTED))
        elements.append(_line(cx + 6 * scale, body_y + 20 * scale, cx + 26 * scale, body_y + 20 * scale))
    elif accessory == "bulb":
        elements.append(_circle(cx + 15 * scale, body_y + 10 * scale, 5 * scale, fill=ACCENT))
        elements.append(_rect(cx + 12 * scale, body_y + 14 * scale, 6 * scale, 4 * scale, 1.5 * scale, fill=BASE))
    elif accessory == "board":
        elements.append(_rect(cx + 8 * scale, body_y + 4 * scale, 18 * scale, 13 * scale, 3 * scale, fill=MUTED))
        elements.append(_line(cx + 8 * scale, body_y + 21 * scale, cx + 26 * scale, body_y + 21 * scale))
    return elements


def _house_body(x: float = 24, y: float = 34, width: float = 52, height: float = 42) -> list[str]:
    return [
        _polygon(f"{x + width / 2},{y - 13} {x + 3},{y + 2} {x + width - 3},{y + 2}", fill=STROKE, stroke=None, opacity=0.14),
        _polygon(f"{x + width / 2},{y - 16} {x},{y} {x + width},{y}", fill=ACCENT),
        _rect(x, y, width, height, 8, fill=BASE),
        _rect(x + 4, y + 5, width - 8, 5, 2.5, fill=MUTED, stroke=None, opacity=0.36),
        _rect(x + 8, y + 10, 10, 10, 2.5, fill=MUTED, stroke=None, opacity=0.92),
        _rect(x + width - 18, y + 10, 10, 10, 2.5, fill=MUTED, stroke=None, opacity=0.92),
        _rect(x + width * 0.38, y + height * 0.42, width * 0.24, height * 0.58, 4, fill=MUTED),
        _rect(x + width * 0.32, y + height + 1, width * 0.36, 4, 2, fill=STROKE, stroke=None, opacity=0.22),
    ]


def _building_body(x: float, y: float, width: float, height: float, floors: int = 3, accent: bool = False) -> list[str]:
    elements = [
        _rect(x, y + 2, width, height, 8, fill=STROKE, stroke=None, opacity=0.12),
        _rect(x, y, width, height, 8, fill=ACCENT if accent else BASE),
        _rect(x + 3, y + 4, width - 6, 6, 2.5, fill=MUTED, stroke=None, opacity=0.28),
    ]
    window_fill = MUTED if accent else ACCENT
    window_shine = WHITE if accent else MUTED
    cols = 2 if width < 28 else 3
    gutter_x = width / (cols + 1)
    window_w = 5.5
    window_h = 6
    for col in range(cols):
        for row in range(floors):
            wx = x + 5 + col * gutter_x
            wy = y + 6 + row * (height - 16) / max(floors - 0.25, 1)
            elements.append(
                _rect(
                    wx,
                    wy,
                    window_w,
                    window_h,
                    1.5,
                    fill=window_fill,
                    stroke=None,
                )
            )
            elements.append(
                _line(
                    wx + 1.1,
                    wy + 2.1,
                    wx + window_w - 1.1,
                    wy + 2.1,
                    stroke=window_shine,
                    stroke_width=1.1,
                    opacity=0.46,
                )
            )
    if height >= 32:
        elements.append(_rect(x + width * 0.38, y + height - 12, width * 0.24, 12, 2.5, fill=MUTED, stroke=None, opacity=0.9))
    return elements


def _chart_axes() -> list[str]:
    return [
        _line(26, 72, 26, 28, stroke=MUTED, stroke_width=7, opacity=0.15),
        _line(24, 74, 74, 74, stroke=MUTED, stroke_width=7, opacity=0.15),
        _line(26, 72, 26, 28, stroke_width=4),
        _line(24, 74, 74, 74, stroke_width=4),
        _line(26, 58, 74, 58, stroke=MUTED, stroke_width=2, opacity=0.3),
        _line(26, 44, 74, 44, stroke=MUTED, stroke_width=2, opacity=0.24),
        _line(40, 74, 40, 28, stroke=MUTED, stroke_width=1.4, opacity=0.22),
        _line(54, 74, 54, 28, stroke=MUTED, stroke_width=1.4, opacity=0.18),
        _line(68, 74, 68, 28, stroke=MUTED, stroke_width=1.4, opacity=0.16),
    ]


def _arrow(direction: str = "right", *, circular: bool = False, double: bool = False, curve: bool = False) -> list[str]:
    if circular:
        return [
            _path("M 30 34 Q 50 16 70 34", fill="none", stroke=MUTED, stroke_width=8, opacity=0.16),
            _path("M 70 66 Q 50 84 30 66", fill="none", stroke=MUTED, stroke_width=8, opacity=0.16),
            _path("M 30 34 Q 50 16 70 34", fill="none", stroke=ACCENT, stroke_width=4),
            _path("M 70 66 Q 50 84 30 66", fill="none", stroke=ACCENT, stroke_width=4),
            _polyline("63,28 74,33 66,43", stroke=ACCENT, stroke_width=4),
            _polyline("36,57 26,67 38,71", stroke=ACCENT, stroke_width=4),
            _circle(30, 34, 3, fill=BASE, stroke=None, opacity=0.9),
            _circle(70, 66, 3, fill=BASE, stroke=None, opacity=0.9),
        ]
    if curve:
        if direction == "down":
            return [
                _path("M 28 30 C 62 28 72 48 72 64", fill="none", stroke=MUTED, stroke_width=8, opacity=0.16),
                _path("M 28 30 C 62 28 72 48 72 64", fill="none", stroke=ACCENT, stroke_width=4),
                _polyline("64,58 72,68 80,58", stroke=ACCENT, stroke_width=4),
            ]
        return [
            _path("M 24 60 C 38 32 58 32 72 46", fill="none", stroke=MUTED, stroke_width=8, opacity=0.16),
            _path("M 24 60 C 38 32 58 32 72 46", fill="none", stroke=ACCENT, stroke_width=4),
            _polyline("64,38 76,46 64,54", stroke=ACCENT, stroke_width=4),
        ]
    if direction in {"up", "down"}:
        arrow_points = "42,32 50,22 58,32" if direction == "up" else "42,68 50,78 58,68"
        tail_y1, tail_y2 = (72, 28) if direction == "up" else (28, 72)
        elements = [
            _line(50, tail_y1, 50, tail_y2, stroke=MUTED, stroke_width=8, opacity=0.16),
            _line(50, tail_y1, 50, tail_y2, stroke=ACCENT, stroke_width=4),
            _polyline(arrow_points, stroke=ACCENT, stroke_width=4),
            _circle(50, tail_y1, 3, fill=BASE, stroke=None, opacity=0.88),
        ]
        if double:
            arrow_points_2 = "42,68 50,78 58,68" if direction == "up" else "42,32 50,22 58,32"
            elements.append(_polyline(arrow_points_2, stroke=ACCENT, stroke_width=4))
        return elements
    if direction == "left":
        return [
            _line(74, 50, 26, 50, stroke=MUTED, stroke_width=8, opacity=0.16),
            _line(74, 50, 26, 50, stroke=ACCENT, stroke_width=4),
            _polyline("34,42 24,50 34,58", stroke=ACCENT, stroke_width=4),
            _circle(74, 50, 3, fill=BASE, stroke=None, opacity=0.88),
        ]
    elements = [
        _line(26, 50, 74, 50, stroke=MUTED, stroke_width=8, opacity=0.16),
        _line(26, 50, 74, 50, stroke=ACCENT, stroke_width=4),
        _polyline("66,42 76,50 66,58", stroke=ACCENT, stroke_width=4),
        _circle(26, 50, 3, fill=BASE, stroke=None, opacity=0.88),
    ]
    if double:
        elements.append(_polyline("34,42 24,50 34,58", stroke=ACCENT, stroke_width=4))
    return elements


def _document(x: float = 28, y: float = 20, width: float = 42, height: float = 56, seal: bool = False) -> list[str]:
    elements = [
        _path(
            f"M {x + 4} {y + 4} L {x + width - 8} {y + 4} L {x + width + 4} {y + 16} L {x + width + 4} {y + height + 4} L {x + 4} {y + height + 4} Z",
            fill=STROKE,
            stroke=None,
            opacity=0.12,
        ),
        _path(f"M {x} {y} L {x + width - 12} {y} L {x + width} {y + 12} L {x + width} {y + height} L {x} {y + height} Z", fill=BASE),
        _rect(x + 6, y + 8, width - 20, 8, 2.5, fill=ACCENT, stroke=None, opacity=0.94),
        _polyline(f"{x + width - 12},{y} {x + width - 12},{y + 12} {x + width},{y + 12}", fill=MUTED),
        _line(x + 8, y + 18, x + width - 18, y + 18, stroke=WHITE, stroke_width=1.6, opacity=0.54),
        _line(x + 8, y + 22, x + width - 8, y + 22),
        _line(x + 8, y + 32, x + width - 10, y + 32),
        _line(x + 8, y + 42, x + width - 16, y + 42),
        _line(x + 8, y + 50, x + width - 18, y + 50, stroke=MUTED, stroke_width=2.2, opacity=0.28),
    ]
    if seal:
        elements.append(_circle(x + width - 14, y + height - 10, 8, fill=ACCENT, stroke=None, opacity=0.2))
        elements.append(_circle(x + width - 14, y + height - 10, 6, fill=ACCENT))
        elements.append(_circle(x + width - 14, y + height - 10, 2.4, fill=WHITE, stroke=None, opacity=0.82))
    return elements


def _render_people(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if asset_id == "family":
        return [
            *_person(35, 50, 1.0),
            *_person(65, 50, 1.0),
            *_person(50, 60, 0.72),
        ]
    if asset_id == "crowd":
        return [
            *_person(28, 50, 0.7),
            *_person(42, 45, 0.9),
            *_person(58, 45, 0.9),
            *_person(72, 50, 0.7),
            *_person(50, 58, 0.75),
        ]
    if asset_id == "person_group":
        return [*_person(32, 52, 0.8), *_person(50, 46, 1.0), *_person(68, 52, 0.8)]

    accessory = None
    if _has(tokens, "worker"):
        accessory = "helmet" if "office" not in tokens else "laptop"
    elif _has(tokens, "manager", "business"):
        accessory = "tie" if "manager" in tokens else "briefcase"
    elif _has(tokens, "consumer", "customer"):
        accessory = "bag"
    elif "voter" in tokens:
        accessory = "ballot"
    elif "student" in tokens:
        accessory = "cap"
    elif "teacher" in tokens:
        accessory = "board"
    elif "doctor" in tokens:
        accessory = "cross"
    elif "elderly" in tokens:
        accessory = "cane"
    elif "entrepreneur" in tokens:
        accessory = "bulb"
    elif "influencer" in tokens:
        accessory = "camera"
    elif "politician" in tokens:
        accessory = "podium"
    elif "protester" in tokens:
        accessory = "megaphone"

    scale = 0.76 if "child" in tokens else 1.0
    cy = 54 if "child" in tokens else 50
    return _person(50, cy, scale, accessory=accessory)


def _render_buildings(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if _has(tokens, "skyline", "city"):
        return [
            *_building_body(16, 36, 18, 40, floors=3),
            *_building_body(34, 28, 20, 48, floors=4, accent=True),
            *_building_body(54, 22, 14, 54, floors=5),
            *_building_body(68, 34, 16, 42, floors=3, accent=True),
        ]
    if _has(tokens, "house"):
        elements = _house_body()
        if "suburban" in tokens:
            elements.extend([_rect(18, 60, 8, 16, 2, fill=BASE), _circle(22, 54, 6, fill=ACCENT)])
        if "luxury" in tokens:
            elements.append(_polygon("74,20 78,28 86,30 80,36 82,44 74,40 66,44 68,36 62,30 70,28", fill=ACCENT))
        if "empty" in tokens:
            elements.append(_line(33, 47, 67, 69, stroke_width=4))
        return elements
    if "factory" in tokens:
        return [
            _polygon("20,72 20,48 34,40 34,50 48,40 48,50 62,40 62,72", fill=BASE),
            _rect(66, 30, 12, 42, 3, fill=ACCENT),
            _circle(76, 24, 6, fill=MUTED),
            _circle(82, 18, 4, fill=MUTED),
        ]
    if "warehouse" in tokens:
        return [_rect(18, 34, 64, 40, 6, fill=BASE), _polygon("18,34 50,20 82,34", fill=ACCENT), _rect(42, 50, 16, 24, 3, fill=MUTED)]
    if "bank" in tokens:
        return [
            _polygon("50,18 20,34 80,34", fill=ACCENT),
            _rect(22, 34, 56, 8, 2, fill=BASE),
            _rect(28, 42, 8, 26, 3, fill=MUTED),
            _rect(46, 42, 8, 26, 3, fill=MUTED),
            _rect(64, 42, 8, 26, 3, fill=MUTED),
            _rect(20, 68, 60, 8, 2, fill=BASE),
        ]
    if "hospital" in tokens:
        return [*_building_body(24, 24, 52, 52, floors=4), _rect(42, 36, 16, 16, 3, fill=MUTED), _line(50, 39, 50, 49), _line(45, 44, 55, 44)]
    if "school" in tokens or "university" in tokens:
        elements = [_rect(22, 28, 56, 48, 6, fill=BASE), _polygon("50,16 18,28 82,28", fill=ACCENT)]
        if "university" in tokens:
            elements.append(_polygon("38,18 50,12 62,18 50,24", fill=MUTED))
        else:
            elements.append(_line(62, 20, 62, 32))
            elements.append(_polygon("62,20 70,24 62,28", fill=MUTED))
        elements.append(_rect(44, 54, 12, 22, 3, fill=MUTED))
        return elements
    if "government" in tokens:
        return [*_building_body(22, 30, 56, 46, floors=3), _line(50, 18, 50, 32), _polygon("50,18 64,22 50,26", fill=ACCENT)]
    if "court" in tokens:
        return [*_building_body(22, 30, 56, 46, floors=3), _line(36, 22, 64, 22), _line(42, 18, 42, 26), _rect(48, 18, 12, 8, 2, fill=ACCENT)]
    if "data" in tokens:
        return [_rect(26, 24, 48, 52, 6, fill=BASE), _rect(32, 32, 36, 10, 3, fill=MUTED), _rect(32, 47, 36, 10, 3, fill=MUTED), _rect(32, 62, 36, 10, 3, fill=MUTED)]
    if "power" in tokens:
        return [_rect(24, 30, 52, 44, 6, fill=BASE), _rect(34, 18, 10, 18, 3, fill=ACCENT), _polygon("54,34 44,54 54,54 46,72 66,46 56,46", fill=ACCENT)]
    if "airport" in tokens:
        return [_rect(18, 42, 64, 26, 6, fill=BASE), *_arrow("right"), _line(24, 68, 76, 68)]
    if "mall" in tokens:
        return [_rect(18, 32, 64, 44, 8, fill=BASE), _rect(24, 26, 52, 12, 4, fill=ACCENT), _rect(42, 52, 16, 24, 3, fill=MUTED)]
    if "store" in tokens or "restaurant" in tokens:
        elements = [_rect(20, 34, 60, 42, 8, fill=BASE), _rect(18, 26, 64, 14, 4, fill=ACCENT), _rect(43, 54, 14, 22, 3, fill=MUTED)]
        if "restaurant" in tokens:
            elements.append(_line(30, 46, 30, 62))
            elements.append(_line(34, 46, 34, 62))
            elements.append(_line(70, 46, 70, 62))
            elements.append(_line(66, 46, 70, 50))
        return elements
    if "apartment" in tokens or "skyscraper" in tokens or "office" in tokens or "corporate" in tokens:
        height = 56 if "skyscraper" in tokens or "corporate" in tokens else 48
        y = 18 if height == 56 else 26
        accent = "corporate" in tokens
        elements = _building_body(32, y, 36, height, floors=5 if height == 56 else 4, accent=accent)
        if "corporate" in tokens:
            elements.append(_line(50, y - 8, 50, y + 4))
            elements.append(_polygon(f"50,{y - 8} 60,{y - 4} 50,{y}", fill=MUTED))
        return elements
    return _building_body(26, 24, 48, 52, floors=4)


def _render_money(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if _has(tokens, "coins", "coin"):
        return [
            _ellipse(50, 66, 24, 8, fill=BASE),
            _rect(26, 44, 48, 22, 0, fill=BASE, stroke=None),
            _ellipse(50, 44, 24, 8, fill=ACCENT),
            _line(50, 36, 50, 54),
            _line(44, 40, 56, 40),
        ]
    if "stack" in tokens:
        return [
            _rect(22, 34, 50, 28, 6, fill=BASE),
            _rect(28, 28, 50, 28, 6, fill=ACCENT),
            _line(36, 42, 64, 42),
            _line(42, 48, 58, 48),
        ]
    if "bag" in tokens:
        return [_path("M 34 34 Q 50 24 66 34 L 62 42 Q 74 50 70 68 Q 62 80 50 80 Q 38 80 30 68 Q 26 50 38 42 Z", fill=BASE), _line(50, 46, 50, 62), _line(44, 54, 56, 54)]
    if "banknote" in tokens:
        return [_rect(20, 34, 60, 32, 6, fill=BASE), _circle(50, 50, 9, fill=MUTED), _line(28, 50, 34, 50), _line(66, 50, 72, 50)]
    if "card" in tokens:
        elements = [_rect(18, 34, 64, 36, 8, fill=BASE), _rect(18, 42, 64, 8, 0, fill=ACCENT, stroke=None), _rect(28, 56, 16, 6, 2, fill=MUTED)]
        if "debit" in tokens:
            elements.append(_rect(24, 52, 10, 8, 2, fill=ACCENT))
        return elements
    if "digital" in tokens:
        return [_rect(24, 20, 24, 48, 6, fill=BASE), _rect(30, 28, 12, 24, 2, fill=MUTED), _path("M 56 36 Q 68 44 56 52", fill="none"), _path("M 60 30 Q 78 44 60 58", fill="none")]
    if "interest" in tokens:
        return [_circle(38, 36, 6, fill=ACCENT), _circle(62, 64, 6, fill=ACCENT), _line(36, 66, 64, 34, stroke_width=4), *_arrow("up")]
    if "loan" in tokens or "tax" in tokens:
        elements = _document(seal=True)
        if "tax" in tokens:
            elements.extend([_line(38, 54, 62, 54), _line(44, 48, 56, 60)])
        else:
            elements.append(_path("M 34 58 Q 42 66 50 58 Q 58 50 66 58", fill="none"))
        return elements
    if "debt" in tokens:
        return [_circle(34, 50, 10, fill=BASE), _circle(66, 50, 10, fill=BASE), _line(44, 50, 56, 50, stroke_width=6), _line(50, 44, 50, 56, stroke_width=6)]
    if "register" in tokens:
        return [_rect(24, 32, 52, 40, 6, fill=BASE), _rect(30, 24, 24, 12, 3, fill=ACCENT), _rect(34, 42, 20, 10, 2, fill=MUTED), _rect(58, 52, 12, 12, 2, fill=MUTED)]
    if "tag" in tokens:
        return [_path("M 24 40 L 54 24 L 78 48 L 48 72 L 24 72 Z", fill=BASE), _circle(52, 38, 4, fill=MUTED)]
    if "cart" in tokens:
        return [_polyline("24,32 32,32 40,60 72,60 78,40 36,40", fill="none"), _circle(44, 70, 5, fill=ACCENT), _circle(68, 70, 5, fill=ACCENT)]
    if "wallet" in tokens:
        return [_rect(22, 38, 56, 28, 8, fill=BASE), _rect(34, 32, 44, 20, 6, fill=ACCENT), _circle(62, 52, 3, fill=MUTED)]
    if "pyramid" in tokens:
        return [_polygon("50,20 24,72 76,72", fill=BASE), _ellipse(50, 58, 12, 7, fill=ACCENT), _line(50, 52, 50, 64)]
    if "income" in tokens or "salary" in tokens:
        return [_rect(22, 54, 18, 18, 4, fill=BASE), _ellipse(70, 44, 12, 8, fill=ACCENT), *_arrow("up")]
    if "market" in tokens or "chart" in tokens:
        elements = _chart_axes()
        if "stock_market" in asset_id:
            elements.append(_rect(62, 20, 14, 18, 3, fill=BASE))
        elements.append(_polyline("30,62 42,54 52,58 66,34 74,38", fill="none", stroke_width=4))
        return elements
    if "gold" in tokens:
        return [_polygon("26,44 62,36 74,54 38,62", fill=ACCENT), _line(42, 44, 64, 40)]
    if "crypto" in tokens:
        return [_circle(50, 50, 18, fill=BASE), _polygon("50,34 62,40 62,60 50,66 38,60 38,40", fill=ACCENT), _line(50, 28, 50, 72)]
    if "blockchain" in tokens:
        return [_rect(24, 30, 16, 16, 3, fill=BASE), _rect(60, 30, 16, 16, 3, fill=ACCENT), _rect(42, 54, 16, 16, 3, fill=BASE), _line(40, 38, 60, 38), _line(50, 46, 50, 54), _line(58, 62, 68, 46)]
        return [_rect(22, 32, 56, 36, 8, fill=BASE), _circle(50, 50, 10, fill=ACCENT)]


def _render_charts(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    elements = _chart_axes()
    if "line" in tokens or "trend" in tokens or "curve" in tokens:
        points = "30,64 42,58 56,44 72,30"
        if "down" in tokens:
            points = "30,34 42,42 56,52 72,66"
        if "price" in tokens:
            points = "28,58 42,50 54,52 68,34 74,40"
        elements.append(_polyline(points, fill="none", stroke_width=4))
    elif "bar" in tokens:
        elements.extend([_rect(32, 54, 8, 18, 2, fill=BASE), _rect(46, 44, 8, 28, 2, fill=ACCENT), _rect(60, 34, 8, 38, 2, fill=BASE)])
    elif "pie" in tokens:
        elements = [_circle(50, 50, 22, fill=BASE), _path("M 50 50 L 50 28 A 22 22 0 0 1 69 60 Z", fill=ACCENT), _line(50, 50, 50, 28), _line(50, 50, 69, 60)]
    elif "inflation" in tokens:
        elements.extend([_polyline("30,62 42,54 54,44 70,32", fill="none", stroke_width=4), _line(64, 28, 74, 28), _line(69, 22, 69, 34)])
    elif "demand" in tokens or "supply" in tokens:
        elements.extend([_line(30, 66, 72, 30), _line(30, 30, 72, 66)])
    elif "cycle" in tokens:
        elements = _arrow("right", circular=True)
        elements.extend([_circle(50, 50, 10, fill=BASE), _circle(50, 50, 4, fill=MUTED)])
    elif "bubble" in tokens:
        elements.extend([_circle(36, 58, 8, fill=BASE), _circle(54, 46, 12, fill=ACCENT), _circle(70, 34, 6, fill=BASE)])
    elif "network" in tokens:
        elements.extend([_line(36, 36, 60, 42), _line(60, 42, 70, 62), _line(36, 36, 46, 66), _circle(36, 36, 5, fill=BASE), _circle(60, 42, 5, fill=ACCENT), _circle(70, 62, 5, fill=BASE), _circle(46, 66, 5, fill=ACCENT)])
    elif "growth" in tokens:
        elements = _arrow("up")
    elif "decline" in tokens:
        elements = _arrow("down")
    return elements


def _render_systems(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if asset_id == "node":
        return [_circle(50, 50, 16, fill=BASE), _circle(50, 50, 6, fill=ACCENT)]
    if "nodes" in tokens:
        return [_line(34, 36, 50, 50), _line(50, 50, 68, 36), _line(50, 50, 68, 66), _line(50, 50, 32, 66), _circle(34, 36, 6, fill=BASE), _circle(68, 36, 6, fill=ACCENT), _circle(68, 66, 6, fill=BASE), _circle(32, 66, 6, fill=ACCENT), _circle(50, 50, 7, fill=BASE)]
    if "connections" in tokens:
        return [_line(24, 34, 42, 50, stroke_width=4), _line(42, 50, 60, 34, stroke_width=4), _line(42, 50, 60, 66, stroke_width=4), _line(42, 50, 24, 66, stroke_width=4), _line(60, 34, 76, 50, stroke_width=4), _line(60, 66, 76, 50, stroke_width=4)]
    if "diagram" in tokens:
        return [_rect(18, 32, 20, 16, 4, fill=BASE), _rect(42, 32, 20, 16, 4, fill=ACCENT), _rect(66, 32, 16, 16, 4, fill=BASE), _line(38, 40, 42, 40), _line(62, 40, 66, 40), _polyline("74,48 78,58 70,58", fill="none")]
    if "loop" in tokens or "feedback" in tokens or "circular" in tokens:
        return _arrow("right", circular=True)
    if "chain" in tokens or "supply" in tokens:
        return [_rect(20, 40, 18, 14, 4, fill=BASE), _rect(42, 40, 18, 14, 4, fill=ACCENT), _rect(64, 40, 16, 14, 4, fill=BASE), _line(38, 47, 42, 47), _line(60, 47, 64, 47)]
    if "hierarchy" in tokens or "pyramid" in tokens:
        return [_rect(40, 24, 20, 12, 4, fill=ACCENT), _rect(30, 42, 40, 12, 4, fill=BASE), _rect(20, 60, 60, 12, 4, fill=ACCENT)]
    if "decision" in tokens:
        return [_polygon("50,22 68,38 50,54 32,38", fill=ACCENT), _line(50, 54, 50, 76), _line(50, 76, 34, 76), _line(50, 76, 66, 76), _polyline("30,72 24,76 30,80", fill="none"), _polyline("70,72 76,76 70,80", fill="none")]
    if "domino" in tokens:
        return [_rect(24, 34, 12, 32, 3, fill=BASE), _rect(42, 30, 12, 36, 3, fill=ACCENT), _rect(60, 26, 12, 40, 3, fill=BASE), _line(36, 50, 42, 48), _line(54, 46, 60, 44)]
    return [_circle(34, 50, 7, fill=BASE), _circle(50, 36, 7, fill=ACCENT), _circle(66, 50, 7, fill=BASE), _line(34, 50, 50, 36), _line(50, 36, 66, 50), _line(34, 50, 66, 50)]


def _render_arrows(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "up" in tokens:
        return _arrow("up", double="double" in tokens)
    if "down" in tokens:
        return _arrow("down", double="double" in tokens)
    if "left" in tokens:
        return _arrow("left", double="double" in tokens)
    if "curved" in tokens or "cause" in tokens:
        return _arrow("right", curve=True)
    if "loop" in tokens or "cycle" in tokens:
        return _arrow("right", circular=True)
    if "double" in tokens:
        return _arrow("right", double=True)
    if "timeline" in tokens:
        return [_line(24, 50, 74, 50, stroke_width=4), _polyline("66,42 76,50 66,58", fill="none", stroke_width=4), _circle(34, 50, 4, fill=BASE), _circle(48, 50, 4, fill=ACCENT), _circle(62, 50, 4, fill=BASE)]
    if "process" in tokens or "flow" in tokens:
        return [_rect(18, 42, 14, 14, 4, fill=BASE), _rect(43, 42, 14, 14, 4, fill=ACCENT), _rect(68, 42, 14, 14, 4, fill=BASE), _line(32, 49, 43, 49, stroke_width=4), _line(57, 49, 68, 49, stroke_width=4)]
    return _arrow("right")


def _render_work(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "briefcase" in tokens:
        return [_rect(22, 36, 56, 32, 8, fill=BASE), _rect(38, 28, 24, 12, 4, fill=ACCENT), _line(42, 36, 58, 36)]
    if "desk" in tokens:
        return [_rect(22, 44, 56, 12, 4, fill=BASE), _line(28, 56, 28, 74), _line(72, 56, 72, 74), _rect(50, 28, 18, 12, 2, fill=ACCENT), _rect(28, 32, 18, 18, 2, fill=MUTED)]
    if "laptop" in tokens:
        return [_rect(26, 28, 48, 28, 4, fill=BASE), _rect(32, 34, 36, 16, 2, fill=MUTED), _path("M 22 62 L 78 62 L 70 72 L 30 72 Z", fill=ACCENT)]
    if "email" in tokens:
        return [_rect(20, 30, 60, 40, 6, fill=BASE), _polyline("20,34 50,54 80,34", fill="none"), _line(20, 70, 42, 50), _line(80, 70, 58, 50)]
    if "meeting" in tokens:
        return [_ellipse(50, 50, 26, 14, fill=BASE), *_person(28, 48, 0.45), *_person(50, 34, 0.45), *_person(72, 48, 0.45)]
    if "task" in tokens:
        return [_rect(24, 24, 52, 52, 8, fill=BASE), _line(36, 40, 66, 40), _line(36, 54, 66, 54), _line(36, 68, 58, 68), _polyline("28,39 31,43 36,35", fill="none"), _polyline("28,53 31,57 36,49", fill="none")]
    if "calendar" in tokens:
        return [_rect(22, 26, 56, 50, 8, fill=BASE), _rect(22, 26, 56, 14, 8, fill=ACCENT), _line(34, 18, 34, 34), _line(66, 18, 66, 34), _rect(34, 48, 12, 12, 2, fill=MUTED)]
    if "clock" in tokens:
        elements = [_circle(50, 50, 24, fill=BASE), _line(50, 50, 50, 36), _line(50, 50, 62, 56)]
        if "overtime" in tokens:
            elements.extend([*_arrow("right", curve=True)])
        return elements
    if "ladder" in tokens:
        return [_line(34, 24, 34, 76, stroke_width=4), _line(66, 24, 66, 76, stroke_width=4), _line(34, 34, 66, 34), _line(34, 46, 66, 46), _line(34, 58, 66, 58), _line(34, 70, 66, 70)]
    if "promotion" in tokens:
        return [_rect(26, 58, 16, 14, 4, fill=BASE), _rect(50, 42, 16, 30, 4, fill=ACCENT), *_arrow("up")]
    if "burnout" in tokens:
        return [_circle(50, 50, 20, fill=BASE), _line(42, 44, 46, 48), _line(58, 44, 54, 48), _path("M 40 62 Q 50 56 60 62", fill="none"), _path("M 68 26 L 58 36 L 66 38 L 54 52", fill="none")]
    return [_rect(24, 28, 52, 44, 8, fill=BASE), _rect(34, 38, 32, 18, 3, fill=MUTED)]


def _render_technology(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "smartphone" in tokens:
        return [_rect(32, 18, 36, 64, 8, fill=BASE), _rect(38, 26, 24, 44, 4, fill=MUTED), _circle(50, 76, 3, fill=ACCENT)]
    if "app" in tokens:
        return [_rect(24, 24, 16, 16, 4, fill=BASE), _rect(44, 24, 16, 16, 4, fill=ACCENT), _rect(24, 44, 16, 16, 4, fill=ACCENT), _rect(44, 44, 16, 16, 4, fill=BASE)]
    if "bell" in tokens:
        return [_path("M 34 62 Q 34 34 50 28 Q 66 34 66 62 L 74 68 L 26 68 Z", fill=BASE), _circle(50, 74, 5, fill=ACCENT)]
    if "algorithm" in tokens:
        return [_polygon("50,20 70,36 50,52 30,36", fill=ACCENT), _line(50, 52, 50, 76), _rect(38, 76, 24, 8, 3, fill=BASE)]
    if "brain" in tokens or asset_id == "ai_network":
        return [_path("M 34 36 Q 32 22 46 24 Q 50 18 58 24 Q 70 22 68 36 Q 76 42 68 52 Q 70 66 56 68 Q 50 74 42 68 Q 28 66 32 52 Q 24 42 34 36 Z", fill=BASE), _line(44, 34, 44, 60), _line(56, 34, 56, 60), _line(38, 42, 62, 42), _line(38, 52, 62, 52)]
    if "robot" in tokens:
        return [_rect(28, 26, 44, 36, 8, fill=BASE), _circle(40, 44, 4, fill=MUTED), _circle(60, 44, 4, fill=MUTED), _line(50, 26, 50, 18), _circle(50, 14, 4, fill=ACCENT), _rect(36, 62, 28, 14, 4, fill=ACCENT)]
    if "cloud" in tokens:
        return [_circle(38, 54, 10, fill=BASE), _circle(52, 46, 12, fill=BASE), _circle(66, 54, 10, fill=BASE), _rect(30, 54, 44, 14, 7, fill=BASE)]
    if "server" in tokens:
        return [_rect(26, 24, 48, 16, 4, fill=BASE), _rect(26, 42, 48, 16, 4, fill=ACCENT), _rect(26, 60, 48, 16, 4, fill=BASE), _circle(34, 32, 2, fill=MUTED), _circle(34, 50, 2, fill=MUTED), _circle(34, 68, 2, fill=MUTED)]
    if "database" in tokens:
        return [_ellipse(50, 28, 22, 8, fill=BASE), _rect(28, 28, 44, 34, 0, fill=BASE, stroke=None), _ellipse(50, 62, 22, 8, fill=BASE), _ellipse(50, 44, 22, 8, fill=ACCENT)]
    if "globe" in tokens:
        return [_circle(50, 50, 24, fill=BASE), _ellipse(50, 50, 10, 24, fill="none"), _line(26, 50, 74, 50), _path("M 30 38 Q 50 30 70 38", fill="none"), _path("M 30 62 Q 50 70 70 62", fill="none")]
    if "wifi" in tokens:
        return [_circle(50, 68, 4, fill=ACCENT), _path("M 40 58 Q 50 48 60 58", fill="none"), _path("M 32 50 Q 50 34 68 50", fill="none"), _path("M 24 42 Q 50 20 76 42", fill="none")]
    if "cybersecurity" in tokens or "lock" in tokens:
        return [_rect(30, 42, 40, 30, 8, fill=BASE), _path("M 38 42 L 38 34 Q 38 22 50 22 Q 62 22 62 34 L 62 42", fill="none"), _circle(50, 56, 5, fill=ACCENT), _line(50, 60, 50, 66)]
    if "code" in tokens:
        return [_polyline("42,34 30,50 42,66", fill="none", stroke_width=4), _polyline("58,34 70,50 58,66", fill="none", stroke_width=4), _line(54, 30, 46, 70)]
    return [_rect(24, 24, 52, 52, 10, fill=BASE), _circle(50, 50, 10, fill=ACCENT)]


def _render_social(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "like" in tokens:
        return [_path("M 50 70 L 24 46 Q 20 34 30 28 Q 40 22 50 34 Q 60 22 70 28 Q 80 34 76 46 Z", fill=BASE)]
    if "comment" in tokens:
        return [_path("M 22 30 H 78 V 60 H 52 L 38 74 V 60 H 22 Z", fill=BASE)]
    if "share" in tokens:
        return [_circle(28, 50, 6, fill=BASE), _circle(60, 34, 6, fill=ACCENT), _circle(60, 66, 6, fill=ACCENT), _line(34, 48, 54, 36), _line(34, 52, 54, 64)]
    if "follower" in tokens:
        return [*_person(42, 50, 0.72), _circle(68, 38, 10, fill=ACCENT), _line(68, 32, 68, 44), _line(62, 38, 74, 38)]
    if "network" in tokens:
        return _render_systems("network_nodes")
    if "hashtag" in tokens:
        return [_line(38, 28, 34, 72), _line(62, 28, 58, 72), _line(28, 42, 72, 42), _line(26, 58, 70, 58)]
    if "viral" in tokens or "trend" in tokens:
        return [_polyline("28,66 42,52 54,56 72,34", fill="none", stroke_width=4), _polyline("64,28 76,34 68,44", fill="none", stroke_width=4), _circle(32, 64, 4, fill=ACCENT), _circle(72, 34, 4, fill=ACCENT)]
    if "feed" in tokens:
        return [_rect(24, 22, 52, 56, 8, fill=BASE), _rect(32, 30, 36, 12, 3, fill=ACCENT), _line(32, 50, 68, 50), _line(32, 60, 68, 60)]
    if "notification" in tokens:
        return [_circle(50, 50, 22, fill=BASE), _circle(64, 34, 8, fill=ACCENT), _line(64, 30, 64, 38), _line(60, 34, 68, 34)]
    if "creator" in tokens:
        return [*_person(40, 52, 0.8, accessory="camera"), _circle(68, 34, 8, fill=ACCENT)]
    if "camera" in tokens:
        return [_rect(22, 34, 46, 28, 6, fill=BASE), _rect(32, 42, 16, 12, 3, fill=MUTED), _circle(40, 48, 6, fill=ACCENT), _polygon("68,42 80,36 80,60 68,54", fill=ACCENT)]
    if "video" in tokens:
        return [_rect(20, 32, 50, 32, 8, fill=BASE), _polygon("44,40 60,48 44,56", fill=MUTED), _polygon("70,40 82,34 82,62 70,56", fill=ACCENT)]
    if "live" in tokens:
        return [_rect(20, 34, 42, 28, 8, fill=BASE), _circle(70, 48, 10, fill=ACCENT), _path("M 78 34 Q 88 48 78 62", fill="none"), _path("M 62 38 Q 56 48 62 58", fill="none")]
    return [_circle(50, 50, 22, fill=BASE), _circle(50, 50, 8, fill=ACCENT)]


def _render_governance(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "parliament" in tokens:
        return [_render_buildings("government_building")[0], *_building_body(24, 30, 52, 46, floors=3), _polygon("50,16 58,20 50,24", fill=ACCENT)]
    if "hammer" in tokens:
        return [_rect(34, 30, 22, 12, 3, fill=BASE), _rect(26, 24, 10, 24, 3, fill=ACCENT), _line(54, 42, 72, 60, stroke_width=5)]
    if "law" in tokens:
        return _document(seal=True)
    if "constitution" in tokens:
        return [_path("M 28 30 Q 36 22 44 30 L 44 72 Q 36 64 28 72 Z", fill=BASE), _path("M 56 30 Q 64 22 72 30 L 72 72 Q 64 64 56 72 Z", fill=ACCENT), _line(50, 30, 50, 72)]
    if "ballot" in tokens:
        return [_document(), _polyline("36,54 44,62 62,42", fill="none", stroke_width=4)]
    if "voting" in tokens:
        return [_rect(24, 46, 52, 24, 6, fill=BASE), _rect(38, 24, 24, 22, 4, fill=MUTED), _line(42, 36, 58, 36)]
    if "flag" in tokens:
        return [_line(34, 20, 34, 78, stroke_width=4), _path("M 36 24 H 72 L 62 40 H 36 Z", fill=ACCENT)]
    if "badge" in tokens:
        return [_polygon("50,22 66,30 70,48 50,78 30,48 34,30", fill=BASE), _circle(50, 44, 8, fill=MUTED)]
    if "camera" in tokens:
        return [_rect(24, 32, 44, 24, 6, fill=BASE), _circle(46, 44, 7, fill=MUTED), _rect(68, 38, 12, 12, 3, fill=ACCENT)]
    if "satellite" in tokens:
        return [_rect(44, 38, 12, 12, 3, fill=BASE), _line(50, 50, 50, 66), _polygon("30,34 42,38 42,50 30,46", fill=ACCENT), _polygon("58,38 70,34 70,46 58,50", fill=ACCENT), _path("M 60 24 Q 72 28 78 40", fill="none")]
    if "tank" in tokens:
        return [_rect(24, 44, 40, 18, 6, fill=BASE), _rect(40, 34, 20, 14, 4, fill=ACCENT), _line(60, 40, 80, 32, stroke_width=4), _circle(34, 66, 5, fill=MUTED), _circle(48, 66, 5, fill=MUTED), _circle(62, 66, 5, fill=MUTED)]
    if "handshake" in tokens:
        return [_path("M 24 48 Q 32 34 46 40 L 52 46 L 44 56 Q 34 60 26 52 Z", fill=BASE), _path("M 76 48 Q 68 34 54 40 L 48 46 L 56 56 Q 66 60 74 52 Z", fill=ACCENT), _line(44, 56, 56, 56)]
    if "border" in tokens:
        return [_line(30, 18, 30, 82, stroke_width=4), _line(70, 18, 70, 82, stroke_width=4), _line(30, 30, 70, 30), _line(30, 70, 70, 70), _polyline("44,42 56,50 44,58", fill="none", stroke_width=4)]
    return [_rect(22, 28, 56, 48, 8, fill=BASE), _circle(50, 52, 10, fill=ACCENT)]


def _render_global(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "globe" in tokens or "map" in tokens:
        return _render_technology("internet_globe")
    if "routes" in tokens:
        return [_line(26, 34, 72, 34), _line(34, 66, 66, 44), _circle(26, 34, 4, fill=BASE), _circle(72, 34, 4, fill=ACCENT), _circle(34, 66, 4, fill=BASE), _circle(66, 44, 4, fill=ACCENT)]
    if "container" in tokens:
        return [_rect(20, 34, 60, 32, 4, fill=BASE), _line(32, 34, 32, 66), _line(44, 34, 44, 66), _line(56, 34, 56, 66), _line(68, 34, 68, 66)]
    if "ship" in tokens:
        return [_path("M 20 62 H 68 L 78 48 L 82 48 L 72 70 H 28 Z", fill=BASE), _rect(32, 36, 24, 12, 2, fill=ACCENT), _line(22, 72, 78, 72)]
    if "airplane" in tokens:
        return [_path("M 18 52 L 80 34 L 68 48 L 86 54 L 82 64 L 60 58 L 52 76 L 42 74 L 46 56 L 20 62 Z", fill=BASE)]
    if "pipeline" in tokens:
        return [_line(22, 42, 46, 42, stroke_width=6), _line(46, 42, 46, 62, stroke_width=6), _line(46, 62, 78, 62, stroke_width=6), _circle(46, 42, 4, fill=ACCENT), _circle(46, 62, 4, fill=ACCENT)]
    if "grid" in tokens:
        return [_line(28, 26, 28, 74), _line(50, 26, 50, 74), _line(72, 26, 72, 74), _line(20, 34, 80, 34), _line(20, 50, 80, 50), _line(20, 66, 80, 66), _circle(50, 50, 6, fill=ACCENT)]
    if "satellite" in tokens:
        return _render_governance("spy_satellite")
    if "communication" in tokens:
        return _render_systems("network_nodes")
    if "migration" in tokens:
        return [_circle(30, 50, 8, fill=BASE), _circle(70, 50, 8, fill=ACCENT), *_arrow("right")]
    return [_circle(50, 50, 24, fill=BASE), _line(50, 26, 50, 74)]


def _render_crisis(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "warning" in tokens:
        return [_polygon("50,18 78,74 22,74", fill=BASE), _line(50, 36, 50, 56, stroke_width=5), _circle(50, 66, 3, fill=MUTED)]
    if "crack" in tokens:
        return [_line(28, 24, 44, 40, stroke_width=5), _line(44, 40, 38, 52, stroke_width=5), _line(38, 52, 56, 64, stroke_width=5), _line(56, 64, 50, 78, stroke_width=5), _line(50, 78, 72, 62, stroke_width=5)]
    if "domino" in tokens:
        return _render_systems("domino_chain")
    if "falling" in tokens or "crash" in tokens or "panic" in tokens:
        return [*_chart_axes(), _polyline("30,34 44,42 56,54 72,68", fill="none", stroke_width=4), *_arrow("down")]
    if "bank" in tokens:
        return [*_render_buildings("bank_building"), _line(22, 74, 78, 26, stroke_width=4)]
    if "building" in tokens:
        return [*_render_buildings("office_building"), _line(38, 28, 62, 76, stroke_width=4)]
    if "power" in tokens:
        return [_render_global("energy_grid")[0], *_render_global("energy_grid")[1:], _line(20, 20, 80, 80, stroke_width=4)]
    if "supply" in tokens:
        return [_render_systems("supply_chain")[0], *_render_systems("supply_chain")[1:], _line(52, 32, 52, 72, stroke_width=4)]
    if "water" in tokens:
        return [_path("M 50 24 Q 64 44 64 56 Q 64 72 50 76 Q 36 72 36 56 Q 36 44 50 24 Z", fill=BASE), _line(34, 62, 66, 44, stroke_width=4)]
    if "climate" in tokens:
        return [_circle(50, 50, 20, fill=ACCENT), _path("M 62 22 L 68 10", fill="none"), _path("M 72 30 L 82 24", fill="none"), _path("M 78 44 L 90 44", fill="none")]
    if "storm" in tokens:
        return [_circle(38, 48, 10, fill=BASE), _circle(52, 42, 12, fill=BASE), _circle(66, 48, 10, fill=BASE), _polygon("48,52 40,70 52,70 44,86 64,62 52,62", fill=ACCENT)]
    if "wildfire" in tokens:
        return [_path("M 50 22 Q 66 40 62 56 Q 60 74 50 78 Q 40 74 38 56 Q 34 40 50 22 Z", fill=ACCENT), _path("M 50 36 Q 58 46 56 58 Q 54 68 50 70 Q 46 68 44 58 Q 42 46 50 36 Z", fill=MUTED)]
    if "flood" in tokens:
        return [_path("M 22 58 Q 30 50 38 58 T 54 58 T 70 58 T 86 58", fill="none"), _path("M 22 70 Q 30 62 38 70 T 54 70 T 70 70 T 86 70", fill="none"), _rect(34, 26, 32, 18, 4, fill=BASE)]
    if "virus" in tokens or "pandemic" in tokens:
        return [_circle(50, 50, 16, fill=BASE), _line(50, 20, 50, 30), _line(50, 70, 50, 80), _line(20, 50, 30, 50), _line(70, 50, 80, 50), _line(30, 30, 36, 36), _line(64, 64, 70, 70), _circle(50, 50, 5, fill=ACCENT)]
    return [_polygon("50,18 78,74 22,74", fill=BASE)]


def _render_environment(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "tree" in tokens:
        return [_circle(50, 38, 16, fill=BASE), _circle(38, 48, 10, fill=BASE), _circle(62, 48, 10, fill=BASE), _rect(46, 54, 8, 22, 3, fill=ACCENT)]
    if "forest" in tokens:
        return [*_render_environment("tree"), _polygon("28,62 40,36 52,62", fill=ACCENT), _polygon("56,62 68,36 80,62", fill=ACCENT)]
    if "water" in tokens and "drop" in tokens:
        return [_path("M 50 20 Q 64 40 64 54 Q 64 72 50 78 Q 36 72 36 54 Q 36 40 50 20 Z", fill=BASE)]
    if "river" in tokens:
        return [_path("M 24 28 Q 52 44 40 74", fill="none", stroke_width=8), _path("M 52 26 Q 74 42 62 76", fill="none", stroke_width=6)]
    if "mountain" in tokens:
        return [_polygon("18,72 38,34 56,58 68,28 82,72", fill=BASE), _polygon("34,42 38,34 42,42", fill=MUTED), _polygon("64,36 68,28 72,36", fill=MUTED)]
    if asset_id == "sun":
        return [_circle(50, 50, 18, fill=ACCENT), _line(50, 18, 50, 28), _line(50, 72, 50, 82), _line(18, 50, 28, 50), _line(72, 50, 82, 50), _line(28, 28, 34, 34), _line(66, 66, 72, 72), _line(66, 34, 72, 28), _line(28, 72, 34, 66)]
    if "wind" in tokens:
        return [_line(50, 26, 50, 76), _circle(50, 34, 5, fill=BASE), _polygon("50,34 70,42 50,46", fill=ACCENT), _polygon("50,34 34,22 46,42", fill=ACCENT), _polygon("50,34 44,56 58,50", fill=ACCENT)]
    if "solar" in tokens:
        return [_polygon("26,58 68,46 74,66 32,78", fill=BASE), _line(32, 78, 28, 84), _line(70, 66, 74, 84), _line(38, 54, 44, 74), _line(50, 50, 56, 70)]
    if "barrel" in tokens:
        return [_ellipse(50, 26, 18, 6, fill=BASE), _rect(32, 26, 36, 44, 0, fill=BASE, stroke=None), _ellipse(50, 70, 18, 6, fill=BASE), _line(32, 40, 68, 40), _line(32, 54, 68, 54)]
    if "pipeline" in tokens:
        return _render_global("pipeline")
    if "farmland" in tokens:
        return [_path("M 24 66 Q 36 54 48 66 T 72 66", fill="none"), _path("M 24 78 Q 36 66 48 78 T 72 78", fill="none"), _line(50, 28, 50, 56), _path("M 50 40 Q 42 34 36 40", fill="none"), _path("M 50 46 Q 58 40 64 46", fill="none")]
    if "food" in tokens:
        return [_circle(50, 52, 18, fill=BASE), _path("M 50 34 Q 56 26 64 30", fill="none"), _line(32, 52, 28, 68), _line(68, 52, 72, 68)]
    return [_circle(50, 50, 18, fill=BASE)]


def _render_future(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if asset_id == "ai_network":
        return _render_technology("ai_brain")
    if asset_id == "robot_worker":
        return [*_render_technology("robot"), _rect(62, 56, 12, 10, 2, fill=ACCENT)]
    if "car" in tokens:
        return [_rect(24, 46, 52, 18, 8, fill=BASE), _path("M 36 46 L 46 34 H 62 L 72 46 Z", fill=ACCENT), _circle(36, 68, 6, fill=MUTED), _circle(64, 68, 6, fill=MUTED)]
    if "city" in tokens:
        elements = _render_buildings("city_skyline")
        elements.append(_line(22, 76, 78, 76))
        elements.append(_circle(72, 24, 4, fill=ACCENT))
        return elements
    if "currency" in tokens:
        return [_circle(50, 50, 20, fill=BASE), _polygon("50,30 64,40 50,70 36,40", fill=ACCENT), _line(50, 24, 50, 76)]
    if "quantum" in tokens or "chip" in tokens:
        return [_rect(30, 30, 40, 40, 6, fill=BASE), _rect(40, 40, 20, 20, 4, fill=ACCENT), _line(20, 40, 30, 40), _line(20, 60, 30, 60), _line(70, 40, 80, 40), _line(70, 60, 80, 60), _line(40, 20, 40, 30), _line(60, 20, 60, 30), _line(40, 70, 40, 80), _line(60, 70, 60, 80)]
    if "automation" in tokens or ("factory" in tokens and "automation" in asset_id):
        return [*_render_buildings("factory"), *_render_abstract("gear")]
    if "satellite" in tokens:
        return _render_governance("spy_satellite")
    if "drone" in tokens:
        return [_circle(50, 50, 8, fill=BASE), _line(50, 50, 30, 34), _line(50, 50, 70, 34), _line(50, 50, 30, 66), _line(50, 50, 70, 66), _circle(30, 34, 6, fill=ACCENT), _circle(70, 34, 6, fill=ACCENT), _circle(30, 66, 6, fill=ACCENT), _circle(70, 66, 6, fill=ACCENT)]
    return [_rect(24, 24, 52, 52, 10, fill=BASE), _circle(50, 50, 10, fill=ACCENT)]


def _render_abstract(asset_id: str) -> list[str]:
    tokens = _token_set(asset_id)
    if "gear" in tokens:
        return [_circle(50, 50, 18, fill=BASE), _circle(50, 50, 7, fill=MUTED), _rect(46, 18, 8, 14, 2, fill=ACCENT), _rect(46, 68, 8, 14, 2, fill=ACCENT), _rect(18, 46, 14, 8, 2, fill=ACCENT), _rect(68, 46, 14, 8, 2, fill=ACCENT), _rect(23, 23, 10, 8, 2, fill=ACCENT), _rect(67, 69, 10, 8, 2, fill=ACCENT), _rect(23, 69, 10, 8, 2, fill=ACCENT), _rect(67, 23, 10, 8, 2, fill=ACCENT)]
    if "lightbulb" in tokens:
        return [_path("M 50 22 Q 68 22 68 42 Q 68 54 58 60 L 58 68 H 42 V 60 Q 32 54 32 42 Q 32 22 50 22 Z", fill=BASE), _rect(42, 68, 16, 8, 2, fill=ACCENT), _line(44, 38, 56, 50), _line(56, 38, 44, 50)]
    if "puzzle" in tokens:
        return [_path("M 26 36 H 42 Q 44 28 50 28 Q 56 28 58 36 H 74 V 52 Q 66 54 66 60 Q 66 66 74 68 V 74 H 58 Q 56 66 50 66 Q 44 66 42 74 H 26 Z", fill=BASE)]
    if "magnet" in tokens:
        return [_path("M 34 24 H 46 V 52 Q 46 62 50 62 Q 54 62 54 52 V 24 H 66 V 54 Q 66 76 50 76 Q 34 76 34 54 Z", fill=BASE), _rect(34, 18, 12, 8, 2, fill=ACCENT), _rect(54, 18, 12, 8, 2, fill=ACCENT)]
    if "chain" in tokens:
        elements = [_ellipse(38, 50, 12, 18, fill="none"), _ellipse(62, 50, 12, 18, fill="none")]
        if "broken" in tokens:
            elements.append(_line(48, 44, 54, 36, stroke_width=4))
            elements.append(_line(48, 56, 54, 64, stroke_width=4))
        else:
            elements.append(_line(50, 42, 50, 58, stroke_width=4))
        return elements
    if asset_id == "key":
        return [_circle(36, 50, 12, fill=BASE), _line(48, 50, 74, 50, stroke_width=5), _line(64, 50, 64, 60, stroke_width=4), _line(72, 50, 72, 58, stroke_width=4)]
    if asset_id == "lock":
        return _render_technology("cybersecurity_lock")
    if "search" in tokens:
        return [_circle(44, 44, 16, fill="none", stroke_width=5), _line(56, 56, 74, 74, stroke_width=5)]
    if "question" in tokens:
        return [_path("M 40 36 Q 40 24 52 24 Q 64 24 64 36 Q 64 44 54 48 Q 48 50 48 58", fill="none", stroke_width=5), _circle(48, 70, 3, fill=ACCENT)]
    if "exclamation" in tokens:
        return [_line(50, 24, 50, 58, stroke_width=5), _circle(50, 70, 4, fill=ACCENT)]
    if "target" in tokens:
        return [_circle(50, 50, 20, fill="none", stroke_width=4), _circle(50, 50, 12, fill="none", stroke_width=4), _circle(50, 50, 4, fill=ACCENT)]
    if "signal" in tokens or "wave" in tokens:
        return [_path("M 20 58 Q 30 42 40 58 T 60 58 T 80 58", fill="none", stroke_width=4), _path("M 24 44 Q 32 30 40 44 T 56 44 T 72 44", fill="none", stroke_width=4)]
    if "balance" in tokens or "scale" in tokens:
        return [_line(50, 24, 50, 74, stroke_width=4), _line(34, 34, 66, 34, stroke_width=4), _line(34, 34, 28, 52), _line(66, 34, 72, 52), _path("M 20 52 H 36 Q 34 64 28 64 Q 22 64 20 52 Z", fill=BASE), _path("M 64 52 H 80 Q 78 64 72 64 Q 66 64 64 52 Z", fill=ACCENT)]
    return [_circle(50, 50, 20, fill=BASE), _circle(50, 50, 8, fill=ACCENT)]


def _render_compatibility(asset_id: str) -> list[str]:
    if asset_id == "bird":
        return [_path("M 20 54 Q 38 28 58 44 Q 68 34 80 38 Q 70 48 62 60 Q 46 70 30 64 Z", fill=BASE), _circle(66, 42, 2, fill=MUTED)]
    if asset_id == "fish":
        return [_path("M 24 50 Q 40 28 62 40 L 76 30 V 70 L 62 60 Q 40 72 24 50 Z", fill=BASE), _circle(54, 46, 2, fill=MUTED)]
    if asset_id == "bee":
        return [_ellipse(50, 52, 18, 12, fill=BASE), _line(42, 44, 42, 60), _line(50, 40, 50, 64), _line(58, 44, 58, 60), _ellipse(40, 40, 8, 6, fill=MUTED), _ellipse(60, 40, 8, 6, fill=MUTED)]
    if asset_id == "deer":
        return [_path("M 28 62 Q 34 38 52 40 Q 68 42 72 58 L 64 58 L 62 74 L 56 74 L 56 60 L 44 60 L 44 74 L 38 74 L 38 58 Z", fill=BASE), _line(46, 36, 40, 24), _line(46, 36, 52, 24), _line(58, 36, 52, 24), _line(58, 36, 64, 24)]
    if asset_id == "turtle":
        return [_ellipse(50, 52, 22, 16, fill=BASE), _circle(72, 50, 6, fill=ACCENT), _circle(34, 66, 4, fill=ACCENT), _circle(66, 66, 4, fill=ACCENT), _polyline("28,52 18,48 18,56", fill="none")]
    if asset_id == "shield":
        return _render_governance("police_badge")
    if asset_id == "lightning":
        return [_polygon("52,18 34,52 48,52 40,82 68,42 54,42", fill=ACCENT)]
    return _render_fallback(asset_id)


def _render_fallback(asset_id: str) -> list[str]:
    _ = asset_id
    return [_circle(50, 50, 18, fill=BASE), _circle(50, 50, 8, fill=ACCENT)]


FAMILY_RENDERERS = {
    "people_society": _render_people,
    "buildings_infrastructure": _render_buildings,
    "money_economy": _render_money,
    "charts_data_visualization": _render_charts,
    "systems_network_diagrams": _render_systems,
    "arrows_flow_indicators": _render_arrows,
    "work_productivity": _render_work,
    "technology_internet": _render_technology,
    "social_media_system": _render_social,
    "governance_power": _render_governance,
    "global_systems": _render_global,
    "crisis_risk": _render_crisis,
    "environment_resources": _render_environment,
    "future_technology": _render_future,
    "abstract_system_symbols": _render_abstract,
    "legacy_compatibility": _render_compatibility,
}
