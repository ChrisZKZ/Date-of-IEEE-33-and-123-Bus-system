"""Supplementary toy example: OSA uncertainty set.

This script is an independent illustrative example rather than the main
IEEE 33-/123-bus workflow in the repository.

Note
----
The reference value ``kexi_sm`` is a precomputed shape parameter obtained from
an SM-style example and is kept explicit here to preserve the original example
logic while making the script self-contained.
"""

import cvxpy as cp
import matplotlib.pyplot as plt
import numpy as np

from hyperplane import build_hyperplanes


# Copyright (c) 2026.
# Licensed under the Apache License, Version 2.0.


def main():
    np.random.seed(8)

    phi = np.zeros(2)
    cov = np.array([[1, 0.3], [0.3, 2]])

    n_samples = 800
    sigma_shift = np.random.uniform(-0.2, 0.2, size=2)
    rng = np.random.default_rng(seed=42)
    xi_samples = rng.multivariate_normal(phi, cov, size=n_samples) + sigma_shift

    d1 = xi_samples[: n_samples // 3]
    d2 = xi_samples[n_samples // 3 :]

    kexi_sm = np.array([2.70649391, 2.80211792])

    kexi_bound1 = np.zeros_like(kexi_sm)
    kexi_bound2 = np.zeros_like(kexi_sm)
    k_star = 259
    sorted_d1_col0 = np.sort(d1[:, 0])
    sorted_d1_col1 = np.sort(d1[:, 1])
    kexi_bound1[0] = sorted_d1_col0[k_star - 1]
    kexi_bound1[1] = sorted_d1_col1[-1]
    kexi_bound2[0] = sorted_d1_col0[-1]
    kexi_bound2[1] = sorted_d1_col1[k_star - 1]
    kexi_bounds = np.stack((kexi_bound1, kexi_bound2))
    print(f"x_bounds is {kexi_bounds}")

    bound_points_nodewise = np.zeros((2, 2, 2))
    bound_points_nodewise[0] = np.stack((kexi_bound1, kexi_sm))
    bound_points_nodewise[1] = np.stack((kexi_bound2, kexi_sm))
    normal, offset = build_hyperplanes(bound_points_nodewise)

    kexi_inside = np.zeros_like(kexi_sm)
    kexi_inside[0] = sorted_d1_col0[k_star - 1]
    kexi_inside[1] = sorted_d1_col1[k_star - 1]
    print(f"the sign of normal vector is {np.dot(normal[0], kexi_inside) + offset[0]}")

    a_matrix = np.eye(2)
    b_vec = np.array([5, 10])

    x = cp.Variable(2)
    kexi_opt = cp.Variable(2)

    constraints = []
    for j in range(2):
        constraints.append(kexi_opt[j] <= b_vec[j] - a_matrix[j] @ x)

    for l in range(2):
        constraints.append(normal[l] @ kexi_opt + offset[l] <= 0)

    c1 = np.array([1, 0])
    x_norm = np.array([4, 6])
    c2 = np.array([1, 1])
    objective = cp.Maximize(c1 @ x - c2 @ cp.square(x - x_norm))

    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.GUROBI)
    print("Optimal x:", x.value)
    print("Objective value:", prob.value)
    print("Optimal kexi_opt:", kexi_opt.value)
    print("kexi_sm:", kexi_sm)
    x_star = x.value

    lower_bound = b_vec - kexi_opt.value
    x_min, y_min = lower_bound
    x_max = -d2[:, 0].min() + b_vec[0] + 0.5
    y_max = -d2[:, 1].min() + b_vec[1] + 0.5

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(-d2[:, 0] + b_vec[0], -d2[:, 1] + b_vec[1], c="orange", label="Sampled $\\xi$ in $D_2$", alpha=0.6)
    feasible_box = plt.Rectangle(
        (x_min, y_min),
        x_max - x_min,
        y_max - y_min,
        edgecolor="blue",
        facecolor="none",
        linewidth=2,
        label="OSA uncertainty set $U_\\xi^r$",
    )
    ax.add_patch(feasible_box)
    ax.scatter(*x_star, c="red", marker="x", s=100, label="x_osa")
    ax.set_xlabel("PV at t=1")
    ax.set_ylabel("PV at t=2")
    ax.set_title(f"OSA obj value: {prob.value}")
    ax.legend()
    ax.grid(True)
    ax.axis("equal")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
