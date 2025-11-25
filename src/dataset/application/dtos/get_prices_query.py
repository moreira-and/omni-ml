from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class PricesQueryDto:
    codes: List[str]
    interval: str
    start: datetime
    end: datetime | None = None
