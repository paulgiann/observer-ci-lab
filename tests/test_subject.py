import pytest
from unittest.mock import MagicMock

from trading.subject import MarketDataSubject, NotificationError


def test_attach_avoids_duplicates():
    subject = MarketDataSubject()
    obs = MagicMock()
    subject.attach(obs)
    subject.attach(obs)
    assert list(subject.observers) == [obs]


def test_attach_and_notify_calls_update_once():
    subject = MarketDataSubject()
    obs = MagicMock()
    subject.attach(obs)
    subject.notify(101.0)
    obs.update.assert_called_once_with(101.0)


def test_detach_is_idempotent():
    subject = MarketDataSubject()
    obs = MagicMock()
    subject.detach(obs)
    subject.attach(obs)
    subject.detach(obs)
    subject.detach(obs)


def test_detach_stops_notifications():
    subject = MarketDataSubject()
    obs = MagicMock()
    subject.attach(obs)
    subject.detach(obs)
    subject.notify(101.0)
    obs.update.assert_not_called()


def test_notify_preserves_order():
    subject = MarketDataSubject()
    calls = []

    class A:
        def update(self, price: float) -> None:
            calls.append(('A', price))

    class B:
        def update(self, price: float) -> None:
            calls.append(('B', price))

    subject.attach(A())
    subject.attach(B())
    subject.notify(5.0)
    assert calls == [('A', 5.0), ('B', 5.0)]


def test_notify_propagates_error_by_default():
    subject = MarketDataSubject()
    good = MagicMock()

    class Bad:
        def update(self, price: float) -> None:
            raise RuntimeError('boom')

    subject.attach(Bad())
    subject.attach(good)

    with pytest.raises(RuntimeError):
        subject.notify(1.0)

    good.update.assert_not_called()


def test_notify_continue_on_error_notifies_all(subject_continue):
    subject = subject_continue
    good = MagicMock()

    class Bad:
        def update(self, price: float) -> None:
            raise RuntimeError('boom')

    subject.attach(Bad())
    subject.attach(good)

    with pytest.raises(NotificationError):
        subject.notify(1.0)

    good.update.assert_called_once_with(1.0)
