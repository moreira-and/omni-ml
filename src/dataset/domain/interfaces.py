from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from .entities import Asset
from .enums import CandleInterval
from .value_objects import Candle


class AssetRepository(ABC):
    @abstractmethod
    def get_by_symbol(self, symbol: str) -> Iterable[Asset]:
        pass

    @abstractmethod
    def delete_by_symbol(self, symbol: str) -> None:
        pass

    @abstractmethod
    def save(self, asset: Asset) -> None:
        pass


class CandleRepository(ABC):
    @abstractmethod
    def get_candles(
        self, symbol: str, interval: CandleInterval, start_ts: datetime, end_ts: datetime
    ) -> Iterable[Candle]:
        pass
