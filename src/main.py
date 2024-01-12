import pathlib

from game import WordDebtGame

if __name__ == "__main__":
    game = WordDebtGame(pathlib.Path("data/prod.json"))
