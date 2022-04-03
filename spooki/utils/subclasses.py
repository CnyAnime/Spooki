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


class ConfirmationView(discord.ui.View):
    """ from https://github.com/LeoCx1000/discord-bots/blob/rewrite/utils/context.py#L47-L79 """
    def __init__(self, ctx: SpookiContext, *, timeout: int = 60) -> None:
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None
        self.message: discord.Message | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    async def on_timeout(self) -> None:
        if self.message:
            for item in self.children:
                item.disabled = True
            await self.message.edit(content=f'Timed out waiting for a button press from {self.ctx.author}.', view=self)

    def stop(self) -> None:
        super().stop()

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.value = True
        self.stop()
        await interaction.message.delete()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.value = False
        self.stop()
        await interaction.message.delete()


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

    async def confirm(self, content=None, /, *, timeout: int = 30, **kwargs) -> bool | None:
        """ from https://github.com/LeoCx1000/discord-bots/blob/rewrite/utils/context.py#L165-L192 """
        view = ConfirmationView(self, timeout=timeout)
        try:
            view.message = await self.channel.send(content, **kwargs, view=view)
            await view.wait()
            return view.value
        except discord.HTTPException:
            view.stop()
            return None


class Cog(commands.Cog):
    def __init__(self, bot: Spooki):
        self.bot: Spooki = bot
