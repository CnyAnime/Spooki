from typing import List

from discord.ext import commands

from config import mention_prefix, prefix
from spooki.utils.database import CannotExecuteQueryError

# for typing
from discord import Guild
from spooki.utils.subclasses import SpookiContext

class PrefixMixin:
    @staticmethod
    def format_prefixes(prefixes: List[str]) -> str:
        return ", ".join(f"`{p}`" for p in prefixes)

    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx: SpookiContext):
        prefixes = await ctx.db.get_prefixes(ctx.guild.id)
        if len(prefixes) > 1:
            formatted = self.format_prefixes(prefixes[:-1]) + f" and `{prefixes[-1]}`"
        else:
            formatted = self.format_prefixes(prefixes)
        if mention_prefix:
            formatted += ". You can also use my mention as a prefix"
        await ctx.send(f"The prefixes are {formatted}.")

    @prefix.command()
    async def add(self, ctx: SpookiContext, prefix: str):
        try:
            await ctx.db.add_prefix(ctx.guild.id, prefix)
        except:
            return await ctx.send("That prefix is already added!")
        await ctx.send(f"Added `{prefix}` as a prefix.")

    @prefix.command()
    async def remove(self, ctx: SpookiContext, prefix: str):
        try:
            result = await ctx.db.remove_prefix(ctx.guild.id, prefix)
        except CannotExecuteQueryError as exc:
            return await ctx.send(exc)
        if result == "DELETE 0":
            return await ctx.send("That prefix is not added yet!")
        await ctx.send(f"Removed `{prefix}` as a prefix.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await self.bot.db.add_prefix(guild.id, prefix)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        await self.bot.db.clear_prefixes(guild.id)