import asyncio
import os
import re
import sys

import config
from .bot import Spooki

# yikes. - Leo
init = """from ._base import Base{0}
from spooki.bot import Spooki


class {0}(Base{0}):
    pass


async def setup(bot: Spooki):
    await bot.add_cog({0}(bot))
"""

# yikes. - Leo
_base = """from spooki.utils.subclasses import Cog


class Base{}(Cog):
    pass
"""

# yikes. - Leo
standalone = """from spooki.utils.subclasses import Cog
from spooki.bot import Spooki


class {0}(Cog):
    pass


async def setup(bot: Spooki):
    await bot.add_cog({0}(bot))
"""


def snake_to_camel(string: str) -> str:
    """Convert snake case to camel case.

    Parameters
    ----------
    string : :class:`str`
        The snake-cased string to convert to camel case"""
    return string[0].upper() + re.sub(
        r"_([a-z])", lambda char: char.group(1).upper(), string[1:]
    )


args = sys.argv[1:]

if args and args[0] == "newcog":  # yikes. - Leo
    base = f"spooki/cogs/{args[1]}"
    name = snake_to_camel(args[1]) + "Cog"
    if len(args) > 2 and args[2].lower() in ("-pkg", "--package"):
        os.mkdir(base)
        with open(f"{base}/__init__.py", "w") as f:
            f.write(init.format(name))
        with open(f"{base}/_base.py", "w") as f:
            f.write(_base.format(name))
    else:
        with open(f"{base}.py", "w") as f:
            f.write(standalone.format(name))

elif __name__ == "__main__":
    Spooki().run()
