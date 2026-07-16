from math import inf

import pytest

from python_tsp.exact import solve_tsp_branch_and_bound
from tests.data import (
    distance_matrix1,
    distance_matrix2,
    distance_matrix3,
    optimal_distance1,
    optimal_distance2,
    optimal_distance3,
)


@pytest.mark.parametrize(
    "distance_matrix", [distance_matrix1, distance_matrix2, distance_matrix3]
)
def test_solution_has_all_nodes(distance_matrix):
    permutation, _ = solve_tsp_branch_and_bound(distance_matrix)

    num_nodes = len(distance_matrix)
    assert len(permutation) == num_nodes
    assert set(permutation) == set(range(num_nodes))


@pytest.mark.parametrize(
    "distance_matrix, expected_distance",
    [
        (distance_matrix1, optimal_distance1),
        (distance_matrix2, optimal_distance2),
        (distance_matrix3, optimal_distance3),
    ],
)
def test_solution_is_optimal(distance_matrix, expected_distance):
    _, distance = solve_tsp_branch_and_bound(distance_matrix)

    assert distance == expected_distance


def test_solver_on_an_unfeasible_problem():
    distance_matrix = [
        [inf, 10, 15, 20, inf],
        [inf, inf, 12, inf, 25],
        [inf, inf, inf, 8, 18],
        [inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf],
    ]
    permutation, distance = solve_tsp_branch_and_bound(distance_matrix)

    assert permutation == []
    assert distance == inf
