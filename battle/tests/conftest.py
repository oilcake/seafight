import pytest

from ..game import Player, Game


@pytest.fixture
def dummy_player():
    return Player()


@pytest.fixture
def dummy_game():
    return Game()
