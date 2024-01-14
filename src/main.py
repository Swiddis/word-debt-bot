import os
import pathlib

from game import WordDebtGame

TOKEN_PATH = pathlib.Path("data/TOKEN")
DB_PATH = pathlib.Path("data/prod.json")


def get_token():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(
            f"Missing TOKEN file. The bot requires a Discord bot token at `{TOKEN_PATH}` to run."
        )
    with open(TOKEN_PATH, "r") as token_file:
        return token_file.read()


if __name__ == "__main__":
    token = get_token()
    game = WordDebtGame(DB_PATH)
