import json
import pathlib
from pprint import pprint


def read_journal_file(journal_file: pathlib.Path):
    with open(journal_file, "r") as journal:
        return [json.loads(line) for line in journal]


def get_journal(
    base_journal_path: pathlib.Path, edits_journal_path: pathlib.Path | None = None
):
    base_journal = read_journal_file(base_journal_path)
    edits_journal = read_journal_file(edits_journal_path) if edits_journal_path else []
    return sorted(base_journal + edits_journal, key=lambda x: x["time"])


if __name__ == "__main__":
    journal = get_journal(
        pathlib.Path("data/journal.ndjson"), pathlib.Path("data/edits.ndjson")
    )
    pprint(journal)
