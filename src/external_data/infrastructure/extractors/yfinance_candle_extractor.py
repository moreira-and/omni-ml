from typing import Iterable, Optional, Mapping, Any
from datetime import datetime

from ....config import logger

from ...domain.enums import DataKind
from ...domain.models import CandleStick
from ...domain.enums.external_source import ExternalSource
from ...domain.entities.extract_definition import ExtractDefinition

from ...domain.interfaces import ExtractExecutor

import  yfinance as yf
import pandas as pd


class YFinanceCandlesSeries(ExtractExecutor):

    def execute(self, definition: ExtractDefinition, params: Mapping[str, Any] | None = None):
        if not params:
            raise ValueError("CandlesExtractor requires criterious")

        return self.extract_between(
            definition=definition,
            start=params["start"],
            end=params["end"],
        )
    
    def extract_between(
            self,
            definition: ExtractDefinition,
            start:datetime,
            end:datetime,
        ) -> Iterable[CandleStick]:

        # Fetch candlestick data from yfinance
        df_candles: Optional[pd.DataFrame] = None

        try:
            df_candles = yf.download(
                definition.code.value, start=start, end=end, auto_adjust=True, interval= definition.time_window.value
            )
        except Exception as e:
            logger.error(f"Error loading {definition.code.value}: {e}")

        # Convert fetched data to list of Candle entities
        if df_candles is None or df_candles.empty:
            logger.warning(f"No data returned for {definition.code.value}")
        else:
            for candle in df_candles.itertuples():
                yield self._convert_to_candlestick(definition, candle)

    def _convert_to_candlestick(self, route: ExtractDefinition, candle) -> CandleStick:
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