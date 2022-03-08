from __future__ import annotations
from typing import Literal, List, Coroutine, Any, Union, TypeVar

from discord import Guild, User, Member

from config import mention_prefix
from .base import BaseDB
from .cache import getter, setter
from .errors import CannotExecuteQueryError

T = TypeVar("T")
Response = Coroutine[Any, Any, T]
BlacklistType = Union[Guild, User, Member]

class Database(BaseDB):
    @getter("prefix")
    async def get_prefixes(self, guild_id: int) -> List[str]:
        """Get the prefixes for a guild.

        Parameters
        ----------
        guild_id : :class:`int`
            The id of the guild to get the prefixes for.

        Returns
        -------
        List[:class:`str`]
            The prefix for the guild."""
        data = await self.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", guild_id)
        return [row["prefix"] for row in data]

    @setter("prefix", (0,))
    def add_prefix(self, guild_id: int, prefix: str) -> Response[str]:
        """Add a prefix to a guild.

        Parameters
        ----------
        guild_id : :class:`int`
            The id of the guild to add the prefix to.
        prefix : :class:`str`
            The prefix to add to the guild."""
        return self.execute("INSERT INTO prefixes VALUES ($1, $2)", guild_id, prefix)

    @setter("prefix", (0,))
    async def remove_prefix(self, guild_id: int, prefix: str) -> str:
        """Remove a prefix from a guild.

        Parameters
        ----------
        guild_id : :class:`int`
            The id of the guild to remove the prefix from.
        prefix : :class:`str`
            The prefix to remove from the guild."""
        async with self.acquire() as db:
            if not mention_prefix:
                prefixes = await db.get_prefixes(guild_id)
                if len(prefixes) == 1:
                    raise CannotExecuteQueryError("Cannot remove the only prefix")
            return await db.execute(
                "DELETE FROM prefixes WHERE (guild_id, prefix) = ($1, $2)", guild_id, prefix
            )

    @setter("prefix")
    def clear_prefixes(self, guild_id: int) -> Response[str]:
        """Remove all the prefixes in a guild.
        This is meant to be used when removing a guild from the database.

        Parameters
        ----------
        guild_id : :class:`int`
            The id of the guild to remove prefixes from."""
        return self.execute("DELETE FROM prefixes WHERE guild_id = $1", guild_id)

    @getter("blacklist")
    def is_blacklisted(self, id: int) -> Response[bool]:
        """Check whether a guild/user is blacklisted or not

        Parameters
        ----------
        id : :class:`int`
            The id of the guild/user to check.

        Returns
        -------
        :class:`bool`
            Boolean indicating whether the guild/user is blacklisted or not."""
        return self.fetchval("SELECT EXISTS(SELECT 1 FROM blacklist WHERE id = $1)", id)

    @getter("blacklist")
    async def blacklisted_ids(self, type: Literal["user", "guild"]) -> Response[List[int]]:
        """Get the ids in the blacklist of guilds or users.
        
        Parameters
        ----------
        type : Literal["user", "guild"]
            The type of ids to get.

        Returns
        -------
        List[:class:`int`]
            The ids in the blacklist."""
        data = await self.fetch("SELECT id FROM blacklist WHERE type = $1", type)
        return [row["id"] for row in data]

    def _resolve_blacklist_type(self, obj: BlacklistType) -> str:
        if isinstance(obj, Guild):
            return "guild"
        elif isinstance(obj, (User, Member)):
            return "user"
        raise TypeError("obj must be a Guild, User, or Member")

    @setter("blacklist")
    async def blacklist(self, obj: BlacklistType) -> str:
        """Blacklist a guild/user.
        
        Parameters
        ----------
        obj : Union[:class:`discord.Guild`, :class:`discord.User`, :class:`discord.Member`]
            The guild/user to blacklist."""
        type_ = self._resolve_blacklist_type(obj)
        ret = await self.execute("INSERT INTO blacklist VALUES ($1, $2)", obj.id, type_)
        self.blacklisted_ids.func.remove(type_)
        return ret

    @setter("blacklist")
    async def unblacklist(self, obj: BlacklistType) -> str:
        """Remove a guild/user from the blacklist

        Parameters
        ----------
        obj : Union[:class:`discord.Guild`, :class:`discord.User`, :class:`discord.Member`]
            The id of the guild/user to remove."""
        type_ = self._resolve_blacklist_type(obj)
        ret = await self.execute("DELETE FROM blacklist WHERE id = $1", obj.id)
        if ret != "DELETE 0":
            self.blacklisted_ids.func.remove(type_)
        return ret