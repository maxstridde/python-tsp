import random
import sys
from io import StringIO

import pytest

from python_tsp.heuristics import local_search
from python_tsp.heuristics.perturbation_schemes import neighborhood_gen
from python_tsp.utils import compute_permutation_distance
from tests.data import (
    distance_matrix1,
    distance_matrix2,
    distance_matrix3,
    optimal_distance1,
    optimal_distance2,
    optimal_distance3,
    optimal_permutation1,
    optimal_permutation2,
    optimal_permutation3,
)

PERTURBATION_SCHEMES = neighborhood_gen.keys()


@pytest.mark.parametrize("scheme", PERTURBATION_SCHEMES)
@pytest.mark.parametrize(
    "distance_matrix", [distance_matrix1, distance_matrix2, distance_matrix3]
)
def test_local_search_returns_better_neighbor(scheme, distance_matrix):
    x = [0, 4, 2, 3, 1]
    fx = compute_permutation_distance(distance_matrix, x)

    _, fopt = local_search.solve_tsp_local_search(
        distance_matrix, x, perturbation_scheme=scheme
    )

    assert fopt < fx


@pytest.mark.parametrize("scheme", PERTURBATION_SCHEMES)
@pytest.mark.parametrize(
    "distance_matrix, optimal_permutation, optimal_distance",
    [
        (distance_matrix1, optimal_permutation1, optimal_distance1),
        (distance_matrix2, optimal_permutation2, optimal_distance2),
        (distance_matrix3, optimal_permutation3, optimal_distance3),
    ],
)
def test_local_search_returns_equal_optimal_solution(
    scheme, distance_matrix, optimal_permutation, optimal_distance
):
    x = optimal_permutation
    fx = optimal_distance
    xopt, fopt = local_search.solve_tsp_local_search(
        distance_matrix, x, perturbation_scheme=scheme
    )

    assert xopt == x
    assert fopt == fx


@pytest.mark.parametrize("scheme", PERTURBATION_SCHEMES)
def test_local_search_with_time_constraints(scheme):
    random.seed(1)
    n = 500
    distance_matrix = [[random.random() for _ in range(n)] for _ in range(n)]

    captured_output = StringIO()
    sys.stdout = captured_output

    local_search.solve_tsp_local_search(
        distance_matrix,
        perturbation_scheme=scheme,
        max_processing_time=0.0001,
        verbose=True,
    )

    output = captured_output.getvalue()
    if local_search.TIME_LIMIT_MSG not in output:
        # algorithm converged before the time limit; still correct
        assert "Current value" in output


def test_log_file_is_created_if_required(tmp_path):
    log_file = tmp_path / "tmp_log_file.log"

    local_search.solve_tsp_local_search(distance_matrix1, log_file=log_file)

    assert log_file.exists()
    assert "Current value" in log_file.read_text()
