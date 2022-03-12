from spooki.bot import Spooki
from ._base import BaseOwnerCog
from .blacklist import BlacklistMixin
from .extensions import ExtensionMixin


class OwnerCog(BaseOwnerCog, BlacklistMixin, ExtensionMixin, name="Owner"):
    pass


def setup(bot: Spooki):
    bot.add_cog(OwnerCog(bot))
