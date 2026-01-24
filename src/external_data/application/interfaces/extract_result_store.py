from abc import ABC, abstractmethod

from ...domain.models.batchs import ExtractBatch


class ExtractResultStore(ABC):
    @abstractmethod
    def store(self, batch: ExtractBatch) -> None: ...
