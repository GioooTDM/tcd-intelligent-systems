"""Plot TV advertising budget against sales from Advertising.csv."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = MODULE_DIR / "data" / "advertising.csv"
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "advertising-tv-sales-scatter.svg"


with DATA_FILE.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

tv_budget = [float(row["TV"]) for row in rows]
sales = [float(row["sales"]) for row in rows]

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(tv_budget, sales, color="#2563eb", alpha=0.75, edgecolors="none")

ax.set(
    title="Sales vs TV advertising budget",
    xlabel="TV advertising budget (thousands of USD)",
    ylabel="Sales (thousands of units)",
    xlim=(0, 300),
    ylim=(0, 30),
)
ax.grid(color="#d9dee8", linewidth=0.8)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved {len(rows)} observations to {OUTPUT_FILE}")
