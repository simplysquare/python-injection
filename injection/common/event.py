from abc import ABC, abstractmethod
from contextlib import ContextDecorator, ExitStack, contextmanager, suppress
from dataclasses import dataclass, field
from typing import ContextManager
from weakref import WeakSet

__all__ = ("Event", "EventChannel", "EventListener")


class Event(ABC):
    __slots__ = ()


class EventListener(ABC):
    __slots__ = ("__weakref__",)

    @abstractmethod
    def on_prevent(self, event: Event, /) -> ContextManager | None:
        raise NotImplementedError

    @abstractmethod
    def on_event(self, event: Event, /):
        raise NotImplementedError


@dataclass(repr=False, eq=False, frozen=True, slots=True)
class EventChannel:
    __listeners: WeakSet[EventListener] = field(default_factory=WeakSet, init=False)

    @contextmanager
    def dispatch(self, event: Event) -> ContextManager | ContextDecorator:
        listeners = tuple(self.__listeners)

        with ExitStack() as stack:
            for listener in listeners:
                context_manager = listener.on_prevent(event)

                if context_manager is None:
                    continue

                stack.enter_context(context_manager)

            yield

            for listener in listeners:
                listener.on_event(event)

    def add_listener(self, listener: EventListener):
        self.__listeners.add(listener)
        return self

    def remove_listener(self, listener: EventListener):
        with suppress(KeyError):
            self.__listeners.remove(listener)

        return self
