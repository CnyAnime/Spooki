from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any, List, Optional, Union

import discord
from discord.ext import commands

from .emojis import *

if TYPE_CHECKING:
    from ..bot import Spooki
    from .database import Database

__all__ = ("SpookiContext", "Cog")


class SpookiContext(commands.Context):
    @property
    def db(self) -> Database:
        return self.bot.db

    @staticmethod
    def tick(self, value: bool) -> str:
        return TICKS(value)
        
    async def send(self, content: Union[str, Any] = None, *, embed: discord.Embed = None,
                    embeds: List[discord.Embed] = None, reply: bool = True, color: bool = True,
                    footer: bool = True, reference: Union[discord.Message, discord.MessageReference] = None,
                    file: discord.File = None, reminders: bool = True, **kwargs) -> discord.Message:

        if embed and embeds:
            raise ValueError("You can't use both embed and embeds")

        if embed:
            if footer:
                embed.set_footer(text=f"Requested by {self.author.display_name}", icon_url=self.author.display_avatar.url)
                embed.timestamp = discord.utils.utcnow()

            if color:
                embed.color = self.bot.color

            if reminders:
                embed.set_footer(text=random.choice(self.bot.support_reminders))

        if embeds:
            for embed in embeds:
                if footer:
                    embed.set_footer(text=f"Requested by {self.author.display_name}", icon_url=self.author.display_avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                if color:
                    embed.color = self.bot.color

                if reminders:
                    embed.set_footer(text=random.choice(self.bot.support_reminders))

        reference = (reference or self.message.reference or self.message) if reply is True else reference
        embeds = [embed] if embed else (embeds or [])

        try:
            return await super().send(content=content, embeds=embeds, reference=reference, file=file, **kwargs)
        except discord.HTTPException:
            return await super().send(content=content, embeds=embeds, reference=None, file=file, **kwargs)


class Cog(commands.Cog):
    def __init__(self, bot: Spooki):
        self.bot: Spooki = bot
