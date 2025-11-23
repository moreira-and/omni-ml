from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from .entities import MacroeconomicIndicatorFact, PriceBarFact


class PriceReadRepository(ABC):
    @abstractmethod
    def get_prices(
        self,
        *,
        ticker: str,
        interval: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[PriceBarFact]: ...


class IndicatorReadRepository(ABC):
    @abstractmethod
    def get_indicator(
        self,
        *,
        name: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[MacroeconomicIndicatorFact]: ...
