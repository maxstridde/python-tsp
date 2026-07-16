import pytest

from python_tsp.distances import euclidean_distance_matrix


@pytest.fixture
def sources():
    return [[1.0, -1.0], [2.0, -2.0], [3.0, -3.0], [4.0, -4.0]]


@pytest.fixture
def destinations():
    return [[5.0, -5.0], [6.0, -6.0], [7.0, -7.0]]


def test_distance_is_euclidean():
    source = [1.0, 1.0]
    destination = [4.0, 5.0]

    distance_matrix = euclidean_distance_matrix(source, destination)

    assert distance_matrix[0][0] == 5.0


def test_all_elements_are_non_negative(sources, destinations):
    distance_matrix = euclidean_distance_matrix(sources, destinations)

    assert all(v >= 0 for row in distance_matrix for v in row)


def test_square_matrix_has_zero_diagonal(sources):
    distance_matrix = euclidean_distance_matrix(sources)

    for i in range(len(sources)):
        assert distance_matrix[i][i] == 0


def test_square_matrix_is_symmetric(sources):
    distance_matrix = euclidean_distance_matrix(sources)
    n = len(distance_matrix)
    for i in range(n):
        for j in range(n):
            assert abs(distance_matrix[i][j] - distance_matrix[j][i]) < 1e-10


def test_matrix_has_proper_shape(sources, destinations):
    distance_matrix = euclidean_distance_matrix(sources, destinations)

    N, M = len(sources), len(destinations)
    assert len(distance_matrix) == N
    assert all(len(row) == M for row in distance_matrix)
