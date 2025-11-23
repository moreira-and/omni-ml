# src/dataset/application/use_cases/get_prices_uc.py
from datetime import datetime
from typing import Iterable

from src.dataset.application.dtos import PricesQueryDto
from src.dataset.domain.entities import PriceBarFact
from src.dataset.domain.interfaces import PriceReadRepository


class GetPricesMultipleTickers:
    def __init__(self, price_repo: PriceReadRepository) -> None:
        self._price_repo = price_repo

    def get_prices(
        self,
        query: PricesQueryDto,
    ) -> Iterable[PriceBarFact]:
        # aqui é só orquestração de domínio

        result: Iterable[PriceBarFact] = []

        for ticker in query.tickers:
            partial_result = self._price_repo.get_prices(
                ticker=ticker,
                interval=query.interval,
                start=query.start,
                end=query.end,
            )
            result = list(result) + list(partial_result)

        return result
