"""Supplementary toy example: SM uncertainty set.

This script is an independent illustrative example rather than the main
IEEE 33-/123-bus workflow in the repository.
"""

import cvxpy as cp
import matplotlib.pyplot as plt
import numpy as np


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

    kexi_base = np.mean(d1, axis=0)
    print(f"kexi_hat is {kexi_base}")

    c_matrix = np.eye(2)
    tau = 10
    g_r_values = []
    for kexi in d2:
        max_gr = 0
        for j in range(len(c_matrix)):
            numerator = c_matrix[j] @ kexi + tau
            denominator = kexi_base[j] + tau
            gr_j = numerator / denominator
            max_gr = max(max_gr, gr_j)
        g_r_values.append(max_gr)

    g_r_sorted = np.sort(g_r_values)
    k_star_r = 516
    s_r_star = g_r_sorted[k_star_r - 1]
    print(f"the estimated params for s_r_star of the uncertainty set: {s_r_star}")

    kexi_sm = s_r_star * (kexi_base + tau) - tau
    print(f"kexi_sm is {kexi_sm}")

    a_matrix = np.eye(2)
    b_vec = np.array([5, 10])

    x = cp.Variable(2)
    constraints = []
    for j in range(2):
        constraints.append(kexi_sm[j] <= b_vec[j] - a_matrix[j] @ x)

    c1 = np.array([1, 0])
    x_norm = np.array([4, 6])
    c2 = np.array([1, 1])
    objective = cp.Maximize(c1 @ x - c2 @ cp.square(x - x_norm))

    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.GUROBI)
    print("Optimal x:", x.value)
    print("Objective value:", prob.value)
    x_star = x.value

    lower_bound = b_vec - kexi_sm
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
        label="SM Uncertainty Set $U_\\xi^r$",
    )
    ax.add_patch(feasible_box)
    ax.scatter(*x_star, c="red", marker="x", s=100, label="x_opt")
    ax.set_xlabel("PV at t=1")
    ax.set_ylabel("PV at t=2")
    ax.set_title(f"SM obj value: {prob.value}")
    ax.legend()
    ax.grid(True)
    ax.axis("equal")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
