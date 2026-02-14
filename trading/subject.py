from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, List, Iterable


class Observer(Protocol):
    def update(self, price: float) -> None:
        ...


@dataclass(frozen=True)
class NotificationError(Exception):
    observer: object
    original: Exception

    def __str__(self) -> str:
        return f"Observer {self.observer!r} raised {self.original!r}"


class MarketDataSubject:
    def __init__(self, *, continue_on_error: bool = False):
        self._observers: List[Observer] = []
        self._continue_on_error = continue_on_error

    @property
    def observers(self) -> Iterable[Observer]:
        return tuple(self._observers)

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            return

    def notify(self, price: float) -> None:
        errors: list[NotificationError] = []
        for obs in list(self._observers):
            try:
                obs.update(price)
            except Exception as e:
                if not self._continue_on_error:
                    raise
                errors.append(NotificationError(obs, e))
        if errors:
            raise errors[0]
