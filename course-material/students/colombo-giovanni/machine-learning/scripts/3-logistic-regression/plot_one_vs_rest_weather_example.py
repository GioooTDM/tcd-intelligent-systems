"""Draw a four-class one-vs-rest weather example for training and prediction."""

from html import escape
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parents[2] / "images/3-logistic-regression"
FONT = "Arial, Helvetica, sans-serif"
CLASSES = ("Sunny", "Cloudy", "Rain", "Snow")


def svg_text(x, y, value, size=16, colour="#26384b", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" '
        f'font-size="{size}" fill="{colour}" {extra}>{escape(value)}</text>'
    )


def training_diagram():
    width, height = 1000, 510
    columns = (80, 280, 440, 600, 760, 920)
    centres = (360, 520, 680, 840)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">One-vs-rest training labels for four weather classes</title>',
        '<desc id="desc">Four weather classes have original labels zero '
        'through three. In each one-vs-rest binary training column, the '
        'named class becomes plus one and all other classes become minus one.</desc>',
        f'<rect width="{width}" height="{height}" rx="18" fill="#f5f8fb"/>',
        svg_text(40, 46, "One-vs-rest: relabel weather classes", 26,
                 extra='font-weight="700"'),
        svg_text(40, 77, "Original classes use 0–3; each binary classifier uses +1 for its class and −1 for the rest.",
                 17, "#526273"),
        '<rect x="80" y="120" width="840" height="326" rx="14" '
        'fill="#fff" stroke="#d9e3ec"/>',
        '<path d="M80 134 Q80 120 94 120 H906 Q920 120 920 134 V174 H80 Z" '
        'fill="#e9f0f6"/>',
        svg_text(180, 153, "Original y", 15, "#344a61",
                 'font-weight="700" text-anchor="middle"'),
    ]

    for centre, category in zip(centres, CLASSES):
        parts.append(svg_text(centre, 153, f"{category} vs rest", 15,
                              "#344a61", 'font-weight="700" text-anchor="middle"'))
    for x in columns[1:-1]:
        parts.append(
            f'<line x1="{x}" y1="120" x2="{x}" y2="446" '
            'stroke="#d9e3ec"/>'
        )
    for y in (174, 242, 310, 378):
        parts.append(
            f'<line x1="80" y1="{y}" x2="920" y2="{y}" '
            'stroke="#d9e3ec"/>'
        )

    for index, original in enumerate(CLASSES):
        top = 174 + index * 68
        baseline = top + 42
        parts.append(svg_text(180, baseline, f"{original} ({index})", 16,
                              "#344a61", 'font-weight="700" text-anchor="middle"'))
        for centre, category in zip(centres, CLASSES):
            positive = category == original
            fill = "#e4f4eb" if positive else "#f1f4f7"
            ink = "#227d56" if positive else "#6b7886"
            parts.extend([
                f'<rect x="{centre-33}" y="{top+17}" width="66" '
                f'height="36" rx="9" fill="{fill}"/>',
                svg_text(centre, baseline, "+1" if positive else "−1", 17,
                         ink, 'font-weight="700" text-anchor="middle"'),
            ])

    parts.extend([
        svg_text(500, 484, "Train one binary classifier from each relabelled column.",
                 16, "#344a61", 'text-anchor="middle"'),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


def prediction_diagram():
    width, height = 1100, 490
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">One-vs-rest prediction for a new weather observation</title>',
        '<desc id="desc">A new cool, overcast day is evaluated by four '
        'binary classifiers. Sunny scores minus one point two, Cloudy '
        'plus one point three, Rain minus zero point four, and Snow '
        'minus one point five. Cloudy has the highest score and is selected.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
        'refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{width}" height="{height}" rx="18" fill="#f5f8fb"/>',
        svg_text(40, 46, "One-vs-rest: classify a new day", 26,
                 extra='font-weight="700"'),
        svg_text(40, 77, "Illustrative scores from four trained classifiers; scores are not probabilities.",
                 17, "#526273"),
        '<rect x="35" y="196" width="278" height="106" rx="15" '
        'fill="#fff" stroke="#d9e3ec"/>',
        svg_text(58, 228, "New observation", 17, "#526273"),
        svg_text(58, 264, "Cool, overcast", 21, "#26384b",
                 'font-weight="700"'),
        '<path d="M313 249 H355 M355 138 V378" fill="none" '
        'stroke="#9fb0bf" stroke-width="2"/>',
    ]

    classifiers = (
        (108, "Sunny vs rest", "−1.2", "−1", False),
        (188, "Cloudy vs rest", "+1.3", "+1", True),
        (268, "Rain vs rest", "−0.4", "−1", False),
        (348, "Snow vs rest", "−1.5", "−1", False),
    )
    for top, name, score, prediction, selected in classifiers:
        centre_y = top + 30
        fill = "#eaf7ef" if selected else "#fff"
        border = "#2e9867" if selected else "#d9e3ec"
        parts.extend([
            f'<line x1="355" y1="{centre_y}" x2="390" y2="{centre_y}" '
            'stroke="#9fb0bf" stroke-width="2" marker-end="url(#arrow)"/>',
            f'<rect x="390" y="{top}" width="315" height="60" rx="12" '
            f'fill="{fill}" stroke="{border}"/>',
            svg_text(410, top+25, name, 17, "#26384b",
                     'font-weight="700"'),
            svg_text(410, top+47, f"score {score}  →  sign {prediction}", 16,
                     "#526273"),
            f'<line x1="705" y1="{centre_y}" x2="750" y2="{centre_y}" '
            'stroke="#9fb0bf" stroke-width="2"/>',
        ])

    parts.extend([
        '<line x1="750" y1="138" x2="750" y2="378" '
        'stroke="#9fb0bf" stroke-width="2"/>',
        '<line x1="750" y1="249" x2="790" y2="249" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        svg_text(929, 190, "Highest score", 16, "#526273",
                 'text-anchor="middle"'),
        '<rect x="790" y="207" width="278" height="86" rx="14" '
        'fill="#eaf7ef" stroke="#2e9867"/>',
        svg_text(929, 239, "Selected class", 17, "#526273",
                 'text-anchor="middle"'),
        svg_text(929, 271, "Cloudy", 22, "#227d56",
                 'font-weight="700" text-anchor="middle"'),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
for name, content in (
    ("one-vs-rest-weather-training.svg", training_diagram()),
    ("one-vs-rest-weather-prediction.svg", prediction_diagram()),
):
    output = OUTPUT_DIR / name
    output.write_text(content, encoding="utf-8")
    print(output)
