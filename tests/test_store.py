from word_debt_bot import game

from .fixtures import *


def test_game_removes_spent_cranes(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    player.cranes = 50
    game_state.register_player(player)

    game_state.spend_cranes(player.user_id, 25)

    assert game_state._state.users[player.user_id].cranes == 25


def test_game_blocks_overspending(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    player.cranes = 50
    game_state.register_player(player)

    with pytest.raises(ValueError):
        game_state.spend_cranes(player.user_id, 100)


def test_game_blocks_negative_spending(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    player.cranes = 50
    game_state.register_player(player)

    with pytest.raises(ValueError):
        game_state.spend_cranes(player.user_id, -50)


def test_game_handles_bonus_genre(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    game_state.add_bonus_genre("fantasy")
    game_state.submit_words(player.user_id, 2000)
    assert game_state._state.users[player.user_id].cranes == 8
