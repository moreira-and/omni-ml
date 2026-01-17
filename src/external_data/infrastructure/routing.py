from typing import List



from ..domain.entities import ExternalDataExtractDefinition
from ..application.interfaces import DataExtractor, ExtractionRouter
from .extractors.yfinance import YFinanceCandlesSeries
from .extractors.bcb import BcbLoadingStrategy


class DefaultExtractionRouter(ExtractionRouter):
    def __init__(self, extractors: List[DataExtractor] | None = None):
        self._extractors = extractors or [
            YFinanceCandlesSeries(),
            BcbLoadingStrategy()
        ]

    def get_extractor(self, route: ExternalDataExtractDefinition) -> DataExtractor:
        for extractor in self._extractors:
            if (
                extractor.get_by_kind == route.data_kind
                and extractor.get_by_source == route.source
            ):
                return extractor

        raise ValueError(
            f"No extractor found for type={route.data_kind} source={route.source}"
        )
