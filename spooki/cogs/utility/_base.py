import asyncio

from spooki.utils.subclasses import Cog


class BaseUtilityCog(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.event = asyncio.Event()
        self.current_timer = None
        self.task = self.bot.loop.create_task(self.dispatch_timers())
        self.bot = bot

    async def dispatch_timers(self):
        ...
