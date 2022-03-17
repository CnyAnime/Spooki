from spooki.bot import Spooki
from ._base import BaseEconomyCog


class EconomyCog(BaseEconomyCog):
    pass


def setup(bot: Spooki):
    bot.add_cog(EconomyCog(bot))

# MATE WHY ARE U HERE
