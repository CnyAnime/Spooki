from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from ..bot import Spooki
    from .database import Database

__all__ = ("SpookiContext", "Cog")


class SpookiContext(commands.Context):
    @property
    def db(self) -> Database:
        return self.bot.db


class Cog(commands.Cog):
    def __init__(self, bot: Spooki):
        self.bot: Spooki = bot
