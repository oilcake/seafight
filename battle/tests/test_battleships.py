from ..battleships import default_grid


def test_default_grid():
    grid = default_grid(0)
    assert isinstance(grid, list) is True
