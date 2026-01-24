from abc import ABC, abstractmethod

from ...domain.entities import ExtractDefinition
from ..params import ExtractParams


class ExtractParamsResolver(ABC):
    @abstractmethod
    def resolve(
        self,
        definition: ExtractDefinition,
        config: dict[str, object],
    ) -> ExtractParams: ...
