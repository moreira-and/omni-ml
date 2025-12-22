from datetime import datetime

from ..domain.entities import Asset
from ..domain.enums import CandleInterval
from ..domain.interfaces import CandleRepository


class AssetBuilder:
    def __init__(self, candle_repository: CandleRepository):
        self._candle_repository = candle_repository

    def build_by_symbol(
        self, symbol: str, interval: CandleInterval, start_ts: datetime, end_ts: datetime
    ) -> Asset:

        asset = Asset(
            symbol=symbol,
            candles=self._candle_repository.get_candles(symbol, interval, start_ts, end_ts),
        )
        return asset
