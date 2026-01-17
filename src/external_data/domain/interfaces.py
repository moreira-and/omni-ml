from abc import ABC, abstractmethod
from typing import Iterable

from .entities import ExternalDataExtractDefinition
from .enums import ExternalSource
from .value_objects import ExternalCode

class ExtractDefinitionRepository(ABC):

    @abstractmethod
    def by_code(self, code: ExternalCode) -> Iterable[ExternalDataExtractDefinition]:
        """
        Retorna todas as policies associadas a um código.
        A decisão de prioridade/fallback é do domínio.
        """
        ...

    @abstractmethod
    def by_source(self, source: ExternalSource) -> Iterable[ExternalDataExtractDefinition]:
        """
        Retorna todas as policies associadas a uma origem.
        A decisão de prioridade/fallback é do domínio.
        """
        ...

    @abstractmethod
    def save(self, route: ExternalDataExtractDefinition) -> None:
        ...
