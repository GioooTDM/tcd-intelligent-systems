"""Illustrate a quadratic regression pattern before and after x -> x²."""

from html import escape
from pathlib import Path
import random


OUT = Path(__file__).resolve().parents[2] / "images/4-features-engineering"
OUT.mkdir(parents=True, exist_ok=True)
BLUE = "#2563eb"
ORANGE = "#d97706"
INK = "#172033"
MUTED = "#526174"
GRID = "#e8edf3"
FONT = "Arial, Helvetica, sans-serif"


def make_data():
    rng = random.Random(24)
    result = []
    for i in range(95):
        x = max(-4.85, min(4.85, -5 + 10 * i / 94 + rng.uniform(-0.045, 0.045)))
        y = max(0.6, 5.5 + 0.92 * x * x + rng.gauss(0, 2.3))
        result.append((x, y))
    return result


DATA = make_data()
mean_u = sum(x * x for x, _ in DATA) / len(DATA)
mean_y = sum(y for _, y in DATA) / len(DATA)
slope = sum((x*x - mean_u) * (y - mean_y) for x, y in DATA) / sum(
    (x*x - mean_u)**2 for x, _ in DATA
)
intercept = mean_y - slope * mean_u
mean_x = sum(x for x, _ in DATA) / len(DATA)
linear_slope = sum((x - mean_x) * (y - mean_y) for x, y in DATA) / sum(
    (x - mean_x) ** 2 for x, _ in DATA
)
linear_intercept = mean_y - linear_slope * mean_x


def text(x, y, value, size=18, color=INK, anchor="middle", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">{escape(value)}</text>'
    )


def panel(x0, y0, width, height, transformed=False, fit=False):
    x_min, x_max = (0, 25) if transformed else (-5, 5)
    y_min, y_max = 0, 35

    def sx(value):
        return x0 + width * (value - x_min) / (x_max - x_min)

    def sy(value):
        return y0 + height * (y_max - value) / (y_max - y_min)

    p = [f'<rect x="{x0}" y="{y0}" width="{width}" height="{height}" fill="#fff"/>']
    for value in ((0, 5, 10, 15, 20, 25) if transformed else (-5, -2.5, 0, 2.5, 5)):
        px = sx(value)
        p.append(f'<path d="M{px:.1f} {y0}V{y0+height}" stroke="{GRID}" stroke-width="1"/>')
        p.append(text(px, y0 + height + 26, f"{value:g}", 15, MUTED))
    for value in (0, 5, 10, 15, 20, 25, 30, 35):
        py = sy(value)
        p.append(f'<path d="M{x0} {py:.1f}H{x0+width}" stroke="{GRID}" stroke-width="1"/>')
        p.append(text(x0 - 13, py + 5, str(value), 15, MUTED, "end"))
    if fit:
        path = []
        for i in range(241):
            value = x_min + (x_max - x_min) * i / 240
            predicted = intercept + slope * (value if transformed else value * value)
            path.append(f'{"M" if i == 0 else "L"}{sx(value):.2f} {sy(predicted):.2f}')
        p.append(f'<path d="{" ".join(path)}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round"/>')
    for x, y in DATA:
        px, py = sx(x*x if transformed else x), sy(y)
        p.append(f'<path d="M{px-3.2:.1f} {py-3.2:.1f}l6.4 6.4m0-6.4l-6.4 6.4" stroke="{BLUE}" stroke-width="1.5" stroke-linecap="round"/>')
    p.extend([
        f'<rect x="{x0}" y="{y0}" width="{width}" height="{height}" fill="none" stroke="#9eacbc" stroke-width="1.5"/>',
        text(x0 + width / 2, y0 + height + 60, "x²" if transformed else "x", 22),
        f'<g transform="translate({x0-62} {y0+height/2}) rotate(-90)">{text(0, 0, "y", 22)}</g>',
    ])
    return "".join(p)


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
    text(410, 52, "A curved pattern in the original input", 26, weight="bold"),
    text(410, 86, "The same values of y can occur at negative and positive x", 17, MUTED),
    panel(155, 115, 520, 465),
    f'<path d="M337 674l12 12m0-12-12 12" stroke="{BLUE}" stroke-width="2" stroke-linecap="round"/>',
    text(369, 688, "Observed examples", 17, MUTED, "start"),
])
(OUT / "quadratic-pattern-original-input.svg").write_text(svg(
    820, 720, "Quadratic pattern in original input",
    "Noisy observations form a U-shaped pattern when y is plotted against the original input x.",
    single,
))

