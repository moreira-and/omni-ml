from typing import Any, Iterable, Mapping
from abc import ABC, abstractmethod

from ..domain.entities import ExternalDataExtractDefinition
from ..domain.enums import ExternalSource, DataKind

## 2. Define DataExtractor interface
class DataExtractor(ABC):

    @abstractmethod
    def extract(self, route: ExternalDataExtractDefinition, params: Mapping[str, Any] | None = None) -> Iterable[Any]:
        ...

    @property
    @abstractmethod
    def get_by_source(self) -> ExternalSource:
        ...   

    @property
    @abstractmethod
    def get_by_kind(self) -> DataKind:
        ...

## 1. Define ExtractionRouter interface
class ExtractionRouter(ABC):
    @abstractmethod
    def get_extractor(self, route: ExternalDataExtractDefinition) -> DataExtractor:
        ...


class ExtractionResultStorage(ABC):
    @abstractmethod
    def store_data(self, results: Mapping[ExternalDataExtractDefinition, Any]) -> None:
        ...
