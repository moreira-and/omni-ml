import time

from loguru import logger
import typer

from src.external_data.application.usecases import BatchExtractService, RunExternalDataExtractionBatch
from src.external_data.domain.interfaces import ExtractionRouter

from src.external_data.infrastructure.resolver import DefaultExtractionRouter
from src.external_data.infrastructure.repositories.csv_extract_definition_repository import LocalRouteRepository
from src.external_data.infrastructure.storage.csv_result_storage import LocalResultStorage


from src.external_data.infrastructure.extractors.yfinance_extraction import YFinanceCandlesSeries
from src.external_data.infrastructure.extractors.bcb_extraction import BcbLoadingStrategy

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

build_extractor = lambda: BatchExtractService(build_router())

def SystemClock():
    from datetime import datetime, timezone         
    return datetime.now(timezone.utc)

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
        use_case = RunExternalDataExtractionBatch(
            repository=build_repository(),
            extractor=build_extractor(),
            storage=build_storage(),
            clock=SystemClock(),
        )      

        use_case.execute(lookback_days=days)

    except Exception as e:
        logger.exception("Raw data loading failed")
        raise

    finally:
        elapsed_time = time.time() - start_time
        logger.info(f"Total time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    app()
