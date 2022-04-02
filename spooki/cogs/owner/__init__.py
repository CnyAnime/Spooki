LOCAL = False # set this to True if a private.py file exists in this directory

from spooki.bot import Spooki
from ._base import BaseOwnerCog
from .blacklist import BlacklistMixin
from .extensions import ExtensionMixin

if LOCAL:
    from .private import PrivateMixin


class OwnerCog(BaseOwnerCog, BlacklistMixin, ExtensionMixin, PrivateMixin or None, name="Owner"):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(OwnerCog(bot))
