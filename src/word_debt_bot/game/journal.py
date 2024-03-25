import pathlib

import ndjson


class WordDebtJournal:
    def __init__(self, journal_path: pathlib.Path):
        self.journal_path = journal_path

    def scan(self):
        with open(self.journal_path, "r") as journal_file:
            journal = ndjson.load(journal_file)
        return journal
