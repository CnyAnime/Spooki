from spooki.utils.subclasses import Cog, SpookiContext


class BaseOwnerCog(Cog):
    def cog_check(self, ctx: SpookiContext):
        return self.bot.is_owner(ctx.author)