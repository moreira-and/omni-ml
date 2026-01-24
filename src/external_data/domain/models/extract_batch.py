from datetime import datetime

from ..entities.extract_definition import ExtractDefinition
from .base import DomainModel
from ..params import ExtractParams


class ExtractBatch:
    def __init__(
        self,
        *,
        definition: ExtractDefinition,
        params: ExtractParams,
        results: list[DomainModel],
        executed_at: datetime,
    ):
        self._definition = definition
        self._params = params
        self._results = results
        self._executed_at = executed_at

    @property
    def definition(self) -> ExtractDefinition:
        return self._definition

    @property
    def params(self) -> ExtractParams:
        return self._params

    @property
    def results(self) -> list[DomainModel]:
        return self._results

    @property
    def executed_at(self) -> datetime:
        return self._executed_at

    def has_results(self) -> bool:
        return any(True for _ in self._results)
