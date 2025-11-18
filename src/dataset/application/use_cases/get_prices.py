# src/dataset/application/use_cases/get_prices_uc.py
from datetime import datetime
from typing import Iterable

from src.dataset.application.dtos import PricesQueryDto
from src.dataset.domain.entities import IPriceBarFact
from src.dataset.domain.interfaces import PriceReadRepository


class GetPrices:
    def __init__(self, price_repo: PriceReadRepository) -> None:
        self._price_repo = price_repo

    def get_prices(
        self,
        query: PricesQueryDto,
    ) -> Iterable[IPriceBarFact]:
        # aqui é só orquestração de domínio
        return self._price_repo.get_prices(
            ticker=query.ticker,
            bar=query.bar,
            start=query.start,
            end=query.end,
        )
