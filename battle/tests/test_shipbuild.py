from ..shipbuild import default_sea, Tile


def test_default_grid():
    grid = default_sea(Tile)
    assert isinstance(grid, list) is True
    assert grid[0][0] is not grid[0][1]


def test_default_Tile():
    tile = Tile()
    assert tile.state == 'default'
