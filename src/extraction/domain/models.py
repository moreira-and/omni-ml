from dataclasses import dataclass
from datetime import datetime

from .enums import TimeWindow

@dataclass(frozen=True)
class CandleStick:
    """
    Represents a single candlestick data point in trading.
    """
    code: str
    name: str
    timestamp: datetime
    time_window: TimeWindow
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class Indicator:
    code: str
    name: str
    timestamp: datetime
    time_window: TimeWindow
    value: float
