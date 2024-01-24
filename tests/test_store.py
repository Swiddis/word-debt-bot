from word_debt_bot import game

from .fixtures import *


def test_game_handles_bonus_genre(
    game_state: game.WordDebtGame, player: game.WordDebtPlayer
):
    game_state.register_player(player)
    game_state.add_bonus_genre("fantasy")
    game_state.submit_words(player.user_id, 2000)
    assert game_state._state.users[player.user_id].cranes == 8
