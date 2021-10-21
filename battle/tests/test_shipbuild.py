from ..shipbuild import default_grid, Tile


def test_default_grid():
    grid = default_grid(Tile)
    assert isinstance(grid, list) is True
    assert grid[0][0] is not grid[0][1]


def test_default_Tile():
    tile = Tile()
    assert tile.state == 'default'
