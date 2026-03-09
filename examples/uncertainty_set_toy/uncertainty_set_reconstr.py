"""Supplementary toy example: reconstructed uncertainty set.

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
    _ = d1  # kept for consistency with other examples

    x_hat = np.array([2.10395761, 5.98554812])
    a_matrix = np.eye(2)
    b_vec = np.array([5, 10])
    gamma = np.eye(2)
    d_vec = b_vec - a_matrix @ x_hat
    print(f"kexi_shape is {d_vec}")

    tau = 1e-3
    g_r_values = []
    for kexi in d2:
        max_gr = 0
        for j in range(len(a_matrix)):
            numerator = -gamma[j] @ kexi + tau
            denominator = d_vec[j] + tau
            gr_j = numerator / denominator
            max_gr = max(max_gr, gr_j)
        g_r_values.append(max_gr)

    g_r_sorted = np.sort(g_r_values)
    g_r_indices_sorted = np.argsort(g_r_values)
    k_star_r = 516
    s_r_star = g_r_sorted[k_star_r - 1]
    kexi_index = g_r_indices_sorted[k_star_r - 1]
    kexi_star = d2[kexi_index]
    print(f"the estimated params for s_r_star of the uncertainty set: {s_r_star}")
    print(f"supporting sample is {kexi_star}")

    x = cp.Variable(2)
    lamda = cp.Variable((2, 2), nonneg=True)

    constraints = []
    for j in range(2):
        lhs = lamda[j, :] @ (s_r_star * (d_vec + tau) - tau)
        rhs = b_vec[j] - a_matrix[j] @ x
        constraints.append(lhs <= rhs)

        gamma_j_expr = lamda[j, :] @ gamma
        constraints.append(cp.sum_squares(gamma[j] - gamma_j_expr) <= 1e-6)

    c1 = np.array([1, 0])
    x_norm = np.array([4, 6])
    c2 = np.array([1, 1])
    objective = cp.Maximize(c1 @ x - c2 @ cp.square(x - x_norm))

    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.GUROBI)
    print("Optimal x:", x.value)
    print("Optimal lamda:", lamda.value)
    print("Objective value:", prob.value)
    x_star = x.value

    lower_bound = b_vec + (tau - s_r_star * (d_vec + tau))
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
        label="Reconstructed uncertainty set $U_\\xi^r$",
    )
    ax.add_patch(feasible_box)
    ax.scatter(*x_hat, c="red", marker="x", s=100, label="x_hat")
    ax.scatter(*x_star, c="green", marker="x", s=100, label="x_reconstr")
    ax.set_xlabel("PV at t=1")
    ax.set_ylabel("PV at t=2")
    ax.set_title(f"Reconstruction obj value: {prob.value}")
    ax.legend()
    ax.grid(True)
    ax.axis("equal")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
