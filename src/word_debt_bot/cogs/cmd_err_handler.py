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

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(err, commands.CommandNotFound):
            await ctx.send(
                "Unknown command! Maybe ask Toast to make it?\n"
                "For a list of available commands type '.help'."
            )

        elif isinstance(err, commands.BadArgument):
            await ctx.send(
                f"Invalid inputs were supplied for {ctx.command}!\n"
                f"For more information type '.help {ctx.command}'."
            )

        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(
                f"Not all required inputs were given for {ctx.command}!\n"
                f"For more information type '.help {ctx.command}'."
            )

        elif isinstance(err.__cause__, AttributeError) and not self.game:
            await ctx.send("Game not loaded. (Yell at Toast!)")

        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send(
                f"An error occured when invoking {ctx.command}!\n"
                f"Error: {str(err)}\n"
                f"Type: {type(err)}\n"
                f"For more information type '.help {ctx.command}'.\n"
            )

        else:
            await ctx.send(
                "An unhandled error occured!"
                f"Error: {str(err)}\n"
                f"Type: {type(err)}\n"
                f"For more information type '.help {ctx.command}'.\n"
            )
            # TODO add handlers for the remaining exception types:
            # https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exceptions
            # TODO Log base cases?
            # TODO Finish test_submit_words_no_game unit test
