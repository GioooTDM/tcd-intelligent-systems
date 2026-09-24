"""Draw ten labelled emails and their one-parameter logistic cost."""

from math import exp, log1p
from pathlib import Path


OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "images/3-logistic-regression/logistic-cost-ten-emails.svg"
)

# Feature: number of spam keywords. Labels: normal -1, spam +1.
EMAILS = [
    (0, -1), (1, -1), (2, -1), (3, -1), (6, -1),
    (4, +1), (5, +1), (7, +1), (8, +1), (9, +1),
]
WIDTH, HEIGHT = 1000, 640


def cost(intercept):
    """Average logistic loss with score = intercept + keyword count."""
    return sum(
        log1p(exp(-label_value * (intercept + count)))
        for count, label_value in EMAILS
    ) / len(EMAILS)


def svg_text(x, y, value, size=16, colour="#26384b", extra=""):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" '
        'font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{colour}" {extra}>{value}</text>'
    )


def email_x(count):
    return 190 + count * 700 / 9


def cost_x(intercept):
    return 160 + (intercept + 8) * 750 / 7


def cost_y(value):
    return 555 - value * 165 / 1.05


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
    '<title id="title">Logistic cost for ten labelled emails</title>',
    '<desc id="desc">The upper plot shows five normal and five spam emails '
    'at different spam-keyword counts. With slope one and intercept minus '
    'four point five, the boundary lies between counts four and five; '
    'a spam email at four and a normal email at six are misclassified. '
    'The lower plot shows their average logistic cost as the intercept '
    'changes. It is convex and has a minimum near minus four point five.</desc>',
    '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
    'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
    'fill="#41566d"/></marker></defs>',
    f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#f5f8fb"/>',
    svg_text(38, 44, "Logistic cost for ten labelled emails", 26,
             extra='font-weight="700"'),
    svg_text(38, 72, "One feature: spam-keyword count · slope θ₁ = 1 · intercept θ₀ varies",
             16, "#526273"),
    '<rect x="25" y="91" width="950" height="239" rx="16" '
    'fill="#fff" stroke="#d9e3ec"/>',
    svg_text(48, 117, "The emails at the best boundary", 17,
             extra='font-weight="700"'),
    f'<rect x="170" y="130" width="{email_x(4.5)-170:.1f}" height="145" '
    'fill="#fff0ee"/>',
    f'<rect x="{email_x(4.5):.1f}" y="130" '
    f'width="{910-email_x(4.5):.1f}" height="145" fill="#eef6fc"/>',
    svg_text(350, 153, "Predict normal (−1)", 15, "#a33f38",
             'font-weight="700" text-anchor="middle"'),
    svg_text(730, 153, "Predict spam (+1)", 15, "#21648f",
             'font-weight="700" text-anchor="middle"'),
    f'<line x1="{email_x(4.5):.1f}" y1="130" '
    f'x2="{email_x(4.5):.1f}" y2="275" '
    'stroke="#2e9867" stroke-width="2.5" stroke-dasharray="7 6"/>',
    svg_text(155, 190, "Spam +1", 14, "#526273", 'text-anchor="end"'),
    svg_text(155, 244, "Normal −1", 14, "#526273", 'text-anchor="end"'),
]

for count, true_label in EMAILS:
    x = email_x(count)
    y = 185 if true_label == 1 else 239
    wrong = (count >= 5) != (true_label == 1)
    if wrong:
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y}" r="14" fill="none" '
            'stroke="#e4a137" stroke-width="3"/>'
        )
    colour = "#2979b4" if true_label == 1 else "#d4554c"
    parts.append(
        f'<circle cx="{x:.1f}" cy="{y}" r="8" fill="{colour}" '
        'stroke="#fff" stroke-width="2"/>'
    )

for count in range(10):
    x = email_x(count)
    parts.extend([
        f'<line x1="{x:.1f}" y1="269" x2="{x:.1f}" y2="281" '
        'stroke="#41566d" stroke-width="1.5"/>',
        svg_text(x, 303, str(count), 14, "#526273", 'text-anchor="middle"'),
    ])
parts.extend([
    '<line x1="170" y1="275" x2="920" y2="275" stroke="#41566d" '
    'stroke-width="2" marker-end="url(#arrow)"/>',
    svg_text(540, 321, "number of spam keywords", 14, "#344a61",
             'text-anchor="middle"'),
    '<rect x="25" y="345" width="950" height="270" rx="16" '
    'fill="#fff" stroke="#d9e3ec"/>',
    svg_text(48, 372, "Average logistic cost as the intercept changes", 17,
             extra='font-weight="700"'),
])

for tick in (0, 0.25, 0.5, 0.75, 1):
    y = cost_y(tick)
    if tick:
        parts.append(
            f'<line x1="160" y1="{y:.1f}" x2="910" y2="{y:.1f}" '
            'stroke="#e5ebf0" stroke-width="1"/>'
        )
    parts.extend([
        f'<line x1="154" y1="{y:.1f}" x2="166" y2="{y:.1f}" '
        'stroke="#41566d" stroke-width="1.5"/>',
        svg_text(143, y+5, f"{tick:g}", 14, "#526273", 'text-anchor="end"'),
    ])

for tick in range(-8, 0):
    x = cost_x(tick)
    parts.extend([
        f'<line x1="{x:.1f}" y1="549" x2="{x:.1f}" y2="561" '
        'stroke="#41566d" stroke-width="1.5"/>',
        svg_text(x, 581, str(tick).replace("-", "−"), 14,
                 "#526273", 'text-anchor="middle"'),
    ])

curve = []
for step in range(281):
    intercept = -8 + step * 0.025
    curve.append(f"{cost_x(intercept):.1f},{cost_y(cost(intercept)):.1f}")
parts.append(
    f'<polyline points="{" ".join(curve)}" fill="none" '
    'stroke="#344a61" stroke-width="3.5" stroke-linejoin="round"/>'
)

# The symmetric data place the optimum at -4.5 with the slope fixed to 1.
best_intercept = -4.5
best_x, best_y = cost_x(best_intercept), cost_y(cost(best_intercept))
parts.extend([
    f'<line x1="{best_x:.1f}" y1="{best_y:.1f}" '
    f'x2="{best_x:.1f}" y2="555" '
    'stroke="#2e9867" stroke-width="2" stroke-dasharray="6 5"/>',
    f'<circle cx="{best_x:.1f}" cy="{best_y:.1f}" r="8" '
    'fill="#2e9867" stroke="#fff" stroke-width="2"/>',
    svg_text(best_x, best_y-16, "minimum: θ₀ = −4.5, J ≈ 0.36", 15,
             "#227d56", 'font-weight="700" text-anchor="middle"'),
    '<line x1="160" y1="555" x2="920" y2="555" stroke="#41566d" '
    'stroke-width="2" marker-end="url(#arrow)"/>',
    '<line x1="160" y1="555" x2="160" y2="382" stroke="#41566d" '
    'stroke-width="2" marker-end="url(#arrow)"/>',
    svg_text(70, 474, "average cost J(θ₀)", 15, "#344a61",
             'text-anchor="middle" transform="rotate(-90 70 474)"'),
    svg_text(535, 606, "intercept θ₀", 16, "#344a61",
             'text-anchor="middle"'),
    '</svg>',
])

assert len(EMAILS) == 10
assert sum((count >= 5) != (true_label == 1) for count, true_label in EMAILS) == 2
assert cost(best_intercept) < cost(-5) and cost(best_intercept) < cost(-4)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"{OUTPUT}: J(-4.5) = {cost(best_intercept):.3f}")
