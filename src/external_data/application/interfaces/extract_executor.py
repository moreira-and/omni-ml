from abc import ABC, abstractmethod
from typing import Generic, Iterable

from ...domain.entities import ExtractDefinition
from ...domain.enums import DataKind, ExternalSource
from ...domain.models import TModel
from ...domain.params import ExtractParams


## 2. Define Extractor interface
class ExtractExecutor(ABC, Generic[TModel]):

    @abstractmethod
    def execute(
        self, definition: ExtractDefinition, params: ExtractParams
    ) -> Iterable[TModel]: ...

    @property
    @abstractmethod
    def source(self) -> ExternalSource: ...

    @property
    @abstractmethod
    def data_kind(self) -> DataKind: ...
