"""Show gradient descent on convex and non-convex 3D cost surfaces."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MODULE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = MODULE_DIR / "images" / "2-linear-regression" / "gradient-descent-3d.svg"


def follow_gradient(start, gradient, learning_rate, steps):
    """Return the parameter pairs visited by gradient descent."""
    path = [np.array(start, dtype=float)]
    for _ in range(steps):
        path.append(path[-1] - learning_rate * np.array(gradient(*path[-1])))
    return np.array(path)


def sampled_path(path, every=3):
    """Keep a few path points so the 3D figure remains uncluttered."""
    sampled = path[::every]
    if not np.array_equal(sampled[-1], path[-1]):
        sampled = np.vstack((sampled, path[-1]))
    return sampled


def style_3d_axis(ax):
    """Apply a light, consistent style to a 3D axis."""
    ax.set_box_aspect((1.1, 1, 0.7))
    ax.tick_params(labelsize=9, pad=1)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 1))
        axis._axinfo["grid"]["color"] = (0.85, 0.87, 0.91, 1)


fig = plt.figure(figsize=(13, 5.5))

# Convex least-squares surface for y = 1 + 2x on three training examples.
x_train = np.array([0.0, 1.0, 2.0])
y_train = np.array([1.0, 3.0, 5.0])


def least_squares_cost(theta_0, theta_1):
    predictions = theta_0[..., None] + theta_1[..., None] * x_train
    return np.mean((predictions - y_train) ** 2, axis=-1)


def least_squares_gradient(theta_0, theta_1):
    errors = theta_0 + theta_1 * x_train - y_train
    return 2 * np.mean(errors), 2 * np.mean(errors * x_train)


theta_0_values = np.linspace(-2, 4, 100)
theta_1_values = np.linspace(-1, 4, 100)
theta_0_grid, theta_1_grid = np.meshgrid(theta_0_values, theta_1_values)
convex_cost = least_squares_cost(theta_0_grid, theta_1_grid)
convex_path = follow_gradient((-1.5, -0.5), least_squares_gradient, 0.12, 22)
convex_path_cost = least_squares_cost(convex_path[:, 0], convex_path[:, 1])

convex_ax = fig.add_subplot(1, 2, 1, projection="3d")
convex_ax.plot_wireframe(
    theta_0_grid,
    theta_1_grid,
    convex_cost,
    color="#94a3b8",
    alpha=0.7,
    linewidth=0.55,
    rstride=5,
    cstride=5,
)
convex_ax.plot(
    convex_path[:, 0],
    convex_path[:, 1],
    convex_path_cost + 0.35,
    color="#dc2626",
    linewidth=2.6,
)
convex_markers = sampled_path(convex_path)
convex_ax.scatter(
    convex_markers[:, 0],
    convex_markers[:, 1],
    least_squares_cost(convex_markers[:, 0], convex_markers[:, 1]) + 0.35,
    color="#dc2626",
    s=24,
)
convex_ax.scatter([1], [2], [0.15], color="#dc2626", s=45)
convex_ax.set(
    title="Convex least-squares cost",
    xlabel=r"$\theta_0$",
    ylabel=r"$\theta_1$",
    zlabel=r"$J(\theta_0,\theta_1)$",
)
convex_ax.view_init(elev=27, azim=-58)
style_3d_axis(convex_ax)

# Generic non-convex surface with several valleys.
def nonconvex_cost(theta_0, theta_1):
    return np.sin(theta_0) * np.cos(theta_1) + 0.06 * (theta_0**2 + theta_1**2) + 1.6


def nonconvex_gradient(theta_0, theta_1):
    return (
        np.cos(theta_0) * np.cos(theta_1) + 0.12 * theta_0,
        -np.sin(theta_0) * np.sin(theta_1) + 0.12 * theta_1,
    )


surface_values = np.linspace(-5, 5, 120)
surface_theta_0, surface_theta_1 = np.meshgrid(surface_values, surface_values)
surface_cost = nonconvex_cost(surface_theta_0, surface_theta_1)
paths = [
    follow_gradient((-4.2, 3.8), nonconvex_gradient, 0.18, 28),
    follow_gradient((4.3, -3.6), nonconvex_gradient, 0.18, 28),
]

nonconvex_ax = fig.add_subplot(1, 2, 2, projection="3d")
nonconvex_ax.plot_wireframe(
    surface_theta_0,
    surface_theta_1,
    surface_cost,
    color="#94a3b8",
    alpha=0.7,
    linewidth=0.55,
    rstride=6,
    cstride=6,
)
for path, colour in zip(paths, ("#dc2626", "#7c3aed")):
    path_cost = nonconvex_cost(path[:, 0], path[:, 1])
    nonconvex_ax.plot(
        path[:, 0],
        path[:, 1],
        path_cost + 0.18,
        color=colour,
        linewidth=2.5,
    )
    path_markers = sampled_path(path, every=4)
    nonconvex_ax.scatter(
        path_markers[:, 0],
        path_markers[:, 1],
        nonconvex_cost(path_markers[:, 0], path_markers[:, 1]) + 0.18,
        color=colour,
        s=22,
    )

nonconvex_ax.set(
    title="Non-convex cost",
    xlabel=r"$\theta_0$",
    ylabel=r"$\theta_1$",
    zlabel=r"$J(\theta_0,\theta_1)$",
)
nonconvex_ax.view_init(elev=31, azim=-52)
style_3d_axis(nonconvex_ax)

fig.tight_layout()
fig.savefig(OUTPUT_FILE, facecolor="white")

print(f"Saved 3D gradient-descent illustration to {OUTPUT_FILE}")
