from ._base import BaseOwnerCog
from .blacklist import BlacklistMixin
from .extensions import ExtensionMixin

# for typing
from spooki.bot import Spooki

class OwnerCog(BaseOwnerCog, BlacklistMixin, ExtensionMixin, name="Owner"):
    pass

def setup(bot):
    bot.add_cog(OwnerCog(bot))
