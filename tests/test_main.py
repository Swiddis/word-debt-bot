from pathlib import Path

import pytest

import word_debt_bot.main as main
from word_debt_bot.game.core import WordDebtGame

from .fixtures import *


def test_token_read(tmp_path: Path):
    with open(tmp_path / "TOKEN", "w") as token_file:
        token_file.write("sample_token")

    token = main.get_token(tmp_path / "TOKEN")

    assert token == "sample_token"


def test_token_read_missing_token(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="Missing TOKEN file"):
        main.get_token(tmp_path / "TOKEN")


def test_add_cogs(game_state: WordDebtGame):
    bot = main.make_bot()
    main.add_cogs(bot, game_state)
    assert bot.get_cog("Core Gameplay Module") is not None
