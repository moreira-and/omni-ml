from abc import ABC, abstractmethod
from typing import Generic

from ...domain.entities import ExtractDefinition
from ...domain.models.schemas import TModel
from .extract_executor import ExtractExecutor


## 1. Define ExtractorResolver interface
class ExtractExecutorResolver(ABC, Generic[TModel]):
    @abstractmethod
    def resolve(self, definition: ExtractDefinition) -> ExtractExecutor[TModel]: ...
