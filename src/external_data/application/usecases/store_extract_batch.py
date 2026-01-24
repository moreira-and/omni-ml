from ....config import logger
from ...domain.models import ExtractBatch
from ..errors import ApplicationError
from ..interfaces import ExtractResultStore


class StoreExtractBatch:
    def __init__(
        self,
        result_store: ExtractResultStore,
    ):
        self._result_store = result_store

    def execute(self, batch: ExtractBatch) -> None:
        try:
            self._result_store.store(batch)
        except ApplicationError as e:
            logger.exception(e)
            raise
