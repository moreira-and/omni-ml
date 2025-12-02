from enum import Enum


class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    BOND = "BOND"
    FX = "FX"
    OTHER = "OTHER"
