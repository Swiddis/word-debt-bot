import copy
from unittest.mock import AsyncMock

import pytest
from callee import Regex, String
from discord.ext import commands

from word_debt_bot import game as game_lib

from .fixtures import *


@pytest.mark.asyncio
async def test_registration_valueerror(
    bot: client.WordDebtBot, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    ctx.author.name = player.display_name
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")

    await game_cmds_cog.register.invoke(ctx)
    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.register.invoke(ctx)

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with("Error: already registered!")


@pytest.mark.asyncio
async def test_submit_words_with_error(
    bot: client.WordDebtBot, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")
    game_cmds_cog.game.register_player(player)

    @bot.command()
    async def log_test_m1k(ctx, words=-1000):
        await game_cmds_cog.log(ctx, words, unit="words", genre=None)

    game_cmds_cog.log_test_m1k = log_test_m1k

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.log_test_m1k.invoke(ctx)

    ctx.command.name = "log"

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with(String() & Regex("Error:.*"))


@pytest.mark.asyncio
async def test_submit_words_with_no_register(
    bot: client.WordDebtBot, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")

    @bot.command()
    async def log_test_10(ctx, words=10):
        await game_cmds_cog.log(ctx, words, "words", None)

    game_cmds_cog.log_test_10 = log_test_10

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.log_test_10.invoke(ctx)

    ctx.command.name = "log"

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with(String() & Regex("Not registered!.*"))


@pytest.mark.asyncio
async def test_buy_with_value_error(
    bot: client.WordDebtBot, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    target_player = copy.copy(player)
    target_player.user_id = "12345"
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")
    game_cmds_cog.game.register_player(player)
    game_cmds_cog.game.register_player(target_player)

    @bot.command()
    async def buy_test_err(ctx):
        await game_cmds_cog.buy(
            ctx, "debt increase", args=f"<@{target_player.user_id}>"
        )

    game_cmds_cog.buy_test_err = buy_test_err

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.buy_test_err.invoke(ctx)

    ctx.command.name = "buy"

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with("Error: insufficient cranes")


@pytest.mark.asyncio
async def test_missing_args(bot):
    await dpytest.message(".register")
    await dpytest.empty_queue()

    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message(".log")

    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Not all required inputs were given")
    )


@pytest.mark.asyncio
async def test_invalid_args(bot):
    await dpytest.message(".register")
    await dpytest.empty_queue()

    with pytest.raises(commands.BadArgument):
        await dpytest.message(".log fiction")

    assert dpytest.verify().message().contains().content("Invalid inputs were supplied")


@pytest.mark.asyncio
async def test_invalid_command(bot):
    with pytest.raises(commands.CommandNotFound):
        await dpytest.message(".nonexistent")
    assert dpytest.verify().message().nothing()
