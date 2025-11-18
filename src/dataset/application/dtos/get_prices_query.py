from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PricesQueryDto:
    ticker: str
    bar: str
    start: datetime
    end: datetime | None = None
