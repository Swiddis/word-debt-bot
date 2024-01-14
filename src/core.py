import discord
from discord.ext import commands

_intents = discord.Intents.default()
_intents.message_content = True
bot = commands.Bot(".", intents=_intents)


@bot.command()
async def ping(ctx):
    await ctx.send("Pong")
