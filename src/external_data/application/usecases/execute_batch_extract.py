from ....config import logger
from ...domain.models.batchs import ExtractBatch
from ..clocks import Clock
from ..errors import ApplicationError
from ..interfaces import ExtractExecutorResolver


class ExecuteBatchExtract:
    def __init__(
        self,
        executor_resolver: ExtractExecutorResolver,
        clock: Clock,
    ):
        self._executor_resolver = executor_resolver
        self._clock = clock

    def execute(self, definition, params) -> ExtractBatch:
        requested_at = self._clock.now()

        try:
            executor = self._executor_resolver.resolve(definition)

            results = list(executor.execute(definition, params, clock=self._clock))
            if not results:
                raise ApplicationError("Extraction returned no results")

            return ExtractBatch(
                definition=definition,
                params=params,
                results=results,
                executed_at=self._clock.now(),
            )

        except ApplicationError as e:
            logger.exception(e)
            raise

        finally:
            definition.mark_as_requested(requested_at)
