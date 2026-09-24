"""Generate the two-view illustration for lecture 3 using only the Python standard library."""

from pathlib import Path


OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "images/3-logistic-regression/decision-boundary-3d-and-2d.svg"
)

# Coordinates are shared by both views. The class is sign(x1 - x2).
EXAMPLES = [
    (0.15, 0.72, -1),
    (0.30, 0.62, -1),
    (0.46, 0.82, -1),
    (0.69, 0.90, -1),
    (0.32, 0.10, +1),
    (0.57, 0.25, +1),
    (0.74, 0.18, +1),
    (0.83, 0.40, +1),
]


def project_3d(x1, x2, label):
    """Oblique projection of (x1, x2, predicted label) onto the SVG canvas."""
    return 375 + 230 * x1 - 140 * x2, 270 + 75 * x1 + 75 * x2 - 90 * label


def project_2d(x1, x2):
    return 720 + 460 * x1, 515 - 320 * x2


def point_list(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" '
    'viewBox="0 0 1280 640" role="img" aria-labelledby="title desc">',
    '<title id="title">The same linear classifier in 3D and 2D</title>',
    '<desc id="desc">The left panel plots the predicted class as a height of plus one or minus one above the x one and x two plane. The right panel shows the same eight examples and the decision boundary x one equals x two from above.</desc>',
    '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" '
    'orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#34475b"/></marker></defs>',
    '<rect width="1280" height="640" rx="22" fill="#f4f7fa"/>',
    '<rect x="24" y="24" width="600" height="552" rx="18" fill="#fff" stroke="#d8e1e9"/>',
    '<rect x="656" y="24" width="600" height="552" rx="18" fill="#fff" stroke="#d8e1e9"/>',
    '<g font-family="Arial, Helvetica, sans-serif" fill="#172533">',
    '<text x="54" y="69" font-size="27" font-weight="700">3D view: predicted class as height</text>',
    '<text x="54" y="101" font-size="18" fill="#526273">The surface jumps between −1 and +1 at the boundary.</text>',
    '<text x="686" y="69" font-size="27" font-weight="700">2D view: the same boundary from above</text>',
    '<text x="686" y="101" font-size="18" fill="#526273">The dashed line is x₁ = x₂.</text>',
    '</g>',
]

# 3D view: lower and upper class regions are triangular pieces of one unit square.
lower = [project_3d(0, 0, -1), project_3d(0, 1, -1), project_3d(1, 1, -1)]
upper = [project_3d(0, 0, +1), project_3d(1, 0, +1), project_3d(1, 1, +1)]
wall = [project_3d(0, 0, +1), project_3d(1, 1, +1),
        project_3d(1, 1, -1), project_3d(0, 0, -1)]
base = [project_3d(0, 0, -1), project_3d(1, 0, -1),
        project_3d(1, 1, -1), project_3d(0, 1, -1)]
parts.extend([
    '<g transform="translate(-84 0)">',
    f'<polygon points="{point_list(base)}" fill="#f8fafc" stroke="#c8d4df" stroke-width="2"/>',
    f'<polygon points="{point_list(lower)}" fill="#f9deda" stroke="#c75349" stroke-width="2.5"/>',
    f'<polygon points="{point_list(wall)}" fill="#e3e9f0" stroke="#8193a5" stroke-width="2"/>',
    f'<polygon points="{point_list(upper)}" fill="#dcebf9" stroke="#2773a7" stroke-width="2.5"/>',
    '<line x1="375" y1="360" x2="610" y2="437" stroke="#34475b" '
    'stroke-width="2.5" marker-end="url(#arrow)"/>',
    '<line x1="375" y1="360" x2="230" y2="438" stroke="#34475b" '
    'stroke-width="2.5" marker-end="url(#arrow)"/>',
    '<line x1="375" y1="360" x2="375" y2="172" stroke="#34475b" '
    'stroke-width="2.5" marker-end="url(#arrow)"/>',
    '<g font-family="Arial, Helvetica, sans-serif" font-size="19" fill="#172533">',
    '<text x="605" y="467">x₁</text><text x="204" y="460">x₂</text>',
    '<text x="345" y="161">h</text>',
    '<text x="533" y="223" fill="#215f8b" font-weight="700">+1</text>',
    '<text x="241" y="466" fill="#ad3f38" font-weight="700">−1</text>',
    '</g>',
])

