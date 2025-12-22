from datetime import datetime, timedelta

import pytest

from src.dataset.domain.entities import Candle
from src.dataset.domain.enums import CandleInterval

from .test_fixture import candle_repository


@pytest.mark.integration
def test_get_candles(candle_repository):
    symbol = "^BVSP"
    interval = CandleInterval.ONE_DAY
    start_ts = datetime.today() - timedelta(days=10)
    end_ts = datetime.today() - timedelta(days=1)

    for candle in candle_repository.get_candles(symbol, interval, start_ts, end_ts):
        assert_valid_candle(candle, interval)


def assert_valid_candle(candle: Candle, interval):
    assert candle.ts is not None
    assert candle.open > 0
    assert candle.high >= candle.open
    assert candle.low <= candle.open
    assert candle.close > 0
    assert candle.volume >= 0
    assert candle.interval == interval
