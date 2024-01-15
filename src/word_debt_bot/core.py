import discord
from discord.ext import commands

from .game import WordDebtPlayer

_intents = discord.Intents.default()
_intents.message_content = True
bot = commands.Bot(".", intents=_intents)


@bot.command()
async def ping(ctx):
    if hasattr(bot, "game"):
        await ctx.send("Pong! All systems normal.")
    else:
        await ctx.send("I'm alive, but I'm not sure where Toast hid the game state...")


@bot.command()
async def register(ctx):
    if not hasattr(bot, "game"):
        return
    player = WordDebtPlayer(str(ctx.author.id), ctx.author.name, 10_000)
    try:
        bot.game.register_player(player)
        await ctx.send("Registered with 10,000 debt!")
    except ValueError:
        await ctx.send("Already registered!")
