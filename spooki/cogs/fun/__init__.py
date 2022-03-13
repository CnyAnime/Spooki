from spooki.bot import Spooki
from ._base import BaseFunCog
from .games import GamesMixin
from .telephone import TelephoneMixin


class FunCog(BaseFunCog, GamesMixin, TelephoneMixin):
    pass


def setup(bot: Spooki):
    bot.add_cog(FunCog(bot))
