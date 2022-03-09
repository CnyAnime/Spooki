# for typing
from spooki.bot import Spooki
from ._base import BaseReminderCog


class ReminderCog(BaseReminderCog):
    pass


def setup(bot: Spooki):
    bot.add_cog(ReminderCog(bot))
