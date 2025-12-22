from datetime import datetime

import pytest

from src.dataset.domain.entities import Asset, Candle
from src.dataset.domain.enums import CandleInterval
from src.dataset.infrastructure.asset import LocalFileAssetRepository
from src.dataset.infrastructure.candle import CandleByYfinance


@pytest.fixture
def sample_asset():
    candles = [
        Candle(
            ts=datetime(2025, 1, 2),
            open=10.0,
            high=12.0,
            low=9.5,
            close=11.0,
            volume=1000,
            interval=CandleInterval.ONE_DAY,
        ),
        Candle(
            ts=datetime(2025, 1, 3),
            open=11.0,
            high=13.0,
            low=10.5,
            close=12.0,
            volume=1500,
            interval=CandleInterval.ONE_DAY,
        ),
    ]

    return Asset(symbol="^BVSP", candles=candles)


@pytest.fixture
def asset_repository():
    return LocalFileAssetRepository()


@pytest.fixture
def candle_repository():
    return CandleByYfinance()
