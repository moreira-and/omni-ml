from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime


from ..domain.entities import ModelRoute
from ..domain.enums import TimeWindow
from ..domain.models import CandleStick

from ..application.interfaces import ModelExtractor


class CandlesExtractor(ModelExtractor, ABC):

    
    @abstractmethod
    def extract_between(self, route: ModelRoute, start:datetime, end:datetime, time_window: TimeWindow) -> Iterable[CandleStick]:
        ...

