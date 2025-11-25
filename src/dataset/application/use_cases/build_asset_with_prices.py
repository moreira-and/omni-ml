# src/dataset/application/use_cases/build_asset_with_prices.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional

from src.dataset.domain.entities import Asset
from src.dataset.domain.interfaces import PriceReadRepository
from src.dataset.domain.value_objects import PriceBarFact


@dataclass(slots=True)
class BuildAssetWithPrices:
    """Use case: construir um Asset e carregar seu histórico de preços.

    Responsabilidades:
        - Consultar o repositório de preços para um code em um intervalo de tempo.
        - Ordenar as barras por timestamp.
        - (Opcional) Verificar consistência entre o code do Asset e das barras.
        - Retornar um agregado `Asset` completamente construído.

    Ubiquitous language:
        - "asset" = agregado Asset identificado por `code` (code).
        - "prices" = lista de `PriceBarFact` normalizados pelo domínio.

    Dependências:
        - PriceReadRepository: porta de leitura de preços (infra adaptável).
    """

    price_repo: PriceReadRepository

    def __call__(
        self,
        *,
        code: str,
        interval: str,
        start: datetime,
        end: Optional[datetime] = None,
        name: Optional[str] = None,
        exchange: Optional[str] = None,
        currency: Optional[str] = None,
    ) -> Asset:
        """Executa o caso de uso.

        Args:
            code:
                code do ativo (asset code), ex.: "AAPL", "PETR4".
                Será usado como `code` na chamada ao repositório.
            interval:
                Intervalo temporal das barras, ex.: "1d", "1h".
                Encaminhado diretamente para o `PriceReadRepository`.
            start:
                Data/hora inicial (inclusiva) da janela de preços.
            end:
                Data/hora final (opcional) da janela de preços.
                Quando None, o repositório deve trazer até o último dado disponível.
            name:
                Nome descritivo opcional do ativo.
            exchange:
                Bolsa/mercado em que o ativo é negociado.
            currency:
                Moeda base de negociação do ativo.

        Returns:
            Asset:
                Instância de `Asset` com os metadados fornecidos e a lista
                de `PriceBarFact` já carregada e ordenada por `ts`.

        Raises:
            ValueError:
                - Se alguma barra de preço tiver code inconsistente (quando
                  o VO `PriceBarFact` expõe o atributo `code`).
        """
        raw_prices: Iterable[PriceBarFact] = self.price_repo.get_prices(
            code=code,
            interval=interval,
            start=start,
            end=end,
        )

        # Normaliza para lista e ordena por timestamp
        prices: List[PriceBarFact] = sorted(raw_prices, key=lambda bar: bar.ts)

        # Validação opcional de consistência (só roda se PriceBarFact tiver .code)
        for bar in prices:
            bar_code = getattr(bar, "code", None)
            if bar_code is not None and bar_code != code:
                raise ValueError(
                    f"Inconsistent code in PriceBarFact: expected {code!r}, got {bar_code!r}"
                )

        # Como Asset é frozen, já construímos com preços no construtor
        asset = Asset(
            code=code,
            name=name,
            exchange=exchange,
            currency=currency,
            prices=prices,
            # indicators pode ser carregado em outro caso de uso
        )

        return asset
