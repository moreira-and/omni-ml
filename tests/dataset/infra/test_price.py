from datetime import datetime, timedelta, timezone

import pytest

from src.dataset.domain.value_objects import AssetPrice
from src.dataset.infrastructure.price import YfinancePrice, price_router

SYMBOLS = ["AAPL", "MSFT"]
INTERVAL = "1d"
START = datetime.now(tz=timezone.utc) - timedelta(days=5)
END = datetime.now(tz=timezone.utc)


@pytest.mark.integration
def test_yfinance_price_adapter_returns_AssetPrices():
    repo = YfinancePrice()

    prices = list(
        repo.get_prices(
            symbol=SYMBOLS[0],
            interval=INTERVAL,
            start=START,
            end=END,
        )
    )

    assert prices, "Nenhum preço retornado pelo YfinancePrice."

    first = prices[0]
    assert isinstance(first, AssetPrice)
    assert first.listing.symbol == SYMBOLS[0].upper()
    assert first.listing.currency is not None
    assert first.listing.exchange is not None


@pytest.mark.integration
def test_price_router_returns_repo_and_repo_fetches_prices():
    # Router deve escolher o adapter correto para o symbol
    repo = price_router(SYMBOLS[0])

    prices = list(
        repo.get_prices(
            symbol=SYMBOLS[0],
            interval=INTERVAL,
            start=START,
            end=END,
        )
    )

    assert prices, "Nenhum preço retornado pelo repo do price_router."

    first = prices[0]
    assert isinstance(first, AssetPrice)
    assert first.listing.symbol == SYMBOLS[0].upper()
