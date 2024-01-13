import pathlib
import random
import string
import tempfile

import pytest

from src.game import WordDebtGame, WordDebtPlayer


@pytest.fixture
def game():
    state_file_path = tempfile.mkstemp(suffix=".json")
    return WordDebtGame(pathlib.Path(state_file_path[1]))


@pytest.fixture
def player():
    user_id = str(random.randint(10**7, 10**8 - 1))
    user_name = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    return WordDebtPlayer(user_id, user_name)


def test_game_initializes(game):
    assert game._state == {}


def test_game_registers_player(game, player):
    game.register_player(player)
    assert game._state[player.user_id] == player


def test_game_refuses_duplicate_registration(game, player):
    game.register_player(player)
    with pytest.raises(ValueError):
        game.register_player(player)
