from unittest.mock import AsyncMock

import pytest

import src.core as core


@pytest.mark.asyncio
async def test_ping():
    ctx = AsyncMock()
    await core.ping(ctx)
    ctx.send.assert_called()