# Small ticks show the scale without crowding the two class surfaces.
for fraction in (0.25, 0.5, 0.75):
    x, y = project_3d(fraction, 0, -1)
    parts.append(
        f'<line x1="{x-3:.1f}" y1="{y+7:.1f}" x2="{x+3:.1f}" y2="{y-7:.1f}" '
        'stroke="#526273" stroke-width="1.6"/>'
    )
    x, y = project_3d(0, fraction, -1)
    parts.append(
        f'<line x1="{x-4:.1f}" y1="{y-7:.1f}" x2="{x+4:.1f}" y2="{y+7:.1f}" '
        'stroke="#526273" stroke-width="1.6"/>'
    )

for height in (-0.5, 0, 0.5):
    x, y = project_3d(0, 0, height)
    parts.append(
        f'<line x1="{x-6:.1f}" y1="{y:.1f}" x2="{x+6:.1f}" y2="{y:.1f}" '
        'stroke="#526273" stroke-width="1.6"/>'
    )

parts.extend([
    '<g font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#526273">',
    '<text x="483" y="424">0.5</text>',
    '<text x="278" y="384">0.5</text>',
    '<text x="351" y="275">0</text>',
    '</g>',
])

for x1, x2, label in EXAMPLES:
    x, y = project_3d(x1, x2, label)
    colour = "#2279b2" if label == 1 else "#d65148"
    parts.append(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{colour}" '
        'stroke="#fff" stroke-width="2.5"/>'
    )

parts.append('</g>')

# 2D view: the two coloured triangles meet on x1 = x2.
parts.extend([
    '<polygon points="720,195 1180,195 720,515" fill="#fce9e6"/>',
    '<polygon points="720,515 1180,195 1180,515" fill="#e9f3fb"/>',
    '<rect x="720" y="195" width="460" height="320" fill="none" '
    'stroke="#c8d4df" stroke-width="1.5"/>',
    '<line x1="720" y1="515" x2="1180" y2="195" stroke="#34475b" '
    'stroke-width="3.5" stroke-dasharray="12 9"/>',
    '<line x1="720" y1="515" x2="1193" y2="515" stroke="#34475b" '
    'stroke-width="2.5" marker-end="url(#arrow)"/>',
    '<line x1="720" y1="515" x2="720" y2="182" stroke="#34475b" '
    'stroke-width="2.5" marker-end="url(#arrow)"/>',
    '<g font-family="Arial, Helvetica, sans-serif" fill="#172533">',
    '<text x="1192" y="543" font-size="20">x₁</text>',
    '<text x="690" y="189" font-size="20">x₂</text>',
    '<text x="760" y="391" font-size="20" font-weight="700" fill="#ad3f38">−1: x₂ &gt; x₁</text>',
    '<text x="1000" y="356" font-size="20" font-weight="700" fill="#215f8b">+1: x₁ &gt; x₂</text>',
    '</g>',
])

# Quarter-interval ticks match the 3D axes without restoring number labels.
for fraction in (0.25, 0.5, 0.75):
    x, y = project_2d(fraction, 0)
    parts.append(
        f'<line x1="{x:.1f}" y1="{y-6:.1f}" x2="{x:.1f}" y2="{y+6:.1f}" '
        'stroke="#526273" stroke-width="1.6"/>'
    )
    x, y = project_2d(0, fraction)
    parts.append(
        f'<line x1="{x-6:.1f}" y1="{y:.1f}" x2="{x+6:.1f}" y2="{y:.1f}" '
        'stroke="#526273" stroke-width="1.6"/>'
    )

for x1, x2, label in EXAMPLES:
    x, y = project_2d(x1, x2)
    colour = "#2279b2" if label == 1 else "#d65148"
    parts.append(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{colour}" '
        'stroke="#fff" stroke-width="2.5"/>'
    )

parts.extend([
    '<text x="640" y="612" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
    'font-size="19" fill="#40546a">One rule: hθ(x) = sign(0.5x₁ − 0.5x₂)</text>',
    '</svg>',
])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(OUTPUT)
