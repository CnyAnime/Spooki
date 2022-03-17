from spooki.bot import Spooki
from ._base import BaseUtilityCog
from .reminder import ReminderMixin


class UtilityCog(BaseUtilityCog, ReminderMixin, name="Utility"):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(UtilityCog(bot))