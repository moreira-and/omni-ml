from typing import Iterable

from ...domain.entities import ExtractDefinition
from ..interfaces import ExtractDefinitionRepository


class ListExtractDefinitions:
    def __init__(
        self,
        definitions_repo: ExtractDefinitionRepository,
    ):
        self._definitions_repo = definitions_repo

    def execute(self) -> Iterable[ExtractDefinition]:
        return self._definitions_repo.all()
