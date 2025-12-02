from __future__ import annotations

from dataclasses import dataclass
import re
from typing import ClassVar
from uuid import UUID

from ..enums import InstrumentType


@dataclass(frozen=True, slots=True)
class EconomicUnitListing:
    """Listing de instrumento associado a uma unidade econômica.

    Exemplos:
        - UNIT: EconomicUnit(id de PETROBRAS, CORPORATE, BR)
          instrument_symbol: "PETR4.SA", exchange: "B3", currency: "BRL"
        - UNIT: EconomicUnit(id dos EUA, SOVEREIGN)
          instrument_symbol: "US10Y", exchange: "UST", currency: "USD"
        - FX (visão local): "BRL/USD", "USD/BRL"
    """

    economic_unit_id: UUID  # referencia EconomicUnit.id
    exchange: str  # "NASDAQ", "NYSE", "B3", "CME", ...
    currency: str  # "USD", "BRL", ...
    instrument_symbol: str  # "AAPL", "MSFT34", "PETR4.SA", "BRL/USD"
    instrument_type: InstrumentType

    _CURRENCY_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z]{3}$")

    def __post_init__(self) -> None:
        # exchange
        if not self.exchange or not self.exchange.strip():
            raise ValueError("EconomicUnitListing.exchange não pode ser vazio.")
        exchange_norm = self.exchange.strip().upper()
        if exchange_norm != self.exchange:
            object.__setattr__(self, "exchange", exchange_norm)

        # currency (ISO-4217-like)
        if not self.currency or not self.currency.strip():
            raise ValueError("EconomicUnitListing.currency não pode ser vazio.")
        currency_norm = self.currency.strip().upper()
        if not self._CURRENCY_PATTERN.match(currency_norm):
            raise ValueError(
                f"EconomicUnitListing.currency inválido: {self.currency!r}. "
                "Use códigos de 3 letras, ex.: 'USD', 'BRL'."
            )
        if currency_norm != self.currency:
            object.__setattr__(self, "currency", currency_norm)

        # instrument_symbol
        if not self.instrument_symbol or not self.instrument_symbol.strip():
            raise ValueError("EconomicUnitListing.instrument_symbol não pode ser vazio.")
        symbol_norm = self.instrument_symbol.strip().upper()
        if self.is_fx():
            # convenção rígida FX: "BASE/QUOTE"
            parts = symbol_norm.split("/")
            if len(parts) != 2 or not all(p and self._CURRENCY_PATTERN.match(p) for p in parts):
                raise ValueError(
                    "Para FX, EconomicUnitListing.instrument_symbol deve ser 'BASE/QUOTE', "
                    "ex.: 'BRL/USD', 'USD/BRL'."
                )
        else:
            # para não-FX, evita ambiguidade com códigos tipo "AAA/BBB"
            if "/" in symbol_norm:
                raise ValueError(
                    "instrument_symbol não deve conter '/' para instrument_type != FX."
                )

        if symbol_norm != self.instrument_symbol:
            object.__setattr__(self, "instrument_symbol", symbol_norm)

    def is_fx(self) -> bool:
        return self.instrument_type == InstrumentType.FX

    def fx_currencies(self) -> tuple[str, str] | None:
        """Retorna (base, quote) se for FX, caso contrário None."""
        if not self.is_fx():
            return None
        base, quote = self.instrument_symbol.split("/")
        return base, quote
