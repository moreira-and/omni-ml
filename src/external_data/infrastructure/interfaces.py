from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime


from ..domain.entities import ExternalDataExtractDefinition
from ..domain.models import CandleStick, Indicator

from ..application.interfaces import DataExtractor


class CandlesExtractor(DataExtractor, ABC):

    
    @abstractmethod
    def extract_between(self, route: ExternalDataExtractDefinition, start:datetime, end:datetime) -> Iterable[CandleStick]:
        ...


class IndicatorExtractor(DataExtractor, ABC):

    @abstractmethod
    def extract_between(self, route: ExternalDataExtractDefinition, start:datetime, end:datetime) -> Iterable[Indicator]:
        ...