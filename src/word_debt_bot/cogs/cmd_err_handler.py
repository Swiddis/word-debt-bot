from discord.ext import commands

import word_debt_bot.client as client


class CmdErrHandler(commands.Cog):
    def __init__(self, bot: client.WordDebtBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err: commands.CommandError):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if isinstance(err, commands.CommandNotFound):
            await ctx.send(
                "Unknown command! Maybe ask Toast to make it?\n"
                "For a list of available commands type '.help'."
            )
        elif isinstance(err, commands.BadArgument):
            await ctx.send(
                "Invalid inputs were supplied for the given command!\n"
                f"For more information type '.help {ctx.command}'."
            )
        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(
                "Not all required inputs were given for that command!\n"
                f"For more information type '.help {ctx.command}'."
            )
        else:
            await ctx.send(
                f"Error: {str(err)}\n"
                f"Type: {type(err)}\n"
                f"For more information type '.help {ctx.command}'.\n"
                "This was an unhandeld error! (Blame -> MO-W59)"
            )
            # TODO add handlers for the remaining exception types:
            # https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exceptions
