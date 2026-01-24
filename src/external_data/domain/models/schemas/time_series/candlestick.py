from dataclasses import dataclass
from datetime import datetime

from src.external_data.domain.errors import DomainError

from ....enums import TimeWindow
from ...schemas.base import DomainModel


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
        corrected_high = max(self.high, self.open, self.close)
        corrected_low = min(self.low, self.open, self.close)

        object.__setattr__(self, "high", corrected_high)
        object.__setattr__(self, "low", corrected_low)

        if corrected_high < corrected_low:
            raise DomainError("Invalid candle after correction")
