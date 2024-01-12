import pathlib
import tempfile

from src.game import WordDebtGame


def test_game_initializes():
    state_file_path = tempfile.mkstemp(suffix=".json")
    game = WordDebtGame(pathlib.Path(state_file_path[1]))
    assert game._state == {}
