from src.dataset.domain.interfaces.economic_unit_repository import (
    AssetPriceReadRepository,
)
from src.dataset.infrastructure.price.yfinance_price import YfinancePrice


def price_router(ticker: str) -> AssetPriceReadRepository:
    match ticker:
        case t if t in YfinancePrice.valid_tickers():
            return YfinancePrice()
        case _:
            raise ValueError(f"Unknown price source: {ticker}")
