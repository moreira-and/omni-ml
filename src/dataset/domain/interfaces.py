from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from .value_objects import AssetIndicator, AssetPrice, CountryIndicator


class AssetPriceReadRepository(ABC):
    @abstractmethod
    def get_prices(
        self,
        *,
        symbol: str,
        interval: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[AssetPrice]: ...


class AssetIndicatorReadRepository(ABC):
    @abstractmethod
    def get_asset_indicators(
        self,
        *,
        symbol: str,
        name: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[AssetIndicator]: ...


class CountryIndicatorReadRepository(ABC):
    @abstractmethod
    def get_country_indicators(
        self,
        *,
        country_code: str,
        name: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[CountryIndicator]: ...
