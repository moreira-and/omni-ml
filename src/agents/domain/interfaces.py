from abc import ABC, abstractmethod
from typing import Dict, Any

class Agent(ABC):
    name: str

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
