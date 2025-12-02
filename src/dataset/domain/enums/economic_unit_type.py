from enum import Enum


class EconomicUnitType(str, Enum):
    SOVEREIGN = "SOVEREIGN"  # País / governo (ex.: "BR", "US")
    CORPORATE = "CORPORATE"  # Empresa / corporação (ex.: "PETR", "MSFT")
    SUPRANATIONAL = "SUPRANATIONAL"  # BID, FMI, etc.
    OTHER = "OTHER"
