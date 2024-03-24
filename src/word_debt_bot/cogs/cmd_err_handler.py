from discord.ext import commands

import word_debt_bot.client as client
import word_debt_bot.game as game


class CmdErrHandler(commands.Cog, name="Command Error Handler"):
    def __init__(self, bot: client.WordDebtBot, game: game.WordDebtGame):
        self.bot = bot
        self.game = game

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

        # Prevents any commands with local handlers being handled here in on_command_error
        if hasattr(ctx.command, "on_error"):
            return

        match err:
            case commands.CommandNotFound():
                return
            case commands.BadArgument():
                await ctx.send(
                    f"Invalid inputs were supplied for {ctx.command}!\n"
                    f"For more information type `.help {ctx.command}`"
                )
            case commands.MissingRequiredArgument():
                await ctx.send(
                    f"Not all required inputs were given for {ctx.command}!\n"
                    f"For more information type `.help {ctx.command}`"
                )
            case commands.CommandInvokeError():
                await self.handle_invoke_error(err.__cause__, ctx)
            case _:
                await ctx.send(
                    f"An unhandled error occured when invoking {ctx.command}!\n"
                    f"Error: {str(err)}\n"
                    f"Type: {type(err)}\n"
                    f"For more information type `.help {ctx.command}` (and report this error to Toast!)\n"
                )

    async def handle_invoke_error(self, cause, ctx):
        match cause:
            case ValueError():
                await ctx.send(f"Error: {str(cause)}")
            case KeyError():
                await ctx.send("Not registered! `.register`")
            case _:
                await ctx.send(
                    f"An unhandled error occured when invoking {ctx.command}!\n"
                    f"Error: {str(cause)}\n"
                    f"Type: {type(cause)}\n"
                    f"For more information type `.help {ctx.command}`\n"
                )
