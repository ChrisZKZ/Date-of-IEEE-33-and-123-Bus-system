"""Helper functions for supplementary uncertainty-set toy examples.

This file is part of the supplementary illustrative examples for the paper:
"Asynchronous Distributed Scheduling of Active Distribution Network and
Thermostatically Controlled Loads With MPC-Based Aggregation".
"""

import numpy as np


def build_hyperplanes(bound_points_nodewise: np.ndarray):
    """Build one hyperplane for each node from a set of points.

    Parameters
    ----------
    bound_points_nodewise : np.ndarray
        Array of shape (node_num, T, T). For each node, T points in T dimensions
        are provided and used to construct a hyperplane a_i @ x + b_i = 0.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        normals with shape (node_num, T) and offsets with shape (node_num,).
    """
    node_num, horizon, _ = bound_points_nodewise.shape
    normals = np.zeros((node_num, horizon))
    offsets = np.zeros(node_num)

    for idx in range(node_num):
        points = bound_points_nodewise[idx]
        system = np.ones((horizon, horizon + 1))
        system[:, :-1] = points

        _, _, vh = np.linalg.svd(system)
        solution = vh[-1]

        normals[idx] = solution[:-1]
        offsets[idx] = solution[-1]

    return normals, offsets
