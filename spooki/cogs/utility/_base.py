from spooki.utils.subclasses import Cog
from bs4 import BeautifulSoup

class BaseUtilityCog(Cog):
    async def parse_roblox_audio(self, url: str):
        content = await (await self.bot.session.get(url)).read()
        bs = BeautifulSoup(content, "html.parser")
        button = bs.find("div", class_="MediaPlayerIcon icon-play")
        return button.get("data-mediathumb-url")