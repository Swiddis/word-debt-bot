import pathlib
from unittest.mock import AsyncMock

import pytest
from callee import Regex, String

from word_debt_bot import cogs
from word_debt_bot import game as game_lib

from .fixtures import *


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
async def test_submit_words(
    game_commands_cog: cogs.GameCommands, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_commands_cog.game.register_player(player)

    await game_commands_cog.log(game_commands_cog, ctx, 1000, genre=None)

    ctx.send.assert_called_with(String() & Regex("Logged 1,000 words!.*"))


@pytest.mark.asyncio
async def test_request_leaderboard_no_register(game_commands_cog: cogs.GameCommands):
    ctx = AsyncMock()

    await game_commands_cog.leaderboard(game_commands_cog, ctx, "debt", 1)

    ctx.send.assert_called_with(String() & Regex("No registered users.*"))


@pytest.mark.asyncio
async def test_buy_bonus_genre_sends_buy_message(
    game_commands_cog: cogs.GameCommands, player: game_lib.WordDebtPlayer
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_commands_cog.game.register_player(player)
    game_commands_cog.shop_path = pathlib.Path("tests/test_data/shop.yaml")
    await game_commands_cog.log(game_commands_cog, ctx, 100000, None)
    await game_commands_cog.buy(
        game_commands_cog, ctx, "bonus genre", args="historical fiction"
    )

    ctx.send.assert_called_with("New bonus genre active: historical fiction")


@pytest.mark.asyncio
async def test_buy_bonus_genre_subtracts_correct_price(
    game_commands_cog: cogs.GameCommands,
    player: game_lib.WordDebtPlayer,
    game_state: game_lib.WordDebtGame,
):
    ctx = AsyncMock()
    ctx.author.id = player.user_id
    game_commands_cog.game.register_player(player)
    game_commands_cog.shop_path = pathlib.Path("tests/test_data/shop.yaml")
    await game_commands_cog.log(game_commands_cog, ctx, 300000, None)
    await game_commands_cog.buy(
        game_commands_cog, ctx, "bonus genre", args="historical fiction"
    )

    assert game_state._state.users[player.user_id].cranes == 400


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


@pytest.mark.asyncio
async def test_shop(game_commands_cog: cogs.GameCommands):
    ctx = AsyncMock()
    game_commands_cog.shop_path = pathlib.Path("tests/test_data/shop.yaml")
    await game_commands_cog.shop(game_commands_cog, ctx)
    ctx.send.assert_called_with(
        '- "bonus genre": For the next week, words logged with this genre are worth twice as many cranes. Costs 200 cranes.\n- "debt increase": Increase another player\'s debt by 10000. Costs 100 cranes.\n'
    )
