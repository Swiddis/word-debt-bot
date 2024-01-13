import pathlib
import tempfile

import pytest

from src.game import WordDebtGame, WordDebtPlayer


def test_game_initializes():
    state_file_path = tempfile.mkstemp(suffix=".json")
    game = WordDebtGame(pathlib.Path(state_file_path[1]))
    assert game._state == {}


def test_game_registers_player():
    state_file_path = tempfile.mkstemp(suffix=".json")
    game = WordDebtGame(pathlib.Path(state_file_path[1]))
    player = WordDebtPlayer("123", "Test Player", 100000)
    game.register_player(player)
    print(game._state)
    assert game._state[player.user_id] == player


def test_game_refuses_duplicate_registration():
    state_file_path = tempfile.mkstemp(suffix=".json")
    game = WordDebtGame(pathlib.Path(state_file_path[1]))
    player = WordDebtPlayer("123", "Test Player", 100000)
    game.register_player(player)
    with pytest.raises(ValueError):
        game.register_player(player)
