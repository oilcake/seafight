from ..game import Game
from seafight.views import stamp_client


def test_game_created(dummy_game):
    assert isinstance(dummy_game, Game) is True


def test_game_is_idle(dummy_game):
    assert dummy_game.state == 'idle'


def test_player_is_added(dummy_game):
    client_name = 'Pasha'
    game = dummy_game
    game.add_player(client_name, stamp_client(client_name))
    assert len(game.players) == 1
