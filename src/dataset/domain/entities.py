from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class PriceBarFact:
    ticker: str  # ex.: "AAPL", "MSFT"
    interval: str  # ex.: "1min" | "5min" | "1h" | "1d"
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


from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
import re
from typing import ClassVar
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class MacroeconomicIndicatorFact:
    country: str  # ex.: "BRAZIL", "USA"
    ts: datetime  # período de referência (UTC, precisão em minutos)
    name: str  # ex.: "SELIC", "CPI", "GDP"
    value: Decimal
    id: UUID = field(default_factory=uuid4)

    # Regras do domínio (não são dados, são constantes da classe)
    _ALLOWED_INTERVALS: ClassVar[set[str]] = {
        # intraday
        "1min",
        "5min",
        "15min",
        "30min",
        "1h",
        "4h",
        # diário / maior
        "1d",
        "1wk",
        "1mo",
        "3mo",
        "6mo",
        "1y",
    }

    # Convenção de nome de indicador (opcional, mas saudável):
    # letras, dígitos, underscore, ponto e hífen (ex.: "SMA_20", "RSI.14", "MACD-12_26_9")
    _NAME_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z0-9_.\-]+$")

    def __post_init__(self) -> None:
        # --- ticker ---
        if not self.country or not self.country.strip():
            raise ValueError("IndicatorFact.ticker não pode ser vazio.")

        ticker_norm = self.country.strip().upper()
        if ticker_norm != self.country:
            object.__setattr__(self, "ticker", ticker_norm)

        # --- name ---
        if not self.name or not self.name.strip():
            raise ValueError("IndicatorFact.name não pode ser vazio.")

        name_norm = self.name.strip().upper()
        if not self._NAME_PATTERN.match(name_norm):
            raise ValueError(
                f"IndicatorFact.name inválido: {self.name!r}. "
                "Use apenas [A-Z0-9_.-], ex.: 'SMA_20', 'RSI_14'."
            )
        if name_norm != self.name:
            object.__setattr__(self, "name", name_norm)

        # --- ts: UTC, precisão em minutos ---
        if self.ts.tzinfo is None or self.ts.utcoffset() is None:
            raise ValueError("IndicatorFact.ts deve ser timezone-aware em UTC.")

        if self.ts.second != 0 or self.ts.microsecond != 0:
            raise ValueError(
                "IndicatorFact.ts deve ter precisão em minutos "
                "(second == 0 e microsecond == 0)."
            )

        # --- value: Decimal válido e finito ---
        if not isinstance(self.value, Decimal):
            try:
                normalized = Decimal(str(self.value))
            except (InvalidOperation, TypeError) as e:
                raise ValueError(f"IndicatorFact.value inválido: {self.value!r}") from e
            object.__setattr__(self, "value", normalized)

        if self.value.is_nan() or not self.value.is_finite():
            raise ValueError(f"IndicatorFact.value deve ser finito, recebido: {self.value!r}")

        # --- id ---
        if not isinstance(self.id, UUID):
            raise ValueError("IndicatorFact.id deve ser um UUID válido.")
