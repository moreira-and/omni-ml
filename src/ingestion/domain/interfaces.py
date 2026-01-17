from abc import ABC, abstractmethod
from typing import Iterable

from .entities import ModelRouteDefinition
from .enums import ModelSource
from .value_objects import ModelCode

class ModelRouteRepository(ABC):

    @abstractmethod
    def by_code(self, code: ModelCode) -> Iterable[ModelRouteDefinition]:
        """
        Retorna todas as policies associadas a um código.
        A decisão de prioridade/fallback é do domínio.
        """
        ...

    @abstractmethod
    def by_source(self, source: ModelSource) -> Iterable[ModelRouteDefinition]:
        """
        Retorna todas as policies associadas a uma origem.
        A decisão de prioridade/fallback é do domínio.
        """
        ...

    @abstractmethod
    def save(self, route: ModelRouteDefinition) -> None:
        ...
