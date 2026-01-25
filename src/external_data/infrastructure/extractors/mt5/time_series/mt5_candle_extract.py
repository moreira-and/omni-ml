from datetime import datetime, timedelta
from typing import Iterable

import MetaTrader5 as mt5
import pandas as pd

from ......config import logger
from .....application.clocks import Clock
from .....application.interfaces import ExtractExecutor
from .....domain.entities.extract_definition import ExtractDefinition
from .....domain.enums import DataKind, TimeWindow
from .....domain.enums.external_source import ExternalSource
from .....domain.models.params import TimeRange
from .....domain.models.schemas.time_series import CandleStick
from ..mt5_session import MT5Session


class MT5CandleExtract(ExtractExecutor):

    TIMEFRAME_MAP = {
        TimeWindow.ONE_HOUR: mt5.TIMEFRAME_H1,
        TimeWindow.FIFTEEN_MINUTES: mt5.TIMEFRAME_M15,
        TimeWindow.FIVE_MINUTES: mt5.TIMEFRAME_M5,
        TimeWindow.ONE_MINUTE: mt5.TIMEFRAME_M1,
    }

    def execute(
        self, definition: ExtractDefinition, params: TimeRange, clock: Clock
    ) -> Iterable[CandleStick]:

        with MT5Session():
            if not params:
                raise ValueError("Extractor requires criterious")

            _start = params.start
            _end = params.end
            _now = clock.now()

            if _end > _now:
                logger.warning(f"end param adjusted because end > now: {_end} → {_now}")
                _end = _now

            if _start > _end:
                logger.warning(f"end param adjusted because start > end: {_end} → {_start}")
                _end = _start

            limit = timedelta(days=2)
            if limit is not None:
                max_lookback = _now - limit
                if _start < max_lookback:
                    logger.warning(
                        f"start param adjusted due to time window limit: {_start} → {max_lookback}"
                    )
                    _start = max_lookback

            return self.extract_between(
                definition=definition,
                start=_start,
                end=_end,
            )

    def extract_between(
        self,
        definition: ExtractDefinition,
        start: datetime,
        end: datetime,
    ) -> Iterable[CandleStick]:

        timeframe = self.TIMEFRAME_MAP.get(definition.time_window)
        if timeframe is None:
            raise ValueError(f"Unsupported time window: {definition.time_window}")

        if not mt5.initialize():
            raise RuntimeError("MetaTrader5 initialize() failed")

        symbol = definition.code.value

        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Symbol not available in MT5: {symbol}")

        logger.info(f"Downloading {definition.alias.value} ({symbol}) from MT5...")

        try:
            rates = mt5.copy_rates_range(symbol, timeframe, start, end)
        except Exception as e:
            logger.error(f"Error loading {symbol}: {e}")
            rates = None

        if rates is None or len(rates) == 0:
            logger.warning(f"No data returned for {symbol}")
            return

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)

        logger.success(f"{definition.alias.value} ({symbol}) extracted!")

        for row in df.itertuples(index=False):
            yield self._convert_to_candlestick(definition, row)

    def _convert_to_candlestick(self, definition: ExtractDefinition, row) -> CandleStick:

        volume = (
            row.real_volume
            if hasattr(row, "real_volume") and row.real_volume is not None
            else row.tick_volume
        )

        return CandleStick(
            code=definition.code.value,
            alias=definition.alias.value,
            timestamp=row.time.to_pydatetime(),
            open=row.open,
            high=row.high,
            low=row.low,
            close=row.close,
            volume=volume,
            time_window=definition.time_window,
        )

    @property
    def source(self) -> ExternalSource:
        return ExternalSource("metatrader5")

    @property
    def data_kind(self) -> DataKind:
        return DataKind.CANDLESTICK
