from spooki.bot import Spooki
from ._base import BaseImagesCog
from .waifu import WaifuMixin


class ImagesCog(BaseImagesCog, WaifuMixin, name="Images"):
    pass


def setup(bot: Spooki):
    bot.add_cog(ImagesCog(bot))
