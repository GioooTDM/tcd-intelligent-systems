"""Illustrate stopping criteria and learning-rate behaviour."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "gradient-descent-training-diagnostics.svg"


iterations = np.arange(0, 251)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Stopping criterion: stop once consecutive improvements become negligible.
cost = 0.8 + 9 * np.exp(-iterations / 55)
improvements = np.abs(np.diff(cost))
threshold = 0.01
stopping_iteration = int(np.flatnonzero(improvements < threshold)[0] + 1)

axes[0].plot(iterations, cost, color="#2563eb", linewidth=2.5)
axes[0].scatter(
    [stopping_iteration],
    [cost[stopping_iteration]],
    color="#dc2626",
    s=55,
    zorder=3,
)
axes[0].annotate(
    r"Stop: $|J_t-J_{t-1}|<\varepsilon$",
    xy=(stopping_iteration, cost[stopping_iteration]),
    xytext=(stopping_iteration - 75, cost[stopping_iteration] + 2.2),
    arrowprops={"arrowstyle": "->", "color": "#dc2626"},
    color="#b91c1c",
)
axes[0].set(
    title="Stopping criterion",
    xlabel="Iteration",
    ylabel=r"Cost $J(\theta)$",
    xlim=(0, 250),
    ylim=(0, 11),
)

# Learning-rate comparison using actual updates on J(theta) = 0.5 * theta squared.
def quadratic_cost_path(learning_rate):
    theta = np.sqrt(20.0)  # The initial cost is 10.
    costs = []
    for _ in iterations:
        costs.append(0.5 * theta**2)
        theta = theta - learning_rate * theta
    return np.array(costs)


small_rate = quadratic_cost_path(0.004)
suitable_rate = quadratic_cost_path(0.03)
large_rate = quadratic_cost_path(2.001)

axes[1].plot(iterations, small_rate, color="#2563eb", linewidth=2.2, label=r"Too small $\alpha$: slow")
axes[1].plot(iterations, suitable_rate, color="#16a34a", linewidth=2.4, label=r"Suitable $\alpha$")
axes[1].plot(iterations, large_rate, color="#dc2626", linewidth=2.1, label=r"Too large $\alpha$: unstable")
axes[1].set(
    title="Effect of the learning rate",
    xlabel="Iteration",
    ylabel=r"Cost $J(\theta)$",
    xlim=(0, 250),
    ylim=(0, 18),
)
axes[1].legend(frameon=False, loc="upper right")

for ax in axes:
    ax.grid(color="#d9dee8", linewidth=0.8)
    ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved training diagnostics to {OUTPUT_FILE}")
