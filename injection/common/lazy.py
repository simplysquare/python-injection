from collections.abc import Callable, Iterator, Mapping
from types import MappingProxyType
from typing import Generic, TypeVar

from injection.common.tools.threading import thread_lock

__all__ = ("Lazy", "LazyMapping")

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


class Lazy(Generic[_T]):
    __slots__ = ("__cache", "__is_set")

    def __init__(self, factory: Callable[[], _T]):
        self.__setup_cache(factory)

    def __invert__(self) -> _T:
        return next(self.__cache)

    def __call__(self) -> _T:
        return ~self

    @property
    def is_set(self) -> bool:
        return self.__is_set

    def __setup_cache(self, factory: Callable[[], _T]):
        def new_cache() -> Iterator[_T]:
            with thread_lock:
                self.__is_set = True

            nonlocal factory
            cached = factory()
            del factory

            while True:
                yield cached

        self.__cache = new_cache()
        self.__is_set = False


class LazyMapping(Mapping[_K, _V]):
    __slots__ = ("__lazy",)

    def __init__(self, iterator: Iterator[tuple[_K, _V]]):
        self.__lazy = Lazy(lambda: MappingProxyType(dict(iterator)))

    def __getitem__(self, key: _K, /) -> _V:
        return (~self.__lazy)[key]

    def __iter__(self) -> Iterator[_K]:
        yield from ~self.__lazy

    def __len__(self) -> int:
        return len(~self.__lazy)

    @property
    def is_set(self) -> bool:
        return self.__lazy.is_set
