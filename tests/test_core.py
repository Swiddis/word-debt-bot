from unittest.mock import AsyncMock
import discord

import pytest

import src.word_debt_bot.core as core

from .test_game import game
from callee import String, Regex


@pytest.fixture
def bot(game: core.WordDebtGame) -> core.WordDebtBot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = core.WordDebtBot(command_prefix='.', intents=intents)
    bot.game = game
    return bot


@pytest.mark.asyncio
async def test_ping_sends_response_no_game(bot: core.WordDebtBot):
    bot.game = None
    ctx = AsyncMock()

    await bot.ping(bot, ctx)

    ctx.send.assert_called_with(String() & Regex("I'm alive.*"))


@pytest.mark.asyncio
async def test_ping_sends_response(bot: core.WordDebtBot):
    ctx = AsyncMock()

    await bot.ping(bot, ctx)

    ctx.send.assert_called_with(String() & Regex("Pong.*"))
