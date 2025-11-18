from datetime import datetime
from decimal import Decimal
from typing import Iterable, List

from loguru import logger
import pandas as pd
import yfinance as yf

from src.dataset.domain.entities import IPriceBarFact
from src.dataset.domain.interfaces import PriceReadRepository


class YfinancePrice(PriceReadRepository):
    def __init__(self) -> None:
        super().__init__()

    def get_prices(
        self,
        *,
        ticker: str,
        bar: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[IPriceBarFact]:
        """
        Adapter de infraestrutura:
        - Usa yfinance (Pandas) internamente
        - Retorna apenas entidades de domínio (PriceBarFact)
        """
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=True,
                interval=bar,
                progress=False,
            )

            if df.empty:
                logger.warning(
                    f"[PriceYfinance] No data returned for "
                    f"ticker={ticker}, bar={bar}, "
                    f"start={start}, end={end}"
                )
                return []

            # Garante índice em UTC (period end)
            idx = df.index
            if idx.tz is None:
                idx = idx.tz_localize("UTC")
            else:
                idx = idx.tz_convert("UTC")

            # Normaliza as colunas
            if isinstance(df.columns, pd.MultiIndex):
                # como o exemplo veio com names=['Price', 'Ticker'],
                # basta derrubar o nível 'Ticker'
                if "Ticker" in df.columns.names:
                    df = df.droplevel("Ticker", axis=1)
                else:
                    # fallback: pega só o primeiro nível
                    df.columns = df.columns.get_level_values(0)

            # itertuples é mais eficiente que iterrows
            results: List[IPriceBarFact] = []
            for ts, row in zip(idx, df.itertuples(index=False), strict=False):
                # row.<col> vem como float; convertemos para Decimal
                close = Decimal(str(row.Close))

                open_ = Decimal(str(row.Open)) if not pd.isna(row.Open) else None
                high = Decimal(str(row.High)) if not pd.isna(row.High) else None
                low = Decimal(str(row.Low)) if not pd.isna(row.Low) else None

                volume = None
                if hasattr(row, "Volume") and not pd.isna(row.Volume):
                    volume = int(row.Volume)

                results.append(
                    IPriceBarFact(
                        ticker=ticker,
                        bar=bar,
                        ts=ts.to_pydatetime(),  # já em UTC
                        close=close,
                        open=open_,
                        high=high,
                        low=low,
                        volume=volume,
                    )
                )

            return results

        except Exception as e:
            logger.error(
                f"[PriceYfinance] Error loading yfinance data for "
                f"ticker={ticker}, bar={bar}, "
                f"start={start}, end={end}: {e}"
            )
            raise

    @staticmethod
    def valid_tickers() -> List[str]:
        return [
            "AAPL",
            "^BVSP",
            "^IXIC",
            "^GSPC",
            "^DJI",
            "BTC-USD",
            "EURUSD=X",
            "GC=F",
            "SI=F",
            "HG=F",
            "CL=F",
            "HO=F",
            "NG=F",
            "RB=F",
            "SB=F",
            "ZC=F",
            "ZR=F",
            "ZS=F",
            "KC=F",
            "LE=F",
            "HE=F",
            "CT=F",
            "ZB=F",
        ]
