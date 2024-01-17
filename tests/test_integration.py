import discord.ext.test as dpytest

from .fixtures import *


@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message(".ping")
    assert dpytest.verify().message().contains().content("Pong!")


@pytest.mark.asyncio
async def test_basic_usage(bot):
    await dpytest.message(".register")
    await dpytest.message(".log 1500")
    await dpytest.message(".log 1500")
    assert dpytest.verify().message().contains().content("Registered")
    assert dpytest.verify().message().contains().content("8,500")
    assert dpytest.verify().message().contains().content("7,000")
