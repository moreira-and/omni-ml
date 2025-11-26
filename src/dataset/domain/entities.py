from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple
from uuid import UUID, uuid4

from .value_objects import AssetIndicator, AssetListing, AssetPrice, CountryIndicator


@dataclass(frozen=True, slots=True)
class Country:
    """Aggregate root de país."""

    code: str  # ex.: "BR", "US"
    name: str  # ex.: "BRAZIL", "UNITED STATES"
    indicators: Tuple[CountryIndicator, ...] = field(default_factory=tuple)

    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class Asset:
    """Aggregate root de ativo financeiro."""

    name: str  # ex.: "Apple Inc.", "Microsoft Corporation"
    listings: Tuple[AssetListing, ...]  # múltiplas listagens (cross-listing)

    country_code: Optional[str] = None  # ex.: "US", "BR"
    prices: Tuple[AssetPrice, ...] = field(default_factory=tuple)
    indicators: Tuple[AssetIndicator, ...] = field(default_factory=tuple)

    id: UUID = field(default_factory=uuid4)
