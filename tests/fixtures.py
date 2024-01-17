import os
import pathlib
import random
import string
import tempfile

import discord
import pytest

from word_debt_bot import core
from word_debt_bot.game.core import WordDebtGame
from word_debt_bot.game.player import WordDebtPlayer


@pytest.fixture
def game(tmp_path: pathlib.Path) -> WordDebtGame:
    return WordDebtGame(tmp_path / "state.json")


@pytest.fixture
def player() -> WordDebtPlayer:
    user_id = str(random.randint(10**7, 10**8 - 1))
    user_name = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    return WordDebtPlayer(user_id, user_name)


@pytest.fixture
def bot(game: core.WordDebtGame, tmp_path: pathlib.Path) -> core.WordDebtBot:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = core.WordDebtBot(command_prefix=".", intents=intents)
    bot.game = game
    bot.journal_path = tmp_path / "journal.ndjson"

    return bot
