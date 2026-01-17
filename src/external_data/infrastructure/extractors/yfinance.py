from typing import Iterable, Optional, Mapping, Any
from datetime import datetime

from ....config import logger

from ...domain.enums import DataKind
from ...domain.models import CandleStick
from ...domain.enums import ExternalSource
from ...domain.entities import ExternalDataExtractDefinition

from ..interfaces import CandlesExtractor

import  yfinance as yf
import pandas as pd


class YFinanceCandlesSeries(CandlesExtractor):

    def extract(self, route: ExternalDataExtractDefinition, params: Mapping[str, Any] | None = None):
        if not params:
            raise ValueError("CandlesExtractor requires criterious")

        return self.extract_between(
            route=route,
            start=params["start"],
            end=params["end"],
        )
    
    def extract_between(
            self,
            route: ExternalDataExtractDefinition,
            start:datetime,
            end:datetime,
        ) -> Iterable[CandleStick]:

        # Fetch candlestick data from yfinance
        df_candles: Optional[pd.DataFrame] = None

        try:
            df_candles = yf.download(
                route.code.value, start=start, end=end, auto_adjust=True, interval= route.time_window.value
            )
        except Exception as e:
            logger.error(f"Error loading {route.code.value}: {e}")

        # Convert fetched data to list of Candle entities
        if df_candles is None or df_candles.empty:
            logger.warning(f"No data returned for {route.code.value}")
        else:
            for candle in df_candles.itertuples():
                yield self._convert_to_candlestick(route, candle)

    def _convert_to_candlestick(self, route: ExternalDataExtractDefinition, candle) -> CandleStick:
        # Convert a single data point from yfinance to a Candle entity
        candle = CandleStick(
            code=route.code.value,
            alias=route.alias.value,
            timestamp=candle.Index.to_pydatetime(),
            close=candle._1,
            high=candle._2,
            low=candle._3,
            open=candle._4,
            volume=candle._5,
            time_window=route.time_window,
        )

        return candle


    @property
    def get_by_source(self) -> ExternalSource:
        return ExternalSource("yfinance")
    
    @property
    def get_by_kind(self) -> DataKind:
        return DataKind.CANDLESTICK