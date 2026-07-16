import random
import sys
from io import StringIO

import pytest

from python_tsp.heuristics import simulated_annealing
from python_tsp.heuristics.perturbation_schemes import neighborhood_gen
from tests.data import (
    distance_matrix1,
    distance_matrix2,
    distance_matrix3,
)

PERTURBATION_SCHEMES = neighborhood_gen.keys()


@pytest.fixture
def permutation():
    return [0, 1, 2, 3, 4]


@pytest.mark.parametrize(
    "distance_matrix", [distance_matrix1, distance_matrix2, distance_matrix3]
)
@pytest.mark.parametrize("scheme", PERTURBATION_SCHEMES)
def test_simulated_annealing_solution_is_valid(
    permutation, distance_matrix, scheme
):
    x, _ = simulated_annealing.solve_tsp_simulated_annealing(
        distance_matrix, perturbation_scheme=scheme
    )

    assert set(x) == set(range(5))
    assert x[0] == 0


@pytest.mark.parametrize("scheme", PERTURBATION_SCHEMES)
def test_simulated_annealing_with_time_constraints(permutation, scheme):
    max_processing_time = 1
    random.seed(1)
    n = 500
    distance_matrix = [[random.random() for _ in range(n)] for _ in range(n)]

    captured_output = StringIO()
    sys.stdout = captured_output

    simulated_annealing.solve_tsp_simulated_annealing(
        distance_matrix,
        perturbation_scheme=scheme,
        max_processing_time=max_processing_time,
        verbose=True,
    )

    assert simulated_annealing.TIME_LIMIT_MSG in captured_output.getvalue()


def test_log_file_is_created_if_required(permutation, tmp_path):
    log_file = tmp_path / "tmp_log_file.log"

    simulated_annealing.solve_tsp_simulated_annealing(
        distance_matrix1, log_file=log_file
    )

    assert log_file.exists()
    assert "Temperature" in log_file.read_text()
    assert "Current value" in log_file.read_text()
