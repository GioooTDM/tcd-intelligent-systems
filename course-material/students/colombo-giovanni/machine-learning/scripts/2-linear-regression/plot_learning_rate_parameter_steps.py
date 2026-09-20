"""Show how the learning rate changes gradient-descent steps in parameter space."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "learning-rate-parameter-steps.svg"


def gradient_descent_path(start, learning_rate, steps):
    """Run gradient descent on J(theta) = theta squared."""
    path = [start]
    for _ in range(steps):
        derivative = 2 * path[-1]
        path.append(path[-1] - learning_rate * derivative)
    return np.array(path)


theta = np.linspace(-5.5, 5.5, 500)
settings = [
    (0.05, 6, "Small learning rate\nStable but slow", "#2563eb"),
    (0.70, 6, "Suitable learning rate\nOscillates and converges", "#16a34a"),
    (1.10, 5, "Learning rate too large\nOscillations grow", "#dc2626"),
]

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharex=True, sharey=True)

for ax, (learning_rate, steps, title, colour) in zip(axes, settings):
    path = gradient_descent_path(2.0, learning_rate, steps)
    path_cost = path**2

    ax.plot(theta, theta**2, color="#64748b", linewidth=2.2)
    ax.scatter(path, path_cost, color=colour, s=42, zorder=3)
    for start_x, start_y, end_x, end_y in zip(
        path[:-1], path_cost[:-1], path[1:], path_cost[1:]
    ):
        ax.annotate(
            "",
            xy=(end_x, end_y),
            xytext=(start_x, start_y),
            arrowprops={"arrowstyle": "->", "color": colour, "linewidth": 1.8},
        )

    ax.scatter([0], [0], color="#111827", s=48, zorder=4)
    ax.set(
        title=title + rf"  ($\alpha={learning_rate:.2f}$)",
        xlabel=r"Parameter $\theta$",
        xlim=(-5.5, 5.5),
        ylim=(0, 31),
    )
    ax.grid(color="#d9dee8", linewidth=0.8)
    ax.set_axisbelow(True)

axes[0].set_ylabel(r"Cost $J(\theta)$")
fig.suptitle(r"Gradient-descent steps on $J(\theta)=\theta^2$", fontsize=15)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved learning-rate step comparison to {OUTPUT_FILE}")
