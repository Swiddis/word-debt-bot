import pytest

from .fixtures import *
import src.word_debt_bot.core as core

def test_game_initializes(game: core.WordDebtGame):
    assert game._state == {}


def test_game_registers_player(game: core.WordDebtGame, player: core.WordDebtPlayer):
    game.register_player(player)
    assert game._state[player.user_id] == player


def test_game_refuses_duplicate_registration(game: core.WordDebtGame, player):
    game.register_player(player)
    with pytest.raises(ValueError):
        game.register_player(player)


def test_game_accepts_payment(game: core.WordDebtGame, player: core.WordDebtPlayer):
    game.register_player(player)
    game.add_debt(player.user_id, 10000)
    game.submit_words(player.user_id, 2500)
    updated = game._state[player.user_id]
    assert updated.word_debt == 7500
    assert updated.cranes == 4
    assert updated.crane_payment_rollover == 500


def test_game_handles_rollover(game: core.WordDebtGame, player: core.WordDebtPlayer):
    game.register_player(player)
    game.add_debt(player.user_id, 10000)
    game.submit_words(player.user_id, 1250)
    game.submit_words(player.user_id, 1250)
    updated = game._state[player.user_id]
    assert updated.word_debt == 7500
    assert updated.cranes == 4
    assert updated.crane_payment_rollover == 500


def test_game_handles_empty_debt(game: core.WordDebtGame, player: core.WordDebtPlayer):
    game.register_player(player)
    game.add_debt(player.user_id, 5000)
    game.submit_words(player.user_id, 10000)
    updated = game._state[player.user_id]
    assert updated.word_debt == 0
    assert updated.cranes == 20


def test_game_rejects_negative_payment(game: core.WordDebtGame, player: core.WordDebtPlayer):
    game.register_player(player)
    game.add_debt(player.user_id, 10000)
    with pytest.raises(ValueError):
        game.submit_words(player.user_id, -1000)


def test_game_rejects_negative_debt(game: core.WordDebtGame, player: core.WordDebtPlayer):
    game.register_player(player)
    with pytest.raises(ValueError):
        game.add_debt(player.user_id, -10000)
