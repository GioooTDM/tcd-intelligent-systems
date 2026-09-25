"""Redraw the lecture's two Covid charts from approximate visual readings."""

from html import escape
from math import log
from pathlib import Path


OUT = Path(__file__).resolve().parents[2] / "images/4-features-engineering/covid-cases-original-vs-log.svg"

# Approximate values read from the slide image, not its original dataset.
# Days 1–11 come from the log panel because the count panel has little
# vertical resolution near zero; days 12–40 come from the count panel.
COUNTS = (
    1, 2, 7, 14, 18, 20, 22, 26, 37, 47,
    73, 105, 158, 184, 237, 316, 395, 579, 711, 803,
    921, 1158, 1368, 1605, 1842, 2132, 2447, 2658, 2921, 3250,
    3487, 3895, 4316, 4632, 5026, 5395, 5737, 6092, 6605, 7013,
)
DATA = list(enumerate(COUNTS, start=1))

BLUE = "#2563eb"
ORANGE = "#d97706"
INK = "#172033"
MUTED = "#526174"
GRID = "#e8edf3"
BORDER = "#aab7c6"
FONT = "Arial, Helvetica, sans-serif"


def text(x, y, value, size=18, color=INK, anchor="start", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">{escape(value)}</text>'
    )


def panel(x0, y0, width, height, transformed):
    ymax = 15 if transformed else 8000
    yticks = (0, 5, 10, 15) if transformed else (0, 2000, 4000, 6000, 8000)

    def sx(day):
        return x0 + width * day / 40

    def sy(value):
        return y0 + height * (1 - value / ymax)

    items = []
    for day in (0, 10, 20, 30, 40):
        x = sx(day)
        items.append(f'<path d="M{x:.1f} {y0}V{y0+height}" stroke="{GRID}"/>')
        items.append(text(x, y0 + height + 27, str(day), 16, MUTED, "middle"))
    for tick in yticks:
        y = sy(tick)
        items.append(f'<path d="M{x0} {y:.1f}H{x0+width}" stroke="{GRID}"/>')
        items.append(text(x0 - 12, y + 5, f"{tick:,}", 16, MUTED, "end"))

    curve = " ".join(
        f'{"M" if i == 0 else "L"}{sx(day):.1f} {sy(log(count) if transformed else count):.1f}'
        for i, (day, count) in enumerate(DATA)
    )
    items.append(
        f'<path d="{curve}" fill="none" stroke="{BLUE}" stroke-width="3.5" '
        'stroke-linejoin="round" stroke-linecap="round"/>'
    )
    for day in (10, 20, 30, 40):
        count = COUNTS[day - 1]
        items.append(
            f'<circle cx="{sx(day):.1f}" cy="{sy(log(count) if transformed else count):.1f}" '
            f'r="4.7" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>'
        )

    if transformed:
        # The lecture's dashed line runs approximately from (0, 0) to (40, 14).
        items.append(
            f'<path d="M{sx(0):.1f} {sy(0):.1f}L{sx(40):.1f} {sy(14):.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="3.5" '
            'stroke-dasharray="11 9"/>'
        )

    items.append(
        f'<rect x="{x0}" y="{y0}" width="{width}" height="{height}" '
        f'fill="none" stroke="{BORDER}" stroke-width="1.5"/>'
    )
    items.append(text(x0 + width / 2, y0 + height + 63, "Day k", 20, INK, "middle"))
    ylabel = "ln(cases), yₖ" if transformed else "Cases (people), zₖ"
    items.append(
        f'<g transform="translate({x0-70} {y0+height/2}) rotate(-90)">'
        f'{text(0, 0, ylabel, 19, INK, "middle")}</g>'
    )
    return "".join(items)


WIDTH, HEIGHT = 1320, 650
content = "".join(
    [
        text(360, 75, "Original counts", 21, INK, "middle", "bold"),
        text(995, 75, "Natural log of counts", 21, INK, "middle", "bold"),
        panel(125, 106, 470, 390, False),
        panel(760, 106, 470, 390, True),
        f'<path d="M425 601h37" stroke="{BLUE}" stroke-width="3.5"/>',
        text(472, 608, "Approximate slide values", 17, MUTED),
        f'<path d="M720 601h37" stroke="{ORANGE}" stroke-width="3.5" stroke-dasharray="11 9"/>',
        text(767, 608, "Slide trend (approx.)", 17, MUTED),
    ]
)
OUT.write_text(
    "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
            '<title id="title">Ireland Covid case counts before and after log transformation</title>',
            '<desc id="desc">Two side-by-side plots redrawn from approximate lecture figure values. '
            'The left shows case counts; the right shows their natural logarithms and an approximate dashed exponential trend.</desc>',
            f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#fff"/>',
            content,
            "</svg>\n",
        ]
    ),
    encoding="utf-8",
)
