"""Show how scaling SVM parameters changes scores but not the boundary."""

from pathlib import Path
from xml.sax.saxutils import escape


OUTPUT = Path(__file__).resolve().parents[2] / "images/3-logistic-regression/svm-scaling-same-boundary.svg"
WIDTH, HEIGHT = 900, 425


def label(x, y, value, size=16, colour="#26384b", extra=""):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{colour}" {extra}>{escape(value)}</text>'
    )


def px(feature):
    return 130 + (feature - 2) * 235


def py(score):
    return 235 - score * 45


def main():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Scaling SVM parameters leaves the decision boundary unchanged</title>',
        '<desc id="desc">The score lines x minus three and two x minus six cross zero '
        'at the same feature value, three. For a positive example at feature value '
        '3.5, doubling the parameters raises the score from 0.5 to 1 and reduces '
        'hinge loss from 0.5 to zero without changing the predicted class.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#f5f8fb"/>',
        label(34, 45, "Same boundary, different scores", 25,
              extra='font-weight="700"'),
        label(34, 70, "Scaling the parameters changes the score but not the prediction.",
              16, "#526273"),
        '<rect x="24" y="89" width="852" height="307" rx="16" '
        'fill="#fff" stroke="#d9e3ec"/>',
        f'<rect x="{px(2):.1f}" y="135" width="{px(3)-px(2):.1f}" '
        'height="200" fill="#fff0ee"/>',
        f'<rect x="{px(3):.1f}" y="135" width="{px(4)-px(3):.1f}" '
        'height="200" fill="#eef6fc"/>',
        f'<line x1="{px(3):.1f}" y1="135" x2="{px(3):.1f}" y2="335" '
        'stroke="#2e9867" stroke-width="2.5" stroke-dasharray="6 5"/>',
        label(px(3), 124, "boundary x₁ = 3", 15, "#23724d",
              'font-weight="700" text-anchor="middle"'),
    ]

    for score in (-2, -1, 0, 1, 2):
        y = py(score)
        parts.extend([
            f'<line x1="124" y1="{y:.1f}" x2="136" y2="{y:.1f}" '
            'stroke="#41566d" stroke-width="1.5"/>',
            label(116, y + 5, str(score).replace("-", "−"), 14, "#526273",
                  'text-anchor="end"'),
        ])
    for feature in (2, 3, 4):
        x = px(feature)
        parts.extend([
            f'<line x1="{x:.1f}" y1="230" x2="{x:.1f}" y2="241" '
            'stroke="#41566d" stroke-width="1.5"/>',
            label(x, 258, str(feature), 14, "#526273", 'text-anchor="middle"'),
        ])

    parts.extend([
        f'<line x1="{px(2):.1f}" y1="{py(-1):.1f}" '
        f'x2="{px(4):.1f}" y2="{py(1):.1f}" '
        'stroke="#344a61" stroke-width="3.5"/>',
        f'<line x1="{px(2):.1f}" y1="{py(-2):.1f}" '
        f'x2="{px(4):.1f}" y2="{py(2):.1f}" '
        'stroke="#c46a28" stroke-width="3.5"/>',
        f'<line x1="{px(3.5):.1f}" y1="{py(1):.1f}" '
        f'x2="{px(3.5):.1f}" y2="{py(0):.1f}" '
        'stroke="#8292a3" stroke-width="1.5" stroke-dasharray="5 5"/>',
        f'<circle cx="{px(3.5):.1f}" cy="{py(1):.1f}" r="6" '
        'fill="#c46a28" stroke="#fff" stroke-width="2"/>',
        f'<circle cx="{px(3.5):.1f}" cy="{py(0.5):.1f}" r="6" '
        'fill="#344a61" stroke="#fff" stroke-width="2"/>',
        f'<line x1="{px(2):.1f}" y1="{py(0):.1f}" '
        f'x2="{px(4)+9:.1f}" y2="{py(0):.1f}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        f'<line x1="{px(2):.1f}" y1="335" '
        f'x2="{px(2):.1f}" y2="128" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        label(365, 379, "feature x₁", 16, "#344a61", 'text-anchor="middle"'),
        label(49, 235, "score θᵀx", 16, "#344a61",
              'text-anchor="middle" transform="rotate(-90 49 235)"'),
        '<line x1="496" y1="190" x2="637" y2="168" '
        'stroke="#c46a28" stroke-width="1.5"/>',
        '<line x1="496" y1="212.5" x2="637" y2="255" '
        'stroke="#344a61" stroke-width="1.5"/>',
        '<rect x="640" y="137" width="213" height="64" rx="10" '
        'fill="#fff7f0" stroke="#e9c9ad"/>',
        label(654, 162, "2θ: score 1", 17, "#9d501e", 'font-weight="700"'),
        label(654, 187, "hinge loss 0", 16, "#9d501e"),
        '<rect x="640" y="229" width="213" height="64" rx="10" '
        'fill="#f2f6fa" stroke="#ccd9e4"/>',
        label(654, 254, "θ: score 0.5", 17, "#344a61", 'font-weight="700"'),
        label(654, 279, "hinge loss 0.5", 16, "#344a61"),
        label(747, 327, "Example: x₁ = 3.5, y = +1", 14, "#526273",
              'text-anchor="middle"'),
        '</svg>',
    ])
    OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
