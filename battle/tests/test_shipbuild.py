import pytest

from ..game import Ship
from ..shipbuild import Tile
from ..shipbuild import default_sea, tile_is_valid, tile_is_empty, go_random
from ..shipbuild import enough_room_around
from ..shipbuild import BOARDHEIGHT, BOARDWIDTH


def test_default_grid():
    sea = default_sea(Tile)
    assert isinstance(sea, list) is True
    assert sea[0][0] is not sea[0][1]


def test_default_Tile():
    tile = Tile()
    assert tile.state == 'default'
    assert tile.ship is None


@pytest.mark.parametrize('y, x, result', [
                            (5, 7, True),
                            (3, 3, True),
                            (3, -1, False),
                            (-1, 5, False),
                            (-1, 11, False)
                            ])
def test_tile_is_valid(y, x, result):
    assert tile_is_valid(y, x) is result


def test_tile_is_empty():
    sea = default_sea(Tile)
    y, x = go_random()
    assert tile_is_empty(sea[y][x]) is True


def test_tile_is_not_empty():
    sea = default_sea(Tile)
    y, x = go_random()
    ship_properties = (1, 'straight')
    sea[y][x].ship = Ship(ship_properties)
    assert tile_is_empty(sea[y][x]) is False


@pytest.mark.parametrize('y, x, result', [
                            (0, 0, False),
                            (4, 4, True)
                            ])
def test_enough_room_around(y, x, result):
    sea = default_sea(Tile)
    assert enough_room_around(sea, y, x) is result


@pytest.mark.parametrize('y, x, result', [
                            (1, 1, False),
                            (BOARDHEIGHT - 2, BOARDWIDTH - 2, False),
                            # (8, 9, True),
                            ])
def test_not_enough_room_around(y, x, result):
    sea = default_sea(Tile)
    ship_properties = (1, 'straight')
    sea[0][0].ship = Ship(ship_properties)
    sea[BOARDHEIGHT - 1][BOARDWIDTH - 1].ship = Ship(ship_properties)
    assert enough_room_around(sea, y, x) is result
