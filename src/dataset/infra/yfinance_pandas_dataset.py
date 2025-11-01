import pandas as pd
import yfinance as yf

from src.config import logger
from src.dataset.domain.interfaces import Dataset
from src.dataset.domain.value_objects import Batch


class YfinancePandasDataset(Dataset):
    def __init__(self, ticker, start_date: str, end_date: str, interval="1d"):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval

    def load(self) -> Batch:
        df = pd.DataFrame()
        try:
            df = yf.download(
                self.ticker,
                start=self.start_date,
                end=self.end_date,
                auto_adjust=True,
                interval=self.interval,
            )  # return pd.DataFrame
            if not df.empty:
                df.columns = df.columns.get_level_values(0)
                df["Ticker"] = self.ticker
            else:
                logger.warning(f"No data returned for {self.ticker}")
        except Exception as e:
            logger.error(f"Error loading {self.ticker}: {e}")

        return Batch(X=df)
