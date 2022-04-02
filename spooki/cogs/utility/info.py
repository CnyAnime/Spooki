from typing import Optional, Union

import discord
from discord.ext import commands
from spooki.utils.subclasses import SpookiContext


class InfoMixin:
    @commands.command()
    async def userinfo(self, ctx: SpookiContext, user: Optional[Union[discord.Member, discord.User]]):
        await ctx.trigger_typing()
        if user is None:
            if ctx.message.reference:
                user = ctx.message.reference.resolved.author

            user = ctx.author

        if isinstance(user, discord.Member):
            embed = discord.Embed(title="User info")

            embed.add_field(name=f"General info", value=f"""
Display name: {user.display_name}
Discriminator: #{user.discriminator}
ID: `{user.id}`
Bot?: {'Yes' if user.bot else 'No'}

            """)

            await ctx.send(embed=embed)

        else:
            await ctx.send("fuck your mom1")