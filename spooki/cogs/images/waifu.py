from typing import Optional

from discord.ext import commands

from spooki.utils.subclasses import SpookiContext


class WaifuFlags(commands.FlagConverter, case_insensitive=True, delimiter=" ", prefix="--"):
    tag: str
    gif: Optional[bool]
    nsfw: Optional[bool]


class WaifuCog:
    @commands.command()
    async def flags_test(self, ctx: SpookiContext, *, flags: WaifuFlags):
        if flags.tag not in ['uniform', 'maid', 'waifu', 'marin-kitagawa', 'mori-calliope', 'raiden-shogun', 'selfies',
                             'oppai']:
            return

        if flags.nsfw and not ctx.channel.is_nsfw():
            return

        image = await ctx.bot.waifu.random(selected_tags=[flags.tag], gif=flags.gif or False,
                                           is_nsfw=flags.nsfw or False)
        return await ctx.send(content=f"{image}")
