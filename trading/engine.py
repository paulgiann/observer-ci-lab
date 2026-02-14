from __future__ import annotations

import pandas as pd

from .subject import MarketDataSubject
from .broker import Broker


class Engine:
    def __init__(self, subject: MarketDataSubject, strategy, broker: Broker, *, trade_qty: int = 1):
        if trade_qty <= 0:
            raise ValueError("trade_qty must be positive")
        self.subject = subject
        self.strategy = strategy
        self.broker = broker
        self.trade_qty = int(trade_qty)

        self.subject.attach(self.strategy)

    def run(self, prices: pd.Series) -> float:
        if len(prices) == 0:
            raise ValueError("prices is empty")

        last_price = None
        for x in prices:
            p = float(x)
            last_price = p

            self.subject.notify(p)

            sig = int(getattr(self.strategy, "last_signal"))
            if sig == 1:
                self.broker.market_order("buy", self.trade_qty, p)
            elif sig == -1:
                self.broker.market_order("sell", self.trade_qty, p)

        return self.broker.equity(float(last_price))
