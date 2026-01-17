from dataclasses import dataclass
from datetime import datetime

from .base import DomainModel
from ..enums import TimeWindow


@dataclass(frozen=True)
class Indicator(DomainModel):
    code: str
    alias: str
    timestamp: datetime
    time_window: TimeWindow
    value: float
