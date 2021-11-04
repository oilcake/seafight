from ..game import Game
from seafight.views import stamp


def test_game_is_created(dummy_game):
    assert isinstance(dummy_game, Game) is True


def test_game_is_idle(dummy_game):
    assert dummy_game.state == 'idle'


def test_player_is_added(dummy_game):
    client = 'Pasha'
    game = dummy_game
    player_added = game.add_player(client, stamp(client))
    assert player_added == 'accepted'
    assert len(game.players) == 1
    assert game.state == 'waiting_for_enemy'


def test_two_players_are_added(dummy_game):
    clients = ['Pasha', 'Gosha']
    game = dummy_game
    for client in clients:
        game.add_player(client, stamp(client))
    assert len(game.players) == 2
    assert game.state == 'in_progress'


def test_third_player_is_not_added(dummy_game):
    clients = ['Pasha', 'Gosha']
    game = dummy_game
    for client in clients:
        game.add_player(client, stamp(client))
    one_more_client = game.add_player('Henry', stamp('Henry'))
    assert one_more_client == 'refused'
    assert len(game.players) == 2
    assert game.state == 'in_progress'


def test_reset_game(dummy_game):
    game = dummy_game
    game.reset()
    assert len(game.players) == 0
    assert game.state == 'idle'
