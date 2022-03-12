import asyncio
import contextlib
import functools
from io import StringIO
from typing import List

from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

from spooki.utils.subclasses import Cog


def executor(executor=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            partial = functools.partial(func, *args, **kwargs)
            loop = asyncio.get_running_loop()
            return loop.run_in_executor(executor, partial)

        return wrapper

    return decorator


class BaseUtilityCog(Cog):

    async def parse_roblox_audio(self, url: str):
        content = await (await self.bot.session.get(url)).read()
        bs = BeautifulSoup(content, "html.parser")
        button = bs.find("div", class_="MediaPlayerIcon icon-play")
        return button.get("data-mediathumb-url")

    async def parse_reddit(self, url: str):
        r = BeautifulSoup(await (await self.bot.session.get(url)).read(), "html.parser")
        res = r.find_all("meta")
        u = res[17].get("content")
        return "/".join(u.split("/")[:4])

    @executor()
    def yt_download(self, options: dict, urls: List):
        with contextlib.redirect_stdout(stream := StringIO()):
            with YoutubeDL(options) as ydl:
                ydl.download(urls)
        return stream.getvalue()
