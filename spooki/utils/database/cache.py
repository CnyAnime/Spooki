from __future__ import annotations
from collections import OrderedDict
from functools import partial
from typing import Optional, Any, Callable, Coroutine, Dict, Tuple, Type, TypeVar, overload

__all__ = ("getter", "setter")

T = TypeVar("T")
Coro = Coroutine[Any, Any, Any]
Cache = OrderedDict[Tuple[Any], Any]

class Base:
    sections: Dict[str, Cache] = {}

    def __init__(self, coro: Coro, section: str):
        self.coro: Coro = coro
        self.section: str = section
        self.cache: Cache = self.sections.setdefault(section, OrderedDict())

    @overload
    def __get__(self, instance: None, owner: Type[T]) -> Base:
        pass

    @overload
    def __get__(self, instance: T, owner: Type[T]) -> Callable[Any, Coro]:
        pass

    def __get__(self, instance: Optional[T], owner: Type[T]) -> Any:
        if instance is None:
            return self
        return partial(self, instance)

class Getter(Base):
    def __init__(self, coro: Coro, section: str, max_size: Optional[int] = None):
        super().__init__(coro, section)
        self.max_size: Optional[int] = max_size

    def remove(self, *args: Any) -> None:
        """Remove arguments from the cache.

        Parameters
        ----------
        args: Any
            The arguments to remove from the cache.

        Raises
        ------
        :exc:`KeyError`
            The arguments were not found in cache."""
        del self.cache[args]

    async def __call__(self, instance, *args):
        if args in self.cache:
            self.cache.move_to_end(args)
            return self.cache[args]
        result = await self.coro(instance, *args)
        self.cache[args] = result
        if self.max_size and len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        return result

class Setter(Base):
    def __init__(self, coro: Coro, section: str, args_order: Optional[Tuple[int]] = None):
        super().__init__(coro, section)
        self.args_order: Optional[Tuple[int]] = args_order

    async def __call__(self, instance, *args):
        result = await self.coro(instance, *args)
        if self.args_order:
            args = tuple(args[i] for i in self.args_order)
        if args in self.cache:
            del self.cache[args]
        return result

def getter(section: str, max_size: Optional[int] = None) -> Callable[Coro, Getter]:
    """Create a "getter", a function that fetches values from the database
    This decorator is similar to :func:`functools.lru_cache`, but allows setters
    that reset the value of the cache.

    Parameters
    ----------
    section : :class:`str`
        The section to cache the values in.
    max_size : Optional[:class:`int`]
        The maximum number of values to cache. If None, no limit is imposed."""
    return partial(Getter, section=section, max_size=max_size)

def setter(section: str, args_order: Optional[Tuple[int]] = None) -> Callable[Coro, Setter]:
    """Create a "setter", a function that changes values in the database
    This resets the value in the cache.

    Parameters
    ----------
    section : :class:`str`
        The section to reset the value for.
    args_order : Optional[:class:`Tuple[int]`]
        The order in which the arguments of the decorated function are used
        to reset the value in the cache

    Example:
    ```
    class MyDatabase(BaseDB):
        @getter("numbers") # a getter that stores cache in "numbers"
        async def get_number(self, name: str):
            return await self.fetchval("SELECT phone_number FROM phonebook WHERE name = $1", name)
            # When this function is called the first time, it stores (name,) in the cache
            # When used again with the same parameters, it returns the value from the cache

        @setter("numbers", args_order=(0,)) # a setter for the values in the database
                                            # which updates the values in "numbers" cache
        async def set_number(self, name: str, number: int):
            # this function takes name and number, but our getter takes name only.
            # with args_order=(0,) the setter will think that the key in the cache would
            # be the 0th argument of this function, which is the name.
            await self.execute(
                "UPDATE phonebook SET phone_number = $2 WHERE name = $1", name, number
            )
    ```"""
    return partial(Setter, section=section, args_order=args_order)
