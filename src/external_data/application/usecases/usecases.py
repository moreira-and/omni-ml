from typing import Any, Mapping
from datetime import datetime, timezone, timedelta
from ...domain.entities.extract_definition import ExtractDefinition
from ...domain.models.models import ExtractionBatch
from ...domain.interfaces import ExtractionRouter

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
    
    def __init__(self, router: ExtractionRouter) -> None:
        self._router = router

    def execute(
        self,
        route: ExtractDefinition,
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
    


class RunExternalDataExtractionBatch:
    def __init__(
        self,
        repository,
        extractor,
        storage,
        clock,
    ):
        self._repository = repository
        self._extractor = extractor
        self._storage = storage
        self._clock = clock

    def execute(self, *, lookback_days: int) -> None:
        params = self._build_params(lookback_days)

        for definition in self._repository.all():
            batch = self._extractor.extract(definition, params)

            if not batch.results:
                continue

            self._storage.store(batch)

    def _build_params(self, lookback_days: int):
        end = self._clock.now()
        start = end - timedelta(days=lookback_days)

        return {
            "start": start,
            "end": end,
        }
