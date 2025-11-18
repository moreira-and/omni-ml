from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from .entities import IPriceBarFact


class PriceReadRepository(ABC):
    @abstractmethod
    def get_prices(
        self,
        *,
        ticker: str,
        bar: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[IPriceBarFact]: ...
