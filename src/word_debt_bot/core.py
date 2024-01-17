import importlib.metadata
import json
import subprocess
from datetime import datetime

import discord
from discord.ext import commands

from .game import WordDebtPlayer

_intents = discord.Intents.default()
_intents.message_content = True
bot = commands.Bot(".", intents=_intents)


def journal(entry: dict) -> None:
    entry["time"] = datetime.now().timestamp()
    with open("data/journal.ndjson", "a") as logfile:
        logfile.write(json.dumps(entry) + "\n")


@bot.command()
async def ping(ctx):
    if hasattr(bot, "game"):
        await ctx.send("Pong! All systems normal.")
    else:
        await ctx.send("I'm alive, but I'm not sure where Toast hid the game state...")


@bot.command()
async def version(ctx):
    version = importlib.metadata.version("word_debt_bot")
    commit = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], encoding="utf-8"
    )
    await ctx.send(f"Version: {version}\nCommit: {commit}")


@bot.command()
async def register(ctx):
    if not hasattr(bot, "game"):
        await ctx.send("Game not loaded. (Yell at Toast!)")
        return
    player = WordDebtPlayer(str(ctx.author.id), ctx.author.name, 10_000)
    try:
        bot.game.register_player(player)
        journal({"command": "register", "user": str(ctx.author.id)})
        await ctx.send("Registered with 10,000 debt!")
    except ValueError:
        await ctx.send("Already registered!")


@bot.command()
async def log(ctx, words: int):
    if not hasattr(bot, "game"):
        await ctx.send("Game not loaded. (Yell at Toast!)")
        return
    try:
        new_debt = bot.game.submit_words(str(ctx.author.id), words)
        journal({"command": "log", "words": words, "user": str(ctx.author.id)})
        await ctx.send(f"Logged {words:,} words! New debt: {new_debt:,}")
    except KeyError as _err:
        await ctx.send("Not registered! `.register`")
    except ValueError as err:
        await ctx.send(f"Error: {str(err)}")
