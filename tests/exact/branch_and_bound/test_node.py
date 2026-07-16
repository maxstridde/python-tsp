from math import inf

import pytest

from python_tsp.exact.branch_and_bound import Node


@pytest.fixture
def cost_matrix():
    return [
        [inf, 20, 30, 10, 11],
        [15, inf, 16, 4, 2],
        [3, 5, inf, 2, 4],
        [19, 6, 18, inf, 3],
        [16, 4, 7, 16, inf],
    ]


@pytest.fixture
def reduced_cost_matrix():
    return [
        [inf, 10, 17, 0, 1],
        [12, inf, 11, 2, 0],
        [0, 3, inf, 0, 2],
        [15, 3, 12, inf, 0],
        [11, 0, 0, 12, inf],
    ]


def _matrix_equal(a, b):
    return all(
        a[i][j] == b[i][j] for i in range(len(a)) for j in range(len(a[0]))
    )


def test_compute_reduced_matrix(cost_matrix, reduced_cost_matrix):
    for request_matrix, expected_reduced_matrix, expected_cost in [
        (cost_matrix, reduced_cost_matrix, 25),
        (reduced_cost_matrix, reduced_cost_matrix, 0),
    ]:
        response_matrix, response_cost = Node.compute_reduced_matrix(
            matrix=request_matrix
        )

        assert _matrix_equal(response_matrix, expected_reduced_matrix)
        assert response_cost == expected_cost


def test_compute_reduced_matrix_with_invalid_matrices():
    invalid_matrix = [[inf] * 5 for _ in range(5)]
    response_matrix, response_cost = Node.compute_reduced_matrix(
        matrix=invalid_matrix
    )

    assert _matrix_equal(response_matrix, invalid_matrix)
    assert response_cost == 0


def test_create_node_from_cost_matrix(cost_matrix, reduced_cost_matrix):
    response = Node.from_cost_matrix(cost_matrix=cost_matrix)

    assert response.level == 0
    assert response.index == 0
    assert response.cost == 25
    assert _matrix_equal(response.cost_matrix, reduced_cost_matrix)
    assert response.path == [0]


@pytest.mark.parametrize(
    "index, expected_cost", [(1, 35), (2, 53), (3, 25), (4, 31)]
)
def test_create_node_from_parent(cost_matrix, index, expected_cost):
    parent = Node.from_cost_matrix(cost_matrix=cost_matrix)
    response = Node.from_parent(parent=parent, index=index)

    assert response.level == 1
    assert response.index == index
    assert response.cost == expected_cost
    assert response.path == [parent.index, response.index]


@pytest.mark.parametrize("index, expected_cost", [(1, 35), (2, 53), (4, 31)])
def test_min_cost_node(cost_matrix, index, expected_cost):
    min_cost_node = Node.from_cost_matrix(cost_matrix=cost_matrix)
    response = Node.from_parent(parent=min_cost_node, index=index)

    assert min_cost_node.cost == 25
    assert response.cost == expected_cost
    assert min_cost_node < response
