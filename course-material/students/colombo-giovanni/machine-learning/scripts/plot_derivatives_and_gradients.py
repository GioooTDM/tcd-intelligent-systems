"""Create separate figures for a tangent line and a tangent plane."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[1]
DERIVATIVE_OUTPUT_FILE = MODULE_DIR / "images" / "derivative-tangent-line.svg"
PLANE_OUTPUT_FILE = MODULE_DIR / "images" / "gradient-tangent-plane.svg"


# One input: the derivative is the slope of the tangent line.
curve_fig, curve_ax = plt.subplots(figsize=(7, 4.5))
x = np.linspace(-2.2, 2.2, 300)
curve_ax.plot(x, x**2, color="#2563eb", linewidth=2.5, label=r"$f(x)=x^2$")
curve_ax.plot(x, 2 * x - 1, color="#f59e0b", linewidth=2, label=r"Tangent: slope $f'(1)=2$")
curve_ax.scatter([1], [1], color="#dc2626", s=50, zorder=3)
curve_ax.set(
    title="One input: tangent line",
    xlabel=r"$x$",
    ylabel=r"$f(x)$",
    xlim=(-2.2, 2.2),
    ylim=(-2, 5.2),
)
curve_ax.grid(color="#d9dee8", linewidth=0.8)
curve_ax.set_axisbelow(True)
curve_ax.legend(frameon=False, loc="upper left")
curve_fig.tight_layout()
curve_fig.savefig(DERIVATIVE_OUTPUT_FILE, facecolor="white")
plt.close(curve_fig)

# Two inputs: the first-order approximation is a tangent plane.
surface_fig = plt.figure(figsize=(7, 5.2))
surface_ax = surface_fig.add_subplot(1, 1, 1, projection="3d")
x_1 = np.linspace(-2, 2, 45)
x_2 = np.linspace(-2, 2, 45)
x_1_grid, x_2_grid = np.meshgrid(x_1, x_2)
surface = x_1_grid**2 + x_2_grid**2
surface_ax.plot_wireframe(
    x_1_grid,
    x_2_grid,
    surface,
    color="#94a3b8",
    linewidth=0.55,
    rstride=4,
    cstride=4,
    alpha=0.75,
)

plane_values = np.linspace(0.3, 1.7, 10)
plane_x_1, plane_x_2 = np.meshgrid(plane_values, plane_values)
tangent_plane = 2 + 2 * (plane_x_1 - 1) + 2 * (plane_x_2 - 1)
surface_ax.plot_surface(
    plane_x_1,
    plane_x_2,
    tangent_plane,
    color="#fbbf24",
    alpha=0.45,
    linewidth=0,
)
surface_ax.scatter([1], [1], [2], color="#dc2626", s=45)
surface_ax.set(
    title="Two inputs: tangent plane",
    xlabel=r"$x_1$",
    ylabel=r"$x_2$",
    zlabel=r"$f(x_1,x_2)$",
    xlim=(-2, 2),
    ylim=(-2, 2),
    zlim=(0, 8),
)
surface_ax.view_init(elev=28, azim=-58)
surface_ax.set_box_aspect((1, 1, 0.72))
surface_fig.tight_layout()
surface_fig.savefig(PLANE_OUTPUT_FILE, facecolor="white")
plt.close(surface_fig)

print(f"Saved tangent-line figure to {DERIVATIVE_OUTPUT_FILE}")
print(f"Saved tangent-plane figure to {PLANE_OUTPUT_FILE}")
