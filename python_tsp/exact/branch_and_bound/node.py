from __future__ import annotations

from dataclasses import dataclass
from math import inf


@dataclass
class Node:
    """
    Represents a node in the search tree for the Traveling Salesperson Problem.

    Attributes
    ----------
    level
        The level of the node in the search tree.
    index
        The index of the current city in the path.
    path
        The list of city indices visited so far.
    cost
        The total cost of the path up to this node.
    cost_matrix
        The cost matrix representing the distances between cities.

    Methods
    -------
    compute_reduced_matrix
        Compute the reduced matrix and the cost of reducing it.
    from_cost_matrix
        Create a Node object from a given cost matrix.
    from_parent
        Create a new Node object based on a parent node and a city index.
    """

    level: int
    index: int
    path: list[int]
    cost: float
    cost_matrix: list[list[float]]

    @staticmethod
    def compute_reduced_matrix(
        matrix: list[list[float]],
    ) -> tuple[list[list[float]], float]:
        """
        Compute the reduced matrix and the cost of reducing it.

        Parameters
        ----------
        matrix
            The cost matrix to compute the reductions.

        Returns
        -------
        Tuple
            A tuple containing the reduced matrix and the total
            cost of reductions.
        """
        n = len(matrix)
        reduced = [row[:] for row in matrix]
        total_reduction = 0.0

        min_rows = [min(row) for row in reduced]
        for i in range(n):
            if min_rows[i] != inf and min_rows[i] != 0:
                for j in range(n):
                    if reduced[i][j] != inf:
                        reduced[i][j] -= min_rows[i]
                total_reduction += min_rows[i]

        min_cols = [min(reduced[i][j] for i in range(n)) for j in range(n)]
        for j in range(n):
            if min_cols[j] != inf and min_cols[j] != 0:
                for i in range(n):
                    if reduced[i][j] != inf:
                        reduced[i][j] -= min_cols[j]
                total_reduction += min_cols[j]

        return reduced, total_reduction

    @classmethod
    def from_cost_matrix(cls, cost_matrix: list[list[float]]) -> Node:
        """
        Create a Node object from a given cost matrix.

        Parameters
        ----------
        cost_matrix
            The cost matrix representing the distances between cities.

        Returns
        -------
        Node
            A new Node object initialized with the reduced cost matrix.
        """
        _cost_matrix, _cost = cls.compute_reduced_matrix(matrix=cost_matrix)
        return cls(
            level=0,
            index=0,
            path=[0],
            cost=_cost,
            cost_matrix=_cost_matrix,
        )

    @classmethod
    def from_parent(cls, parent: Node, index: int) -> Node:
        """
        Create a new Node object based on a parent node and a city index.

        Parameters
        ----------
        parent
            The parent node.
        index
            The index of the new city to be added to the path.

        Returns
        -------
        Node
            A new Node object with the updated path and cost.
        """
        matrix = [row[:] for row in parent.cost_matrix]
        n = len(matrix)
        matrix[parent.index] = [inf] * n
        for i in range(n):
            matrix[i][index] = inf
        matrix[index][0] = inf
        _cost_matrix, _cost = cls.compute_reduced_matrix(matrix=matrix)
        return cls(
            level=parent.level + 1,
            index=index,
            path=parent.path[:] + [index],
            cost=(
                parent.cost + _cost + parent.cost_matrix[parent.index][index]
            ),
            cost_matrix=_cost_matrix,
        )

    def __lt__(self: Node, other: Node):
        """
        Compare two Node objects based on their costs.

        Parameters
        ----------
        other
            The other Node object to compare with.

        Returns
        -------
        bool
            True if this Node's cost is less than the other Node's
            cost, False otherwise.
        """
        return self.cost < other.cost
