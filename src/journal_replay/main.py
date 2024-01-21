import json
import pathlib
import tempfile
from pprint import pprint

from word_debt_bot.game import WordDebtGame
from word_debt_bot.game.player import WordDebtPlayer


def read_journal_file(journal_file: pathlib.Path):
    with open(journal_file, "r") as journal:
        return [json.loads(line) for line in journal]


def get_journal(
    base_journal_path: pathlib.Path, edits_journal_path: pathlib.Path | None = None
):
    base_journal = read_journal_file(base_journal_path)
    edits_journal = read_journal_file(edits_journal_path) if edits_journal_path else []
    return sorted(base_journal + edits_journal, key=lambda x: x["time"])


def apply_entry(entry, game):
    if entry["command"] == "register":
        if entry["user"] not in game._state:
            # TODO handle display names
            # Probably need to pull from existing state to get config options
            game.register_player(
                WordDebtPlayer(
                    user_id=entry["user"], display_name="unknown", word_debt=10000
                )
            )
    if entry["command"] == "log":
        game.submit_words(entry["user"], entry["words"])


def replay_journal(journal: list[dict]) -> WordDebtGame:
    temp_state = tempfile.mkstemp()
    game = WordDebtGame(pathlib.Path(temp_state[1]))

    for entry in journal:
        apply_entry(entry, game)

    return game


if __name__ == "__main__":
    journal = get_journal(
        pathlib.Path("data/journal.ndjson"), pathlib.Path("data/edits.ndjson")
    )
    game = replay_journal(journal)
    pprint(game._state)
