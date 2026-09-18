"""Compare simple linear models with different parameter values."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = MODULE_DIR / "data" / "Advertising.csv"
OUTPUT_FILE = MODULE_DIR / "images" / "linear-model-parameter-examples.svg"


with DATA_FILE.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

tv_budget = [float(row["TV"]) for row in rows]
sales = [float(row["sales"]) for row in rows]
x_line = [0, 300]
models = [(15, 0), (0, 0.1), (5, 0.1)]

fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharex=True, sharey=True)

for ax, (theta_0, theta_1) in zip(axes, models):
    predictions = [theta_0 + theta_1 * x for x in x_line]
    ax.scatter(tv_budget, sales, color="#2563eb", alpha=0.65, s=12, edgecolors="none")
    ax.plot(x_line, predictions, color="#dc2626", linewidth=2)
    ax.set(
        title=rf"$\theta_0={theta_0},\ \theta_1={theta_1}$",
        xlabel="TV budget (thousands of USD)",
        xlim=(0, 300),
        ylim=(0, 30),
    )
    ax.grid(color="#d9dee8", linewidth=0.8)
    ax.set_axisbelow(True)

axes[0].set_ylabel("Sales (thousands of units)")
fig.suptitle("How the parameters change the regression line", fontsize=15)
fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved parameter comparison to {OUTPUT_FILE}")
