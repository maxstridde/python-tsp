import math
from typing import Optional

from .data_processing import process_input

EARTH_RADIUS_METERS = 6371000


def _great_circle_distance(src: list[float], dst: list[float]) -> float:
    src_rad = [math.radians(c) for c in src]
    dst_rad = [math.radians(c) for c in dst]

    delta_lambda = src_rad[1] - dst_rad[1]
    phi1 = src_rad[0]
    phi2 = dst_rad[0]

    delta_sigma = math.atan2(
        math.sqrt(
            (math.cos(phi2) * math.sin(delta_lambda)) ** 2
            + (
                math.cos(phi1) * math.sin(phi2)
                - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
            )
            ** 2
        ),
        (
            math.sin(phi1) * math.sin(phi2)
            + math.cos(phi1) * math.cos(phi2) * math.cos(delta_lambda)
        ),
    )

    return EARTH_RADIUS_METERS * delta_sigma


def great_circle_distance_matrix(
    sources: list[list[float]] | list[float],
    destinations: Optional[list[list[float]] | list[float]] = None,
) -> list[list[float]]:
    """Distance matrix using the Great Circle distance
    This is an Euclidean-like distance but on spheres [1]. In this case it is
    used to estimate the distance in meters between locations in the Earth.

    Parameters
    ----------
    sources, destinations
        Lists with each row containing the coordinates of a point in the form
        [lat, lng]. Notice it only considers the first two columns.
        Also, if ``destinations`` is `None`, compute the distance between each
        source in ``sources``.

    Returns
    -------
    distance_matrix
        list with the (i, j) entry indicating the Great Circle distance (in
        meters) between the i-th row in ``sources`` and the j-th row in
        ``destinations``.

    References
    ----------
    [1] https://en.wikipedia.org/wiki/Great-circle_distance
    Using the third computational formula
    """
    sources, destinations = process_input(sources, destinations)
    result = []
    for src in sources:
        row = [_great_circle_distance(src, dst) for dst in destinations]
        result.append(row)
    return result
