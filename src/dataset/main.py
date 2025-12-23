from datetime import datetime, timedelta
from pathlib import Path
import time

from loguru import logger
import typer
import yaml

from src.config import PROJ_ROOT, mlflow
from src.dataset.application import AssetBuilder
from src.dataset.domain.enums import CandleInterval
from src.dataset.infrastructure.asset import LocalFileAssetRepository
from src.dataset.infrastructure.candle import CandleByYfinance

app = typer.Typer()


@app.command()
def main(
    # ----  DEFAULT PATHS --------------------------
    config_path: Path = PROJ_ROOT / "config/dataset.yaml",
    # ----------------------------------------------
):
    # -----------------------------------------
    start_time = time.time()
    logger.info("Starting raw data loading...")

    try:
        # Load external configuration
        config = yaml.safe_load(open(config_path))
        interval = CandleInterval.ONE_DAY
        start_ts = datetime.today() - timedelta(days=10)
        end_ts = datetime.today() - timedelta(days=1)

        builder = AssetBuilder(CandleByYfinance())
        repo = LocalFileAssetRepository()

        for key, value in config.items():
            logger.info(f"{key}: {value}")

            if key == "yfinance":
                for name, code in value.items():
                    logger.info(f"{name}: {code}")

                    asset = builder.build_by_symbol(
                        symbol=code,
                        interval=interval,
                        start_ts=start_ts,
                        end_ts=end_ts,
                    )

                    repo.save(asset)

                    logger.info(f"Asset {code} with candles from {start_ts} to {end_ts} saved.")

        """
        settings = DatasetSettings(**config)

        # Build pipeline according to Clean Architecture
        pipeline, context = build_dataset_pipeline(settings)

        logger.info("Starting dataset pipeline...")
        pipeline.run(context)
        """
    except Exception as e:
        logger.error(f"Dataset pipeline failed: {e}")
        raise

    logger.success("Raw data successfully loaded...")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Total time taken: {elapsed_time:.2f} seconds")

    if mlflow.active_run() is not None:
        mlflow.log_metric("data_loading_time_seconds", elapsed_time)
        mlflow.log_artifact(str(config_path), artifact_path="configs")


if __name__ == "__main__":
    app()
