from typing import Optional, TextIO

from python_tsp.exact import solve_tsp_brute_force
from python_tsp.utils import _optional_open, setup_initial_solution


def _cycle_to_successors(cycle: list[int]) -> list[int]:
    successors = cycle[:]
    n = len(cycle)
    for i, _ in enumerate(cycle):
        successors[cycle[i]] = cycle[(i + 1) % n]
    return successors


def _successors_to_cycle(successors: list[int]) -> list[int]:
    cycle = successors[:]
    j = 0
    for i, _ in enumerate(successors):
        cycle[i] = j
        j = successors[j]
    return cycle


def _minimizes_hamiltonian_path_distance(
    tabu: list[list[int]],
    iteration: int,
    successors: list[int],
    ejected_edge: tuple[int, int],
    distance_matrix: list[list[float]],
    hamiltonian_path_distance: float,
    hamiltonian_cycle_distance: float,
) -> tuple[int, int, float]:
    a, b = ejected_edge
    best_c = c = last_c = successors[b]
    path_cb_distance = distance_matrix[c][b]
    path_bc_distance = distance_matrix[b][c]
    hamiltonian_path_distance_found = hamiltonian_cycle_distance

    while successors[c] != a:
        d = successors[c]
        path_cb_distance += distance_matrix[c][last_c]
        path_bc_distance += distance_matrix[last_c][c]
        new_hamiltonian_path_distance_found = (
            hamiltonian_path_distance
            + distance_matrix[b][d]
            - distance_matrix[c][d]
            + path_cb_distance
            - path_bc_distance
        )

        if (
            new_hamiltonian_path_distance_found + distance_matrix[a][c]
            < hamiltonian_cycle_distance
        ):
            return c, d, new_hamiltonian_path_distance_found

        if (
            tabu[c][d] != iteration
            and new_hamiltonian_path_distance_found
            < hamiltonian_path_distance_found
        ):
            hamiltonian_path_distance_found = (
                new_hamiltonian_path_distance_found
            )
            best_c = c

        last_c = c
        c = d

    return best_c, successors[best_c], hamiltonian_path_distance_found


def _print_message(
    msg: str, verbose: bool, log_file_handler: Optional[TextIO]
) -> None:
    if log_file_handler:
        print(msg, file=log_file_handler)

    if verbose:
        print(msg)


def _solve_tsp_brute_force(
    distance_matrix: list[list[float]],
    log_file: Optional[str] = None,
    verbose: bool = False,
) -> tuple[list[int], float]:
    x, fx = solve_tsp_brute_force(distance_matrix)
    x = x or []

    msg = (
        "Few nodes to use Lin-Kernighan heuristics, "
        "using Brute Force instead. "
    )
    if not x:
        msg += "No solution found."
    else:
        msg += f"Found value: {fx}"

    with _optional_open(log_file, "w") as log_file_handler:
        _print_message(msg, verbose, log_file_handler)

    return x, fx


def solve_tsp_lin_kernighan(
    distance_matrix: list[list[float]],
    x0: Optional[list[int]] = None,
    log_file: Optional[str] = None,
    verbose: bool = False,
) -> tuple[list[int], float]:
    """
    Solve the Traveling Salesperson Problem using the Lin-Kernighan algorithm.

    Parameters
    ----------
    distance_matrix
        Distance matrix of shape (n x n) with the (i, j) entry indicating the
        distance from node i to j

    x0
        Initial permutation. If not provided, it starts with a random path.

    log_file
        If not `None`, creates a log file with details about the whole
        execution.

    verbose
        If true, prints algorithm status every iteration.

    Returns
    -------
    Tuple
        A tuple containing the Hamiltonian cycle and its distance.

    References
    ----------
    Éric D. Taillard, "Design of Heuristic Algorithms for Hard Optimization,"
    Chapter 5, Section 5.3.2.1: Lin-Kernighan Neighborhood, Springer, 2023.
    """
    num_vertices = len(distance_matrix)
    if num_vertices < 4:
        return _solve_tsp_brute_force(distance_matrix, log_file, verbose)

    hamiltonian_cycle, hamiltonian_cycle_distance = setup_initial_solution(
        distance_matrix=distance_matrix, x0=x0
    )
    vertices = list(range(num_vertices))
    iteration = 0
    improvement = True
    tabu = [[0] * num_vertices for _ in range(num_vertices)]

    with _optional_open(log_file, "w") as log_file_handler:
        while improvement:
            iteration += 1
            improvement = False
            successors = _cycle_to_successors(hamiltonian_cycle)

            a = max(
                range(len(vertices)),
                key=lambda i: distance_matrix[vertices[i]][successors[i]],
            )
            b = successors[a]
            hamiltonian_path_distance = (
                hamiltonian_cycle_distance - distance_matrix[a][b]
            )

            while True:
                ejected_edge = a, b

                (
                    c,
                    d,
                    hamiltonian_path_distance_found,
                ) = _minimizes_hamiltonian_path_distance(
                    tabu,
                    iteration,
                    successors,
                    ejected_edge,
                    distance_matrix,
                    hamiltonian_path_distance,
                    hamiltonian_cycle_distance,
                )

                if (
                    hamiltonian_path_distance_found
                    >= hamiltonian_cycle_distance
                ):
                    break

                hamiltonian_path_distance = hamiltonian_path_distance_found

                i, si, successors[b] = b, successors[b], d
                while i != c:
                    successors[si], i, si = i, si, successors[si]

                tabu[c][d] = tabu[d][c] = iteration

                b = c

                msg = (
                    f"Current value: {hamiltonian_cycle_distance}; "
                    f"Ejection chain: {iteration}"
                )
                _print_message(msg, verbose, log_file_handler)

                if (
                    hamiltonian_path_distance + distance_matrix[a][b]
                    < hamiltonian_cycle_distance
                ):
                    improvement = True
                    successors[a] = b
                    hamiltonian_cycle = _successors_to_cycle(successors)
                    hamiltonian_cycle_distance = (
                        hamiltonian_path_distance + distance_matrix[a][b]
                    )

    return hamiltonian_cycle, hamiltonian_cycle_distance
