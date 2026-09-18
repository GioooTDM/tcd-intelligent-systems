"""Illustrate prediction errors used by the least-squares cost function."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = MODULE_DIR / "data" / "Advertising.csv"
OUTPUT_FILE = MODULE_DIR / "images" / "least-squares-cost-idea.svg"


with DATA_FILE.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

x = [float(row["TV"]) for row in rows]
y = [float(row["sales"]) for row in rows]

x_mean = sum(x) / len(x)
y_mean = sum(y) / len(y)
theta_1 = sum((x_i - x_mean) * (y_i - y_mean) for x_i, y_i in zip(x, y)) / sum(
    (x_i - x_mean) ** 2 for x_i in x
)
theta_0 = y_mean - theta_1 * x_mean

x_line = [0, 300]
y_line = [theta_0 + theta_1 * x_i for x_i in x_line]

ordered_points = sorted(zip(x, y))
highlighted = ordered_points[12::25]
highlight_x = [point[0] for point in highlighted]
highlight_y = [point[1] for point in highlighted]
highlight_predictions = [theta_0 + theta_1 * x_i for x_i in highlight_x]

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, color="#93c5fd", s=18, edgecolors="none", label="Observed targets")
ax.plot(x_line, y_line, color="#dc2626", linewidth=2.2, label=r"Predictions $h_\theta(x)$")
ax.vlines(
    highlight_x,
    highlight_y,
    highlight_predictions,
    color="#f59e0b",
    linestyle="--",
    linewidth=1.8,
    label="Prediction errors",
)
ax.scatter(highlight_x, highlight_y, color="#2563eb", s=26, zorder=3)

ax.set(
    title="Least squares measures the gaps between predictions and observations",
    xlabel="TV budget (thousands of USD)",
    ylabel="Sales (thousands of units)",
    xlim=(0, 300),
    ylim=(0, 30),
)
ax.grid(color="#d9dee8", linewidth=0.8)
ax.set_axisbelow(True)
ax.legend(frameon=False)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved least-squares illustration to {OUTPUT_FILE}")
