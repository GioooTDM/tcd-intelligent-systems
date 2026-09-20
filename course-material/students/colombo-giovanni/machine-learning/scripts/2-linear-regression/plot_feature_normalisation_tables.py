"""Create comparison tables for two feature-normalisation methods."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "feature-normalisation-example.svg"


people = [f"Person {i}" for i in range(1, 8)]
ages = np.array([20, 25, 30, 35, 40, 50, 60], dtype=float)
incomes = np.array([24, 30, 38, 48, 62, 82, 110], dtype=float)


def standardise(values):
    return (values - values.mean()) / values.std(ddof=0)


def min_max_scale(values):
    return (values - values.min()) / (values.max() - values.min())


standardised_ages = standardise(ages)
standardised_incomes = standardise(incomes)
scaled_ages = min_max_scale(ages)
scaled_incomes = min_max_scale(incomes)


def add_table(ax, title, rows, header_colour):
    ax.axis("off")
    ax.set_title(title, fontsize=13, pad=10)
    table = ax.table(
        cellText=rows,
        colLabels=["Person", "Age", "Income"],
        cellLoc="center",
        colLoc="center",
        colColours=[header_colour] * 3,
        bbox=[0, 0, 1, 0.9],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)

    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#f8fafc" if row % 2 else "white")


original_rows = [
    [person, f"{age:.0f}", f"{income:.0f}"]
    for person, age, income in zip(people, ages, incomes)
]
standardised_rows = [
    [person, f"{age:.2f}", f"{income:.2f}"]
    for person, age, income in zip(people, standardised_ages, standardised_incomes)
]
scaled_rows = [
    [person, f"{age:.2f}", f"{income:.2f}"]
    for person, age, income in zip(people, scaled_ages, scaled_incomes)
]

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
add_table(axes[0], "Original data\nIncome in thousands of euros", original_rows, "#475569")
add_table(axes[1], "Standardisation\n(z-scores)", standardised_rows, "#2563eb")
add_table(axes[2], "Min-max scaling\n(range [0, 1])", scaled_rows, "#16a34a")

fig.suptitle("Feature normalisation applied independently to age and income", fontsize=15)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved feature-normalisation tables to {OUTPUT_FILE}")
