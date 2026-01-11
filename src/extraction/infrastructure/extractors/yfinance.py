from typing import Iterable, Optional, Mapping, Any
from datetime import datetime

from ....config import logger

from ...domain.enums import ModelType, TimeWindow
from ...domain.models import CandleStick
from ...domain.value_objects import ModelName, ModelSource, ModelCode
from ...domain.entities import ModelRoute

from ..interfaces import CandlesExtractor

import  yfinance as yf
import pandas as pd


class YFinanceCandlesSeries(CandlesExtractor):

    def extract(self, route: ModelRoute, params: Mapping[str, Any] | None = None):
        if not params:
            raise ValueError("CandlesExtractor requires criterious")

        return self.extract_between(
            route=route,
            start=params["start"],
            end=params["end"],
            time_window=TimeWindow(params["time_window"]),
        )
    
    def extract_between(
            self,
            route: ModelRoute,
            start:datetime,
            end:datetime,
            time_window: TimeWindow
        ) -> Iterable[CandleStick]:

        # Fetch candlestick data from yfinance
        df_candles: Optional[pd.DataFrame] = None

        try:
            df_candles = yf.download(
                route.code.value, start=start, end=end, auto_adjust=True, interval=time_window.value
            )
        except Exception as e:
            logger.error(f"Error loading {route.code.value}: {e}")

        # Convert fetched data to list of Candle entities
        if df_candles is None or df_candles.empty:
            logger.warning(f"No data returned for {route.code.value}")
        else:
            for candle in df_candles.itertuples():
                yield self._convert_to_candlestick(route, time_window, candle)

    def _convert_to_candlestick(self, route: ModelRoute, time_window: TimeWindow, candle) -> CandleStick:
        # Convert a single data point from yfinance to a Candle entity
        candle = CandleStick(
            code=route.code.value,
            name=route.name.value,
            timestamp=candle.Index.to_pydatetime(),
            close=candle._1,
            high=candle._2,
            low=candle._3,
            open=candle._4,
            volume=candle._5,
            time_window=time_window,
        )

        return candle


    @property
    def source(self) -> ModelSource:
        return ModelSource("yfinance")
    
    @property
    def type(self) -> ModelType:
        return ModelType.CANDLESTICK