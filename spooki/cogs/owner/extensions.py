from traceback import format_exception
from typing import Awaitable, Callable, Tuple

from discord.ext import commands

# for typing
from spooki.utils.subclasses import SpookiContext

class ExtensionMixin:
    def resolve_name(self, extension: str) -> str:
        """Resolve the extension name.

        Examples
        --------
        resolve_name("owner")             # "spooki.cogs.owner"
        resolve_name("spooki.cogs.owner") # "spooki.cogs.owner"
        resolve_name("jishaku")           # "jishaku"
        """
        if extension == "jishaku" or extension.startswith("spooki.cogs."):
            return extension
        return f"spooki.cogs.{extension}"

    def execute(self, func: Callable[str, None], emoji: str, extension: str) -> str:
        """do a function in try/except and return the result/traceback with emoji"""
        try:
            func(extension)
        except Exception as exc:
            tb = "".join(format_exception(type(exc), exc, exc.__traceback__))
            return f"❌ `{extension}`\n```py\n{tb}\n```"
        return f"{emoji} `{extension}`"

    def load_extension(self, extension: str) -> str:
        """load an extension"""
        if extension in self.bot.extensions:
            return self.execute(self.bot.reload_extension, "🔃", extension)
        else:
            return self.execute(self.bot.load_extension, "➕", extension)

    def unload_extension(self, extension: str) -> str:
        """unload an extension"""
        return self.execute(self.bot.unload_extension, "➖", extension)

    def handle_extension(
        self, ctx: SpookiContext, extensions: Tuple[str], meth: Callable[str, None]
    ) -> Awaitable:
        """main handler for extension commands"""
        extensions = extensions or list(self.bot.extensions.keys())
        return ctx.send("\n".join(meth(self.resolve_name(ext)) for ext in extensions))

    @commands.command(aliases=["reload"])
    async def load(self, ctx: SpookiContext, *extensions: str):
        await self.handle_extension(ctx, extensions, self.load_extension)

    @commands.command()
    async def unload(self, ctx: SpookiContext, *extensions: str):
        await self.handle_extension(ctx, extensions, self.unload_extension)