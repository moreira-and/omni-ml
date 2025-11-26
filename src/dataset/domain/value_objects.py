from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class CountryIndicator:
    country_code: str
    ts: datetime
    name: str
    value: Decimal
    ...


@dataclass(frozen=True, slots=True)
class AssetIndicator:
    symbol: str
    ts: datetime
    name: str
    value: Decimal
    ...


@dataclass(frozen=True, slots=True)
class AssetListing:
    """Identifica um ativo negociado em uma bolsa específica."""

    symbol: str  # "AAPL", "MSFT34", "PETR4.SA"
    exchange: str  # "NASDAQ", "NYSE", "B3"
    currency: str  # "USD", "BRL"


@dataclass(frozen=True, slots=True)
class AssetPrice:
    """Barra de preço (OHLCV) de um ativo em um intervalo de tempo."""

    listing: AssetListing

    interval: str  # "1min" | "5min" | "1h" | "1d"
    ts: datetime  # UTC, period end
    close: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    volume: int

    def __post_init__(self) -> None:
        if self.close < 0:
            raise ValueError("close não pode ser negativo.")

        if self.volume < 0:
            raise ValueError("volume não pode ser negativo.")

        if self.high < self.low:
            raise ValueError("high não pode ser menor que low.")

        if not (self.low <= self.open <= self.high):
            raise ValueError("open deve estar em [low, high].")

        if not (self.low <= self.close <= self.high):
            raise ValueError("close deve estar em [low, high].")

        if self.ts.tzinfo is None or self.ts.utcoffset() is None:
            raise ValueError("ts deve ser timezone-aware em UTC.")
