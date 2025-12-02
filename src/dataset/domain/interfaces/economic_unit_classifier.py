from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities import EconomicUnit
from ..value_objects import EconomicUnitCategories


class EconomicUnitClassifier(ABC):

    @abstractmethod
    def classify(self, unit: EconomicUnit) -> EconomicUnitCategories: ...
