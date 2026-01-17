from dataclasses import dataclass
from datetime import datetime

from src.external_data.domain.errors import DomainError

from .base import DomainModel
from ..enums import TimeWindow

@dataclass(frozen=True)
class CandleStick(DomainModel):
    """
    Represents a single candlestick data point in trading.
    """
    code: str
    alias: str
    timestamp: datetime
    time_window: TimeWindow
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self):
        if self.high < max(self.open, self.close):
            raise DomainError("Invalid candle: high is too low")