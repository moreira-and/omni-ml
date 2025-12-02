from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from ..entities import EconomicUnit
from ..value_objects import EconomicUnitListing


class EconomicUnitListingRepository(ABC):

    @abstractmethod
    def get_listings(
        self,
        *,
        unit: EconomicUnit,
    ) -> Iterable[EconomicUnitListing]: ...
