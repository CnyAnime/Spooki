from spooki.bot import Spooki
from ._base import BaseEconomyCog


class EconomyCog(BaseEconomyCog):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(EconomyCog(bot))

# MATE WHY ARE U HERE
