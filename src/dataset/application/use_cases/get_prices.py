from typing import Iterable

from src.dataset.application.dtos import PricesQueryDto
from src.dataset.domain.interfaces import PriceReadRepository
from src.dataset.domain.value_objects import PriceBarFact


class GetPricesMultipleTickers:
    def __init__(self, price_repo: PriceReadRepository) -> None:
        self._price_repo = price_repo

    def get_prices(
        self,
        query: PricesQueryDto,
    ) -> Iterable[PriceBarFact]:
        # aqui é só orquestração de domínio

        result: Iterable[PriceBarFact] = []

        for ticker in query.codes:
            partial_result = self._price_repo.get_prices(
                code=ticker,
                interval=query.interval,
                start=query.start,
                end=query.end,
            )
            result = list(result) + list(partial_result)

        return result
