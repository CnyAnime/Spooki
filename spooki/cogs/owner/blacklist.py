from typing import Union

import discord
from discord.ext import commands

from config import emojis
from spooki.utils.errors import UserInputError
from spooki.utils.subclasses import SpookiContext

BlacklistType = Union[discord.User, discord.Member, discord.Guild]


class BlacklistMixin:
    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx: SpookiContext, obj: BlacklistType):
        """Commands related to the bots blacklist.
        Use the base command to blacklist a guild/user"""

        try:
            await ctx.db.blacklist(obj or ctx.guild)

        except Exception as exc:
            start = "That guild" if isinstance(obj, discord.Guild) else "That user"
            raise UserInputError(f"{start} is already blacklisted!") from None

        else:
            await ctx.message.add_reaction(emojis["tick"])

    @blacklist.command()
    async def remove(self, ctx: SpookiContext, obj: BlacklistType):
        """Remove a user/guild from the bots blacklist."""

        ret = await ctx.db.unblacklist(obj)
        if ret == "DELETE 0":
            start = "That guild" if isinstance(obj, discord.Guild) else "That user"
            raise UserInputError(f"{start} is not blacklisted!") from None

        await ctx.message.add_reaction(emojis["tick"])

    async def send_blacklist(self, ctx: SpookiContext) -> None:
        """main handler for blacklist viewing commands"""
        type_ = ctx.command.name[:-1]
        ids = map(getattr(ctx.bot, f"get_{type_}"), await ctx.db.blacklisted_ids(type_))
        embed = discord.Embed(
            title=f"Blacklisted {ctx.command.name.capitalize()}",
            description="\n".join(map(str, ids)),
            color=0x6e00ff
        )

        await ctx.send(embed=embed)

    @blacklist.command()
    async def users(self, ctx: SpookiContext):
        await self.send_blacklist(ctx)

    @blacklist.command()
    async def guilds(self, ctx: SpookiContext):
        await self.send_blacklist(ctx)
