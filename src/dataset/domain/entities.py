from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .enums import CandleInterval


@dataclass
class Candle:
    """
    Represents a single candlestick data point in trading.
    """

    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    interval: CandleInterval

    ## Validates the Candle data after initialization.
    def __post_init__(self):
        if self.open <= 0 or self.close <= 0 or self.high <= 0 or self.low <= 0:
            raise ValueError("Open and close prices must be more equal 0.")

        if (self.high < self.open) or (self.high < self.low):
            raise ValueError("High price cannot be lower than others.")

        if (self.low > self.open) or (self.low > self.high):
            raise ValueError("Low price cannot be higher than others.")


@dataclass
class Asset:
    """
    Represents a financial asset with its associated candlestick data.
    """

    symbol: str
    candles: Iterable[Candle]
