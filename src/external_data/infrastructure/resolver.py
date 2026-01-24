from typing import List



from ..domain.entities.extract_definition import ExtractDefinition
from ..domain.interfaces import DataExtractor, ExtractionRouter
from .extractors.yfinance_candle_extractor import YFinanceCandlesSeries
from .extractors.bcb_candle_extractor import BcbLoadingStrategy


class DefaultExtractionRouter(ExtractionRouter):
    def __init__(self, extractors: List[DataExtractor] | None = None):
        self._extractors = extractors or [
            YFinanceCandlesSeries(),
            BcbLoadingStrategy()
        ]

    def get_extractor(self, route: ExtractDefinition) -> DataExtractor:
        for extractor in self._extractors:
            if (
                extractor.get_by_kind == route.data_kind
                and extractor.get_by_source == route.source
            ):
                return extractor

        raise ValueError(
            f"No extractor found for type={route.data_kind} source={route.source}"
        )
