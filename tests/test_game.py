import pytest

from word_debt_bot import game

from .fixtures import *


def test_game_initializes(game_state: game.WordDebtGame):
    assert game_state._state == {}


def test_game_registers_player(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    assert game_state._state[player.user_id] == player


def test_game_refuses_duplicate_registration(game_state: game.WordDebtGame, player):
    game_state.register_player(player)
    with pytest.raises(ValueError):
        game_state.register_player(player)


def test_game_accepts_payment(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    game_state.add_debt(player.user_id, 10000)
    game_state.submit_words(player.user_id, 2500)
    updated = game_state._state[player.user_id]
    assert updated.word_debt == 7500
    assert updated.cranes == 4
    assert updated.crane_payment_rollover == 500


def test_game_handles_rollover(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    game_state.add_debt(player.user_id, 10000)
    game_state.submit_words(player.user_id, 1250)
    game_state.submit_words(player.user_id, 1250)
    updated = game_state._state[player.user_id]
    assert updated.word_debt == 7500
    assert updated.cranes == 4
    assert updated.crane_payment_rollover == 500


def test_game_handles_empty_debt(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    game_state.add_debt(player.user_id, 5000)
    game_state.submit_words(player.user_id, 10000)
    updated = game_state._state[player.user_id]
    assert updated.word_debt == 0
    assert updated.cranes == 20


def test_game_rejects_negative_payment(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    game_state.add_debt(player.user_id, 10000)
    with pytest.raises(ValueError):
        game_state.submit_words(player.user_id, -1000)


def test_game_rejects_negative_debt(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    with pytest.raises(ValueError):
        game_state.add_debt(player.user_id, -10000)


def test_game_rejects_invalid_leaderboard_length(game_state: game.WordDebtGame):
    with pytest.raises(ValueError):
        game_state.create_leaderboard("debt", 0)


def test_game_rejects_invalid_leaderboard_sorting(game_state: game.WordDebtGame):
    with pytest.raises(ValueError):
        game_state.create_leaderboard("INVALID", 1)


def test_game_produces_valid_leaderboard(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    player.display_name = "test_name"
    player.word_debt = 10000
    player.cranes = 0
    game_state.register_player(player)
    assert (
        game_state.create_leaderboard("debt", 1)
        == f"1. {player.display_name} - {player.word_debt:,} debt - {player.cranes:,} cranes\n"
    )
