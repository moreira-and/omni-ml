from abc import ABC, abstractmethod

from ...domain.entities import ExtractDefinition
from ...domain.params import ExtractParams


class ExtractParamsResolver(ABC):
    @abstractmethod
    def resolve(
        self,
        definition: ExtractDefinition,
        config: dict[str, object],
    ) -> ExtractParams: ...
