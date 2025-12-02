from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import re
from typing import ClassVar
from uuid import UUID


@dataclass(frozen=True, slots=True)
class EconomicUnitIndicator:
    """Ponto de série temporal de indicador de uma unidade econômica
    (soberana, corporativa ou supranacional)."""

    economic_unit_id: UUID  # referencia EconomicUnit.id
    ts: datetime  # UTC, precisão em minutos
    name: str  # ex.: "DEBT_GDP", "ROIC", "RATING_S&P"
    value: Decimal

    _NAME_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z0-9_.\-]+$")

    def __post_init__(self) -> None:
        # --- name ---
        if not self.name or not self.name.strip():
            raise ValueError("EconomicUnitIndicator.name não pode ser vazio.")

        name_norm = self.name.strip().upper()
        if not self._NAME_PATTERN.match(name_norm):
            raise ValueError(
                f"EconomicUnitIndicator.name inválido: {self.name!r}. "
                "Use apenas [A-Z0-9_.-], ex.: 'DEBT_GDP', 'ROIC', 'RATING_S&P'."
            )
        if name_norm != self.name:
            object.__setattr__(self, "name", name_norm)

        # --- ts: UTC, precisão em minutos ---
        if self.ts.tzinfo is None or self.ts.utcoffset() is None:
            raise ValueError("EconomicUnitIndicator.ts deve ser timezone-aware em UTC.")
        if self.ts.tzinfo is not timezone.utc:
            # normaliza para UTC se vier com outro tz
            object.__setattr__(self, "ts", self.ts.astimezone(timezone.utc))
        if self.ts.second != 0 or self.ts.microsecond != 0:
            raise ValueError(
                "EconomicUnitIndicator.ts deve ter precisão em minutos "
                "(second == 0 e microsecond == 0)."
            )

        # --- value: Decimal finito ---
        if not isinstance(self.value, Decimal):
            try:
                normalized = Decimal(str(self.value))
            except (InvalidOperation, TypeError) as e:
                raise ValueError(f"EconomicUnitIndicator.value inválido: {self.value!r}") from e
            object.__setattr__(self, "value", normalized)

        if self.value.is_nan() or not self.value.is_finite():
            raise ValueError(
                f"EconomicUnitIndicator.value deve ser finito, recebido: {self.value!r}"
            )
