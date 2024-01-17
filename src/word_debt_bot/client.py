from discord.ext import commands


class WordDebtBot(commands.Bot):
    async def on_ready(self):
        print(f"{self.user.name} is ready.")
