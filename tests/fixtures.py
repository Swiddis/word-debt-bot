import random
import string
from typing import AsyncGenerator

import discord
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
    return cogs.GameCommands(
        bot, game_state, game.WordDebtJournal(tmp_path / "journal.ndjson")
    )


@pytest.fixture
def cmd_err_handler_cog(game_state) -> cogs.CmdErrHandler:
    bot = main.make_bot()
    return cogs.CmdErrHandler(bot, game_state)


@pytest_asyncio.fixture
async def bot(game_state, tmp_path) -> AsyncGenerator[client.WordDebtBot, None]:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = main.make_bot(intents)
    await bot._async_setup_hook()
    await bot.add_cog(
        cogs.GameCommands(
            bot, game_state, game.WordDebtJournal(tmp_path / "journal.ndjson")
        )
    )
    await bot.add_cog(cogs.CmdErrHandler(bot, game_state))
    dpytest.configure(bot)

    yield bot

    await dpytest.empty_queue()
