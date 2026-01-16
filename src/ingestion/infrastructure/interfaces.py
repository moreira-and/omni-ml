from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime


from ..domain.entities import ModelRouteDefinition
from ..domain.enums import TimeWindow
from ..domain.models import CandleStick, Indicator

from ..application.interfaces import ModelExtractor


class CandlesExtractor(ModelExtractor, ABC):

    
    @abstractmethod
    def extract_between(self, route: ModelRouteDefinition, start:datetime, end:datetime, time_window: TimeWindow) -> Iterable[CandleStick]:
        ...


class IndicatorExtractor(ModelExtractor, ABC):

    @abstractmethod
    def extract_between(self, route: ModelRouteDefinition, start:datetime, end:datetime, time_window: TimeWindow) -> Iterable[Indicator]:
        ...