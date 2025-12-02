from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from src.dataset.domain.entities import EconomicUnit


class EconomicUnitRepository(ABC):

    @abstractmethod
    def get_by_id(self, unit_id: UUID) -> Optional[EconomicUnit]:
        """Retorna a EconomicUnit pelo UUID ou None se não encontrada."""
        ...

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[EconomicUnit]:
        """Retorna a EconomicUnit pelo código (ex.: 'BR', 'PETR')."""
        ...

    @abstractmethod
    def list_all(self) -> Iterable[EconomicUnit]:
        """Lista todas as unidades econômicas conhecidas."""
        ...
