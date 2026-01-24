from abc import ABC, abstractmethod

from ...domain.entities import ExtractBatch


class ExtractResultStore(ABC):
    @abstractmethod
    def store(self, batch: ExtractBatch) -> None: ...
