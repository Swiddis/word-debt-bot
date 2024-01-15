import pathlib
import random
import string
import tempfile

import pytest

from src.word_debt_bot.game import WordDebtGame, WordDebtPlayer


@pytest.fixture
def game() -> WordDebtGame:
    state_file_path = tempfile.mkstemp(suffix=".json")
    return WordDebtGame(pathlib.Path(state_file_path[1]))


@pytest.fixture
def player() -> WordDebtPlayer:
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


def test_game_accepts_payment(game, player):
    game.register_player(player)
    game.add_debt(player.user_id, 10000)
    game.submit_words(player.user_id, 2500)
    updated = game._state[player.user_id]
    assert updated.word_debt == 7500
    assert updated.cranes == 4
    assert updated.crane_payment_rollover == 500


def test_game_handles_rollover(game, player):
    game.register_player(player)
    game.add_debt(player.user_id, 10000)
    game.submit_words(player.user_id, 1250)
    game.submit_words(player.user_id, 1250)
    updated = game._state[player.user_id]
    assert updated.word_debt == 7500
    assert updated.cranes == 4
    assert updated.crane_payment_rollover == 500


def test_game_handles_empty_debt(game, player):
    game.register_player(player)
    game.add_debt(player.user_id, 5000)
    game.submit_words(player.user_id, 10000)
    updated = game._state[player.user_id]
    assert updated.word_debt == 0
    assert updated.cranes == 20


def test_game_rejects_negative_payment(game, player):
    game.register_player(player)
    game.add_debt(player.user_id, 10000)
    with pytest.raises(ValueError):
        game.submit_words(player.user_id, -1000)


def test_game_rejects_negative_debt(game, player):
    game.register_player(player)
    with pytest.raises(ValueError):
        game.add_debt(player.user_id, -10000)
