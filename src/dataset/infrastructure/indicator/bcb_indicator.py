from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Iterable, List, Optional

from loguru import logger
import requests

from src.dataset.domain.interfaces.economic_unit_repository import (
    CountryIndicatorReadRepository,
)
from src.dataset.domain.value_objects import CountryIndicator


class BcbIndicator(CountryIndicatorReadRepository):
    """
    Adapter para a API de séries temporais do BCB (SGS).
    Converte JSON -> CountryIndicator sem expor DataFrame.

    Contexto de domínio:
        - Fonte: Banco Central do Brasil (SGS).
        - Escopo: indicadores macroeconômicos do país "BR".
    """

    def __init__(
        self,
        *,
        base_url: str = "https://api.bcb.gov.br/dados/serie",
        session: Optional[requests.Session] = None,
    ) -> None:
        super().__init__()
        self._base_url = base_url.rstrip("/")
        self._session = session or requests.Session()

    def get_country_indicators(
        self,
        *,
        country_code: str,
        name: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[CountryIndicator]:
        """
        Implementação de CountryIndicatorReadRepository para o país BR.

        Args:
            country_code:
                Código do país (ISO 3166-1 alfa-2). Atualmente só "BR" é suportado.
            name:
                Nome lógico do indicador (ex.: "SELIC", "IPCA_Mensal").
            start:
                Data inicial (inclusiva) da janela.
            end:
                Data final (opcional). Quando None, usa data atual em UTC.

        Returns:
            Iterable[CountryIndicator]:
                Pontos da série temporal do indicador.
        """
        if country_code.upper() != "BR":
            logger.warning(
                f"[BcbIndicator] country_code={country_code!r} não suportado. "
                "A implementação atual suporta apenas 'BR'."
            )
            return []

        logger.info(
            f"[BcbIndicator] Downloading {name} for country={country_code} "
            f"from the Central Bank of Brazil API..."
        )

        sgs_code = self._get_code_by_name(name=name) or name

        raw_data = self._request_bcb_series(
            sgs_code=sgs_code,
            start=start,
            end=end,
        )

        facts = self._dicts_to_entities(
            raw_data=raw_data,
            country_code=country_code.upper(),
            name=name,
        )

        return facts

    def _request_bcb_series(
        self,
        *,
        sgs_code: str,
        start: datetime,
        end: datetime | None,
    ) -> list[dict]:
        """
        Chama a API do BCB/SGS e retorna a lista crua de registros.

        Retorno esperado:
            [{ "data": "01/01/2000", "valor": "10.5" }, ...]
        """
        start_str = start.strftime("%d/%m/%Y")
        end_str = (end or datetime.now(tz=timezone.utc)).strftime("%d/%m/%Y")

        url = f"{self._base_url}/bcdata.sgs.{sgs_code}/dados"
        params = {
            "formato": "json",
            "dataInicial": start_str,
            "dataFinal": end_str,
        }

        try:
            response = self._session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"[BcbIndicator] Erro ao conectar à API do BCB: {e}",
                exc_info=True,
            )
            return []
        except ValueError:
            logger.error(
                "[BcbIndicator] Erro ao interpretar a resposta do BCB como JSON.",
                exc_info=True,
            )
            return []

    def _get_code_by_name(self, name: str) -> Optional[str]:
        """
        Mapeia nomes lógicos de domínio para códigos SGS do BCB.
        Exemplo: "SELIC" -> "11"
        """
        name_to_code = {
            "SELIC": "11",
            "CDI": "12",
            "SELIC_Anual": "1178",
            "SELIC_Meta_Anual": "432",
            "IPCA_Mensal": "433",
            "IGP_M_Mensal": "189",
            "INCC_Mensal": "192",
            "Indice_Condicoes_Econ_BR": "27574",
            "Indice_Condicoes_Econ_BR_USD": "29042",
            "Salario_Minimo": "1619",
            "IBC_BR": "24363",
            "Populacao_BR": "21774",
            "PIB_Trimestral_Real": "4380",
            "PIB_Anual_Corrente": "7326",
            "Deflator_Implicito_PIB": "1211",
        }
        return name_to_code.get(name)

    def _dicts_to_entities(
        self,
        *,
        raw_data: list[dict],
        country_code: str,
        name: str,
    ) -> list[CountryIndicator]:
        """
        Converte a lista de dicts da API SGS -> CountryIndicator.
        """
        if not raw_data:
            logger.warning(f"[BcbIndicator] No data returned for {name}")
            return []

        results: list[CountryIndicator] = []

        for item in raw_data:
            try:
                # Campos esperados da API
                date_str = item["data"]
                value_str = item["valor"]

                ts = datetime.strptime(date_str, "%d/%m/%Y").replace(tzinfo=timezone.utc)
                value = Decimal(str(value_str))
            except (KeyError, ValueError, TypeError, InvalidOperation) as exc:
                logger.warning(
                    f"[BcbIndicator] Invalid record for {name}: {item!r}",
                    exc_info=True,
                )
                continue

            results.append(
                CountryIndicator(
                    country_code=country_code,
                    name=name,
                    ts=ts,
                    value=value,
                )
            )

        return results

    @staticmethod
    def valid_indicators() -> List[str]:
        return [
            "SELIC",
            "CDI",
            "SELIC_Anual",
            "SELIC_Meta_Anual",
            "IPCA_Mensal",
            "IGP_M_Mensal",
            "INCC_Mensal",
            "Indice_Condicoes_Econ_BR",
            "Indice_Condicoes_Econ_BR_USD",
            "Salario_Minimo",
            "IBC_BR",
            "Populacao_BR",
            "PIB_Trimestral_Real",
            "PIB_Anual_Corrente",
            "Deflator_Implicito_PIB",
        ]
