import time

import typer

from src.config import logger
from src.external_data.application.usecases import (
    ExecuteAllExtractions,
    ExecuteBatchExtract,
    ListExtractDefinitions,
    PrepareExtractionParams,
    StoreExtractBatch,
)
from src.external_data.infrastructure.composition_root import (
    build_definition_repository,
    build_extract_param_resolver,
    build_extractor_resolver,
    build_result_storage,
    build_sys_clock,
    load_extract_config,
)

app = typer.Typer()


@app.command()
def main():
    start_time = time.time()
    logger.info("Starting raw data loading...")

    try:
        _clock = build_sys_clock()
        _config = load_extract_config()

        _list_definitions = ListExtractDefinitions(definitions_repo=build_definition_repository())

        _prepare_params = PrepareExtractionParams(
            params_resolver=build_extract_param_resolver(clock=_clock)
        )

        _execute_batch = ExecuteBatchExtract(
            executor_resolver=build_extractor_resolver(),
            clock=_clock,
        )

        _store_batch = StoreExtractBatch(result_store=build_result_storage())

        use_case = ExecuteAllExtractions(
            list_definitions=_list_definitions,
            prepare_params=_prepare_params,
            execute_batch=_execute_batch,
            store_batch=_store_batch,
        )

        use_case.execute(_config)

    except Exception:
        logger.exception("Raw data loading failed")
        raise

    finally:
        elapsed_time = time.time() - start_time
        logger.info(f"Total time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    app()
