from ._base import BaseModerationCog
from spooki.bot import Spooki

from .basic import BasicMixin
from .clear import ClearMixin
from .mute import MuteMixin


class ModerationCog(BaseModerationCog, BasicMixin, ClearMixin, MuteMixin):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(ModerationCog(bot))
