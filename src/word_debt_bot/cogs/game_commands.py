import importlib.metadata
import inspect
import json
import os
import pathlib
import re
import typing
from datetime import datetime

import discord.ext.commands as commands
import yaml

import word_debt_bot.client as client
import word_debt_bot.game as game


class GameCommands(commands.Cog, name="Core Gameplay"):
    def __init__(
        self,
        bot: client.WordDebtBot,
        game: game.WordDebtGame,
        journal_path: pathlib.Path = pathlib.Path("data/journal.ndjson"),
        shop_path: pathlib.Path = pathlib.Path("data/shop.yaml"),
    ):
        self.bot = bot
        self.game = game
        self.journal_path = journal_path
        self.shop_path = shop_path

        if not os.path.exists(self.shop_path):
            with open(self.shop_path, "w") as file_handle:
                yaml.dump(
                    {
                        "bonus_genre": {
                            "display_name": "bonus genre",
                            "description": "For the next week, words logged with this genre are worth twice as many cranes.",
                            "price": 200,
                        },
                        "debt_increase": {
                            "display_name": "debt increase",
                            "description": "Increase another player's debt by 10000.",
                            "price": 20,
                        },
                    },
                    file_handle,
                    Dumper=yaml.Dumper,
                )

    def journal(self, entry: dict) -> None:
        entry["time"] = datetime.now().timestamp()
        with open(self.journal_path, "a") as logfile:
            logfile.write(json.dumps(entry) + "\n")

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Check if the bot is running.
        """
        await ctx.send("Pong! All systems normal.")

    @commands.command(name="version")
    async def version(self, ctx):
        """
        Get the current version of the running bot.
        """
        version = importlib.metadata.version("word_debt_bot")
        await ctx.send(f"Version: {version}")

    @commands.command(
        name="register",
    )
    async def register(self, ctx):
        """
        Sign up for the game.

        Required to start logging words.
        """
        player = game.WordDebtPlayer(str(ctx.author.id), ctx.author.name, 10_000)
        self.game.register_player(player)
        self.journal({"command": "register", "user": str(ctx.author.id)})
        await ctx.send("Registered with 10,000 debt!")

    @commands.command(name="info")
    async def info(self, ctx):
        """
        Check your current cranes and debt.
        """
        player = self.game.get_player(str(ctx.author.id), False)
        await ctx.send(
            f"Info for {player.display_name}:\nDebt: {player.word_debt:,}\nCranes: {player.cranes:,}"
        )

    @commands.command(name="log")
    async def log(
        self,
        ctx,
        words: int = commands.parameter(description="The amount of words to log."),
        genre: typing.Optional[str] = commands.parameter(
            default=None,
            displayed_default=inspect.Parameter.empty,
            description="The genre to count the words towards.",
        ),
    ):
        """
        Log words and clear your debt.

        You can also specify a genre to potentially get bonuses. Having debt isn't necessary in order to log.
        """
        new_debt = self.game.submit_words(str(ctx.author.id), words, genre)
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
    async def leaderboard(
        self,
        ctx,
        sort_by: str = commands.parameter(
            description="'debt' or 'cranes', the field to sort by."
        ),
        req_pg: int = commands.parameter(
            default=1, displayed_name="page", description="The page number."
        ),
    ):
        """
        See who's ahead on cranes, or behind on debt...
        """
        pg = self.game.get_leaderboard_page(sort_by, req_pg)
        if pg == "":
            await ctx.send("No registered users, a leaderboard could not be made!")
            return
        await ctx.send(pg)

    @commands.command(name="shop")
    async def shop(
        self,
        ctx,
    ):
        """
        List items available in the shop. Use the `buy` command to buy items.
        """
        with open(self.shop_path) as file_handle:
            shop_items = yaml.load(file_handle, Loader=yaml.FullLoader)

        message = ""
        for _, item in shop_items.items():
            message += f"- \"{item['display_name']}\": {item['description']} Costs {item['price']:,} cranes.\n"

        await ctx.send(f"{message}")

    @commands.command(name="buy")
    async def buy(
        self,
        ctx,
        item: str = commands.parameter(description="The item to buy."),
        *,
        args: str
        | None = commands.parameter(
            default=None,
            displayed_default=inspect.Parameter.empty,
            description="Additional arguments for the purchased item.",
        ),
    ):
        """
        Purchase items from the shop. Use the `shop` command to view the items for sale.
        """
        if args is None:
            args = ""
        match item.lower().strip():
            case "bonus genre":
                await self.buy_bonus_genre(ctx, args)
            case "debt increase":
                await self.buy_debt_increase(ctx, args)
            case _:
                await ctx.send("Invalid shop item")

    async def buy_bonus_genre(self, ctx, args):
        if len(args) == 0:
            await ctx.send("Must specify a genre!")
            return
        genre = " ".join(args.split()).lower()
        user_id = str(ctx.author.id)
        with open(self.shop_path) as file_handle:
            shop_items = yaml.load(file_handle, Loader=yaml.FullLoader)
        price = shop_items["bonus_genre"]["price"]
        self.game.spend_cranes(user_id, price)
        self.game.add_bonus_genre(genre)
        self.journal(
            {
                "command": "buy",
                "user": user_id,
                "item": "bonus genre",
                "genre": genre,
                "price": price,
            }
        )
        await ctx.send(f"New bonus genre active: {genre}")

    async def buy_debt_increase(self, ctx, args):
        target_id = re.match(r"<@(\d+)>", args)
        if not target_id:
            await ctx.send("Must specify a target player!")
            return
        target_player = self.game.get_player(target_id.group(1))
        if not target_player:
            await ctx.send("Target player is not registered!")
            return
        user_id = str(ctx.author.id)
        with open(self.shop_path) as file_handle:
            shop_items = yaml.load(file_handle, Loader=yaml.FullLoader)
        price = shop_items["bonus_genre"]["price"]
        self.game.spend_cranes(user_id, price)
        self.game.add_debt(target_player.user_id, 10000)
        self.journal(
            {
                "command": "buy",
                "user": user_id,
                "item": "debt increase",
                "target": target_player.user_id,
                "price": price,
            }
        )
        await ctx.send(
            f"Increased {target_player.display_name}'s debt by 10,000! How mean..."
        )
