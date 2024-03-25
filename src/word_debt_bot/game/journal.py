import collections
import json
import pathlib
from datetime import datetime

import ndjson


class WordDebtJournal:
    def __init__(self, journal_path: pathlib.Path):
        self.journal_path = journal_path

    def scan(self):
        with open(self.journal_path, "r") as journal_file:
            journal = ndjson.load(journal_file)
        return journal

    def append(self, entry: dict):
        if "command" not in entry:
            raise ValueError("entry must have a command")
        entry["time"] = datetime.now().timestamp()
        with open(self.journal_path, "a") as logfile:
            logfile.write(json.dumps(entry) + "\n")

    def accumulate_read(self, player: str | None) -> dict[str, int]:
        journal = self.scan()
        counts = collections.defaultdict(lambda: 0)

        for entry in filter(
            lambda e: e["command"] == "log" and (player is None or e["user"] == player),
            journal,
        ):
            counts[entry["user"]] += entry["words"]

        return dict(counts)
