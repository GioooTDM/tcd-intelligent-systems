"""Compare linear and quadratic fits for TV and radio advertising data."""

import csv
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = MODULE_DIR / "data" / "advertising.csv"
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "advertising-linear-quadratic-surfaces.svg"


with DATA_FILE.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

tv = np.array([float(row["TV"]) for row in rows])
radio = np.array([float(row["radio"]) for row in rows])
sales = np.array([float(row["sales"]) for row in rows])

# Linear model: intercept, TV, and radio.
linear_features = np.column_stack((np.ones_like(tv), tv, radio))
linear_coefficients = np.linalg.lstsq(linear_features, sales, rcond=None)[0]

# Quadratic model: add squared terms and the TV-radio interaction.
quadratic_features = np.column_stack(
    (np.ones_like(tv), tv, radio, tv**2, radio**2, tv * radio)
)
quadratic_coefficients = np.linalg.lstsq(quadratic_features, sales, rcond=None)[0]

tv_values = np.linspace(0, 300, 45)
radio_values = np.linspace(0, 50, 35)
tv_grid, radio_grid = np.meshgrid(tv_values, radio_values)

linear_surface = (
    linear_coefficients[0]
    + linear_coefficients[1] * tv_grid
    + linear_coefficients[2] * radio_grid
)
quadratic_surface = (
    quadratic_coefficients[0]
    + quadratic_coefficients[1] * tv_grid
    + quadratic_coefficients[2] * radio_grid
    + quadratic_coefficients[3] * tv_grid**2
    + quadratic_coefficients[4] * radio_grid**2
    + quadratic_coefficients[5] * tv_grid * radio_grid
)

fig = plt.figure(figsize=(12, 5.2))

plots = (
    ("Linear model: fitted plane", linear_surface, "#60a5fa"),
    ("Quadratic model: curved surface", quadratic_surface, "#34d399"),
)

for position, (title, surface, colour) in enumerate(plots, start=1):
    ax = fig.add_subplot(1, 2, position, projection="3d")
    ax.plot_surface(
        tv_grid,
        radio_grid,
        surface,
        color=colour,
        alpha=0.48,
        edgecolor="#94a3b8",
        linewidth=0.25,
        rstride=3,
        cstride=3,
    )
    ax.scatter(tv, radio, sales, color="#1d4ed8", s=13, alpha=0.8, depthshade=False)
    ax.set(
        title=title,
        xlabel="TV budget",
        ylabel="Radio budget",
        zlabel="Sales",
        xlim=(0, 300),
        ylim=(0, 50),
        zlim=(0, 35),
    )
    ax.view_init(elev=25, azim=-60)
    ax.set_box_aspect((1.2, 1, 0.8))

fig.suptitle("Advertising data: two models fitted to the same observations", fontsize=15)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved advertising surfaces to {OUTPUT_FILE}")
