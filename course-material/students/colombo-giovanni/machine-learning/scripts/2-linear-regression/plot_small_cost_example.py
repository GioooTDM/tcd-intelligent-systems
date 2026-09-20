"""Plot the cost function and its derivative for the two-point example."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "small-example-cost-function.svg"


theta_1_values = [-1 + i * 2.8 / 400 for i in range(401)]
costs = [
    0.5 * ((3 * theta_1 - 1) ** 2 + (2 * theta_1 - 1) ** 2)
    for theta_1 in theta_1_values
]
derivatives = [13 * theta_1 - 5 for theta_1 in theta_1_values]

minimum_theta_1 = 5 / 13
minimum_cost = 1 / 26

fig, (cost_ax, derivative_ax) = plt.subplots(1, 2, figsize=(12, 4.5))

cost_ax.plot(theta_1_values, costs, color="#2563eb", linewidth=2.5)
cost_ax.scatter(
    [minimum_theta_1],
    [minimum_cost],
    color="#dc2626",
    s=55,
    zorder=3,
    label=rf"Minimum: $\theta_1=5/13\approx{minimum_theta_1:.3f}$",
)
cost_ax.set(
    title=r"Cost function $f(\theta_1)=J(\theta_1)$",
    xlabel=r"$\theta_1$",
    ylabel=r"$J(\theta_1)$",
    xlim=(-1, 1.8),
    ylim=(0, 15),
)
cost_ax.grid(color="#d9dee8", linewidth=0.8)
cost_ax.set_axisbelow(True)
cost_ax.legend(frameon=False)

derivative_ax.plot(theta_1_values, derivatives, color="#16a34a", linewidth=2.5)
derivative_ax.scatter(
    [minimum_theta_1],
    [0],
    color="#dc2626",
    s=55,
    zorder=3,
    label=rf"Zero: $\theta_1=5/13\approx{minimum_theta_1:.3f}$",
)
derivative_ax.set(
    title=r"Derivative $f'(\theta_1)=13\theta_1-5$",
    xlabel=r"$\theta_1$",
    ylabel=r"$f'(\theta_1)$",
    xlim=(-1, 1.8),
    ylim=(-20, 20),
)
derivative_ax.grid(color="#d9dee8", linewidth=0.8)
derivative_ax.set_axisbelow(True)
derivative_ax.legend(frameon=False)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved small cost example to {OUTPUT_FILE}")
