import random
import string

import discord
import pytest
import pytest_asyncio

from word_debt_bot import client, cogs, game


@pytest.fixture
def game_state(tmp_path) -> game.WordDebtGame:
    return game.WordDebtGame(tmp_path / "state.json")


@pytest.fixture
def player() -> game.WordDebtPlayer:
    user_id = str(random.randint(10**7, 10**8 - 1))
    user_name = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    return game.WordDebtPlayer(user_id, user_name)


@pytest.fixture
def game_commands_cog(game_state, tmp_path) -> cogs.GameCommands:
    intents = discord.Intents.default()
    intents.message_content = True

    # Dummy bot required as cog argument -- For bot access use bot fixture
    bot = client.WordDebtBot(command_prefix=".", intents=intents)

    return cogs.GameCommands(bot, game_state, tmp_path / "journal.ndjson")


@pytest_asyncio.fixture
async def bot(game_state, tmp_path) -> client.WordDebtBot:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = client.WordDebtBot(command_prefix=".", intents=intents)
    await bot.add_cog(cogs.GameCommands(bot, game_state, tmp_path / "journal.ndjson"))

    return bot
