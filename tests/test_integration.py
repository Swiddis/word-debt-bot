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


@pytest.mark.asyncio
async def test_bonus_genre_gives_extra_cranes(bot):
    await dpytest.message(".register")
    await dpytest.message(".log 100000")
    await dpytest.empty_queue()

    await dpytest.message('.buy "bonus genre" sci-fi')
    await dpytest.message(".log 10000 sci-fi")
    await dpytest.message(".info")

    assert dpytest.verify().message().content("New bonus genre active: sci-fi")
    assert dpytest.verify().message().contains().content("Logged 10,000")
    assert dpytest.verify().message().contains().content("Cranes: 40")


@pytest.mark.asyncio
async def test_bonus_genre_no_genre_specified(bot):
    await dpytest.message(".register")
    await dpytest.message(".log 100000")
    await dpytest.empty_queue()

    await dpytest.message('.buy "bonus genre"')

    assert dpytest.verify().message().content("Must specify a genre!")
