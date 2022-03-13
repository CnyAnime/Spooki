from spooki.bot import Spooki
from ._base import BaseUtilityCog
from .reminder import ReminderMixin


class UtilityCog(BaseUtilityCog, ReminderMixin, name="Utility"):
    pass


def setup(bot: Spooki):
    bot.add_cog(UtilityCog(bot))
