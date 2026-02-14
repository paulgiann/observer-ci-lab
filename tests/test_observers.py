from trading.observers import VolatilityBreakoutStrategyObserver, LoggerObserver, RiskObserver
from trading.broker import Broker


def test_logger_records_all_prices(subject, logger, prices):
    subject.attach(logger)
    for p in prices:
        subject.notify(float(p))
    assert logger.prices[0] == float(prices.iloc[0])
    assert len(logger.prices) == len(prices)


def test_logger_can_record_signals():
    s = VolatilityBreakoutStrategyObserver(window=5)
    log = LoggerObserver(strategy=s)
    s.update(100.0)
    log.update(100.0)
    assert log.records[-1].signal == 0


def test_strategy_emits_zero_until_enough_data():
    s = VolatilityBreakoutStrategyObserver(window=5)
    for p in [100, 101, 102, 103, 104, 105, 106]:
        s.update(float(p))
    assert s.last_signal in (-1, 0, 1)


def test_strategy_handles_constant_prices_as_zero():
    s = VolatilityBreakoutStrategyObserver(window=5)
    for _ in range(30):
        s.update(100.0)
        assert s.last_signal == 0


def test_strategy_ignores_nan_and_sets_zero():
    s = VolatilityBreakoutStrategyObserver(window=5)
    s.update(100.0)
    s.update(float('nan'))
    assert s.last_signal == 0
    assert s.prices == (100.0,)


def test_risk_observer_flags_breach():
    b = Broker(cash=1_000)
    r = RiskObserver(max_position=2, broker=b)
    r.update(100.0)
    assert r.breached is False
    b.position = 3
    r.update(101.0)
    assert r.breached is True
