import re
import os
import sys
from .bot import Spooki

init = """from ._base import Base{0}

# for typing
from spooki.bot import Spooki

class {0}(Base{0}):
    pass

def setup(bot: Spooki):
    bot.add_cog({0}(bot))
"""

_base = """from spooki.utils.subclasses import Cog

class Base{}(Cog):
    pass
"""

standalone = """from spooki.utils.subclasses import Cog

# for typing
from spooki.bot import Spooki

class {0}(Cog):
    pass

def setup(bot: Spooki):
    bot.add_cog({0}(bot))
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

if args and args[0] == "newcog":
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
else:
    Spooki().run()
