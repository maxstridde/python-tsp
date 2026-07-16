from math import ceil
from typing import Optional

import requests

from .data_processing import process_input


def osrm_distance_matrix(
    sources: list[list[float]] | list[float],
    destinations: Optional[list[list[float]] | list[float]] = None,
    osrm_server_address: str = "http://localhost:5000",
    osrm_batch_size: int = 500,
    cost_type: str = "distances",
) -> list[list[float]]:
    """Compute distance matrix from sources to destinations using OSRM service

    Parameters
    ----------
    sources, destinations
        2D lists of coordinates in the form [lat, lng] for each row
        Also, if ``destinations`` is `None`, compute the distance between each
        source in ``sources``.

    osrm_server_address
        Base address of the OSRM server instance

    osrm_batch_size
        Subset of sources and destinations for each request. This reduces the
        request size, thus alleviating max table issues, but slows down the
        search

    cost_type
        "distances" to get the street distances and "durations" for the street
        time

    Returns
    -------
    Distance (or duration) matrix of size `num_sources x num_destinations`
    """
    sources, destinations = process_input(sources, destinations)

    num_sources = len(sources)
    num_destinations = len(destinations)
    cost_matrix = [[0.0] * num_destinations for _ in range(num_sources)]

    num_batches_i = ceil(num_sources / osrm_batch_size)
    num_batches_j = ceil(num_destinations / osrm_batch_size)

    for i in range(num_batches_i):
        start_i = i * osrm_batch_size
        end_i = min((i + 1) * osrm_batch_size, num_sources)

        for j in range(num_batches_j):
            start_j = j * osrm_batch_size
            end_j = min((j + 1) * osrm_batch_size, num_destinations)
            sources_batch = sources[start_i:end_i]
            destinations_batch = destinations[start_j:end_j]

            batch_result = _get_batch_osrm_distance(
                sources_batch,
                destinations_batch,
                osrm_server_address,
                cost_type=cost_type,
            )

            for ii in range(len(sources_batch)):
                for jj in range(len(destinations_batch)):
                    cost_matrix[start_i + ii][start_j + jj] = batch_result[ii][
                        jj
                    ]

    return cost_matrix


def _get_batch_osrm_distance(
    sources_batch: list[list[float]],
    destinations_batch: list[list[float]],
    osrm_server_address: str,
    cost_type: str,
) -> list[list[float]]:
    url = _format_osrm_url(
        sources_batch, destinations_batch, osrm_server_address, cost_type
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[cost_type]


def _format_osrm_url(
    sources_batch: list[list[float]],
    destinations_batch: list[list[float]],
    osrm_server_address: str,
    cost_type: str,
) -> str:
    url_cost_type = cost_type[:-1]

    sources_coord = ";".join(
        f"{source[1]},{source[0]}" for source in sources_batch
    )

    if (
        _array_equal(sources_batch, destinations_batch)
        and len(sources_batch) > 1
    ):
        return (
            f"{osrm_server_address}/table/v1/driving/"
            f"{sources_coord}"
            f"?annotations={url_cost_type}"
        )

    destinations_coord = ";".join(
        f"{destination[1]},{destination[0]}"
        for destination in destinations_batch
    )
    locations_coord = sources_coord + ";" + destinations_coord

    num_sources = len(sources_batch)
    num_destinations = len(destinations_batch)

    sources_indices = ";".join(str(index) for index in range(num_sources))
    destinations_indices = ";".join(
        str(index)
        for index in range(num_sources, num_sources + num_destinations)
    )

    return (
        f"{osrm_server_address}/table/v1/driving/"
        f"{locations_coord}"
        f"?sources={sources_indices}&destinations={destinations_indices}"
        f"&annotations={url_cost_type}"
    )


def _array_equal(a: list[list[float]], b: list[list[float]]) -> bool:
    if len(a) != len(b):
        return False
    return all(
        len(row_a) == len(row_b) and all(x == y for x, y in zip(row_a, row_b))
        for row_a, row_b in zip(a, b)
    )
