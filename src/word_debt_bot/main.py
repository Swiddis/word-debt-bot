import asyncio
import logging
import os
from pathlib import Path

import discord

import word_debt_bot.cogs as cogs
from word_debt_bot.client import WordDebtBot
from word_debt_bot.game import WordDebtGame


def get_token(token_path):
    if not os.path.exists(token_path):
        raise FileNotFoundError(
            f"Missing TOKEN file. The bot requires a Discord bot token at `{token_path}` to run."
        )
    with open(token_path, "r") as token_file:
        return token_file.read()


def make_bot(intents=None):
    if intents is None:
        intents = discord.Intents.default()
        intents.message_content = True
    return WordDebtBot(".", intents=intents)


def add_cogs(bot: WordDebtBot, game: WordDebtGame):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(bot.add_cog(cogs.GameCommands(bot, game))),
        loop.create_task(bot.add_cog(cogs.CmdErrHandler(bot, game))),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


def main(log_file: Path, state_file: Path, token_file: Path):
    # Set up bot
    game = WordDebtGame(state_file)
    bot = make_bot()
    add_cogs(bot, game)

    # Startup
    token = get_token(token_file)
    handler = logging.FileHandler(filename=log_file, encoding="utf-8", mode="a")
    bot.run(token, log_handler=handler, log_level=logging.INFO)


if __name__ == "__main__":
    main(Path("data/discord.log"), Path("data/prod.json"), Path("data/TOKEN"))
