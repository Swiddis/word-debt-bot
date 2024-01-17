from unittest.mock import AsyncMock

import pytest

import src.word_debt_bot.core as core

from .test_game import game


@pytest.mark.asyncio
async def test_ping_sends_response():
    ctx = AsyncMock()
    await core.ping(ctx)
    ctx.send.assert_called()


@pytest.mark.asyncio
async def test_ping_sends_response_with_game(game):
    core.bot.game = game
    ctx = AsyncMock()
    await core.ping(ctx)
    ctx.send.assert_called_with("Pong! All systems normal.")
