from abc import ABC, abstractmethod
from typing import TypeVar, Iterable

from ..entities import ExtractDefinition
from ..value_objects import ExternalCode
from ..enums import ExternalSource
from ..models.base import DomainModel

TModel = TypeVar("TModel", bound=DomainModel)

class ExtractDefinitionRepository(ABC):

    @abstractmethod
    def find_by_code(self, code: ExternalCode) -> Iterable[ExtractDefinition]:
        ...

    @abstractmethod
    def find_by_source(self, source: ExternalSource) -> Iterable[ExtractDefinition]:
        ...

    @abstractmethod
    def all(self) -> Iterable[ExtractDefinition]:
        ...

    @abstractmethod
    def save(self, definition: ExtractDefinition) -> None:
        ...