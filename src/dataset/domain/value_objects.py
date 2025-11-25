from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import re
from typing import ClassVar, Optional


@dataclass(frozen=True, slots=True)
class PriceBarFact:
    """Barra de preço (OHLCV) de um ativo em um intervalo de tempo."""

    code: str  # "AAPL", "PETR4.SA"
    interval: str  # "1min" | "5min" | "1h" | "1d"
    ts: datetime  # UTC, period end, precisão em minutos
    close: Decimal
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    volume: Optional[int] = None

    def __post_init__(self) -> None:
        # exemplo de invariantes mínimos
        if not self.code or not self.code.strip():
            raise ValueError("PriceBarFact.ticker não pode ser vazio.")

        if self.close < 0:
            raise ValueError("close não pode ser negativo.")

        if self.volume is not None and self.volume < 0:
            raise ValueError("volume não pode ser negativo.")

        if self.high is not None and self.low is not None and self.high < self.low:
            raise ValueError("high não pode ser menor que low.")

        if self.low is not None and self.close < self.low:
            raise ValueError("close não pode ser menor que low.")

        if self.high is not None and self.close > self.high:
            raise ValueError("close não pode ser maior que high.")

        if self.open is not None and self.low is not None and self.high is not None:
            if not (self.low <= self.open <= self.high):
                raise ValueError("open deve estar em [low, high].")


@dataclass(frozen=True, slots=True)
class AssetIndicatorFact:
    """Ponto de série temporal de indicador macroeconômico para um país."""

    code: str  # "AAPL", "PETR4.SA"
    ts: datetime  # UTC, precisão em minutos
    name: str  # "ROI", "VOLATILITY"
    value: Decimal

    _NAME_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z0-9_.\-]+$")

    def __post_init__(self) -> None:
        # code
        if not self.code or not self.code.strip():
            raise ValueError("code não pode ser vazio.")
        code_norm = self.code.strip().upper()
        if code_norm != self.code:
            object.__setattr__(self, "code", code_norm)

        # name
        if not self.name or not self.name.strip():
            raise ValueError("name não pode ser vazio.")
        name_norm = self.name.strip().upper()
        if not self._NAME_PATTERN.match(name_norm):
            raise ValueError(
                f"name inválido: {self.name!r}. "
                "Use apenas [A-Z0-9_.-], ex.: 'SELIC', 'IPCA_MENSAL', 'CPI-CORE'."
            )
        if name_norm != self.name:
            object.__setattr__(self, "name", name_norm)

        # ts: UTC + minutos
        if self.ts.tzinfo is None or self.ts.utcoffset() is None:
            raise ValueError("ts deve ser timezone-aware em UTC.")
        if self.ts.second != 0 or self.ts.microsecond != 0:
            raise ValueError("ts deve ter precisão em minutos (second == 0, microsecond == 0).")

        # value: Decimal finito
        if not isinstance(self.value, Decimal):
            from decimal import InvalidOperation

            try:
                normalized = Decimal(str(self.value))
            except (InvalidOperation, TypeError) as e:
                raise ValueError(f"value inválido: {self.value!r}") from e
            object.__setattr__(self, "value", normalized)

        if self.value.is_nan() or not self.value.is_finite():
            raise ValueError(f"value deve ser finito, recebido: {self.value!r}")


@dataclass(frozen=True, slots=True)
class MacroeconomicIndicatorFact:
    """Ponto de série temporal de indicador macroeconômico para um país."""

    country: str  # "BRAZIL", "USA"
    ts: datetime  # UTC, precisão em minutos
    name: str  # "SELIC", "CPI", "GDP"
    value: Decimal

    _NAME_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z0-9_.\-]+$")

    def __post_init__(self) -> None:
        # country
        if not self.country or not self.country.strip():
            raise ValueError("country não pode ser vazio.")
        country_norm = self.country.strip().upper()
        if country_norm != self.country:
            object.__setattr__(self, "country", country_norm)

        # name
        if not self.name or not self.name.strip():
            raise ValueError("name não pode ser vazio.")
        name_norm = self.name.strip().upper()
        if not self._NAME_PATTERN.match(name_norm):
            raise ValueError(
                f"name inválido: {self.name!r}. "
                "Use apenas [A-Z0-9_.-], ex.: 'SELIC', 'IPCA_MENSAL', 'CPI-CORE'."
            )
        if name_norm != self.name:
            object.__setattr__(self, "name", name_norm)

        # ts: UTC + minutos
        if self.ts.tzinfo is None or self.ts.utcoffset() is None:
            raise ValueError("ts deve ser timezone-aware em UTC.")
        if self.ts.second != 0 or self.ts.microsecond != 0:
            raise ValueError("ts deve ter precisão em minutos (second == 0, microsecond == 0).")

        # value: Decimal finito
        if not isinstance(self.value, Decimal):
            from decimal import InvalidOperation

            try:
                normalized = Decimal(str(self.value))
            except (InvalidOperation, TypeError) as e:
                raise ValueError(f"value inválido: {self.value!r}") from e
            object.__setattr__(self, "value", normalized)

        if self.value.is_nan() or not self.value.is_finite():
            raise ValueError(f"value deve ser finito, recebido: {self.value!r}")
