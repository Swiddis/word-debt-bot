import json
import math
import os.path
import pathlib
from dataclasses import asdict
from datetime import datetime, timedelta

from word_debt_bot.game.state import WordDebtState

from .player import WordDebtPlayer

CURRENT_SERIALIZATION_VERSION = 1


def do_state_migration(state: dict):
    if not state.get("version"):  # Implicit version 0: Users are entire state
        return {
            "version": 1,
            "users": state,
            "modifiers": [],
        }
    if state["version"] != 1:
        raise ValueError("Unknown state version -- Unable to initialize")
    return state


class WordDebtGame:
    def __init__(self, state_file_path: pathlib.Path):
        self.path = state_file_path
        self.init_state()
        self._prune_expired_modifiers()

    def init_state(self):
        # If the file is nonexistent or empty, start a new game
        if not self.path.is_file() or os.path.getsize(self.path) == 0:
            self._state = WordDebtState(version=1, users={}, modifiers=[])
        # Assert that state is readable
        self._state = self._state

    def _prune_expired_modifiers(self):
        state = self._state
        now = datetime.now().timestamp()
        state.modifiers = [mod for mod in state.modifiers if not mod["expires"] <= now]
        self._state = state

    @property
    def _state(self):
        with open(self.path, "r") as state_file:
            raw_dict = json.load(state_file)
        if "version" not in raw_dict:
            raw_dict = do_state_migration(raw_dict)
        if raw_dict["version"] == CURRENT_SERIALIZATION_VERSION:
            return WordDebtState(**raw_dict)
        else:
            raise ValueError("Invalid version")

    @_state.setter
    def _state(self, new_state: WordDebtState):
        with open(self.path, "w") as state_file:
            json.dump(asdict(new_state), state_file)

    def register_player(self, player: WordDebtPlayer):
        state = self._state
        if player.user_id in state.users:
            raise ValueError(f"already registered!")
        state.users[player.user_id] = player
        self._state = state

    def get_player(self, player_id: str, optional=True) -> WordDebtPlayer | None:
        if optional:  # Don't throw a KeyError if missing
            return self._state.users.get(player_id)
        else:
            return self._state.users[player_id]

    def get_player_by_display_name(
        self, display_name: str, optional=True
    ) -> WordDebtPlayer | None:
        for player in self._state.users.values():
            if player.display_name == display_name:
                return player
        if not optional:
            raise ValueError(f"no player with display name {display_name}")
        return None

    def submit_words(
        self, player_id: str, amount: int, genre: str | None = None
    ) -> int:
        if amount <= 0:
            raise ValueError(f"amount must be positive")
        state = self._state
        player = state.users[player_id]
        player.word_debt = max(player.word_debt - amount, 0)
        player.crane_payment_rollover += amount
        crane_payment_ratio = 2 if not self._has_active_bonus_genre(genre) else 4
        player.cranes += crane_payment_ratio * (player.crane_payment_rollover // 1000)
        player.crane_payment_rollover %= 1000
        self._state = state
        return player.word_debt

    def set_player_languages(self, player_id: str, languages: str):
        state = self._state
        state.users[player_id].languages = languages
        self._state = state

    def set_player_display_name(self, player_id: str, display_name: str):
        state = self._state
        state.users[player_id].display_name = display_name
        self._state = state

    def add_debt(self, player_id: str, amount: int):
        if amount <= 0:
            raise ValueError(f"amount must be positive")
        state = self._state
        state.users[player_id].word_debt += amount
        self._state = state

    def spend_cranes(self, player_id: str, amount: int):
        if amount <= 0:
            raise ValueError("amount must be positive")
        state = self._state
        user = state.users[player_id]
        if amount > user.cranes:
            raise ValueError("insufficient cranes")
        user.cranes -= amount
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
        users = sorted(self._state.users.values(), key=key, reverse=True)
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

    def add_bonus_genre(self, genre: str):
        state = self._state
        expiration = datetime.now() + timedelta(days=7)
        state.modifiers.append(
            {"type": "bonus_genre", "genre": genre, "expires": expiration.timestamp()}
        )
        self._state = state

    def _has_active_bonus_genre(self, genre: str | None):
        now = datetime.now()
        for item in self._state.modifiers:
            if (
                item["type"] == "bonus_genre"
                and item["expires"] > now.timestamp()
                and item["genre"] == genre
            ):
                return True
