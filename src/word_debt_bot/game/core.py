import json
import math
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

    def get_leaderboard_page(self, sort_by: str, req_pg: int):
        sort_by = sort_by.lower()
        if sort_by not in ["debt", "cranes"]:
            raise ValueError("ordering is done by 'debt' or 'cranes'")
        if req_pg < 1:
            raise ValueError("requested leaderboard page must be 1 or greater")
        # Make a sort key and sort users
        if sort_by == "debt":
            key = lambda u: u.word_debt
        elif sort_by == "cranes":
            key = lambda u: u.cranes
        users = sorted(self._state.values(), key=key, reverse=True)
        users = list(enumerate(users, start=1))
        # Produce leaderboard string to return
        pg = ""
        pg_strt = (req_pg - 1) * 10
        if pg_strt > len(users):
            return f"The leaderboard is not that long! Last page = {math.ceil(len(users)/10)}"
        pg_end = pg_strt + 10
        if pg_end > len(users):
            pg_end = len(users)
        for i, u in users[pg_strt:pg_end]:
            entry = (
                f"{i}. {u.display_name} - {u.word_debt:,} debt - {u.cranes:,} cranes\n"
            )
            if len(pg + entry) > 2000:
                break
            pg += entry
        return pg
