"""
Domain: Dataset / Market

Este módulo define as entidades de domínio centrais relacionadas a ativos financeiros
e países, usadas como raiz de agregados para associar séries de preços (PriceBarFact)
e indicadores macroeconômicos (MacroeconomicIndicatorFact).

Ubiquitous language:
- FinancialAsset: representa um ativo negociado identificado por código em bolsa.
- Country: representa um país emissor / mercado, associado a indicadores macroeconômicos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from src.dataset.domain.value_objects import (
    AssetIndicatorFact,
    MacroeconomicIndicatorFact,
    PriceBarFact,
)

DOMAIN_SCHEMA = """
{
  "bounded_context": "dataset.market",
  "entities": {
    "Asset": {
      "role": "aggregate_root",
      "identity": ["code", "exchange"],
      "relations": {
        "prices": "list[PriceBarFact]",
        "indicators": "list[AssetIndicatorFact]"
      }
    },
    "Country": {
      "role": "aggregate_root",
      "identity": ["code"],
      "relations": {
        "indicators": "list[MacroeconomicIndicatorFact]"
      }
    }
  }
}
"""


@dataclass(frozen=True, slots=True)
class Asset:
    """Financial asset aggregate root.

    Representa um ativo financeiro identificado por um código (ticker),
    podendo estar associado a uma bolsa, moeda e séries de preços / indicadores.

    Attributes:
        code:
            Código único do ativo no mercado (ticker), ex.: "AAPL", "PETR4".
            Deve ser único dentro de um mesmo `exchange`.
        name:
            Nome descritivo do ativo, ex.: "Apple Inc.", "Petrobras PN".
        exchange:
            Identificador da bolsa/mercado onde o ativo é negociado,
            ex.: "NASDAQ", "NYSE", "B3".
        currency:
            Código da moeda base de negociação do ativo, ex.: "USD", "BRL".
        prices:
            Coleção de barras de preço históricas (`PriceBarFact`) associadas a este ativo.
            Pode ser `None` quando o agregado é carregado sem histórico.
        indicators:
            Coleção de indicadores macroeconômicos (`MacroeconomicIndicatorFact`)
            relevantes para este ativo (ex.: juros, inflação).
        id:
            Identificador interno imutável do agregado (UUID v4).
    """

    code: str  # ex.: "AAPL", "MSFT"
    name: Optional[str] = None  # ex.: "Apple Inc.", "Microsoft Corporation"
    exchange: Optional[str] = None  # ex.: "NASDAQ", "NYSE"
    currency: Optional[str] = None  # ex.: "BRL", "USD"
    prices: Optional[list[PriceBarFact]] = None  # Historical price data
    indicators: Optional[list[AssetIndicatorFact]] = None  # Related indicators
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class Country:
    """Country aggregate root.

    Representa um país e seus metadados relevantes para o domínio financeiro,
    incluindo moeda, séries de preços agregadas e indicadores macroeconômicos.

    Attributes:
        code:
            Código ISO 3166-1 alfa-2 do país, ex.: "BR", "US".
        name:
            Nome do país em maiúsculas ou em inglês, ex.: "BRAZIL", "UNITED STATES".
        currency:
            Código da moeda oficial principal, ex.: "BRL", "USD".
        prices:
            Séries de preços agregadas relacionadas ao país (quando aplicável),
            representadas por `PriceBarFact`.
        indicators:
            Indicadores macroeconômicos nacionais (`MacroeconomicIndicatorFact`),
            ex.: PIB, inflação, taxa de juros.
        id:
            Identificador interno imutável do agregado (UUID v4).
    """

    code: Optional[str]  # ex.: "BR", "US"
    name: Optional[str] = None  # ex.: "BRAZIL", "USA"
    currency: Optional[str] = None  # ex.: "BRL", "USD"
    prices: Optional[list[PriceBarFact]] = None  # Price data for assets in the country
    indicators: Optional[list[MacroeconomicIndicatorFact]] = (
        None  # Macroeconomic indicators for the country
    )
    id: UUID = field(default_factory=uuid4)
