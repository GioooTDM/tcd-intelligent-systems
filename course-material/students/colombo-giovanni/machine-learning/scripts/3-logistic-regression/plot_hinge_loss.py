"""Compare hinge and logistic loss against the score for both class labels."""

from math import exp, log, log1p
from pathlib import Path
from xml.sax.saxutils import escape


OUTPUT = Path(__file__).resolve().parents[2] / "images/3-logistic-regression/hinge-loss-by-score.svg"
WIDTH, HEIGHT = 900, 410


def text(x, y, value, size=16, colour="#26384b", extra=""):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{colour}" {extra}>{escape(value)}</text>'
    )


def panel(parts, x0, label):
    left, right, top, bottom = x0 + 54, x0 + 370, 132, 313

    def px(score):
        return left + (score + 3) * (right - left) / 6

    def py(loss):
        return bottom - loss * (bottom - top) / 5.2

    parts.append(
        f'<rect x="{x0}" y="88" width="410" height="292" rx="16" '
        'fill="#fff" stroke="#d9e3ec"/>'
    )
    parts.append(
        text(x0 + 205, 119, f"True label y = {label:+d}", 18,
             extra='font-weight="700" text-anchor="middle"')
    )
    parts.append(
        f'<rect x="{left}" y="{top}" width="{px(0)-left:.1f}" height="{bottom-top}" '
        f'fill="{"#fff0ee" if label == 1 else "#eef6fc"}"/>'
    )
    parts.append(
        f'<rect x="{px(0):.1f}" y="{top}" width="{right-px(0):.1f}" height="{bottom-top}" '
        f'fill="{"#eef6fc" if label == 1 else "#fff0ee"}"/>'
    )
    parts.append(
        f'<line x1="{px(0):.1f}" y1="{top}" x2="{px(0):.1f}" y2="{bottom}" '
        'stroke="#2e9867" stroke-width="2" stroke-dasharray="6 5"/>'
    )

    for tick in range(6):
        y = py(tick)
        parts.append(
            f'<line x1="{left-5}" y1="{y:.1f}" x2="{left+5}" y2="{y:.1f}" '
            'stroke="#41566d" stroke-width="1.5"/>'
        )
        parts.append(text(left - 12, y + 5, str(tick), 13, "#526273", 'text-anchor="end"'))
    for tick in range(-3, 4):
        x = px(tick)
        parts.append(
            f'<line x1="{x:.1f}" y1="{bottom-5}" x2="{x:.1f}" y2="{bottom+5}" '
            'stroke="#41566d" stroke-width="1.5"/>'
        )
        parts.append(
            text(x, bottom + 22, str(tick).replace("-", "−"), 13,
                 "#526273", 'text-anchor="middle"')
        )

    logistic_points = []
    for step in range(121):
        score = -3 + step * 0.05
        logistic_points.append((px(score), py(log1p(exp(-label * score)) / log(2))))
    parts.append(
        '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in logistic_points)
        + '" fill="none" stroke="#c46a28" stroke-width="3" '
        'stroke-linejoin="round" stroke-linecap="round"/>'
    )

    corner = 1 if label == 1 else -1
    points = (
        [(px(-3), py(4)), (px(1), py(0)), (px(3), py(0))]
        if label == 1 else
        [(px(-3), py(0)), (px(-1), py(0)), (px(3), py(4))]
    )
    parts.append(
        '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        + '" fill="none" stroke="#344a61" stroke-width="3.5" '
        'stroke-linejoin="round" stroke-linecap="round"/>'
    )
    parts.append(
        f'<circle cx="{px(corner):.1f}" cy="{py(0):.1f}" r="5.5" '
        'fill="#344a61" stroke="#fff" stroke-width="2"/>'
    )
    parts.extend([
        f'<line x1="{left}" y1="{bottom}" x2="{right+7}" y2="{bottom}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{left}" y2="{top-7}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        text(x0 + 205, 364, "score θᵀx", 15, "#344a61", 'text-anchor="middle"'),
        text(x0 + 19, 224, "loss per example", 14, "#344a61",
             f'text-anchor="middle" transform="rotate(-90 {x0+19} 224)"'),
    ])


def main():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Hinge and logistic loss by true label</title>',
        '<desc id="desc">Two graphs compare dark hinge loss with orange logistic loss '
        'against score theta transpose x. Logistic loss is divided by log 2 to match '
        'the lecture slides. For true label plus one, hinge loss falls '
        'to zero at score plus one; for true label minus one, it is zero up to score '
        'minus one. Logistic loss decreases smoothly towards zero but does not reach '
        'it. The green dashed line marks score zero.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#f5f8fb"/>',
        text(34, 45, "Hinge and logistic loss", 25, extra='font-weight="700"'),
        text(34, 70, "Same score and true label; different penalties.", 16, "#526273"),
        '<line x1="664" y1="34" x2="692" y2="34" stroke="#344a61" '
        'stroke-width="3.5"/>',
        text(700, 39, "Hinge", 15, "#344a61"),
        '<line x1="664" y1="59" x2="692" y2="59" stroke="#c46a28" '
        'stroke-width="3"/>',
        text(700, 64, "Logistic", 15, "#344a61"),
    ]
    panel(parts, 30, 1)
    panel(parts, 460, -1)
    parts.append("</svg>")
    OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
