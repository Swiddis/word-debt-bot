import json
import os.path
import pathlib


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
            return json.load(state_file)

    @_state.setter
    def _state(self, new_state: dict[int, dict]):
        with open(self.path, "w") as state_file:
            json.dump(new_state, state_file)
