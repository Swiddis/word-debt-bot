import importlib.metadata
import json
import subprocess
from datetime import datetime

from discord.ext import commands

from word_debt_bot.game.core import WordDebtGame

from .game import WordDebtPlayer


class WordDebtBot(commands.Bot):
    game: WordDebtGame | None = None

    def journal(self, entry: dict) -> None:
        entry["time"] = datetime.now().timestamp()
        with open("data/journal.ndjson", "a") as logfile:
            logfile.write(json.dumps(entry) + "\n")


    @commands.command()
    async def ping(self, ctx):
        if self.game:
            await ctx.send("Pong! All systems normal.")
        else:
            await ctx.send("I'm alive, but I'm not sure where Toast hid the game state...")


    @commands.command()
    async def version(self, ctx):
        version = importlib.metadata.version("word_debt_bot")
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], encoding="utf-8"
        )
        await ctx.send(f"Version: {version}\nCommit: {commit}")


    @commands.command()
    async def register(self, ctx):
        if not self.game:
            await ctx.send("Game not loaded. (Yell at Toast!)")
            return
        player = WordDebtPlayer(str(ctx.author.id), ctx.author.name, 10_000)
        try:
            self.game.register_player(player)
            self.journal({"command": "register", "user": str(ctx.author.id)})
            await ctx.send("Registered with 10,000 debt!")
        except ValueError:
            await ctx.send("Already registered!")


    @commands.command()
    async def log(self, ctx, words: int):
        if not self.game:
            await ctx.send("Game not loaded. (Yell at Toast!)")
            return
        try:
            new_debt = self.game.submit_words(str(ctx.author.id), words)
            self.journal({"command": "log", "words": words, "user": str(ctx.author.id)})
            await ctx.send(f"Logged {words:,} words! New debt: {new_debt:,}")
        except KeyError as _err:
            await ctx.send("Not registered! `.register`")
        except ValueError as err:
            await ctx.send(f"Error: {str(err)}")
