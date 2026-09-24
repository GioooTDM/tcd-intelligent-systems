"""Show four weather classes and their one-vs-rest linear boundaries."""

from html import escape
from pathlib import Path


OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "images/3-logistic-regression/one-vs-rest-weather-boundaries.svg"
)

WIDTH, HEIGHT = 1200, 1130
CLASSES = (
    ("Sunny", "#e29a32", "#fff2df", [(0.72, 0.16), (0.81, 0.24), (0.86, 0.13)]),
    ("Cloudy", "#8b73bb", "#f2eef9", [(0.18, 0.16), (0.25, 0.24), (0.31, 0.14)]),
    ("Rain", "#2979b4", "#eaf4fb", [(0.72, 0.77), (0.82, 0.87), (0.89, 0.70)]),
    ("Snow", "#2e9f9a", "#e9f7f5", [(0.16, 0.75), (0.25, 0.86), (0.33, 0.72)]),
)

# Each line separates the listed class from the other three point clusters.
BOUNDARIES = (
    ("Sunny", [(0.4, 0), (1, 0.6)], [(0.4, 0), (1, 0), (1, 0.6)]),
    ("Cloudy", [(0, 0.6), (0.6, 0)], [(0, 0), (0.6, 0), (0, 0.6)]),
    ("Rain", [(0.35, 1), (1, 0.35)], [(0.35, 1), (1, 1), (1, 0.35)]),
    ("Snow", [(0, 0.35), (0.65, 1)], [(0, 0.35), (0, 1), (0.65, 1)]),
)


def svg_text(x, y, value, size=16, colour="#26384b", extra=""):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{colour}" {extra}>{escape(value)}</text>'
    )


def project(x, y, left, top, width, height):
    return left + x * width, top + (1 - y) * height


def axes(left, top, width, height, x_label, y_label):
    bottom = top + height
    return [
        f'<line x1="{left}" y1="{bottom}" x2="{left+width+9}" y2="{bottom}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{left}" y2="{top-9}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        svg_text(left+width/2, bottom+29, x_label, 14, "#526273",
                 'text-anchor="middle"'),
        svg_text(left-34, top+height/2, y_label, 14, "#526273",
                 f'text-anchor="middle" transform="rotate(-90 {left-34} {top+height/2})"'),
    ]


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
    '<title id="title">Four weather classes viewed as one-vs-rest classifiers</title>',
    '<desc id="desc">The top plot contains illustrative Sunny, Cloudy, Rain, '
    'and Snow clusters in temperature and precipitation space. Four lower '
    'plots each highlight one class as positive, leave all other examples '
    'hollow and negative, and show a separate linear decision boundary.</desc>',
    '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
    'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
    'fill="#41566d"/></marker></defs>',
    f'<rect width="{WIDTH}" height="{HEIGHT}" rx="20" fill="#f5f8fb"/>',
    svg_text(46, 48, "One-vs-rest: four weather classes", 28,
             extra='font-weight="700"'),
    svg_text(46, 79, "x₁ = temperature · x₂ = precipitation (illustrative normalised features)",
             17, "#526273"),
    '<rect x="200" y="101" width="800" height="355" rx="17" '
    'fill="#fff" stroke="#d9e3ec"/>',
    svg_text(226, 133, "All classes together", 19,
             extra='font-weight="700"'),
]

main_left, main_top, main_width, main_height = 348, 155, 490, 245
parts.extend(axes(main_left, main_top, main_width, main_height,
                  "temperature x₁", "precipitation x₂"))
for index, (name, colour, _, points) in enumerate(CLASSES):
    legend_y = 186 + index * 47
    parts.extend([
        f'<circle cx="887" cy="{legend_y-5}" r="7" fill="{colour}" '
        'stroke="#fff" stroke-width="1.5"/>',
        svg_text(906, legend_y, name, 16),
    ])
    for x, y in points:
        cx, cy = project(x, y, main_left, main_top, main_width, main_height)
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{colour}" '
            'stroke="#fff" stroke-width="2"/>'
        )

parts.extend([
    '<line x1="600" y1="468" x2="600" y2="496" '
    'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
    svg_text(600, 515,
             "One positive class (+1) against the other three classes (−1)",
             17, "#344a61", 'text-anchor="middle"'),
])

for index, (name, line, positive_polygon) in enumerate(BOUNDARIES):
    column, row = index % 2, index // 2
    panel_x, panel_y = (40 if column == 0 else 620), (535 if row == 0 else 835)
    left, top, width, height = panel_x + 115, panel_y + 54, 385, 175
    colour = next(item[1] for item in CLASSES if item[0] == name)
    pale = next(item[2] for item in CLASSES if item[0] == name)
    points_string = " ".join(
        f"{project(x, y, left, top, width, height)[0]:.1f},"
        f"{project(x, y, left, top, width, height)[1]:.1f}"
        for x, y in positive_polygon
    )
    x1, y1 = project(*line[0], left, top, width, height)
    x2, y2 = project(*line[1], left, top, width, height)
    parts.extend([
        f'<rect x="{panel_x}" y="{panel_y}" width="540" height="280" '
        'rx="16" fill="#fff" stroke="#d9e3ec"/>',
        svg_text(panel_x+25, panel_y+33, f"{name} (+1) vs rest (−1)", 18,
                 extra='font-weight="700"'),
        f'<polygon points="{points_string}" fill="{pale}"/>',
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        'stroke="#344a61" stroke-width="2.5"/>',
    ])
    parts.extend(axes(left, top, width, height, "temperature x₁",
                      "precipitation x₂"))
    for class_name, class_colour, _, class_points in CLASSES:
        for x, y in class_points:
            cx, cy = project(x, y, left, top, width, height)
            if class_name == name:
                fill, stroke, stroke_width = class_colour, "#fff", 1.7
            else:
                fill, stroke, stroke_width = "#fff", "#8190a0", 1.5
            parts.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" '
                f'fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{stroke_width}"/>'
            )

parts.append('</svg>')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(OUTPUT)
