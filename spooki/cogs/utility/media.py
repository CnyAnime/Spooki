import aiofiles
import asyncio
import discord
import random
import string
import json
import os
import re
from discord.ext import commands

from config import emojis

# for typing
from spooki.utils.subclasses import SpookiContext
from ._base import BaseUtilityCog

class DownloadFlags(commands.FlagConverter, delimiter=' ', prefix='--'):
    type: str = "mp4"
    res: int = None

class MediaMixin:
    @commands.command(aliases=["dl"], description="Download Reddit, TikTok, YouTube, Twitter, Roblox, SoundCloud audios and/or videos")
    async def download(self, ctx: SpookiContext, url: str, *, flags: DownloadFlags):
        REDDIT_REGEX = re.compile(r"http[s]?://www\.reddit.com/r/[a-zA-Z0-9_]{2,22}/comments/[a-zA-Z0-9_]{6}/.+$")
        REDDIT_VIDEO_REGEX = re.compile(r"http(?:s)?:\/\/v\.redd\.it\/[a-z0-9]{13}")
        TIKTOK_REGEX = re.compile(r"https?:\/\/www\.tiktok\.com\/(?:@.+)\/video\/(?P<id>\d+).+")
        TIKTOK_MOBILE_REGEX = re.compile(r"https?:\/\/vm\.tiktok\.com\/(?P<id>.+)\/")
        TIKTOK_MOBILE_REGEX2 = re.compile(r"https?:\/\/m\.tiktok\.com\/v\/(?P<id>.+)\.html")
        YOUTUBE_REGEX = re.compile(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$")
        TWITTER_REGEX = re.compile(r"http[s]?://(?:www\.)?twitter\.com/[A-Za-z0-9_]{4,15}/status/\d+")
        ROBLOX_AUDIO_REGEX = re.compile(r"http[s]?://(?:www\.)?roblox\.com/library/\d+/.+$")
        SOUNDCLOUD_REGEX = re.compile(r"http[s]?://(?:www|m\.)?soundcloud\.com/.+/.+")

        resolution = ("best" if flags.type == "mp4" else "bestaudio") if flags.res is None else f"best[height={flags.res}, ext=mp4]"

        name = "".join(random.choices(string.ascii_letters+string.digits, k=16))
        async with aiofiles.tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, f"{name}.{flags.type}")

            if re.match(TIKTOK_MOBILE_REGEX, url) or re.match(TIKTOK_MOBILE_REGEX2, url):
                url = str((await self.bot.session.get(url)).url)

            if match := re.match(TIKTOK_REGEX, url):
                vid_id = match.group("id")
                headers = {"user-agent": "okhttp"}

                api = "https://toolav.herokuapp.com/id/?video_id="+vid_id
                request = (await (await self.bot.session.get(api, headers=headers)).read()).decode()
                resp = json.loads(request)
                aweme_id = resp.get("item", {}).get("aweme_id")
                if not aweme_id:
                    return await ctx.send("Download failed")

                url = f"https://api-h2.tiktokv.com/aweme/v1/play/?video_id={aweme_id}&vr_type=0&is_play_url=1&source=PackSourceEnum_FEED&media_type=4&ratio=default&improve_bitrate=1"
                avi = f"./processed/{name}.avi"
                mp4 = f"./processed/{name}.mp4"

                try:
                    async with ctx.typing():
                        request = await self.bot.session.get(url, headers=headers)
                        async with aiofiles.open(avi, mode="wb") as f:
                            await f.write(await request.read())

                        proc = await asyncio.create_subprocess_shell(
                                f"ffmpeg -i {avi} {mp4}",
                                stdout=asyncio.subprocess.PIPE,
                                stderr=asyncio.subprocess.PIPE
                        )
                        await proc.wait()
                        stdout, stderr = await proc.communicate()
                        stdout, stderr = stdout.decode(), stderr.decode()
                except asyncio.TimeoutError:
                    return await ctx.send("Downloading took over 60 seconds and has therefore been cancelled")

                if flags.type == "mp3":
                    await BaseUtilityCog.convert_mp4_to_mp3(path, mp4)

                

            elif re.match(REDDIT_REGEX, url) or re.match(REDDIT_VIDEO_REGEX, url):
                url = await BaseUtilityCog.parse_reddit(url)
                code = f"ffmpeg -i {url+'/DASHPlaylist.mpd'} {path}"

                async with ctx.typing():
                    proc = await asyncio.create_subprocess_shell(
                            code,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )

                await proc.wait()
                stdout, stderr = await proc.communicate()
                stdout, stderr = stdout.decode(), stderr.decode()

            elif re.match(TWITTER_REGEX, url):
                code = f"youtube-dl {url} --output {path}"

                async with ctx.typing():
                    proc = await asyncio.create_subprocess_shell(
                            code,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )

                await proc.wait()
                stdout, stderr = await proc.communicate()
                stdout, stderr = stdout.decode(), stderr.decode()

            elif re.match(SOUNDCLOUD_REGEX, url):
                path = f"./processed/{name}.mp3"
                flags.type = "mp3"
                code = f"youtube-dl {url} --output {path}"

                async with ctx.typing():
                    proc = await asyncio.create_subprocess_shell(
                            code,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )

                await proc.wait()
                stdout, stderr = await proc.communicate()
                stdout, stderr = stdout.decode(), stderr.decode()

            elif re.match(ROBLOX_AUDIO_REGEX, url):
                path = f"./processed/{name}.mp3"
                flags.type = "mp3"
                async with ctx.typing():
                    res = await BaseUtilityCog.parse_roblox_audio(url)
                    res = await (await self.bot.session.get(res)).read()
                    async with aiofiles.open(path, mode="wb") as _file:
                        await _file.write(res)
                    stdout, stderr = None, None

            elif re.match(YOUTUBE_REGEX, url):
                if flags.type == "mp3":
                    code = {
                        "format": resolution,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192'
                        }],
                        "outtmpl": f"./processed/{name}.mp3",
                        "encoding": "ascii"
                    }

                elif flags.type == "mp4":
                    code = {
                        "format": resolution,
                        "outtmpl": f"./processed/{name}.mp4",
                        "encoding": "ascii"
                    }

                try:
                    async with ctx.typing():
                        stdout = await asyncio.wait_for(
                            BaseUtilityCog.yt_download(self, code, [url]),
                            timeout=60
                        )
                except asyncio.TimeoutError:
                    return await ctx.send("Downloading took over 60 seconds and has therefore been cancelled")

            else: return await ctx.send("Unsupported url")

            if flags.type == "mp3": filetype = "audio"
            if flags.type == "mp4": filetype = "video"
            else: "Unknown"

            msg = await ctx.reply(f"Now downloading {filetype} to `{path}`")

            if not os.path.isfile(path):
                formatted_stdout = f'{stdout}\n'
                await msg.delete()
                return await ctx.send(f"""Download failed with output:
stdout:
{'' if len(stdout) == 0 else formatted_stdout}
stderr:
{stderr}
""")

            await msg.edit(f"Now uploading {filetype} from `{path}`")
            await ctx.send(file=discord.File(path))
            await msg.delete()