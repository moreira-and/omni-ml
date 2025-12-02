from datetime import datetime
from decimal import Decimal
from typing import Iterable, List, Optional

from loguru import logger
import pandas as pd
import yfinance as yf

from src.dataset.domain.interfaces.economic_unit_repository import (
    AssetPriceReadRepository,
)
from src.dataset.domain.value_objects import AssetListing, AssetPrice


class YfinancePrice(AssetPriceReadRepository):
    """Adapter de infraestrutura para leitura de preços via yfinance.

    Responsabilidade:
        - Consumir yfinance (Pandas) como fonte de dados.
        - Converter os dados em value objects de domínio (`AssetPrice` + `AssetListing`).
        - Normalizar timestamps para UTC (period end).

    Limitações/assunções:
        - A heurística de `exchange` e `currency` é simplificada; pode ser refinada
          no futuro usando `yf.Ticker(symbol).fast_info` ou configuração externa.
    """

    def __init__(self) -> None:
        super().__init__()

    def _build_listing(self, symbol: str) -> AssetListing:
        """Heurística simples para mapear symbol -> AssetListing.

        Ajuste conforme o domínio:
            - ".SA" → B3/BRL
            - fallback → exchange genérica "YF" e moeda "USD"
        """
        symbol_norm = symbol.strip().upper()

        if symbol_norm.endswith(".SA"):
            return AssetListing(
                symbol=symbol_norm,
                exchange="B3",
                currency="BRL",
            )

        # fallback genérico; refine conforme necessidade
        return AssetListing(
            symbol=symbol_norm,
            exchange="YF",
            currency="USD",
        )

    def get_prices(
        self,
        *,
        symbol: str,
        interval: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[AssetPrice]:
        """
        Lê preços históricos de uma listagem (symbol) via yfinance
        e devolve uma coleção de `AssetPrice` ordenada por timestamp.

        Args:
            symbol:
                Código negociado da listagem (ex.: "AAPL", "PETR4.SA").
            interval:
                Intervalo temporal ("1d", "1h", "5m", etc.).
            start:
                Data/hora inicial (inclusiva).
            end:
                Data/hora final (opcional).

        Returns:
            Iterable[AssetPrice]:
                Sequência de barras de preço normalizadas para o domínio.
        """
        listing = self._build_listing(symbol)

        try:
            df = yf.download(
                symbol,
                start=start,
                end=end,
                auto_adjust=True,
                interval=interval,
                progress=False,
            )

            if df.empty:
                logger.warning(
                    "[YfinancePrice] No data returned for "
                    f"symbol={symbol}, interval={interval}, "
                    f"start={start}, end={end}"
                )
                return []

            # Garante índice em UTC (period end)
            idx = df.index
            if idx.tz is None:
                idx = idx.tz_localize("UTC")
            else:
                idx = idx.tz_convert("UTC")

            # Normaliza colunas (MultiIndex -> nível de preço)
            if isinstance(df.columns, pd.MultiIndex):
                if "Ticker" in df.columns.names:
                    df = df.droplevel("Ticker", axis=1)
                else:
                    df.columns = df.columns.get_level_values(0)

            results: List[AssetPrice] = []

            # itertuples é mais eficiente que iterrows
            for ts, row in zip(idx, df.itertuples(index=False), strict=False):
                # Converte floats para Decimal
                close_ = Decimal(str(row.Close))

                open_: Optional[Decimal] = (
                    Decimal(str(row.Open)) if not pd.isna(row.Open) else None
                )
                high: Optional[Decimal] = Decimal(str(row.High)) if not pd.isna(row.High) else None
                low_: Optional[Decimal] = Decimal(str(row.Low)) if not pd.isna(row.Low) else None

                volume_: Optional[int] = None
                if hasattr(row, "Volume") and not pd.isna(row.Volume):
                    volume_ = int(row.Volume)

                results.append(
                    AssetPrice(
                        interval=interval,
                        ts=ts.to_pydatetime(),  # já em UTC
                        close=close_,
                        open=open_,
                        high=high,
                        low=low_,
                        volume=volume_,
                        listing=listing,
                    )
                )

            # __post_init__ de AssetPrice já deve garantir invariantes e ordenação
            # (ou a ordenação aqui é mantida pelo índice crescente do yfinance).
            return results

        except Exception as e:
            logger.error(
                "[YfinancePrice] Error loading yfinance data for "
                f"symbol={symbol}, interval={interval}, "
                f"start={start}, end={end}: {e}"
            )
            raise

    @staticmethod
    def valid_tickers() -> List[str]:
        """Lista de symbols de exemplo aceitos pelo adapter."""
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
