from spooki.bot import Spooki
from ._base import BaseUtilityCog
from .reminder import ReminderMixin
from .info import InfoMixin


class UtilityCog(BaseUtilityCog, ReminderMixin, InfoMixin, name="Utility"):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(UtilityCog(bot))