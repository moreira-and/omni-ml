from typing import List



from ..domain.entities import ModelRoute
from ..application.interfaces import ModelExtractor, ExtractorRouter
from .extractors.yfinance import YFinanceCandlesSeries
from .extractors.bcb import BcbLoadingStrategy


class DefaultExtractionRouter(ExtractorRouter):
    def __init__(self, extractors: List[ModelExtractor] | None = None):
        self._extractors = extractors or [
            YFinanceCandlesSeries(),
            BcbLoadingStrategy()
        ]

    def get_extractor(self, route: ModelRoute) -> ModelExtractor:
        for extractor in self._extractors:
            if (
                extractor.type == route.type
                and extractor.source == route.source
            ):
                return extractor

        raise ValueError(
            f"No extractor found for type={route.type} source={route.source}"
        )
