from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from ..entities import EconomicUnit
from ..value_objects import EconomicUnitIndicator


class EconomicUnitIndicatorRepository(ABC):

    @abstractmethod
    def get_indicators(
        self,
        *,
        unit: EconomicUnit,
        start: datetime,
        end: datetime | None = None,
        name: str | None = None,
    ) -> Iterable[EconomicUnitIndicator]: ...
