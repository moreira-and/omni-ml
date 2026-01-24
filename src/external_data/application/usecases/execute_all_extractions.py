from typing import Any

from ....config import logger
from ..errors import ApplicationError
from .execute_batch_extract import ExecuteBatchExtract
from .list_extract_definitions import ListExtractDefinitions
from .prepare_extraction_params import PrepareExtractionParams
from .store_extract_batch import StoreExtractBatch


class ExecuteAllExtractions:
    def __init__(
        self,
        list_definitions: ListExtractDefinitions,
        prepare_params: PrepareExtractionParams,
        execute_batch: ExecuteBatchExtract,
        store_batch: StoreExtractBatch,
    ):
        self._list_definitions = list_definitions
        self._prepare_params = prepare_params
        self._execute_batch = execute_batch
        self._store_batch = store_batch

    def execute(self, extract_config: dict[str, Any]) -> None:
        """
        Executes extraction for all registered definitions.

        - Resolves params per definition
        - Executes extraction
        - Persists resulting batch
        """

        for definition in self._list_definitions.execute():
            try:
                # 1. Prepare params for this definition
                params = self._prepare_params.execute(
                    definition=definition,
                    config=extract_config,
                )

                # 2. Execute extraction (returns ExtractBatch)
                batch = self._execute_batch.execute(
                    definition=definition,
                    params=params,
                )

                # 3. Persist batch
                self._store_batch.execute(batch)

            except ApplicationError as e:
                logger.exception(f"Extraction failed for definition {definition}")
                continue
