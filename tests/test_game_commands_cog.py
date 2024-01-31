import copy
import re
from unittest.mock import AsyncMock

import pytest
from callee import Regex, String
from discord.ext import commands

from word_debt_bot import cogs
from word_debt_bot import game as game_lib

from .fixtures import *


@pytest.mark.asyncio
async def test_ping_sends_response_no_game(game_commands_cog: cogs.GameCommands):
    game_commands_cog.game = None
    ctx = AsyncMock()

    await game_commands_cog.ping(game_commands_cog, ctx)

    ctx.send.assert_called_with(String() & Regex("I'm alive.*"))


@pytest.mark.asyncio
async def test_ping_sends_response(game_commands_cog: cogs.GameCommands):
    ctx = AsyncMock()

    await game_commands_cog.ping(game_commands_cog, ctx)

    ctx.send.assert_called_with(String() & Regex("Pong.*"))


@pytest.mark.asyncio
async def test_version(game_commands_cog: cogs.GameCommands):
    ctx = AsyncMock()

    await game_commands_cog.version(game_commands_cog, ctx)

    ctx.send.assert_called_with(String() & Regex("Version:.*"))


@pytest.mark.asyncio
async def test_registration(
    game_commands_cog: cogs.GameCommands, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    ctx.author.name = player.display_name

    await game_commands_cog.register(game_commands_cog, ctx)

    ctx.send.assert_called_with("Registered with 10,000 debt!")
    assert game_commands_cog.game._state.users[player.user_id].word_debt == 10000


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

    ctx.send.assert_called_with("Already registered!")


@pytest.mark.asyncio
async def test_registration_no_game(
    bot: client.WordDebtBot, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    ctx.author.name = player.display_name
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")
    game_cmds_cog.game = None
    cmd_err_cog.game = None

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.register.invoke(ctx)

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with(String() & Regex("Game not loaded.*"))


@pytest.mark.asyncio
async def test_submit_words(
    game_commands_cog: cogs.GameCommands, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_commands_cog.game.register_player(player)

    await game_commands_cog.log(game_commands_cog, ctx, 1000, genre=None)

    ctx.send.assert_called_with(String() & Regex("Logged 1,000 words!.*"))


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
        await game_cmds_cog.log(ctx, words, genre=None)

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
        await game_cmds_cog.log(ctx, words, None)

    game_cmds_cog.log_test_10 = log_test_10

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.log_test_10.invoke(ctx)

    ctx.command.name = "log"

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with(String() & Regex("Not registered!.*"))


@pytest.mark.asyncio
async def test_submit_words_no_game(
    bot: client.WordDebtBot, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")
    game_cmds_cog.game = None
    cmd_err_cog.game = None

    @bot.command()
    async def log_test_10(ctx, words=10):
        await game_cmds_cog.log(ctx, words, None)

    game_cmds_cog.log_test_10 = log_test_10

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.log_test_10.invoke(ctx)

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with(String() & Regex("Game not loaded.*"))


@pytest.mark.asyncio
async def test_request_leaderboard_no_register(game_commands_cog: cogs.GameCommands):
    ctx = AsyncMock()

    await game_commands_cog.leaderboard(game_commands_cog, ctx, "debt", 1)

    ctx.send.assert_called_with(String() & Regex("No registered users.*"))


@pytest.mark.asyncio
async def test_request_leaderboard_no_game(bot: client.WordDebtBot):
    ctx = AsyncMock()
    game_cmds_cog = bot.get_cog("Core Gameplay")
    cmd_err_cog = bot.get_cog("Command Error Handler")
    game_cmds_cog.game = None
    cmd_err_cog.game = None

    with pytest.raises(commands.CommandInvokeError) as err:
        await game_cmds_cog.leaderboard.invoke(ctx)

    await cmd_err_cog.on_command_error(ctx, err.value)

    ctx.send.assert_called_with(String() & Regex("Game not loaded.*"))


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
async def test_buy_bonus_genre(
    game_commands_cog: cogs.GameCommands, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_commands_cog.game.register_player(player)
    await game_commands_cog.log(game_commands_cog, ctx, 100000, None)
    await game_commands_cog.buy(
        game_commands_cog, ctx, "bonus genre", args="historical fiction"
    )

    ctx.send.assert_called_with("New bonus genre active: historical fiction")


@pytest.mark.asyncio
async def test_info(
    game_commands_cog: cogs.GameCommands, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    player.word_debt = 250000
    game_commands_cog.game.register_player(player)
    await game_commands_cog.log(game_commands_cog, ctx, 100000, None)
    await game_commands_cog.info(game_commands_cog, ctx)

    # Multiline flag is broken, TODO fix and use regular .*
    ctx.send.assert_called_with(String() & Regex(r"(.*\n)*Debt: 150,000(\n.*)*"))
    ctx.send.assert_called_with(String() & Regex(r"(.*\n)*Cranes: 200(\n.*)*"))
