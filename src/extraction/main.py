from  datetime import datetime, timezone, timedelta
import time
from typing import Any, Mapping

from loguru import logger
import typer

from src.extraction.application.usecases import BatchExtractService
from src.extraction.application.interfaces import ExtractorRouter

from src.extraction.infrastructure.routing import DefaultExtractionRouter
from src.extraction.infrastructure.repositories import LocalRouteRepository
from src.extraction.infrastructure.extractors.yfinance import YFinanceCandlesSeries
from src.extraction.infrastructure.storages import LocalResultStorage

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
    return LocalRouteRepository()

def build_storage():
    """
    Composition root for result storage.
    Registers and returns result storage implementations.
    """
    return LocalResultStorage()

@app.command()
def main(
    days: int = typer.Option(30, help="Number of days to look back for data extraction."),
    time_window: str = typer.Option("1d", help="Time window for data extraction.")
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
        # --- Route resolution (placeholder) -----------------
        repository = build_repository()
        router = build_router()
        storage = build_storage()

        # --- services ----------------------
        service = BatchExtractService(router)

        # --- Technical extraction parameters ----------------
        # DEBITE: These should be part of a configuration object BY TYPE
        params: Mapping[str, Any] = {
            "start": datetime.now(timezone.utc) - timedelta(days=days),
            "end": datetime.now(timezone.utc),
            "time_window": time_window,
        }

        for route in repository.all():
            batch = service.extract_batch(route, params)
            if not batch.results:
                logger.warning(f"No results for route ({route.type.value}, {route.source.value}, {route.name.value})")
                continue
            else:
                logger.success(
                    f"Extraction completed for route ({route.type.value}, {route.source.value}, {route.name.value}) "
                )

                storage.store(batch)

        logger.success("Raw data loading completed successfully.")        

    except Exception as e:
        logger.exception("Raw data loading failed")
        raise

    finally:
        elapsed_time = time.time() - start_time
        logger.info(f"Total time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    app()
