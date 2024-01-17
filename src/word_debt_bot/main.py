import logging
import os
import pathlib

import discord

from word_debt_bot.core import bot
from word_debt_bot.game import WordDebtGame


def get_token(token_path):
    if not os.path.exists(token_path):
        raise FileNotFoundError(
            f"Missing TOKEN file. The bot requires a Discord bot token at `{token_path}` to run."
        )
    with open(token_path, "r") as token_file:
        return token_file.read()


if __name__ == "__main__":
    # Config
    intents = discord.Intents.default()
    intents.message_content = True
    handler = logging.FileHandler(
        filename=pathlib.Path("data/discord.log"), encoding="utf-8", mode="a"
    )

    # Loading data
    game = WordDebtGame(pathlib.Path("data/prod.json"))
    token = get_token(pathlib.Path("data/TOKEN"))

    # Starting the bot
    bot.game = game
    bot.run(token, log_handler=handler, log_level=logging.INFO)
