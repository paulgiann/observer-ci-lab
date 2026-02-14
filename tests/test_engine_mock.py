import pandas as pd
from unittest.mock import MagicMock

from trading.subject import MarketDataSubject
from trading.broker import Broker
from trading.engine import Engine


def test_engine_uses_strategy_last_signal_with_mock():
    subject = MarketDataSubject()
    broker = Broker(cash=1000.0)

    fake_strategy = MagicMock()
    fake_strategy.update = MagicMock()

    signals = [0, 1, 0, 0]
    def get_sig(i=[-1]):
        i[0] += 1
        return signals[min(i[0], len(signals)-1)]

    type(fake_strategy).last_signal = property(lambda self: get_sig())

    engine = Engine(subject, fake_strategy, broker, trade_qty=1)

    prices = pd.Series([100.0, 101.0, 102.0, 103.0])
    equity = engine.run(prices)

    assert broker.position == 1
    assert broker.cash == 899.0
    assert equity == 899.0 + 1 * 103.0
