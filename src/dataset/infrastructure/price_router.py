from src.dataset.domain.interfaces import PriceReadRepository
from src.dataset.infrastructure.yfinance_price import YfinancePrice


def price_router(ticker: str) -> PriceReadRepository:
    match ticker:
        case t if t in YfinancePrice.valid_tickers():
            return YfinancePrice()
        case _:
            raise ValueError(f"Unknown price source: {ticker}")
