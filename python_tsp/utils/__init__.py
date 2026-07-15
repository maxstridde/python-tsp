"""Auxiliary functions that may be used in most modules"""

from contextlib import contextmanager
from typing import Optional

from .permutation_distance import compute_permutation_distance  # noqa: F401
from .setup_initial_solution import setup_initial_solution  # noqa: F401


@contextmanager
def _optional_open(filename: Optional[str], mode: str = "r"):
    if filename:
        with open(filename, mode, encoding="utf-8") as f:
            yield f
    else:
        yield None
