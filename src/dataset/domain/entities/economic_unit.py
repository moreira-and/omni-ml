from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple
from uuid import UUID, uuid4

from ..enums import EconomicUnitType
from ..value_objects import (
    EconomicUnitCategories,
    EconomicUnitIndicator,
    EconomicUnitListing,
)


@dataclass(frozen=True, slots=True)
class EconomicUnit:
    """Aggregate root de unidade econômica (soberana ou corporativa).

    Exemplos:
        - SOVEREIGN: "BRAZIL", "UNITED STATES"
        - CORPORATE: "Petróleo Brasileiro S.A.", "Apple Inc."

    Pode emitir ativos financeiros (títulos, ações, etc.) e possuir
    indicadores e categorias próprias.
    """

    id: UUID = field(default_factory=uuid4)

    code: str  # "BR", "US", "PETR", "MSFT"
    name: str  # "BRAZIL", "Petróleo Brasileiro S.A."
    unit_type: EconomicUnitType  # SOVEREIGN, CORPORATE, ...

    indicators: Tuple[EconomicUnitIndicator, ...] = field(default_factory=tuple)
    listings: Tuple[EconomicUnitListing, ...] = field(default_factory=tuple)
    categories: Optional[EconomicUnitCategories] = None
