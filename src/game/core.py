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

    def submit_words(self, player_id: str, amount: int):
        if amount <= 0:
            raise ValueError(f"amount must be positive")
        state = self._state
        player = state[player_id]
        player.word_debt -= amount
        player.crane_payment_rollover += amount
        player.cranes += player.crane_payment_rollover // 1000
        player.crane_payment_rollover %= 1000
        self._state = state

    def add_debt(self, player_id: str, amount: int):
        if amount <= 0:
            raise ValueError(f"amount must be positive")
        state = self._state
        state[player_id].word_debt += amount
        self._state = state
