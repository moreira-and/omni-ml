from datetime import datetime, timedelta

import pytest

from src.dataset.application.dtos import PricesQueryDto
from src.dataset.application.use_cases import GetPricesMultipleTickers
from src.dataset.infrastructure.price import YfinancePrice, price_router

query = PricesQueryDto(
    tickers=["AAPL", "MSFT"],
    interval="1d",
    start=datetime.today() - timedelta(days=5),
    end=datetime.today(),
)


@pytest.mark.integration
def test_PriceYfinance():
    repo = YfinancePrice()
    prices = list(
        repo.get_prices(
            ticker=query.tickers[0],
            interval=query.interval,
            start=query.start,
            end=query.end,
        )
    )

    assert len(prices) > 0
    first = prices[0]
    assert first.ticker == query.tickers[0]


@pytest.mark.integration
def test_PriceSourceRouter():

    repo = price_router(query.tickers[0])
    use_Case = GetPricesMultipleTickers(repo)
    prices = list(use_Case.get_prices(query))

    assert len(prices) > 0
    first = prices[0]
    assert first.ticker == query.tickers[0]