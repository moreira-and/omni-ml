from datetime import date, timedelta

import pytest

from src.dataset.infra.yfinance_pandas_dataset import YfinancePandasDataset


def test_YfinancePandasDataset():
    DatasetTestYfinancePandas = YfinancePandasDataset(
        ticker="^BVSP",
        start_date=(date.today() - timedelta(days=2)).isoformat(),
        end_date=(date.today() - timedelta(days=1)).isoformat(),
        interval="1d",
    )

    batch = DatasetTestYfinancePandas.load()
    assert not batch.X.empty, "DataFrame should not be empty"
    assert "Ticker" in batch.X.columns, "'Ticker' column should be present in DataFrame"
