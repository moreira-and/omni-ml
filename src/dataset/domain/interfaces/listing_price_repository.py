from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from ..enums import CandleInterval
from ..value_objects import EconomicUnitListing, ListingPrice


class ListingPriceRepository(ABC):

    @abstractmethod
    def get_prices(
        self,
        *,
        listing: EconomicUnitListing,
        interval: CandleInterval,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[ListingPrice]: ...
