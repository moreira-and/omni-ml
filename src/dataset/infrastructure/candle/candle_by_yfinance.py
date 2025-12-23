from datetime import datetime
from typing import Iterable, Optional

import pandas as pd
import yfinance as yf

from ....config import logger
from ...domain.enums import CandleInterval
from ...domain.interfaces import CandleRepository
from ...domain.value_objects import Candle


class CandleByYfinance(CandleRepository):
    def get_candles(
        self, symbol: str, interval: CandleInterval, start_ts: datetime, end_ts: datetime
    ) -> Iterable[Candle]:

        # Fetch candlestick data from yfinance
        df: Optional[pd.DataFrame] = None

        try:
            df = yf.download(
                symbol, start=start_ts, end=end_ts, auto_adjust=True, interval=interval.value
            )
        except Exception as e:
            logger.error(f"Error loading {symbol}: {e}")

        # Convert fetched data to list of Candle entities
        if df is None or df.empty:
            logger.warning(f"No data returned for {symbol}")
        else:
            for row in df.itertuples():
                yield self._convert_to_candle(row, interval)

    def _convert_to_candle(self, candle, interval: CandleInterval) -> Candle:
        # Convert a single data point from yfinance to a Candle entity
        candle = Candle(
            ts=candle.Index.to_pydatetime(),
            close=candle._1,
            high=candle._2,
            low=candle._3,
            open=candle._4,
            volume=candle._5,
            interval=interval,
        )
        return candle
