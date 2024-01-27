import importlib.metadata
import json
import pathlib
import re
import typing
from datetime import datetime

import discord.ext.commands as commands

import word_debt_bot.client as client
import word_debt_bot.game as game


class GameCommands(commands.Cog, name="Core Gameplay Module"):
    def __init__(
        self,
        bot: client.WordDebtBot,
        game: game.WordDebtGame,
        journal_path: pathlib.Path = pathlib.Path("data/journal.ndjson"),
    ):
        self.bot = bot
        self.game = game
        self.journal_path = journal_path

    def journal(self, entry: dict) -> None:
        entry["time"] = datetime.now().timestamp()
        with open(self.journal_path, "a") as logfile:
            logfile.write(json.dumps(entry) + "\n")

    @commands.command(name="ping")
    async def ping(self, ctx):
        if self.game:
            await ctx.send("Pong! All systems normal.")
        else:
            await ctx.send(
                "I'm alive, but I'm not sure where Toast hid the game state..."
            )

    @commands.command(name="version")
    async def version(self, ctx):
        version = importlib.metadata.version("word_debt_bot")
        await ctx.send(f"Version: {version}")

    @commands.command(name="register")
    async def register(self, ctx):
        player = game.WordDebtPlayer(str(ctx.author.id), ctx.author.name, 10_000)
        self.game.register_player(player)
        self.journal({"command": "register", "user": str(ctx.author.id)})
        await ctx.send("Registered with 10,000 debt!")

    @commands.command(name="info")
    async def info(self, ctx):
        if not self.game:
            await ctx.send("Game not loaded. (Yell at Toast!)")
            return
        try:
            player = self.game.get_player(str(ctx.author.id))
            await ctx.send(
                f"Info for {player.display_name}:\nDebt: {player.word_debt}\nCranes: {player.cranes}"
            )
        except KeyError:
            await ctx.send("Not registered! `.register`")

    @commands.command(name="log")
    async def log(self, ctx, words: int, genre: typing.Optional[str] = None):
        new_debt = self.game.submit_words(str(ctx.author.id), words)
        journal_entry = {
            "command": "log",
            "words": words,
            "user": str(ctx.author.id),
        }
        if genre:
            journal_entry["genre"] = genre
        self.journal(journal_entry)
        await ctx.send(f"Logged {words:,} words! New debt: {new_debt:,}")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx, sort_by: str = "debt", req_pg: int = 1):
        pg = self.game.get_leaderboard_page(sort_by, req_pg)
        if pg == "":
            await ctx.send("No registered users, a leaderboard could not be made!")
            return
        await ctx.send(pg)

    @commands.command(name="buy")
    async def buy(self, ctx, item: str, *, args):
        match item.lower().strip():
            case "bonus genre":
                if len(args) == 0:
                    await ctx.send("Must specify a genre!")
                    return
                genre = " ".join(args.split()).lower()
                user_id = str(ctx.author.id)
                self.game.spend_cranes(user_id, 200)
                self.game.add_bonus_genre(genre)
                self.journal(
                    {
                        "command": "buy",
                        "user": user_id,
                        "item": "bonus genre",
                        "genre": genre,
                    }
                )
                await ctx.send(f"New bonus genre active: {genre}")
            case "debt increase":
                target_id = re.match(r"<@(\d+)>", args)
                if not target_id:
                    await ctx.send("Must specify a target player!")
                    return
                target_player = self.game.get_player(target_id.group(1))
                if not target_player:
                    await ctx.send("Target player is not registered!")
                    return
                user_id = str(ctx.author.id)
                self.game.spend_cranes(user_id, 20)
                self.game.add_debt(target_player.user_id, 10000)
                self.journal(
                    {
                        "command": "buy",
                        "user": user_id,
                        "item": "debt increase",
                        "target": target_player.user_id,
                    }
                )
                await ctx.send(
                    f"Increased {target_player.display_name}'s debt by 10,000! How mean..."
                )
            case _:
                await ctx.send("Invalid store item")
