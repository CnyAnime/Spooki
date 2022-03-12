# for typing
from spooki.bot import Spooki
from ._base import BaseUtilityCog
from .media import MediaMixin
from .reminder import ReminderMixin


class UtilityCog(BaseUtilityCog, MediaMixin, ReminderMixin, name="Utility"):
    pass


def setup(bot: Spooki):
    bot.add_cog(UtilityCog(bot))
