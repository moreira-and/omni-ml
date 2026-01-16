from typing import Any, Iterable, Mapping
from abc import ABC, abstractmethod

from ..domain.entities import ModelRouteDefinition
from ..domain.value_objects import ModelSource
from ..domain.enums import ModelType


## 2. Define ModelExtractor interface
class ModelExtractor(ABC):

    @abstractmethod
    def extract(self, route: ModelRouteDefinition, params: Mapping[str, Any] | None = None) -> Iterable[Any]:
        ...

    @property
    @abstractmethod
    def source(self) -> ModelSource:
        ...   

    @property
    @abstractmethod
    def type(self) -> ModelType:
        ...

## 1. Define ExtractorRouter interface
class ExtractorRouter(ABC):
    @abstractmethod
    def get_extractor(self, route: ModelRouteDefinition) -> ModelExtractor:
        ...


class ExtractionResultStorage(ABC):
    @abstractmethod
    def store(self, results: Mapping[ModelRouteDefinition, Any]) -> None:
        ...
