from typing import Any, Iterable, Mapping

from ..domain.entities import ModelRoute
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
    
    def __init__(self, router: ExtractorRouter):
        self._router = router

    def extract_batch(
            self,
            routes: Iterable[ModelRoute],
            params: Mapping[str, Any] | None = None
        ) -> dict[ModelRoute, Any]:
        
        results = {}
        for route in routes:
            extractor = self._router.get_extractor(route)
            results[route] = extractor.extract(route, params)
        return results