from abc import ABC, abstractmethod
from typing import TypeVar,Generic

from . import ExtractExecutor
from ..entities import ExtractDefinition
from ..models.base import DomainModel

TModel = TypeVar("TModel", bound=DomainModel)

## 1. Define ExtractorResolver interface
class ExtractResolver(ABC, Generic[TModel]):
    @abstractmethod
    def resolve(self, definition: ExtractDefinition) -> ExtractExecutor[TModel]:
        ...