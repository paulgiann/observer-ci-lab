import pandas as pd
import pytest

from trading.subject import MarketDataSubject
from trading.broker import Broker
from trading.engine import Engine


class ThresholdStrategy:
    def __init__(self, lo: float, hi: float):
        self.lo = float(lo)
        self.hi = float(hi)
        self.last_signal = 0

    def update(self, price: float) -> None:
        p = float(price)
        if p > self.hi:
            self.last_signal = 1
        elif p < self.lo:
            self.last_signal = -1
        else:
            self.last_signal = 0


def test_engine_places_orders_and_returns_equity():
    subject = MarketDataSubject()
    strategy = ThresholdStrategy(lo=99.0, hi=101.0)
    broker = Broker(cash=1_000)
    engine = Engine(subject, strategy, broker, trade_qty=1)

    prices = pd.Series([100.0, 102.0, 102.0, 98.0, 100.0])
    equity = engine.run(prices)

    assert broker.position == 1
    assert broker.cash == 894.0
    assert equity == 894.0 + 1 * 100.0


def test_engine_empty_prices_raises():
    subject = MarketDataSubject()
    strategy = ThresholdStrategy(lo=0.0, hi=1.0)
    broker = Broker(cash=100.0)
    engine = Engine(subject, strategy, broker)

    with pytest.raises(ValueError):
        engine.run(pd.Series([], dtype=float))


def test_engine_propagates_subject_notification_error():
    class BadObs:
        def update(self, price: float) -> None:
            raise RuntimeError('fail')

        @property
        def last_signal(self) -> int:
            return 0

    subject = MarketDataSubject()
    broker = Broker(cash=100.0)
    bad = BadObs()
    engine = Engine(subject, bad, broker)

    with pytest.raises(RuntimeError):
        engine.run(pd.Series([100.0, 101.0]))
