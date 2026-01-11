import datetime
import time
from typing import Any, Mapping

from loguru import logger
import typer

from src.extraction.domain.value_objects import ModelSource

from src.extraction.application.usecases import BatchExtractService
from src.extraction.application.interfaces import ExtractorRouter

from src.extraction.infrastructure.routing import DefaultExtractionRouter
from src.extraction.infrastructure.repositories import LocalModelRouteRepository
from src.extraction.infrastructure.extractors.yfinance import YFinanceCandlesSeries
from src.extraction.infrastructure.storages import LocalExtractionResultStorage

app = typer.Typer()


def build_router() -> ExtractorRouter:
    """
    Composition root for extractor routing.

    Registers available extractors and returns
    a router capable of resolving them by ModelRoute.
    """
    return DefaultExtractionRouter(
        extractors=[
            YFinanceCandlesSeries(),
        ]
    )

def build_repository():
    """
    Composition root for repositories.

    Registers and returns data repositories.
    """
    return LocalModelRouteRepository()

def build_storage():
    """
    Composition root for result storage.
    Registers and returns result storage implementations.
    """
    return LocalExtractionResultStorage()

@app.command()
def main(
    route_id: str | None = None,
):
    """
    CLI entry point for batch data extraction.

    This command resolves extraction routes, executes
    batch extraction through the application use case,
    and reports execution time and status.
    """
    start_time = time.time()
    logger.info("Starting raw data loading...")

    try:
        #if not route_id:
        #    raise ValueError("route_id must be provided")

        #logger.info(f"Processing route ID: {route_id}")

        # --- Route resolution (placeholder) -----------------
        repository = build_repository()
        router = build_router()
        storage = build_storage()

        service = BatchExtractService(router)

        # --- Technical extraction parameters ----------------
        params: Mapping[str, Any] = {
            "start": datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
            "end": datetime.datetime.now(datetime.timezone.utc),
            "time_window": "1d",
        }

        for route in repository.by_source(ModelSource("yfinance")):
            results = service.extract_batch([route], params)
            logger.success(
                f"Extraction completed for {len(results)} route(s)"
            )

            storage.store(results)
        

    except Exception as e:
        logger.exception("Raw data loading failed")
        raise

    finally:
        elapsed_time = time.time() - start_time
        logger.info(f"Total time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    app()
