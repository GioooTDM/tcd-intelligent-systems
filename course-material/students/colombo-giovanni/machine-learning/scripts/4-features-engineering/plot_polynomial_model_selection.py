"""Redraw the polynomial model-selection plots as clean SVG figures."""

from html import escape
from pathlib import Path
import random


OUT = Path(__file__).resolve().parents[2] / "images/4-features-engineering"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#172033"
MUTED = "#526174"
GRID = "#e8edf3"
BORDER = "#aab7c6"
DATA_COLOR = "#2563eb"
MODEL_COLORS = {1: "#d97706", 2: "#9333ea", 6: "#0891b2", 10: "#65a30d"}
FONT = "Arial, Helvetica, sans-serif"

# Reproducible illustrative sales data. The lecture's original dataset is not
# available here, so these points recreate the visual lesson, not its values.
rng = random.Random(61)
DATA = []
for i in range(201):
    x = 300 * i / 200
    underlying_sales = 6 + 0.065 * x - 0.00005 * x * x
    noise_sd = 3.0 + 0.015 * x
    DATA.append((x, underlying_sales + rng.gauss(0, noise_sd)))
SPARSE = DATA[::10]


def legendre_values(t, degree):
    values = [1.0]
    if degree == 0:
        return values
    values.append(t)
    for n in range(2, degree + 1):
        values.append(((2 * n - 1) * t * values[-1] - (n - 1) * values[-2]) / n)
    return values


def solve(matrix, vector):
    """Solve a small dense linear system with Gaussian elimination and pivoting."""
    a = [row[:] + [value] for row, value in zip(matrix, vector)]
    n = len(vector)
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= divisor
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            for j in range(col, n + 1):
                a[row][j] -= factor * a[col][j]
    return [a[row][n] for row in range(n)]


def fit_polynomial(points, degree):
    # Fit in Legendre basis over x ∈ [0, 300], equivalent to a degree-d
    # polynomial in x but numerically more stable than raw powers of x.
    rows = [legendre_values((x - 150) / 150, degree) for x, _ in points]
    gram = [[sum(row[i] * row[j] for row in rows) for j in range(degree + 1)] for i in range(degree + 1)]
    target = [sum(row[i] * y for row, (_, y) in zip(rows, points)) for i in range(degree + 1)]
    return solve(gram, target)


def predict(coefficients, x):
    basis = legendre_values((x - 150) / 150, len(coefficients) - 1)
    return sum(c * b for c, b in zip(coefficients, basis))


def text(x, y, value, size=17, color=INK, anchor="start", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">{escape(value)}</text>'
    )


