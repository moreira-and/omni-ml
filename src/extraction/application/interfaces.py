from typing import Any, Mapping
from abc import ABC, abstractmethod

from ..domain.entities import ModelRoute
from ..domain.value_objects import ModelSource
from ..domain.enums import ModelType


## 2. Define ModelExtractor interface
class ModelExtractor(ABC):

    @abstractmethod
    def extract(self, route: ModelRoute, params: Mapping[str, Any] | None = None) -> Any:
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
    def get_extractor(self, route: ModelRoute) -> ModelExtractor:
        ...


class ExtractionResultStorage(ABC):
    @abstractmethod
    def store(self, results: Mapping[ModelRoute, Any]) -> None:
        ...