comparison = "".join([
    text(690, 52, "A quadratic curve becomes a straight line", 27, weight="bold"),
    text(348, 95, "Original input", 19, MUTED),
    text(1030, 95, "Engineered feature", 19, MUTED),
    panel(125, 126, 475, 460, fit=True),
    panel(800, 126, 475, 460, transformed=True, fit=True),
    f'<path d="M570 680h34" stroke="{ORANGE}" stroke-width="3"/>',
    text(617, 686, "Fitted model", 17, MUTED, "start"),
])
(OUT / "quadratic-feature-mapping.svg").write_text(svg(
    1380, 720, "Quadratic curve and linear fit after squaring x",
    "The same noisy observations have a curved fitted model against x and a straight fitted model against x squared.",
    comparison,
))

# Reuse the same noisy quadratic observations to make an underfitting example.
W, H = 1120, 670
x0, y0, plot_width, plot_height = 110, 48, 900, 500
x_min, x_max, y_min, y_max = -5, 5, 0, 35


def sx(value):
    return x0 + plot_width * (value - x_min) / (x_max - x_min)


def sy(value):
    return y0 + plot_height * (y_max - value) / (y_max - y_min)


underfit_parts = [f'<rect x="{x0}" y="{y0}" width="{plot_width}" height="{plot_height}" fill="#fff"/>']
for value in (-5, -2.5, 0, 2.5, 5):
    px = sx(value)
    underfit_parts.extend([
        f'<path d="M{px:.1f} {y0}V{y0+plot_height}" stroke="{GRID}"/>',
        text(px, y0 + plot_height + 26, f"{value:g}", 15, MUTED),
    ])
for value in range(0, 36, 5):
    py = sy(value)
    underfit_parts.extend([
        f'<path d="M{x0} {py:.1f}H{x0+plot_width}" stroke="{GRID}"/>',
        text(x0 - 13, py + 5, str(value), 15, MUTED, "end"),
    ])

curve = []
for i in range(241):
    x = x_min + (x_max - x_min) * i / 240
    curve.append(f'{"M" if i == 0 else "L"}{sx(x):.2f} {sy(intercept + slope*x*x):.2f}')
underfit_parts.append(
    f'<path d="{" ".join(curve)}" fill="none" stroke="#65a30d" stroke-width="3.5" stroke-linecap="round"/>'
)
underfit_parts.append(
    f'<path d="M{sx(x_min):.2f} {sy(linear_intercept+linear_slope*x_min):.2f} '
    f'L{sx(x_max):.2f} {sy(linear_intercept+linear_slope*x_max):.2f}" '
    'fill="none" stroke="#d97706" stroke-width="3.5" stroke-linecap="round"/>'
)
for x, y in DATA:
    underfit_parts.append(
        f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="3.1" fill="{BLUE}" fill-opacity="0.65"/>'
    )
underfit_parts.extend([
    f'<rect x="{x0}" y="{y0}" width="{plot_width}" height="{plot_height}" fill="none" stroke="#9eacbc" stroke-width="1.5"/>',
    text(x0 + plot_width / 2, y0 + plot_height + 60, "Input x", 22),
    f'<g transform="translate({x0-62} {y0+plot_height/2}) rotate(-90)">{text(0, 0, "Output y", 22)}</g>',
    f'<rect x="790" y="64" width="198" height="70" rx="5" fill="#fff" fill-opacity="0.96" stroke="#aab7c6"/>',
    f'<path d="M798 87h20" stroke="#d97706" stroke-width="3.5"/>',
    text(827, 92, "Linear fit", 15, MUTED, "start"),
    f'<path d="M798 111h20" stroke="#65a30d" stroke-width="3.5"/>',
    text(827, 116, "Quadratic fit", 15, MUTED, "start"),
])
(OUT / "linear-vs-quadratic-underfitting.svg").write_text(svg(
    W, H,
    "Linear and quadratic fits to a quadratic data pattern",
    "Observed data follow a U-shaped quadratic pattern. The linear fit is nearly flat and underfits; the quadratic fit follows the pattern.",
    "".join(underfit_parts),
))
