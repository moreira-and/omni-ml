"""Domain interfaces for reading market data.

Estas interfaces definem contratos de leitura de dados de mercado
(preços de ativos e indicadores macroeconômicos) a partir de fontes
externas (APIs, data lake, banco de dados, etc.).

Implementações concretas (adapters) devem:
- Respeitar os tipos de retorno (`PriceBarFact`, `MacroeconomicIndicatorFact`).
- Garantir ordenação temporal consistente.
- Não expor detalhes de infraestrutura para as camadas de domínio/aplicação.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from .value_objects import MacroeconomicIndicatorFact, PriceBarFact


class PriceReadRepository(ABC):
    """Interface para repositórios de leitura de preços de ativos financeiros.

    Responsável por fornecer séries históricas de preços (barras) de um único
    ativo identificado por `code` e `interval`.

    Ubiquitous language:
        - "preço" = barra de preço representada por `PriceBarFact`
        - "interval" = granularidade temporal da barra (ex.: "1d", "1h")

    Implementações típicas:
        - Adapter para API de mercado (ex.: Yahoo Finance, B3, Alpha Vantage).
        - Leitura de tabelas fact em data warehouse / lakehouse.
    """

    @abstractmethod
    def get_prices(
        self,
        *,
        code: str,
        interval: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[PriceBarFact]:
        """Obtém a série histórica de preços de um ativo.

        Contrato de domínio:
            - Deve retornar apenas `PriceBarFact` associados ao `ticker` informado.
            - As barras devem estar ordenadas por timestamp ascendente.
            - O intervalo [start, end] é fechado em `start` e, por convenção,
              fechado em `end` (a implementação pode documentar se usa < end).
            - Se `end` for `None`, entende-se como "até a última barra disponível".
            - Pode retornar um iterável vazio se não houver dados no período.
            - O campo de intervalo em `PriceBarFact` (quando existir) deve refletir
              o valor de `interval` recebido.

        Args:
            ticker:
                Código do ativo na fonte de dados subjacente, ex.: "AAPL",
                "PETR4.SA". Deve estar no formato esperado pela implementação.
            interval:
                Resolução temporal das barras de preço, ex.: "1d", "1h", "5m".
                O conjunto de valores aceitos é responsabilidade da implementação.
            start:
                Data/hora inicial (inclusiva) da janela de busca. Recomenda-se
                que esteja em UTC ou no timezone documentado pela implementação.
            end:
                Data/hora final (opcional) da janela de busca. Quando `None`,
                a implementação deve buscar até o último dado disponível.

        Returns:
            Iterable[PriceBarFact]:
                Iterável de barras de preço que satisfazem os filtros de
                `ticker`, `interval` e janela temporal.

        Raises:
            ValueError:
                Quando os parâmetros forem inválidos (por exemplo, `start > end`
                ou `ticker` em formato não suportado).
            IOError / RuntimeError:
                Quando houver falha de comunicação com a fonte de dados ou
                erro não recuperável na leitura.
        """
        ...


class IndicatorReadRepository(ABC):
    """Interface para repositórios de leitura de indicadores macroeconômicos.

    Responsável por fornecer séries temporais de indicadores agregados
    (ex.: taxa de juros, inflação, PIB) modelados como
    `MacroeconomicIndicatorFact`.

    Ubiquitous language:
        - "indicator" = série temporal de valores macroeconômicos
        - "name" = identificador lógico/configurável do indicador no domínio
    """

    @abstractmethod
    def get_indicator(
        self,
        *,
        code: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[MacroeconomicIndicatorFact]:
        """Obtém a série temporal de um indicador macroeconômico.

        Contrato de domínio:
            - Deve retornar apenas `MacroeconomicIndicatorFact` associados ao
              identificador lógico `name`.
            - A série retornada deve estar ordenada por timestamp ascendente.
            - O intervalo [start, end] segue a mesma convenção da interface
              de preços (inclusivo em `start`; comportamento em `end` deve
              ser documentado pela implementação).
            - Se `end` for `None`, entende-se como "até o último valor disponível".
            - Pode retornar um iterável vazio se não houver dados no período.

        Args:
            name:
                Nome lógico do indicador no domínio, ex.: "SELIC", "IPCA_MENSAL",
                "PIB_TRIMESTRAL". Este nome costuma ser mapeado internamente
                para códigos específicos da fonte de dados (ex.: códigos SGS/BCB).
            start:
                Data/hora inicial (inclusiva) da janela de busca da série.
            end:
                Data/hora final (opcional) da janela de busca. Quando `None`,
                a implementação deve buscar até o último dado disponível.

        Returns:
            Iterable[MacroeconomicIndicatorFact]:
                Iterável de pontos da série temporal do indicador solicitado.

        Raises:
            ValueError:
                Quando os parâmetros forem inválidos ou o `name` não estiver
                configurado/registrado na implementação.
            IOError / RuntimeError:
                Quando houver erro de acesso à fonte de dados ou falha não
                recuperável durante a leitura.
        """
        ...
