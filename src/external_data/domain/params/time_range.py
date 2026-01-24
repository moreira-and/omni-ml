from dataclasses import dataclass
from datetime import datetime

from .base import ExtractParams


@dataclass(frozen=True)
class TimeRange(ExtractParams):
    start: datetime
    end: datetime
