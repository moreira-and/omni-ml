from abc import ABC, abstractmethod
from typing import Iterable

from .entities import ModelRoute
from .value_objects import ModelCode, RouteId, ModelSource

class ModelRouteRepository(ABC):

    @abstractmethod
    def by_id(self, id: RouteId) -> ModelRoute:
        ...

    @abstractmethod
    def by_code(self, code: ModelCode) -> Iterable[ModelRoute]:
        """
        Retorna todas as policies associadas a um código.
        A decisão de prioridade/fallback é do domínio.
        """
        ...

    @abstractmethod
    def by_source(self, source: ModelSource) -> Iterable[ModelRoute]:
        """
        Retorna todas as policies associadas a uma origem.
        A decisão de prioridade/fallback é do domínio.
        """
        ...

    @abstractmethod
    def save(self, route: ModelRoute) -> None:
        ...
