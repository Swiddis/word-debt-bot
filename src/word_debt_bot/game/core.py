import json
import os.path
import pathlib
from dataclasses import asdict

from .player import WordDebtPlayer


class WordDebtGame:
    def __init__(self, state_file_path: pathlib.Path):
        self.path = state_file_path
        self.init_state()

    def init_state(self):
        # If the file is nonexistent or empty, start a new game
        if not self.path.is_file() or os.path.getsize(self.path) == 0:
            self._state = {}
        # Check that state is readable (provided file is actually json)
        self._state

    @property
    def _state(self):
        with open(self.path, "r") as state_file:
            raw_dict = json.load(state_file)
        return {key: WordDebtPlayer(**value) for key, value in raw_dict.items()}

    @_state.setter
    def _state(self, new_state: dict[str, WordDebtPlayer]):
        serialized = {key: asdict(value) for key, value in new_state.items()}
        with open(self.path, "w") as state_file:
            json.dump(serialized, state_file)

    def register_player(self, player: WordDebtPlayer):
        state = self._state
        if player.user_id in state:
            raise ValueError(f"Player with id {player.user_id} already exists")
        state[player.user_id] = player
        self._state = state

    def submit_words(self, player_id: str, amount: int) -> int:
        if amount <= 0:
            raise ValueError(f"amount must be positive")
        state = self._state
        player = state[player_id]
        player.word_debt = max(player.word_debt - amount, 0)
        player.crane_payment_rollover += amount
        player.cranes += 2 * (player.crane_payment_rollover // 1000)
        player.crane_payment_rollover %= 1000
        self._state = state
        return player.word_debt

    def add_debt(self, player_id: str, amount: int):
        if amount <= 0:
            raise ValueError(f"amount must be positive")
        state = self._state
        state[player_id].word_debt += amount
        self._state = state

    def create_leaderboard(self, sort_by: str, lb_len: int):
        if sort_by not in ["debt", "cranes"]:
            raise ValueError("ordering is done by 'debt' or 'cranes'")
        if lb_len < 1:
            raise ValueError("requested leaderboard length must be 1 or greater")
        # Make a sort key and sort users
        if sort_by == "debt":
            key = lambda u: u[1].word_debt
        elif sort_by == "cranes":
            key = lambda u: u[1].cranes
        users = sorted(self._state.items(), key=key, reverse=True)

        # Produce leaderboard string to return
        lb = ""
        i = 1
        for u in users:
            lb += f"{i}. {u[1].display_name} - {u[1].word_debt:,} debt - {u[1].cranes:,} cranes\n"
            i += 1
            if i > lb_len:
                break
        return lb
