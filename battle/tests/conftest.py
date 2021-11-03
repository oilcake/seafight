import pytest

from ..game import Player, Game


@pytest.fixture
def dummy_player():
    name = 'Misha'
    player = Player(name)
    return player


@pytest.fixture
def dummy_game():
    return Game()
