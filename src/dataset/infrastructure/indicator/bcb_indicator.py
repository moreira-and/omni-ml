from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import time
from typing import Iterable, Optional

from loguru import logger
import requests

from src.dataset.domain.interfaces import IndicatorReadRepository
from src.dataset.domain.value_objects import MacroeconomicIndicatorFact


class BcbIndicator(IndicatorReadRepository):
    """
    Adapter para a API de séries temporais do BCB (SGS).
    Converte JSON -> IndicatorFact sem expor DataFrame.
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

    def get_indicator(
        self,
        *,
        name: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[MacroeconomicIndicatorFact]:

        logger.info(f"[BcbIndicator] Downloading {name} from the Central Bank of Brazil API...")

        sgs_code = self._get_code_by_name(name=name) or name

        raw_data = self._request_bcb_series(
            sgs_code=sgs_code,
            start=start,
            end=end,
        )

        facts = self._dicts_to_entities(raw_data=raw_data, name=name)

        return facts

    def _request_bcb_series(
        self,
        *,
        sgs_code: str,
        start: datetime,
        end: datetime | None,
    ) -> list[dict]:
        """
        Retorna: [{ "data": "01/01/2000", "valor": "10.5" }, ...]
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
        Mapeia nomes comuns para códigos SGS do BCB.
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
        self, raw_data: list[dict], name: str
    ) -> list[MacroeconomicIndicatorFact]:

        if not raw_data:
            logger.warning(f"[BcbIndicator] No data returned for {name}")
            return []

        results: list[MacroeconomicIndicatorFact] = []

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
                MacroeconomicIndicatorFact(
                    country="BR",
                    name=name,
                    ts=ts,
                    value=value,
                )
            )

        return results

    @staticmethod
    def valid_tickers():
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
