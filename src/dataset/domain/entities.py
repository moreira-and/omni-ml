from dataclasses import dataclass
from typing import Iterable

from .value_objects import Candle


@dataclass
class Asset:
    """
    Represents a financial asset with its associated candlestick data.
    """

    symbol: str
    candles: Iterable[Candle]
