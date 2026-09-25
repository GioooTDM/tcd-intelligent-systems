"""Draw the circular-classification example in original and squared features."""

from html import escape
from pathlib import Path
import random


OUT = Path(__file__).resolve().parents[2] / "images/4-features-engineering"
OUT.mkdir(parents=True, exist_ok=True)
RADIUS = 0.255
BLUE = "#2563eb"
ORANGE = "#d97706"
INK = "#172033"
MUTED = "#526174"
GRID = "#e8edf3"
FONT = "Arial, Helvetica, sans-serif"


def points():
    rng = random.Random(14)
    inside = []
    outside = []
    while len(inside) < 20 or len(outside) < 100:
        x = rng.uniform(-0.49, 0.49)
        y = rng.uniform(-0.49, 0.49)
        if x * x + y * y < RADIUS * RADIUS:
            if len(inside) < 20:
                inside.append((x, y))
        elif len(outside) < 100:
            outside.append((x, y))
    return inside, outside


POSITIVE, NEGATIVE = points()


def text(x, y, value, size=18, color=INK, anchor="middle", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">{escape(value)}</text>'
    )


def original_panel(x0, y0, side):
    def sx(x):
        return x0 + side * (x + 0.5)

    def sy(y):
        return y0 + side * (0.5 - y)

    p = [
        f'<rect x="{x0}" y="{y0}" width="{side}" height="{side}" fill="#fff"/>',
    ]
    for tick in (-0.5, -0.25, 0, 0.25, 0.5):
        px, py = sx(tick), sy(tick)
        p.append(f'<path d="M{px:.1f} {y0}V{y0+side} M{x0} {py:.1f}H{x0+side}" stroke="{GRID}" stroke-width="1"/>')
        label = f"{tick:g}"
        p.append(text(px, y0 + side + 25, label, 14, MUTED))
        p.append(text(x0 - 13, py + 5, label, 14, MUTED, "end"))
    p.extend([
        f'<circle cx="{sx(0):.1f}" cy="{sy(0):.1f}" r="{RADIUS*side:.1f}" fill="#fff4e7" stroke="{ORANGE}" stroke-width="2.4"/>',
    ])
    for x, y in NEGATIVE:
        px, py = sx(x), sy(y)
        p.append(f'<path d="M{px-4:.1f} {py-4:.1f}l8 8m0-8l-8 8" stroke="{BLUE}" stroke-width="1.7" stroke-linecap="round"/>')
    for x, y in POSITIVE:
        p.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.2" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>')
    p.extend([
        f'<rect x="{x0}" y="{y0}" width="{side}" height="{side}" fill="none" stroke="#9eacbc" stroke-width="1.5"/>',
        text(x0 + side / 2, y0 + side + 59, "x₁", 22, INK),
        f'<g transform="translate({x0-63} {y0+side/2}) rotate(-90)">{text(0, 0, "x₂", 22, INK)}</g>',
    ])
    return "".join(p)


def mapped_panel(x0, y0, side):
    limit = 0.25

    def sx(u):
        return x0 + side * u / limit

    def sy(v):
        return y0 + side * (1 - v / limit)

    p = [f'<rect x="{x0}" y="{y0}" width="{side}" height="{side}" fill="#fff"/>']
    for i in range(6):
        tick = 0.05 * i
        px, py = sx(tick), sy(tick)
        p.append(f'<path d="M{px:.1f} {y0}V{y0+side} M{x0} {py:.1f}H{x0+side}" stroke="{GRID}" stroke-width="1"/>')
        label = "0" if i == 0 else f"{tick:.2f}"
        p.append(text(px, y0 + side + 25, label, 14, MUTED))
        p.append(text(x0 - 13, py + 5, label, 14, MUTED, "end"))
    p.extend([
        f'<path d="M{sx(0):.1f} {sy(0):.1f}L{sx(RADIUS**2):.1f} {sy(0):.1f}L{sx(0):.1f} {sy(RADIUS**2):.1f}Z" fill="#fff4e7"/>',
        f'<path d="M{sx(0):.1f} {sy(RADIUS**2):.1f}L{sx(RADIUS**2):.1f} {sy(0):.1f}" stroke="{ORANGE}" stroke-width="2.4"/>',
    ])
    for x, y in NEGATIVE:
        px, py = sx(x*x), sy(y*y)
        p.append(f'<path d="M{px-4:.1f} {py-4:.1f}l8 8m0-8l-8 8" stroke="{BLUE}" stroke-width="1.7" stroke-linecap="round"/>')
    for x, y in POSITIVE:
        p.append(f'<circle cx="{sx(x*x):.1f}" cy="{sy(y*y):.1f}" r="4.2" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>')
    p.extend([
        f'<rect x="{x0}" y="{y0}" width="{side}" height="{side}" fill="none" stroke="#9eacbc" stroke-width="1.5"/>',
        text(x0 + side / 2, y0 + side + 59, "x₁²", 22, INK),
        f'<g transform="translate({x0-67} {y0+side/2}) rotate(-90)">{text(0, 0, "x₂²", 22, INK)}</g>',
    ])
    return "".join(p)


def legend(x, y):
    return "".join([
        f'<circle cx="{x}" cy="{y-5}" r="5" fill="#fff" stroke="{ORANGE}" stroke-width="2"/>',
        text(x + 14, y, "Inside (+1)", 16, MUTED, "start"),
        f'<path d="M{x+145} {y-10}l10 10m0-10l-10 10" stroke="{BLUE}" stroke-width="2"/>',
        text(x + 167, y, "Outside (−1)", 16, MUTED, "start"),
    ])


def svg(width, height, title, desc, contents):
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(desc)}</desc>',
        f'<rect width="{width}" height="{height}" fill="#fff"/>',
        contents,
        '</svg>\n',
    ])


single = "".join([
    text(410, 48, "Circular decision boundary", 26, INK, weight="bold"),
    text(410, 82, "Original features", 18, MUTED),
    original_panel(165, 113, 490),
    legend(250, 695),
])
(OUT / "circularly-separated-classes.svg").write_text(svg(
    820, 725, "Classes separated by a circle",
    "Orange positive examples lie inside a circular boundary in x1, x2 space; blue negative examples lie outside.",
    single,
))

comparison = "".join([
    text(690, 49, "A circular boundary becomes a line", 27, INK, weight="bold"),
    text(340, 94, "Original features", 19, MUTED),
    text(1040, 94, "Squared features", 19, MUTED),
    original_panel(105, 130, 475),
    mapped_panel(800, 130, 475),
    legend(511, 700),
])
(OUT / "circular-boundary-feature-mapping.svg").write_text(svg(
    1380, 730, "Circular boundary in original and squared feature spaces",
    "The same orange positive and blue negative examples are separated by a circle in original coordinates and by a straight line in squared coordinates.",
    comparison,
))
