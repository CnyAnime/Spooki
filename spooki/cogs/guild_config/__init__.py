from spooki.bot import Spooki
from ._base import BaseGuildConfig
from .prefixes import PrefixMixin


class GuildConfig(BaseGuildConfig, PrefixMixin, name="Server Settings"):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(GuildConfig(bot))
