from abc import ABC, abstractmethod
from typing import TypeVar,Generic, Iterable, Mapping, Any

from ..entities import ExtractDefinition
from ..enums import ExternalSource, DataKind
from ..models.base import DomainModel

TModel = TypeVar("TModel", bound=DomainModel)


## 2. Define Extractor interface
class ExtractExecutor(ABC, Generic[TModel]):

    @abstractmethod
    def execute(self, definition: ExtractDefinition, params: Mapping[str, Any] | None = None) -> Iterable[TModel]:
        ...

    @property
    @abstractmethod
    def source(self) -> ExternalSource:
        ...   

    @property
    @abstractmethod
    def data_kind(self) -> DataKind:
        ...