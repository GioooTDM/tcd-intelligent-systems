"""Illustrate gradient descent on convex and non-convex cost functions."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = MODULE_DIR / "images" / "gradient-descent-convex-nonconvex.svg"


def descent_path(start, derivative, learning_rate, steps):
    """Return successive parameter values produced by gradient descent."""
    path = [start]
    for _ in range(steps):
        path.append(path[-1] - learning_rate * derivative(path[-1]))
    return path


fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Convex example: every step moves towards the unique global minimum.
convex_x = [-5 + i * 10 / 500 for i in range(501)]
convex_cost = [x**2 for x in convex_x]
convex_path = descent_path(4.2, lambda x: 2 * x, learning_rate=0.2, steps=7)
convex_path_cost = [x**2 for x in convex_path]

axes[0].plot(convex_x, convex_cost, color="#2563eb", linewidth=2.5)
axes[0].scatter(convex_path, convex_path_cost, color="#f59e0b", s=42, zorder=3)
for start_x, start_y, end_x, end_y in zip(
    convex_path[:-1], convex_path_cost[:-1], convex_path[1:], convex_path_cost[1:]
):
    axes[0].annotate(
        "",
        xy=(end_x, end_y),
        xytext=(start_x, start_y),
        arrowprops={"arrowstyle": "->", "color": "#f59e0b", "linewidth": 1.7},
    )
axes[0].scatter([0], [0], color="#dc2626", s=60, zorder=4)
axes[0].text(0.2, 1.1, "Global minimum", color="#b91c1c")
axes[0].text(convex_path[0] - 0.25, convex_path_cost[0] + 1.5, "Start", ha="center")
axes[0].set(
    title="Convex cost: descent reaches the global minimum",
    xlabel=r"Parameter $\theta$",
    ylabel=r"Cost $J(\theta)$",
    xlim=(-5, 5),
    ylim=(0, 25),
)

# Non-convex example: the starting point can lead to a local minimum.
def nonconvex_cost(x):
    return 0.08 * x**4 - 0.8 * x**2 + 0.25 * x + 3


def nonconvex_derivative(x):
    return 0.32 * x**3 - 1.6 * x + 0.25


nonconvex_x = [-3 + i * 6 / 500 for i in range(501)]
nonconvex_y = [nonconvex_cost(x) for x in nonconvex_x]
nonconvex_path = descent_path(2.9, nonconvex_derivative, learning_rate=0.12, steps=8)
nonconvex_path_cost = [nonconvex_cost(x) for x in nonconvex_path]

global_minimum_x = min(nonconvex_x, key=nonconvex_cost)
local_minimum_x = min((x for x in nonconvex_x if x > 0), key=nonconvex_cost)

axes[1].plot(nonconvex_x, nonconvex_y, color="#2563eb", linewidth=2.5)
axes[1].scatter(nonconvex_path, nonconvex_path_cost, color="#f59e0b", s=42, zorder=3)
for start_x, start_y, end_x, end_y in zip(
    nonconvex_path[:-1], nonconvex_path_cost[:-1], nonconvex_path[1:], nonconvex_path_cost[1:]
):
    axes[1].annotate(
        "",
        xy=(end_x, end_y),
        xytext=(start_x, start_y),
        arrowprops={"arrowstyle": "->", "color": "#f59e0b", "linewidth": 1.7},
    )
axes[1].scatter(
    [global_minimum_x],
    [nonconvex_cost(global_minimum_x)],
    color="#dc2626",
    s=60,
    zorder=4,
)
axes[1].scatter(
    [local_minimum_x],
    [nonconvex_cost(local_minimum_x)],
    color="#7c3aed",
    s=60,
    zorder=4,
)
axes[1].text(
    global_minimum_x + 0.12,
    nonconvex_cost(global_minimum_x) + 0.12,
    "Global minimum",
    color="#b91c1c",
)
axes[1].text(
    local_minimum_x - 0.15,
    nonconvex_cost(local_minimum_x) - 0.32,
    "Local minimum",
    color="#6d28d9",
    ha="right",
)
axes[1].text(nonconvex_path[0] - 0.2, nonconvex_path_cost[0] + 0.25, "Start", ha="center")
axes[1].set(
    title="Non-convex cost: descent may stop locally",
    xlabel=r"Parameter $\theta$",
    ylabel=r"Cost $J(\theta)$",
    xlim=(-3, 3),
    ylim=(0, 4),
)

for ax in axes:
    ax.grid(color="#d9dee8", linewidth=0.8)
    ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved gradient-descent illustration to {OUTPUT_FILE}")
