"""Illustrate residuals and two common residual-plot patterns."""

import math
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = MODULE_DIR / "images" / "residual-diagnostics.svg"


fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Panel 1: a residual is the signed vertical gap from a prediction to an observation.
x_line = [0, 6]
y_line = [1, 10]
observed_x = 3
predicted_y = 1 + 1.5 * observed_x
observed_y = 7.5

axes[0].plot(x_line, y_line, color="#dc2626", linewidth=2.3, label="Model prediction")
axes[0].scatter([observed_x], [observed_y], color="#2563eb", s=55, zorder=3, label="Observed target")
axes[0].annotate(
    "",
    xy=(observed_x, observed_y),
    xytext=(observed_x, predicted_y),
    arrowprops={"arrowstyle": "<->", "color": "#f59e0b", "linewidth": 2},
)
axes[0].text(observed_x + 0.18, 6.45, r"residual $y-\hat{y}$", color="#b45309")
axes[0].set(
    title="Residual for one observation",
    xlabel=r"Input $x$",
    ylabel=r"Target $y$",
    xlim=(0, 6),
    ylim=(0, 10),
)
axes[0].legend(frameon=False, loc="upper left")

# Panels 2 and 3: residuals without and with a systematic pattern.
fitted = [0.3 * i for i in range(1, 31)]
random_generator = random.Random(7)
random_residuals = [random_generator.gauss(0, 1.2) for _ in fitted]
curved_residuals = [0.28 * (x - 4.7) ** 2 - 2.2 + 0.35 * math.sin(3 * x) for x in fitted]

for ax, residuals, title in (
    (axes[1], random_residuals, "No clear pattern\nLinear model may be suitable"),
    (axes[2], curved_residuals, "Curved pattern\nLinear model misses structure"),
):
    ax.axhline(0, color="#475569", linewidth=1.4)
    ax.scatter(fitted, residuals, color="#2563eb", s=28, edgecolors="none")
    ax.set(
        title=title,
        xlabel="Fitted value",
        ylabel="Residual",
        xlim=(0, 10),
        ylim=(-4, 5),
    )

for ax in axes:
    ax.grid(color="#d9dee8", linewidth=0.8)
    ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved residual diagnostics to {OUTPUT_FILE}")
