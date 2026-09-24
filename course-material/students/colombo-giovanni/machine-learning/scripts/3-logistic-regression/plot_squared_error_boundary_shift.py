"""Illustrate how an outlier shifts a least-squares class boundary."""

from pathlib import Path


OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "images/3-logistic-regression/squared-error-boundary-shift.svg"
)

BASE = [
    (0.8, -1), (1.1, -1), (1.4, -1),
    (5.2, +1), (5.5, +1), (5.8, +1),
]
WITH_OUTLIER = BASE + [(2.5, +1)]


def least_squares(points):
    """Fit z(x) = intercept + slope*x to labels y in {-1, +1}."""
    count = len(points)
    mean_x = sum(x for x, _ in points) / count
    mean_y = sum(y for _, y in points) / count
    slope = sum((x - mean_x) * (y - mean_y) for x, y in points) / sum(
        (x - mean_x) ** 2 for x, _ in points
    )
    intercept = mean_y - slope * mean_x
    return intercept, slope


def svg_text(x, y, label, size=17, fill="#223247", extra=""):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{fill}" {extra}>{label}</text>'
    )


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="440" '
    'viewBox="0 130 1280 440" role="img" aria-labelledby="title desc">',
    '<title id="title">The effect of an outlier on squared-error classification</title>',
    '<desc id="desc">Both panels show the same three red negative examples near x equals 1 and three blue positive examples near x equals 5.5, in identical positions. Pale red and blue areas mark predictions negative and positive on either side of the dashed green boundary. The second panel adds a blue positive example at x equals 2.5 in the predicted-negative area. The least-squares decision boundary shifts from x equals 3.30 to x equals 2.84.</desc>',
    '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" '
    'orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#41566d"/></marker></defs>',
    '<rect y="130" width="1280" height="440" rx="20" fill="#f5f8fb"/>',
    svg_text(640, 165, "The effect of an outlier on squared-error classification",
             23, "#223247", 'font-weight="700" text-anchor="middle"'),
]


def draw_panel(panel_x, points):
    intercept, slope = least_squares(points)
    boundary = -intercept / slope
    left, right = panel_x + 80, panel_x + 550
    axis_y, scale_y = 350, 75

    def px(x):
        return left + (right - left) * x / 7

    def py(score):
        return axis_y - scale_y * score

    parts.extend([
        f'<rect x="{panel_x}" y="185" width="600" height="340" rx="16" '
        'fill="#fff" stroke="#d9e3ec"/>',
        f'<rect x="{left:.1f}" y="225" width="{px(boundary) - left:.1f}" '
        'height="240" fill="#fff0ee"/>',
        f'<rect x="{px(boundary):.1f}" y="225" '
        f'width="{right - px(boundary):.1f}" height="240" fill="#eef6fc"/>',
        svg_text((left + px(boundary)) / 2, 251, "Predicted −1", 15,
                 "#a33f38", 'font-weight="700" text-anchor="middle"'),
        svg_text((px(boundary) + right) / 2, 251, "Predicted +1", 15,
                 "#21648f", 'font-weight="700" text-anchor="middle"'),
        f'<line x1="{left}" y1="465" x2="{left}" y2="225" stroke="#41566d" '
        'stroke-width="2" marker-end="url(#arrow)"/>',
        svg_text(left - 58, 350, "score z / label y", 14, "#526273",
                 f'text-anchor="middle" transform="rotate(-90 {left - 58} 350)"'),
        svg_text(left - 42, py(+1) + 6, "+1", 15, "#526273"),
        svg_text(left - 42, py(-1) + 6, "−1", 15, "#526273"),
        svg_text(right - 12, 403, "feature x", 16, "#526273",
                 'text-anchor="end"'),
        f'<line x1="{px(boundary):.1f}" y1="225" '
        f'x2="{px(boundary):.1f}" y2="465" '
        'stroke="#2e9867" stroke-width="2.5" stroke-dasharray="7 6"/>',
    ])

    for level in (-1, +1):
        parts.append(
            f'<line x1="{left:.1f}" y1="{py(level):.1f}" '
            f'x2="{right:.1f}" y2="{py(level):.1f}" '
            'stroke="#e3eaf0" stroke-width="1.5"/>'
        )
        parts.append(
            f'<line x1="{left - 6:.1f}" y1="{py(level):.1f}" '
            f'x2="{left + 6:.1f}" y2="{py(level):.1f}" '
            'stroke="#41566d" stroke-width="1.5"/>'
        )

    parts.append(
        f'<line x1="{left}" y1="{axis_y}" x2="{right + 8}" y2="{axis_y}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>'
    )

    line_end = min(7, (225 - axis_y) / (-scale_y * slope) - intercept / slope)
    parts.append(
        f'<line x1="{px(0):.1f}" y1="{py(intercept):.1f}" '
        f'x2="{px(line_end):.1f}" y2="{py(intercept + slope * line_end):.1f}" '
        'stroke="#344a61" stroke-width="3"/>'
    )

    for x, y in points:
        cx, cy = px(x), py(y)
        colour = "#2979b4" if y == 1 else "#d4554c"
        if x == 2.5 and len(points) > len(BASE):
            parts.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="14" '
                'fill="none" stroke="#e4a137" stroke-width="3"/>'
            )
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7.5" fill="{colour}" '
            'stroke="#fff" stroke-width="2"/>'
        )

    for x in range(8):
        tick_x = px(x)
        parts.append(
            f'<line x1="{tick_x:.1f}" y1="344" x2="{tick_x:.1f}" y2="356" '
            'stroke="#41566d" stroke-width="1.5"/>'
        )
        if x != 0:
            parts.append(svg_text(tick_x - 5, 375, str(x), 14, "#526273"))

    parts.append(
        svg_text(px(boundary) - 49, 487, f"boundary x ≈ {boundary:.2f}", 16,
                 "#227d56", 'font-weight="700"')
    )
    return boundary


first = draw_panel(24, BASE)
second = draw_panel(656, WITH_OUTLIER)

parts.extend([
    svg_text(640, 555,
             "The green line separates predicted −1 (left) from predicted +1 (right).",
             18, "#344a61", 'text-anchor="middle"'),
    '</svg>',
])

assert 2.5 < second < first
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"{OUTPUT}: boundaries {first:.2f} and {second:.2f}")
