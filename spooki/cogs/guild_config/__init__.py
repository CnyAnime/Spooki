from ._base import BaseGuildConfig
from .prefixes import PrefixMixin

# for typing
from spooki.bot import Spooki

class GuildConfig(BaseGuildConfig, PrefixMixin, name="Server Settings"):
    pass

def setup(bot: Spooki):
    bot.add_cog(GuildConfig(bot))
