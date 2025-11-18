from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class IPriceBarFact:
    ticker: str  # ex.: "AAPL", "MSFT"
    bar: str  # ex.: "1min" | "5min" | "1h" | "1d"
    ts: datetime  # período de referência (normalizado para "period end" UTC, precisão em minutos)
    close: Decimal
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    volume: Optional[int] = None
    id: UUID = field(default_factory=uuid4)

    def body(self) -> Decimal:
        return self.close - self.open

    def is_bullish(self) -> bool:
        return self.close > self.open

    def __post_init__(self):
        # Invariantes de preço/volume
        if self.close < 0:
            raise ValueError("close cannot be negative.")
        if self.volume is not None and self.volume < 0:
            raise ValueError("volume cannot be negative.")
        if self.high is not None and self.low is not None and self.high < self.low:
            raise ValueError("high cannot be lower than low.")
        # Se open/high/low existem, verifique inclusão do close
        if self.low is not None and self.close < self.low:
            raise ValueError("close cannot be below low.")
        if self.high is not None and self.close > self.high:
            raise ValueError("close cannot be above high.")
        if self.open is not None and self.low is not None and self.high is not None:
            if not (self.low <= self.open <= self.high):
                raise ValueError("open must lie within [low, high].")
