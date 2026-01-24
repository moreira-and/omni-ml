from abc import ABC, abstractmethod
from typing import Any, Dict


class Agent(ABC):
    name: str

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
