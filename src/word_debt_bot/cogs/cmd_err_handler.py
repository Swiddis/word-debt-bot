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

        # Prevents responses to commands that the bot does not have
        if isinstance(err, commands.CommandNotFound):
            return

        if isinstance(err, commands.DisabledCommand):
            await ctx.send(f"Sorry, {ctx.command} is currently disabled.\n")

        elif isinstance(err, commands.MissingPermissions):
            await ctx.send(
                f"Sorry, you do not have the required permissions for {ctx.command}.\n"
            )

        elif isinstance(err, commands.MissingRole):
            await ctx.send(
                f"Sorry, you do not have the required role for {ctx.command}.\n"
            )

        elif isinstance(err, commands.MissingAnyRole):
            await ctx.send(
                f"Sorry, you do not have all the required roles for {ctx.command}.\n"
            )

        elif isinstance(err, commands.BadArgument):
            await ctx.send(
                f"Invalid inputs were supplied for {ctx.command}!\n"
                f"For more information type `.help {ctx.command}`"
            )

        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(
                f"Not all required inputs were given for {ctx.command}!\n"
                f"For more information type `.help {ctx.command}`"
            )

        elif isinstance(err.__cause__, AttributeError) and not self.game:
            await ctx.send("Game not loaded. (Yell at Toast!)")

        elif isinstance(err.__cause__, ValueError) and ctx.command.name == "register":
            await ctx.send("Already registered!")

        elif isinstance(err.__cause__, KeyError) and ctx.command.name == "log":
            await ctx.send("Not registered! `.register`")

        elif isinstance(err.__cause__, ValueError) and ctx.command.name == "log":
            await ctx.send(f"Error: {str(err.__cause__)}")

        elif (
            isinstance(err.__cause__, ValueError) and ctx.command.name == "leaderboard"
        ):
            await ctx.send(f"Error: {str(err.__cause__)}")

        elif isinstance(err.__cause__, AttributeError) and ctx.command.name == "info":
            await ctx.send("Not registered! `.register`")

        elif isinstance(err.__cause__, ValueError) and ctx.command.name == "buy":
            await ctx.send(f"Error: {str(err.__cause__)}")

        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send(
                f"An error occured when invoking {ctx.command}!\n"
                f"Error: {str(err)}\n"
                f"Type: {type(err)}\n"
                f"For more information type `.help {ctx.command}`\n"
            )

        else:
            await ctx.send(
                f"An unhandled error occured when invoking {ctx.command}!\n"
                f"Error: {str(err)}\n"
                f"Type: {type(err)}\n"
                f"For more information type `.help {ctx.command}`\n"
            )
