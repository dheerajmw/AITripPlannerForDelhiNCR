"""Order optimizer unit tests."""

from app.services.order_optimizer import nearest_neighbor_order, optimize_visit_order, route_cost


def _sample_matrix():
    # start + 3 POIs; symmetric minutes in matrix as seconds
    # indices: 0=start, 1=A, 2=B, 3=C
    return [
        [0, 600, 1200, 300],
        [600, 0, 600, 900],
        [1200, 600, 0, 600],
        [300, 900, 600, 0],
    ]


def test_nearest_neighbor_visits_all() -> None:
    order = nearest_neighbor_order(_sample_matrix(), start_index=0)
    assert len(order) == 3
    assert set(order) == {1, 2, 3}


def test_optimize_reduces_cost_vs_random() -> None:
    matrix = _sample_matrix()
    optimized = optimize_visit_order(matrix, start_index=0, use_two_opt=True)
    random_order = [1, 3, 2]
    assert route_cost(matrix, optimized, 0) <= route_cost(matrix, random_order, 0)
