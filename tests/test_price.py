from datetime import datetime, timedelta

import pytest

from src.dataset.application.dtos import PricesQueryDto
from src.dataset.application.use_cases import GetPrices
from src.dataset.infrastructure import YfinancePrice, price_router

query = PricesQueryDto(
    ticker="AAPL",
    bar="1d",
    start=datetime.today() - timedelta(days=5),
    end=datetime.today(),
)


@pytest.mark.integration
def test_PriceYfinance():
    repo = YfinancePrice()
    prices = list(
        repo.get_prices(
            ticker=query.ticker,
            bar=query.bar,
            start=query.start,
            end=query.end,
        )
    )

    assert len(prices) > 0
    first = prices[0]
    assert first.ticker == query.ticker


@pytest.mark.integration
def test_PriceSourceRouter():

    repo = price_router(query.ticker)
    use_Case = GetPrices(repo)
    prices = list(use_Case.get_prices(query))

    assert len(prices) > 0
    first = prices[0]
    assert first.ticker == query.ticker
