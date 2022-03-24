import os
from typing import List

import aiohttp
import colorama
import discord
import fade
from discord.ext import commands
from rich.logging import Console
from waifuim import WaifuAioClient

import config
from .utils.database import Database
from .utils.errors import BlacklistedError
from .utils.subclasses import SpookiContext

__all__ = ("Spooki",)


class Spooki(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=config.intents,
            command_prefix=config.prefix,
            case_insensitive=config.case_insensitive,
            activity=config.activity,
            strip_after_prefix=config.strip_after_prefix,
            allowed_mentions=discord.AllowedMentions.none()
        )

        self.console = Console()

        # info
        self.website = "https://spooki.xyz"
        self.top_gg = "soon"
        self.bots_gg = "soon"
        self.github = "soon"
        self.version = "v1.0 | Beta"
        self.uptime = discord.utils.utcnow()

    async def setup_hook(self):
        await self.load_extension("jishaku")
        for extension in config.extensions:
            await self.load_extension(f"spooki.cogs.{extension}")

        self.session = aiohttp.ClientSession()
        self.waifu = WaifuAioClient()

        await self.db_connect()
        self.add_check(self.blacklist_check, call_once=True)

    async def on_ready(self):
        os.system("cls" if os.name in ("nt", "dos") else "clear")
        self.ascii_art()

    def ascii_art(self):
        colorama.init(strip=True, convert=True, autoreset=True)
        splash = fade.purpleblue(""" 
                ███████╗██████╗  ██████╗  ██████╗ ██╗  ██╗██╗██╗
                ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝██║██║
                ███████╗██████╔╝██║   ██║██║   ██║█████╔╝ ██║██║
                ╚════██║██╔═══╝ ██║   ██║██║   ██║██╔═██╗ ██║╚═╝
                ███████║██║     ╚██████╔╝╚██████╔╝██║  ██╗██║██╗
                ╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝
        """)
        self.console.print(splash, justify="center", end="")

        colorama.deinit()
        self.console.print(f"{self.version}\n", justify="center", style="reset")

    async def db_connect(self) -> None:
        self.db: Database = await Database.connect()

    async def blacklist_check(self, ctx: SpookiContext) -> bool:
        for obj in (ctx.author, ctx.guild):
            if await self.db.is_blacklisted(obj.id):
                raise BlacklistedError()
        return True

    async def get_context(self, message: discord.Message, *, cls=SpookiContext):
        return await super().get_context(message, cls=cls)

    async def get_prefix(self, message: discord.Message) -> List[str]:
        prefixes = await self.db.get_prefixes(message.guild.id)
        if config.mention_prefix:
            if prefixes:
                return commands.when_mentioned_or(*prefixes)(self, message)
            return commands.when_mentioned(self, message)
        return prefixes

    def run(self, token: str = config.token, *, reconnect: bool = True):
        super().run(token, reconnect=reconnect)
