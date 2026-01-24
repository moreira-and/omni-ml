from datetime import datetime, timedelta
from typing import Iterable, Optional

import pandas as pd
import yfinance as yf

from ......config import logger
from .....application.clocks import Clock
from .....application.interfaces import ExtractExecutor
from .....domain.entities.extract_definition import ExtractDefinition
from .....domain.enums import DataKind, TimeWindow
from .....domain.enums.external_source import ExternalSource
from .....domain.models.params import TimeRange
from .....domain.models.schemas.time_series import CandleStick


class YFinanceCandleExtract(ExtractExecutor):

    LOOKBACK_LIMITS = {
        TimeWindow.ONE_HOUR: timedelta(days=730),
        TimeWindow.FIVE_MINUTES: timedelta(days=60),
        TimeWindow.FIFTEEN_MINUTES: timedelta(days=60),
    }

    def execute(
        self, definition: ExtractDefinition, params: TimeRange, clock: Clock
    ) -> Iterable[CandleStick]:

        if not params:
            raise ValueError("Extractor requires criterious")

        _start = params.start
        _end = params.end
        _now = clock.now()

        if _end > _now:
            logger.warning(f"end param adjusted because end > now: " f"{_end} → {_now}")
            _end = _now

        if _start > _end:
            logger.warning(f"end param adjusted because start > end: " f"{_end} → {_start}")
            _end = _start

        limit = self.LOOKBACK_LIMITS.get(definition.time_window)

        if limit is not None:
            max_lookback = _now - limit

            if _start < max_lookback:
                logger.warning(
                    f"start param adjusted due to time window limit: " f"{_start} → {max_lookback}"
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

        # Fetch candlestick data from yfinance
        df_candles: Optional[pd.DataFrame] = None

        logger.info(
            f"Downloading {definition.alias.value} ({definition.code.value}) from the Central Bank of Brazil API..."
        )

        try:
            df_candles = yf.download(
                definition.code.value,
                start=start,
                end=end,
                auto_adjust=True,
                interval=definition.time_window.value,
            )
        except Exception as e:
            logger.error(f"Error loading {definition.code.value}: {e}")

        # Convert fetched data to list of Candle entities
        if df_candles is None or df_candles.empty:
            logger.warning(f"No data returned for {definition.code.value}")
        else:
            logger.success(f"{definition.alias.value} ({definition.code.value}) extracted! ")

            for candle in df_candles.itertuples():
                yield self._convert_to_candlestick(definition, candle)

    def _convert_to_candlestick(self, definition: ExtractDefinition, candle) -> CandleStick:
        # Convert a single data point from yfinance to a Candle entity
        candle = CandleStick(
            code=definition.code.value,
            alias=definition.alias.value,
            timestamp=candle.Index.to_pydatetime(),
            close=candle._1,
            high=candle._2,
            low=candle._3,
            open=candle._4,
            volume=candle._5,
            time_window=definition.time_window,
        )

        return candle

    @property
    def source(self) -> ExternalSource:
        return ExternalSource("yfinance")

    @property
    def data_kind(self) -> DataKind:
        return DataKind.CANDLESTICK
