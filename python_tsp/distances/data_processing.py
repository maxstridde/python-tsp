from __future__ import annotations


def process_input(
    sources: list[list[float]] | list[float],
    destinations: list[list[float]] | list[float] | None = None,
) -> tuple[list[list[float]], list[list[float]]]:
    """Pre-process input
    This function ensures ``sources`` and ``destinations`` are two-dimensional
    lists, and if ``destinations`` is `None`, set it equal to ``sources``.
    """
    if destinations is None:
        destinations = sources

    sources = _ensure_2d(sources)
    destinations = _ensure_2d(destinations)

    return sources, destinations


def _ensure_2d(points: list) -> list[list[float]]:
    if not points:
        return []
    if isinstance(points[0], (int, float)):
        return [points]
    return points
