import numpy as np
import pandas as pd
import pytest

from trading.subject import MarketDataSubject
from trading.observers import VolatilityBreakoutStrategyObserver, LoggerObserver
from trading.broker import Broker


@pytest.fixture
def prices():
    return pd.Series(np.linspace(100, 120, 200))

@pytest.fixture
def subject():
    return MarketDataSubject()

@pytest.fixture
def subject_continue():
    return MarketDataSubject(continue_on_error=True)

@pytest.fixture
def strategy():
    return VolatilityBreakoutStrategyObserver(window=20)

@pytest.fixture
def logger():
    return LoggerObserver()

@pytest.fixture
def broker():
    return Broker(cash=1_000)
