import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

import yfinance as yf

from ....config import RAW_DATA_DIR, logger
from ...domain.entities import Asset
from ...domain.enums import CandleInterval
from ...domain.interfaces import AssetRepository, Candle


class LocalFileAssetRepository(AssetRepository):

    def get_by_symbol(self, symbol: str) -> Iterable[Asset]:
        file_path = RAW_DATA_DIR / f"{symbol}_data.csv"

        if not file_path.exists():
            return []  # ou raise, dependendo do contrato

        def candle_iterator():
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield Candle(
                        ts=datetime.fromisoformat(row["ts"]),
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row["volume"]),
                        interval=CandleInterval(row["interval"]),
                    )

        yield Asset(symbol=symbol, candles=candle_iterator())

    def save(self, asset: Asset) -> None:
        file_path = RAW_DATA_DIR / f"{asset.symbol}_data.csv"
        with open(file_path, "w") as f:
            f.write("ts,open,high,low,close,volume,interval\n")
            for candle in asset.candles:
                f.write(
                    f"{candle.ts},{candle.open},{candle.high},{candle.low},"
                    f"{candle.close},{candle.volume},{candle.interval.value}\n"
                )
        logger.info(f"Asset data for {asset.symbol} saved to {file_path}")

    def delete_by_symbol(self, symbol: str) -> None:
        file_path = RAW_DATA_DIR / f"{symbol}_data.csv"

        if not file_path.exists():
            return  # idempotente: delete inexistente não é erro

        file_path.unlink()
