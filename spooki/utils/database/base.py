from __future__ import annotations
import os
from typing import Optional, Any, List, Tuple, TypeVar

import asyncpg

import config
from .cache import Base as Cache
from .errors import *

__all__ = ("BaseDB",)

Record = TypeVar("Record")

class Acquire:
    def __init__(self, db: BaseDB, timeout: Optional[float] = None) -> None:
        self.type: BaseDB = db.__class__
        self.pool: asyncpg.Pool = db.pool
        self.timeout: Optional[float] = timeout
        self.db: Optional[BaseDB] = None

    async def _acquire(self) -> BaseDB:
        return self.type(self.pool, await self.pool.acquire(timeout=self.timeout))

    def __await__(self) -> BaseDB:
        return self._acquire().__await__()

    async def __aenter__(self) -> BaseDB:
        self.db = await self._acquire()
        return self.db

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.db.release()

class BaseDB:
    # Setup

    def __init__(
        self, pool: asyncpg.Pool, acquired_connection: Optional[asyncpg.Connection] = None
    ) -> None:
        self.pool: asyncpg.Pool = pool
        self.acquired_connection: Optional[asyncpg.Connection] = acquired_connection

    @classmethod
    async def connect(cls, dsn: Optional[str] = None, **pool_kwargs: Any) -> BaseDB:
        """Connect to the database

        Parameters
        ----------
        dsn : Optional[:class:`str`]
            Connection arguments specified using a single string
            in the ``libpq connection URI format``.
        pool_kwargs : Any
            The connection arguments to pass to :meth:`asyncpg.create_cool`

        Returns
        -------
        :class:`BaseDB`
            The database object that you can use to query the db."""
        if not (pool_kwargs or dsn):
            pool_kwargs = {
                k: getattr(config, k, None)
                for k in ("host", "port", "user", "password", "database")
            }
        self = cls(await asyncpg.create_pool(dsn, **pool_kwargs))
        await self.setup_tables()
        return self

    async def setup_tables(self) -> None:
        """Execute the ``schema.sql`` file.
        If no ``schema.sql`` file is found, it does nothing."""
        if not os.path.exists("schema.sql"):
            return
        with open("schema.sql", "r") as f:
            query = f.read()
        await self.execute(query)

    # Shutdown

    async def close(self) -> None:
        """Close the connection pool."""
        if self.acquired_connection:
            await self.release()
        await self.pool.close()

    def clear_cache(self, *sections: str) -> None:
        """Clear the cache.

        Parameters
        ----------
        sections : str
            The sections to clear. If not given, it clears all sections."""
        sections = sections or Cache.sections
        for section in sections:
            Cache.sections[section].clear()

    # Shorthands

    async def _execute(self, method: str, *args: Any, **kwargs) -> Any:
        conn = self.acquired_connection or await self.pool.acquire()
        ret = await getattr(conn, method)(*args, **kwargs)
        if not self.acquired_connection:
            await self.pool.release(conn)
        return ret

    async def execute(self, query: str, *args: Any, timeout: Optional[float] = None) -> str:
        """Similar to :meth:`asyncpg.Connection.execute`
        This uses execute on the acquired connection,
        if any, else it uses it on the pool."""
        return await self._execute("execute", query, *args, timeout=timeout)

    async def executemany(
        self, command: str, args: List[Tuple[Any]], *, timeout: Optional[float] = None
    ) -> None:
        """Similar to :meth:`asyncpg.Connection.executemany`
        This uses executemany on the acquired connection,
        if any, else it uses it on the pool."""
        return await self._execute("executemany", command, args, timeout=timeout)

    async def fetch(
        self, query: str, *args: Any,
        timeout: Optional[float] = None, record_class: Optional[Record] = None
    ) -> List[Record]:
        """Similar to :meth:`asyncpg.Connection.fetch`
        This uses fetch on the acquired connection,
        if any, else it uses it on the pool."""
        return await self._execute(
            "fetch", query, *args, timeout=timeout, record_class=record_class
        )

    async def fetchrow(
        self, query: str, *args: Any,
        timeout: Optional[float] = None, record_class: Optional[Record] = None
    ) -> Optional[Record]:
        """Similar to ``asyncpg.Connection.fetchrow()``
        This uses fetchrow on the acquired connection,
        if any, else it uses it on the pool."""
        return await self._execute(
            "fetchrow", query, *args, timeout=timeout, record_class=record_class
        )

    async def fetchval(
        self, query: str, *args: Any, column: int = 0, timeout: Optional[float] = None
    ) -> Any:
        """Similar to ``asyncpg.Connection.fetchval()``
        This uses fetchval on the acquired connection,
        if any, else it uses it on the pool."""
        return await self._execute("fetchval", query, *args, column=column, timeout=timeout)

    # Acquiring/Realising

    def acquire(self, *, timeout: Optional[float] = None) -> BaseDB:
        """Acquire an :class:`asyncpg.Connection` from the pool.

        Parameters
        ----------
        timeout : Optional[:class:`float`]
            A timeout for acquiring the :class:`asyncpg.Connection`.

        Returns
        -------
        :class:`BaseDB`
            The database object that uses the acquired connection."""
        return Acquire(self, timeout)

    async def release(self, *, timeout: Optional[float] = None) -> None:
        """Release the :class:`asyncpg.Connection` back to the pool

        Parameters
        ----------
        timeout : Optional[:class:`float`]
            A timeout for releasing the :class:`asyncpg.Connection`.
            If not specified, defaults to the timeout provided
            in the corresponding call to :meth:`BaseDB.acquire`.

        Raises
        ------
        NoAcquiredConnectionError
            There was no acquired connection to release."""
        if not self.acquired_connection:
            raise NoAcquiredConnectionError()
        await self.pool.release(self.acquired_connection, timeout=timeout)
