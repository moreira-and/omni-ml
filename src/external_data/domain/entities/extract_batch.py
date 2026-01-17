from datetime import datetime
from typing import Mapping, Iterable
from .extract_definition import ExtractDefinition
from ..models.base import DomainModel


class ExtractBatch:
    def __init__(
        self,
        *,
        executed_at: datetime,
        results: Mapping[ExtractDefinition, Iterable[DomainModel]],
    ):
        self._executed_at = executed_at
        self._results = results

    @property
    def executed_at(self) -> datetime:
        return self._executed_at

    @property
    def results(self) -> Mapping[ExtractDefinition, Iterable[DomainModel]]:
        return self._results

    def has_results(self) -> bool:
        return any(True for _ in self._results.values())
