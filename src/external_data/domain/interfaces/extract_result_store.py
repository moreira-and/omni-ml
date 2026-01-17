from abc import ABC, abstractmethod

from ..entities import ExtractBatch

class ExtractResultStore(ABC):
    @abstractmethod
    def store(self, batch: ExtractBatch) -> None:
        ...