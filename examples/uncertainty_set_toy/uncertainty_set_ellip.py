"""Supplementary toy example: ellipsoidal uncertainty set.

This script is an independent illustrative example rather than the main
IEEE 33-/123-bus workflow in the repository.
"""

import cvxpy as cp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse


# Copyright (c) 2026.
# Licensed under the Apache License, Version 2.0.


def plot_ellipsoid(ax, mean, cov, radius, **kwargs):
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    theta = np.degrees(np.arctan2(*eigvecs[:, 0][::-1]))
    width, height = 2 * np.sqrt(radius * eigvals)
    ellip = Ellipse(xy=mean, width=width, height=height, angle=theta, **kwargs)
    ax.add_patch(ellip)


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

    phi_hat = np.mean(d1, axis=0)
    print(f"phi_hat: {phi_hat}")
    m_hat = np.cov(d1.T, bias=False)

    m_inv = np.linalg.inv(m_hat)
    g_values = [(xi - phi_hat).T @ m_inv @ (xi - phi_hat) for xi in d2]
    g_values_sorted = np.sort(g_values)

    k_star = 516
    print(f"k_star is: {k_star}, number of samples: {len(d2)}")
    r_star = g_values_sorted[k_star - 1]
    print(f"the estimated params for ellipsoidal uncertainty set: {r_star}")

    a_matrix = np.eye(2)
    b_vec = np.array([5, 10])
    c_matrix = np.eye(2)

    x = cp.Variable(2)
    constraints = []
    for j in range(2):
        lhs = c_matrix[j] @ phi_hat + cp.sqrt(r_star * cp.quad_form(c_matrix[j], m_hat))
        constraints.append(lhs <= b_vec[j] - a_matrix[j] @ x)

    c1 = np.array([1, 0])
    x_norm = np.array([4, 6])
    c2 = np.array([1, 1])
    objective = cp.Maximize(c1 @ x - c2 @ cp.square(x - x_norm))

    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.GUROBI)
    print("Optimal x:", x.value)
    print("Objective value:", prob.value)
    x_star = x.value

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(-d2[:, 0] + b_vec[0], -d2[:, 1] + b_vec[1], c="orange", label="Sampled $\\xi$ in $D_2$", alpha=0.6)
    plot_ellipsoid(ax, -phi_hat + b_vec, m_hat, r_star, edgecolor="blue", facecolor="none", linewidth=2, label="Ellipsoidal Set")
    ax.scatter(*x_star, c="blue", marker="x", s=100, label="Optimal $x$")
    ax.set_xlabel("PV at t=1")
    ax.set_ylabel("PV at t=2")
    ax.set_title(f"Ellipsoidal uncertainty set, optimal value: {prob.value}")
    ax.grid(True)
    ax.axis("equal")
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
