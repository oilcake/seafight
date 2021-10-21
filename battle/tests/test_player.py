from ..game import Player
from ..shipbuild import default_grid, Tile


def test_player_created(dummy_player):
    assert isinstance(dummy_player, Player) is True


def test_player_is_in_the_sea(dummy_player):
    assert isinstance(dummy_player.sea, list) is True


def test_reset_sea(dummy_player):
    empty_grid = default_grid(Tile)
    dummy_player.reset_sea()
    assert empty_grid == dummy_player.sea
