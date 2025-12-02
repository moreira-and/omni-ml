from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from ..enums import CandleInterval


@dataclass(frozen=True, slots=True)
class ListingPrice:
    """Barra de preço (OHLCV) de uma listing em um intervalo de tempo."""

    instrument_symbol: str  # deve casar com EconomicUnitListing.instrument_symbol
    interval: CandleInterval  # "1min" | "5min" | "1h" | "1d" | ...
    ts: datetime  # UTC, period end
    close: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    volume: int

    def __post_init__(self) -> None:
        # symbol
        if not self.instrument_symbol or not self.instrument_symbol.strip():
            raise ValueError("ListingPrice.instrument_symbol não pode ser vazio.")
        symbol_norm = self.instrument_symbol.strip().upper()
        if symbol_norm != self.instrument_symbol:
            object.__setattr__(self, "instrument_symbol", symbol_norm)

        # interval (mínimo: não vazio; regra mais forte pode vir depois)
        if not self.interval or not self.interval.strip():
            raise ValueError("ListingPrice.interval não pode ser vazio.")
        interval_norm = self.interval.strip()
        if interval_norm != self.interval:
            object.__setattr__(self, "interval", interval_norm)

        # OHLCV invariants
        if self.close < 0:
            raise ValueError("ListingPrice.close não pode ser negativo.")

        if self.volume < 0:
            raise ValueError("ListingPrice.volume não pode ser negativo.")

        if self.high < self.low:
            raise ValueError("ListingPrice.high não pode ser menor que low.")

        if not (self.low <= self.open <= self.high):
            raise ValueError("ListingPrice.open deve estar em [low, high].")

        if not (self.low <= self.close <= self.high):
            raise ValueError("ListingPrice.close deve estar em [low, high].")

        # ts: UTC, precisão em minutos
        if self.ts.tzinfo is None or self.ts.utcoffset() is None:
            raise ValueError("ListingPrice.ts deve ser timezone-aware em UTC.")
        if self.ts.tzinfo is not timezone.utc:
            object.__setattr__(self, "ts", self.ts.astimezone(timezone.utc))
        if self.ts.second != 0 or self.ts.microsecond != 0:
            raise ValueError(
                "ListingPrice.ts deve ter precisão em minutos " "(second == 0 e microsecond == 0)."
            )
