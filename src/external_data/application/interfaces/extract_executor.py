from abc import ABC, abstractmethod
from typing import Generic, Iterable

from ...application.clocks import Clock
from ...domain.entities import ExtractDefinition
from ...domain.enums import DataKind, ExternalSource
from ...domain.models.params import ExtractParams
from ...domain.models.schemas import TModel


## 2. Define Extractor interface
class ExtractExecutor(ABC, Generic[TModel]):

    @abstractmethod
    def execute(
        self, definition: ExtractDefinition, params: ExtractParams, clock: Clock
    ) -> Iterable[TModel]: ...

    @property
    @abstractmethod
    def source(self) -> ExternalSource: ...

    @property
    @abstractmethod
    def data_kind(self) -> DataKind: ...
