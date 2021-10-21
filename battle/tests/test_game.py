from ..game import Game


def test_game_created(dummy_game):
    assert isinstance(dummy_game, Game) is True
