from ..game import Player


def test_player_created(dummy_player):
    assert isinstance(dummy_player, Player) is True


def test_player_is_in_the_sea(dummy_player):
    assert isinstance(dummy_player.sea, list) is True
