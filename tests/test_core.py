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

@pytest.mark.asyncio
async def test_version(bot: core.WordDebtBot):
    ctx = AsyncMock()

    await bot.version(bot, ctx)

    ctx.send.assert_called_with(String() & Regex("Version:.*\nCommit:.*"))

@pytest.mark.asyncio
async def test_registration(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    ctx.author.name = player.display_name
    
    await bot.register(bot, ctx)

    ctx.send.assert_called_with("Registered with 10,000 debt!")
    assert bot.game._state[player.user_id].word_debt == 10000

@pytest.mark.asyncio
async def test_registration_valueerror(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    ctx.author.name = player.display_name
    
    await bot.register(bot, ctx)
    await bot.register(bot, ctx)

    ctx.send.assert_called_with("Already registered!")

@pytest.mark.asyncio
async def test_registration_no_game(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    ctx.author.name = player.display_name
    bot.game = None
    
    await bot.register(bot, ctx)

    ctx.send.assert_called_with(String() & Regex('Game not loaded.*'))

@pytest.mark.asyncio
async def test_submit_words(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    bot.game.register_player(player)
    
    await bot.log(bot, ctx, 1000)

    ctx.send.assert_called_with(String() & Regex('Logged 1,000 words!.*'))

@pytest.mark.asyncio
async def test_submit_words_with_error(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    bot.game.register_player(player)
    
    await bot.log(bot, ctx, -1000)

    ctx.send.assert_called_with(String() & Regex('Error:.*'))

@pytest.mark.asyncio
async def test_submit_words_with_no_register(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id

    await bot.log(bot, ctx, 1000)

    ctx.send.assert_called_with(String() & Regex('Not registered!.*'))

@pytest.mark.asyncio
async def test_submit_words_no_game(bot: core.WordDebtBot, player: core.WordDebtPlayer):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    bot.game = None
    
    await bot.log(bot, ctx, 1000)

    ctx.send.assert_called_with(String() & Regex('Game not loaded.*'))
