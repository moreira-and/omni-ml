from  datetime import datetime, timezone, timedelta
import time
from typing import Any, Mapping

from loguru import logger
import typer

from src.external_data.application.usecases import BatchExtractService
from src.external_data.application.interfaces import ExtractionRouter

from src.external_data.infrastructure.routing import DefaultExtractionRouter
from src.external_data.infrastructure.repositories import LocalRouteRepository
from src.external_data.infrastructure.storages import LocalResultStorage


from src.external_data.infrastructure.extractors.yfinance import YFinanceCandlesSeries
from src.external_data.infrastructure.extractors.bcb import BcbLoadingStrategy

app = typer.Typer()


def build_router() -> ExtractionRouter:
    """
    Composition root for extractor routing.

    Registers available extractors and returns
    a router capable of resolving them by ModelRoute.
    """
    return DefaultExtractionRouter(
        extractors=[
            YFinanceCandlesSeries(),
            BcbLoadingStrategy()
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
            "end": datetime.now(timezone.utc)
        }

        for route in repository.all():
            batch = service.extract_batch(route, params)
            if not batch.results:
                logger.warning(f"No results for route ({route.data_kind.value}, {route.source.value}, {route.alias.value})")
                continue
            else:
                logger.success(
                    f"Extraction completed for route ({route.data_kind.value}, {route.source.value}, {route.alias.value}) "
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
