from ._base import BaseUtilityCog
from .media import MediaMixin

# for typing
from spooki.bot import Spooki

class UtilityCog(BaseUtilityCog, MediaMixin):
    pass

def setup(bot: Spooki):
    bot.add_cog(UtilityCog(bot))
