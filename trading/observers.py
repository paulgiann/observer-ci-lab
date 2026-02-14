from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Any

import numpy as np
import pandas as pd


class VolatilityBreakoutStrategyObserver:
    def __init__(self, window: int = 20):
        if window < 2:
            raise ValueError("window must be >= 2")
        self.window = int(window)
        self._prices: list[float] = []
        self._last_signal: int = 0

    def update(self, price: float) -> None:
        if not isinstance(price, (int, float)) or not math.isfinite(float(price)):
            self._last_signal = 0
            return

        p = float(price)
        self._prices.append(p)

        if len(self._prices) < 2:
            self._last_signal = 0
            return

        prices = np.asarray(self._prices, dtype=float)
        returns = prices[1:] / prices[:-1] - 1.0

        if returns.size <= self.window:
            self._last_signal = 0
            return

        last_r = float(returns[-1])
        prev_window = returns[-(self.window + 1) : -1]
        sigma = float(np.std(prev_window, ddof=1)) if prev_window.size >= 2 else 0.0

        if sigma <= 0.0:
            self._last_signal = 0
        elif last_r > sigma:
            self._last_signal = 1
        elif last_r < -sigma:
            self._last_signal = -1
        else:
            self._last_signal = 0

    @property
    def last_signal(self) -> int:
        return self._last_signal

    @property
    def prices(self) -> tuple[float, ...]:
        return tuple(self._prices)


class RiskObserver:
    def __init__(self, max_position: int, broker: Any):
        if max_position < 0:
            raise ValueError("max_position must be >= 0")
        self.max_position = int(max_position)
        self._broker = broker
        self.breached = False
        self.last_price: Optional[float] = None

    def update(self, price: float) -> None:
        self.last_price = float(price)
        pos = int(getattr(self._broker, "position"))
        if abs(pos) > self.max_position:
            self.breached = True


@dataclass
class LogRecord:
    price: float
    signal: Optional[int]


class LoggerObserver:
    def __init__(self, strategy: Optional[Any] = None):
        self._strategy = strategy
        self.prices: list[float] = []
        self.records: list[LogRecord] = []

    def update(self, price: float) -> None:
        p = float(price)
        self.prices.append(p)
        sig: Optional[int] = None
        if self._strategy is not None and hasattr(self._strategy, "last_signal"):
            sig = int(getattr(self._strategy, "last_signal"))
        self.records.append(LogRecord(price=p, signal=sig))

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([{"price": r.price, "signal": r.signal} for r in self.records])
