from discord.ext import commands

__all__ = ("BlacklistedError", "UserInputError")

class BlacklistedError(commands.CheckFailure):
    pass

class UserInputError(commands.CommandError):
    pass