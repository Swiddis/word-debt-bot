import random
import string

import discord.ext.test as dpytest
import pytest
import pytest_asyncio

from word_debt_bot import client, cogs, game, main


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
    bot = main.make_bot()
    return cogs.GameCommands(bot, game_state, tmp_path / "journal.ndjson")


@pytest_asyncio.fixture
async def bot(game_state, tmp_path) -> client.WordDebtBot:
    bot = main.make_bot()
    await bot._async_setup_hook()
    await bot.add_cog(cogs.GameCommands(bot, game_state, tmp_path / "journal.ndjson"))
    dpytest.configure(bot)

    yield bot

    await dpytest.empty_queue()
