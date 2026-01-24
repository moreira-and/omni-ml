from abc import ABC, abstractmethod
from typing import Iterable

from ...domain.entities import ExtractDefinition
from ...domain.enums import ExternalSource
from ...domain.value_objects import ExternalCode


class ExtractDefinitionRepository(ABC):

    @abstractmethod
    def find_by_code(self, code: ExternalCode) -> Iterable[ExtractDefinition]: ...

    @abstractmethod
    def find_by_source(self, source: ExternalSource) -> Iterable[ExtractDefinition]: ...

    @abstractmethod
    def all(self) -> Iterable[ExtractDefinition]: ...

    @abstractmethod
    def save(self, definition: ExtractDefinition) -> None: ...
