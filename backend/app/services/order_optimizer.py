"""Visit order heuristics: nearest-neighbor + 2-opt."""

from typing import List, Optional, Sequence


def _matrix_minutes(matrix: Sequence[Sequence[Optional[float]]], i: int, j: int) -> float:
    val = matrix[i][j]
    if val is None:
        return 999999.0
    return val / 60.0


def nearest_neighbor_order(
    matrix: Sequence[Sequence[Optional[float]]],
    start_index: int = 0,
    poi_indices: Optional[List[int]] = None,
) -> List[int]:
    """
    Returns ordered POI indices (into matrix, excluding start).
    matrix[0] is start; POIs are indices 1..n-1 unless poi_indices provided.
    """
    if poi_indices is None:
        poi_indices = list(range(1, len(matrix)))

    if not poi_indices:
        return []

    unvisited = set(poi_indices)
    order: List[int] = []
    current = start_index

    while unvisited:
        nearest = min(unvisited, key=lambda j: _matrix_minutes(matrix, current, j))
        order.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return order


def route_cost(
    matrix: Sequence[Sequence[Optional[float]]],
    order: List[int],
    start_index: int = 0,
) -> float:
    if not order:
        return 0.0
    total = _matrix_minutes(matrix, start_index, order[0])
    for i in range(len(order) - 1):
        total += _matrix_minutes(matrix, order[i], order[i + 1])
    return total


def two_opt_improve(
    matrix: Sequence[Sequence[Optional[float]]],
    order: List[int],
    start_index: int = 0,
    max_iterations: int = 100,
) -> List[int]:
    if len(order) < 3:
        return order

    best = order[:]
    best_cost = route_cost(matrix, best, start_index)
    improved = True
    iterations = 0

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        for i in range(len(best) - 1):
            for j in range(i + 2, len(best)):
                candidate = best[:i] + best[i:j][::-1] + best[j:]
                cost = route_cost(matrix, candidate, start_index)
                if cost < best_cost - 1e-6:
                    best = candidate
                    best_cost = cost
                    improved = True
    return best


def optimize_visit_order(
    matrix: Sequence[Sequence[Optional[float]]],
    start_index: int = 0,
    use_two_opt: bool = True,
) -> List[int]:
    order = nearest_neighbor_order(matrix, start_index=start_index)
    if use_two_opt:
        order = two_opt_improve(matrix, order, start_index=start_index)
    return order
