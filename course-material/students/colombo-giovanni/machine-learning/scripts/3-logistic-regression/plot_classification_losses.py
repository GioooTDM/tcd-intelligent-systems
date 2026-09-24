"""Draw the 0–1 loss curve, an email example, and the logistic loss curve."""

from math import exp, log1p
from pathlib import Path
from xml.sax.saxutils import escape


OUTPUT_DIR = Path(__file__).resolve().parents[2] / "images/3-logistic-regression"
WIDTH, HEIGHT = 900, 400
LEFT, RIGHT, TOP, BOTTOM = 104, 820, 92, 319


def x_pos(margin):
    return LEFT + (margin + 3) * (RIGHT - LEFT) / 6


def y_pos(loss, maximum):
    return BOTTOM - loss * (BOTTOM - TOP) / maximum


def label(x, y, value, size=16, colour="#26384b", extra=""):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" '
        'font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{colour}" {extra}>{escape(value)}</text>'
    )


def logistic_chart():
    title = "Logistic loss by true label"
    description = (
        "Two panels plot logistic loss against the score theta transpose x. "
        "For true label plus one, loss decreases as the score increases. "
        "For true label minus one, loss increases as the score increases. "
        "Both curves pass through log 2 at score zero."
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#f5f8fb"/>',
        label(34, 43, title, 25, extra='font-weight="700"'),
        label(34, 70, "The penalty is small when the score agrees with the true label.",
              16, "#526273"),
    ]

    def panel(panel_x, true_label):
        left, right, top, bottom = panel_x + 50, panel_x + 370, 142, 306

        def px(score):
            return left + (score + 3) * (right - left) / 6

        def py(loss):
            return bottom - loss * (bottom - top) / 3.4

        parts.extend([
            f'<rect x="{panel_x}" y="98" width="410" height="270" '
            'rx="16" fill="#fff" stroke="#d9e3ec"/>',
            label(panel_x + 205, 126, f"True label y = {true_label:+d}", 17,
                  "#26384b", 'font-weight="700" text-anchor="middle"'),
            f'<rect x="{left}" y="{top}" width="{px(0)-left:.1f}" '
            f'height="{bottom-top}" fill="{("#fff0ee" if true_label == 1 else "#eef6fc")}"/>',
            f'<rect x="{px(0):.1f}" y="{top}" width="{right-px(0):.1f}" '
            f'height="{bottom-top}" fill="{("#eef6fc" if true_label == 1 else "#fff0ee")}"/>',
            f'<line x1="{px(0):.1f}" y1="{top}" x2="{px(0):.1f}" '
            f'y2="{bottom}" stroke="#2e9867" stroke-width="2" '
            'stroke-dasharray="6 5"/>',
        ])

        for tick in range(4):
            y = py(tick)
            parts.extend([
                f'<line x1="{left-5}" y1="{y:.1f}" x2="{left+5}" y2="{y:.1f}" '
                'stroke="#41566d" stroke-width="1.5"/>',
                label(left-12, y+5, str(tick), 13, "#526273", 'text-anchor="end"'),
            ])
        for tick in range(-3, 4):
            x = px(tick)
            parts.extend([
                f'<line x1="{x:.1f}" y1="{bottom-5}" x2="{x:.1f}" '
                f'y2="{bottom+5}" stroke="#41566d" stroke-width="1.5"/>',
                label(x, bottom+22, str(tick).replace("-", "−"), 13,
                      "#526273", 'text-anchor="middle"'),
            ])

        points = []
        for step in range(121):
            score = -3 + step * 0.05
            points.append(
                f'{px(score):.1f},{py(log1p(exp(-true_label*score))):.1f}'
            )
        parts.extend([
            f'<polyline points="{" ".join(points)}" fill="none" '
            'stroke="#344a61" stroke-width="3" stroke-linejoin="round"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{right+7}" y2="{bottom}" '
            'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
            f'<line x1="{left}" y1="{bottom}" x2="{left}" y2="{top-7}" '
            'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
            label(panel_x+205, 356, "score θᵀx", 15, "#344a61",
                  'text-anchor="middle"'),
            label(panel_x+17, 222, "loss per example", 14, "#344a61",
                  f'text-anchor="middle" transform="rotate(-90 {panel_x+17} 222)"'),
        ])

    panel(30, +1)
    panel(460, -1)

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def logistic_email_example():
    """Show how one positive email's loss changes across model parameters."""
    left, right, top, bottom = 130, 780, 125, 365
    chart_height = 455

    def px(score):
        return left + (score + 2.5) * (right - left) / 4

    def py(loss):
        return bottom - loss * (bottom - top) / 2.7

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{chart_height}" '
        f'viewBox="0 0 {WIDTH} {chart_height}" role="img" aria-labelledby="title desc">',
        '<title id="title">One spam email: logistic loss falls as its score improves</title>',
        '<desc id="desc">An email with two spam keywords and true label plus one is '
        'evaluated with slope one and four intercepts. As the score changes from '
        'minus two to minus one, the prediction stays negative, but the logistic '
        'penalty falls from 2.13 to 1.31. At scores zero and plus one, the '
        'prediction is positive and the penalty falls further.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{chart_height}" rx="18" fill="#f5f8fb"/>',
        label(34, 43, "One spam email: loss falls as its score improves", 24,
              extra='font-weight="700"'),
        label(34, 70, "2 spam keywords · true label +1 · slope θ₁ = 1", 16,
              "#526273"),
        '<rect x="24" y="91" width="852" height="329" rx="16" '
        'fill="#fff" stroke="#d9e3ec"/>',
        f'<rect x="{left}" y="{top}" width="{px(0)-left:.1f}" '
        f'height="{bottom-top}" fill="#fff0ee"/>',
        f'<rect x="{px(0):.1f}" y="{top}" width="{right-px(0):.1f}" '
        f'height="{bottom-top}" fill="#eef6fc"/>',
        label(420, 190, "Predict normal (−1)", 15, "#a33f38",
              'font-weight="700" text-anchor="middle"'),
        label((px(0)+right)/2, 160, "Predict spam (+1)", 15, "#21648f",
              'font-weight="700" text-anchor="middle"'),
        f'<line x1="{px(0):.1f}" y1="{top}" x2="{px(0):.1f}" '
        f'y2="{bottom}" stroke="#2e9867" stroke-width="2.5" '
        'stroke-dasharray="7 6"/>',
    ]

    for tick in (0, 1, 2):
        y = py(tick)
        parts.extend([
            f'<line x1="{left-6}" y1="{y:.1f}" x2="{left+6}" y2="{y:.1f}" '
            'stroke="#41566d" stroke-width="1.5"/>',
            label(left-18, y+5, str(tick), 14, "#526273", 'text-anchor="end"'),
        ])
    for score in (-2, -1, 0, 1):
        x = px(score)
        parts.extend([
            f'<line x1="{x:.1f}" y1="{bottom-6}" x2="{x:.1f}" '
            f'y2="{bottom+6}" stroke="#41566d" stroke-width="1.5"/>',
            label(x, bottom+25, str(score).replace("-", "−"), 14,
                  "#526273", 'text-anchor="middle"'),
        ])

    curve = []
    for step in range(161):
        score = -2.5 + step * 0.025
        curve.append(f'{px(score):.1f},{py(log1p(exp(-score))):.1f}')
    parts.append(
        f'<polyline points="{" ".join(curve)}" fill="none" '
        'stroke="#344a61" stroke-width="3" stroke-linejoin="round"/>'
    )

    for intercept in (-4, -3, -2, -1):
        score = intercept + 2
        loss = log1p(exp(-score))
        x, y = px(score), py(loss)
        colour = "#d4554c" if score < 0 else "#2979b4"
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{colour}" '
            'stroke="#fff" stroke-width="2"/>'
        )
        parts.append(
            label(x+12, y-20,
                  f'θ₀={str(intercept).replace("-", "−")} · loss {loss:.2f}',
                  14, "#344a61")
        )

    parts.extend([
        f'<line x1="{left}" y1="{bottom}" x2="{right+10}" y2="{bottom}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{left}" y2="{top-8}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        label(53, 245, "penalty for this email", 15, "#344a61",
              'text-anchor="middle" transform="rotate(-90 53 245)"'),
        label((left+right)/2, 448, "score θᵀx", 16, "#344a61",
              'text-anchor="middle"'),
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


def zero_one_loss_chart():
    maximum = 1.4
    title = "0–1 loss: count the mistakes"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        '<desc id="desc">The loss is one when true label times score is negative '
        'and zero when that product is positive. It is flat on either side of zero and '
        'jumps at the decision boundary; the value at zero depends on the '
        'classifier tie rule.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#f5f8fb"/>',
        label(34, 43, title, 25, extra='font-weight="700"'),
        label(34, 70, "True label × score (y · z): negative means wrong, positive means correct",
              16, "#526273"),
        f'<rect x="{LEFT}" y="{TOP}" width="{x_pos(0) - LEFT:.1f}" '
        f'height="{BOTTOM - TOP}" fill="#fff0ee"/>',
        f'<rect x="{x_pos(0):.1f}" y="{TOP}" '
        f'width="{RIGHT - x_pos(0):.1f}" height="{BOTTOM - TOP}" fill="#eef6fc"/>',
        label((LEFT + x_pos(0)) / 2, TOP + 24, "Wrong class", 16, "#a33f38",
              'font-weight="700" text-anchor="middle"'),
        label((x_pos(0) + RIGHT) / 2, TOP + 24, "Correct class", 16, "#21648f",
              'font-weight="700" text-anchor="middle"'),
        f'<line x1="{x_pos(0):.1f}" y1="{TOP}" x2="{x_pos(0):.1f}" '
        f'y2="{BOTTOM}" stroke="#2e9867" stroke-width="2.5" '
        'stroke-dasharray="7 6"/>',
    ]

    for tick in (0, 1):
        y = y_pos(tick, maximum)
        parts.extend([
            f'<line x1="{LEFT - 6}" y1="{y:.1f}" x2="{LEFT + 6}" y2="{y:.1f}" '
            'stroke="#41566d" stroke-width="1.5"/>',
            label(LEFT - 18, y + 5, str(tick), 14, "#526273", 'text-anchor="end"'),
        ])

    parts.extend([
        f'<line x1="{LEFT}" y1="{BOTTOM}" x2="{RIGHT + 10}" y2="{BOTTOM}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        f'<line x1="{LEFT}" y1="{BOTTOM}" x2="{LEFT}" y2="{TOP - 8}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>',
        label(35, 205, "loss per example", 16, "#344a61",
              'text-anchor="middle" transform="rotate(-90 35 205)"'),
        label((LEFT + RIGHT) / 2, 381, "true label × score (y · z)", 16,
              extra='text-anchor="middle"'),
    ])

    for tick in range(-3, 4):
        x = x_pos(tick)
        parts.extend([
            f'<line x1="{x:.1f}" y1="{BOTTOM - 6}" x2="{x:.1f}" '
            f'y2="{BOTTOM + 6}" stroke="#41566d" stroke-width="1.5"/>',
            label(x, BOTTOM + 25, str(tick).replace("-", "−"), 14,
                  "#526273", 'text-anchor="middle"'),
        ])

    high, low = y_pos(1, maximum), y_pos(0, maximum)
    parts.extend([
        f'<line x1="{LEFT}" y1="{high:.1f}" x2="{x_pos(0) - 6:.1f}" '
        f'y2="{high:.1f}" stroke="#344a61" stroke-width="4"/>',
        f'<line x1="{x_pos(0) + 6:.1f}" y1="{low:.1f}" x2="{RIGHT}" '
        f'y2="{low:.1f}" stroke="#344a61" stroke-width="4"/>',
        f'<circle cx="{x_pos(0):.1f}" cy="{high:.1f}" r="5" '
        'fill="#fff" stroke="#344a61" stroke-width="2.5"/>',
        f'<circle cx="{x_pos(0):.1f}" cy="{low:.1f}" r="5" '
        'fill="#fff" stroke="#344a61" stroke-width="2.5"/>',
        label(x_pos(-1.5), high - 14, "loss = 1", 16, "#344a61",
              'text-anchor="middle"'),
        label(x_pos(1.5), low - 14, "loss = 0", 16, "#344a61",
              'text-anchor="middle"'),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def zero_one_email_example():
    left, right, top, bottom = 140, 810, 110, 300
    spam_y, normal_y = 190, 260
    emails = [(0, -1), (1, -1), (2, -1), (2, +1), (4, +1), (5, +1)]

    def count_x(count):
        return left + 20 + (right - left - 40) * count / 6

    boundary = count_x(3)
    mistakes = sum((+1 if count >= 3 else -1) != actual for count, actual in emails)
    assert mistakes == 1

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">0–1 loss in a six-email spam filter example</title>',
        '<desc id="desc">Three normal emails contain zero, one, and two spam keywords. '
        'Three spam emails contain two, four, and five spam keywords. A threshold '
        'at three predicts normal to its left and spam to its right. The spam email '
        'with two keywords is misclassified, so the average 0–1 loss is one sixth.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" '
        'fill="#41566d"/></marker></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="#f5f8fb"/>',
        label(34, 43, "0–1 loss: one mistake in six emails", 25,
              extra='font-weight="700"'),
        label(34, 70, "Feature: number of spam keywords in an email", 16, "#526273"),
        f'<rect x="{left}" y="{top}" width="{boundary - left:.1f}" '
        f'height="{bottom - top}" fill="#fff0ee"/>',
        f'<rect x="{boundary:.1f}" y="{top}" '
        f'width="{right - boundary:.1f}" height="{bottom - top}" fill="#eef6fc"/>',
        label((left + boundary) / 2, 137, "Predict normal (−1)", 16,
              "#a33f38", 'font-weight="700" text-anchor="middle"'),
        label((boundary + right) / 2, 137, "Predict spam (+1)", 16,
              "#21648f", 'font-weight="700" text-anchor="middle"'),
        f'<line x1="{boundary:.1f}" y1="{top}" x2="{boundary:.1f}" '
        f'y2="{bottom}" stroke="#2e9867" stroke-width="2.5" '
        'stroke-dasharray="7 6"/>',
        label(30, 210, "actual class", 16, "#344a61",
              'text-anchor="middle" transform="rotate(-90 30 210)"'),
        label(left - 14, spam_y + 5, "Spam +1", 15, "#526273",
              'text-anchor="end"'),
        label(left - 14, normal_y + 5, "Normal −1", 15, "#526273",
              'text-anchor="end"'),
    ]

    for row_y in (spam_y, normal_y):
        parts.append(
            f'<line x1="{left}" y1="{row_y}" x2="{right}" y2="{row_y}" '
            'stroke="#d9e3ec" stroke-width="1.5"/>'
        )

    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{right + 10}" y2="{bottom}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>'
    )
    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{left}" y2="{top - 8}" '
        'stroke="#41566d" stroke-width="2" marker-end="url(#arrow)"/>'
    )
    for row_y in (spam_y, normal_y):
        parts.append(
            f'<line x1="{left - 6}" y1="{row_y}" x2="{left + 6}" '
            f'y2="{row_y}" stroke="#41566d" stroke-width="1.5"/>'
        )
    for count in range(7):
        x = count_x(count)
        parts.extend([
            f'<line x1="{x:.1f}" y1="{bottom - 6}" x2="{x:.1f}" '
            f'y2="{bottom + 6}" stroke="#41566d" stroke-width="1.5"/>',
            label(x, bottom + 25, str(count), 14, "#526273",
                  'text-anchor="middle"'),
        ])

    for count, actual in emails:
        x = count_x(count)
        y = spam_y if actual == +1 else normal_y
        if count == 2 and actual == +1:
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y}" r="15" fill="none" '
                'stroke="#e4a137" stroke-width="3"/>'
            )
        colour = "#2979b4" if actual == +1 else "#d4554c"
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y}" r="8" fill="{colour}" '
            'stroke="#fff" stroke-width="2"/>'
        )

    parts.extend([
        label(count_x(2), 166, "Missed spam", 15, "#9a6a1c",
              'font-weight="700" text-anchor="middle"'),
        label((left + right) / 2, 353, "number of spam keywords", 16,
              "#344a61", 'text-anchor="middle"'),
        label((left + right) / 2, 384,
              "5 correct + 1 wrong → 0–1 loss = 1/6 ≈ 0.17", 18,
              "#344a61", 'text-anchor="middle"'),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
for name, content in (
    ("zero-one-loss-label-times-score.svg", zero_one_loss_chart()),
    ("zero-one-email-example.svg", zero_one_email_example()),
    ("logistic-loss-by-score.svg", logistic_chart()),
    ("logistic-email-example.svg", logistic_email_example()),
):
    output = OUTPUT_DIR / name
    output.write_text(content, encoding="utf-8")
    print(output)
