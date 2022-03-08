import sys
from traceback import format_exception

import discord
from discord.ext import commands

from config import error_channel, emojis
from spooki.utils.errors import *

# for typing
from spooki.utils.subclasses import SpookiContext

class ErrorHandlingCog(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: SpookiContext, error: commands.CommandError):
        error = getattr(error, "original", error)

        if isinstance(error, (commands.CommandNotFound, BlacklistedError)):
            return

        if isinstance(error, UserInputError):
            await ctx.send(
                embed=discord.Embed(description=f"{emojis['cross']} | {error}", color=0x6e00ff)
            )

        else:
            tb = "".join(format_exception(type(error), error, error.__traceback__))
            channel = ctx.bot.get_channel(error_channel)
            if channel:
                await channel.send(embed=discord.Embed(
                    title=f"Error in {ctx.command.qualified_name}",
                    description=f"```py\n{tb}\n```",
                    color=0x6e00ff,
                    url=ctx.message.jump_url
                ))
            else:
                print(
                    f"Ignoring exception in command {ctx.command.qualified_name}:",
                    file=sys.stderr
                )
                print(tb, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorHandlingCog())