def panel(x0, y0, width, height, x_domain, y_domain, points, degrees, clip_id, observed_range=None):
    x_min, x_max = x_domain
    y_min, y_max = y_domain

    def sx(x):
        return x0 + width * (x - x_min) / (x_max - x_min)

    def sy(y):
        return y0 + height * (y_max - y) / (y_max - y_min)

    parts = [f'<rect x="{x0}" y="{y0}" width="{width}" height="{height}" fill="#fff"/>']
    if observed_range:
        lo = max(x_min, observed_range[0])
        hi = min(x_max, observed_range[1])
        if hi > lo:
            parts.append(
                f'<rect x="{sx(lo):.1f}" y="{y0}" width="{sx(hi)-sx(lo):.1f}" '
                f'height="{height}" fill="#f3f7fc"/>'
            )

    x_ticks = [tick for tick in (-100, 0, 50, 100, 150, 200, 250, 300, 400, 500) if x_min <= tick <= x_max]
    y_step = 10 if y_max - y_min >= 60 else 5
    y_ticks = list(range(int(y_min), int(y_max) + 1, y_step))
    for tick in x_ticks:
        x = sx(tick)
        parts.append(f'<path d="M{x:.1f} {y0}V{y0+height}" stroke="{GRID}"/>')
        parts.append(text(x, y0 + height + 24, str(tick), 15, MUTED, "middle"))
    for tick in y_ticks:
        y = sy(tick)
        parts.append(f'<path d="M{x0} {y:.1f}H{x0+width}" stroke="{GRID}"/>')
        parts.append(text(x0 - 10, y + 5, str(tick), 15, MUTED, "end"))

    parts.append(f'<defs><clipPath id="{clip_id}"><rect x="{x0}" y="{y0}" width="{width}" height="{height}"/></clipPath></defs>')
    for degree in degrees:
        coefficients = fit_polynomial(points, degree)
        segments = []
        current = []
        for i in range(601):
            x = x_min + (x_max - x_min) * i / 600
            y = predict(coefficients, x)
            if y_min <= y <= y_max:
                current.append((sx(x), sy(y)))
            else:
                if len(current) > 1:
                    segments.append(current)
                current = []
        if len(current) > 1:
            segments.append(current)
        paths = []
        for segment in segments:
            paths.append(" ".join(f'{"M" if i == 0 else "L"}{x:.2f} {y:.2f}' for i, (x, y) in enumerate(segment)))
        d = " ".join(paths)
        parts.append(
            f'<path d="{d}" fill="none" stroke="{MODEL_COLORS[degree]}" '
            f'stroke-width="3" stroke-linecap="round" clip-path="url(#{clip_id})"/>'
        )

    for x, y in points:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            parts.append(
                f'<circle cx="{sx(x):.2f}" cy="{sy(y):.2f}" r="2.8" '
                f'fill="{DATA_COLOR}" fill-opacity="0.62"/>'
            )

    parts.extend(
        [
            f'<rect x="{x0}" y="{y0}" width="{width}" height="{height}" fill="none" stroke="{BORDER}" stroke-width="1.4"/>',
            text(x0 + width / 2, y0 + height + 55, "TV advertising", 18, INK, "middle"),
            f'<g transform="translate({x0-55} {y0+height/2}) rotate(-90)">{text(0, 0, "Sales", 18, INK, "middle")}</g>',
        ]
    )
    return "".join(parts)


def legend(x, y, degrees):
    names = {1: "Linear", 2: "Quadratic", 6: "6th degree", 10: "10th degree"}
    entries = [(names[degree], MODEL_COLORS[degree]) for degree in degrees]
    box_height = 14 + 22 * len(entries)
    parts = [
        f'<rect x="{x}" y="{y}" width="166" height="{box_height}" rx="5" '
        f'fill="#fff" fill-opacity="0.96" stroke="{BORDER}" stroke-width="1"/>'
    ]
    for i, (name, color) in enumerate(entries):
        yy = y + 25 + i * 22
        parts.append(f'<path d="M{x+7} {yy-5}h18" stroke="{color}" stroke-width="3"/>')
        parts.append(text(x + 32, yy, name, 14, MUTED))
    return "".join(parts)


def document(name, description, content, height=655):
    (OUT / name).write_text(
        "\n".join(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="{height}" viewBox="0 0 1480 {height}" role="img" aria-labelledby="title desc">',
                f'<title id="title">{escape(description)}</title>',
                f'<desc id="desc">{escape(description)} Data are illustrative and do not reproduce the original advertising dataset.</desc>',
                f'<rect width="1480" height="{height}" fill="#fff"/>',
                content,
                "</svg>\n",
            ]
        ),
        encoding="utf-8",
    )


DEGREES = (1, 2, 6, 10)
plot_y, plot_h, plot_w = 70, 490, 535
left_plot_x, right_plot_x = 145, 890

sparse = "".join(
    [
        panel(left_plot_x, plot_y, plot_w, plot_h, (0, 300), (-20, 50), SPARSE, (1,), "sparse-linear"),
        panel(right_plot_x, plot_y, plot_w, plot_h, (0, 300), (-20, 50), SPARSE, DEGREES, "sparse-polynomial"),
        legend(right_plot_x + 14, plot_y + 14, DEGREES),
    ]
)
document(
    "polynomial-fits-sparse-data.svg",
    "Polynomial models fitted to sparse advertising data",
    sparse,
)

more = "".join(
    [
        panel(left_plot_x, plot_y, plot_w, plot_h, (0, 300), (0, 30), DATA, DEGREES, "more-data-fit"),
        panel(right_plot_x, plot_y, plot_w, plot_h, (-100, 500), (-20, 50), DATA, DEGREES, "extrapolation-fit", (0, 300)),
        legend(left_plot_x + 14, plot_y + 14, DEGREES),
    ]
)
document(
    "polynomial-fits-more-data.svg",
    "Polynomial fits with more training data and extrapolation",
    more,
)
