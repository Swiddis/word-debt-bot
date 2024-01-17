from unittest.mock import AsyncMock

import pytest

import src.word_debt_bot.core as core

from .fixtures import *
from callee import String, Regex


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
