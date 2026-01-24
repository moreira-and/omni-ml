from dataclasses import dataclass
from datetime import datetime

from ...enums import TimeWindow
from ..base import DomainModel


@dataclass(frozen=True)
class Indicator(DomainModel):
    code: str
    alias: str
    timestamp: datetime
    time_window: TimeWindow
    value: float
