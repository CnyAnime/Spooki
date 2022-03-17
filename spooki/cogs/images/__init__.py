from spooki.bot import Spooki
from ._base import BaseImagesCog
from .waifu import WaifuMixin


class ImagesCog(BaseImagesCog, WaifuMixin, name="Images"):
    pass


async def setup(bot: Spooki):
    await bot.add_cog(ImagesCog(bot))
