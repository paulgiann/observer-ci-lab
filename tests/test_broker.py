import pytest
from trading.broker import Broker


def test_buy_updates_cash_and_position():
    b = Broker(cash=100.0)
    b.market_order('buy', 2, 10.0)
    assert b.position == 2
    assert b.cash == 80.0


def test_sell_updates_cash_and_position():
    b = Broker(cash=100.0)
    b.market_order('buy', 2, 10.0)
    b.market_order('sell', 1, 12.0)
    assert b.position == 1
    assert b.cash == 92.0


def test_invalid_side_qty_price():
    b = Broker(cash=100.0)
    with pytest.raises(ValueError):
        b.market_order('hold', 1, 10.0)
    with pytest.raises(ValueError):
        b.market_order('buy', 0, 10.0)
    with pytest.raises(ValueError):
        b.market_order('buy', 1, 0.0)


def test_insufficient_cash():
    b = Broker(cash=5.0)
    with pytest.raises(ValueError):
        b.market_order('buy', 1, 10.0)


def test_insufficient_shares():
    b = Broker(cash=100.0)
    with pytest.raises(ValueError):
        b.market_order('sell', 1, 10.0)


def test_equity():
    b = Broker(cash=100.0)
    b.market_order('buy', 2, 10.0)
    assert b.equity(12.0) == 104.0
