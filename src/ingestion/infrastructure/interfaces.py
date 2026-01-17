from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime


from ..domain.entities import ModelRouteDefinition
from ..domain.models import CandleStick, Indicator

from ..application.interfaces import ModelExtractor


class CandlesExtractor(ModelExtractor, ABC):

    
    @abstractmethod
    def extract_between(self, route: ModelRouteDefinition, start:datetime, end:datetime) -> Iterable[CandleStick]:
        ...


class IndicatorExtractor(ModelExtractor, ABC):

    @abstractmethod
    def extract_between(self, route: ModelRouteDefinition, start:datetime, end:datetime) -> Iterable[Indicator]:
        ...