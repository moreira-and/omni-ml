from abc import ABC, abstractmethod

from src.dataset.domain.value_objects import Batch


class Dataset(ABC):
    @abstractmethod
    def load(self) -> Batch: ...
