from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class EconomicUnitCategories:
    """Ponto de série temporal de indicador de uma unidade econômica
    (soberana, corporativa ou supranacional)."""

    economic_unit_id: UUID  # referencia EconomicUnit.id
