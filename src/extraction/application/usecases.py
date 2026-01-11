from typing import Any, Mapping
from datetime import datetime, timezone

from ..domain.entities import ModelRoute
from ..domain.models import ExtractionBatch
from .interfaces import ExtractorRouter


class BatchExtractService:
    """
    Application service responsible for executing batch data extractions
    based on a set of model routes.

    This use case orchestrates the extraction flow by:
    - Resolving the appropriate ModelExtractor for each ModelRoute
      using the ExtractorRouter.
    - Delegating the extraction execution to the resolved extractor.
    - Aggregating the results per route.

    This service does not contain extraction logic itself.
    It coordinates routing and execution, keeping policies centralized
    in the router and behavior in the extractors.

    Parameters passed to extractors are treated as technical criteria
    and interpreted by each concrete extractor implementation.

    This use case is designed for batch-oriented execution, where
    multiple routes may be processed independently within a single call.
    """
    
    def __init__(self, router: ExtractorRouter) -> None:
        self._router = router

    def extract_batch(
        self,
        route: ModelRoute,
        params: Mapping[str, Any] | None = None,
    ) -> ExtractionBatch:

        try:
            extractor = self._router.get_extractor(route)
        except ValueError:
            return ExtractionBatch(
                executed_at=self._now(),
                results={}
            )

        result = extractor.extract(route, params)

        return ExtractionBatch(
            executed_at=self._now(),
            results={route: result}
        )

    @staticmethod
    def _now():
        return datetime.now(timezone.utc)
    
    


from ..domain.enums import TimeWindow
from datetime import timedelta

class ExtractionService:
    def __init__(self, config, clock, router):
        self._config = config
        self._clock = clock
        self._router = router

    def extract_batch(self, route: ModelRoute) -> ExtractionBatch:
        params = self._build_params(route.type.value)

        extractor = self._router.get_extractor(route)
        results = extractor.extract(route, params)

        return ExtractionBatch(
            executed_at=self._clock.now(),
            results={route: results},
        )

    def _build_params(self, model_type: str) -> dict:
        cfg = self._config[model_type]

        end = self._clock.now()
        start = end - timedelta(days=cfg["lookback_days"])

        return {
            "start": start,
            "end": end,
            "time_window": TimeWindow[cfg["time_window"]],
        }
