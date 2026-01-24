from typing import Dict, Iterable, Optional, Mapping, Any
from datetime import datetime

from ....config import logger

from ...domain.enums import DataKind
from ...domain.models import Indicator
from ...domain.enums.external_source import ExternalSource
from ...domain.entities.extract_definition import ExtractDefinition

from ...domain.interfaces import ExtractExecutor

import requests


class BcbLoadingStrategy(ExtractExecutor):

    def execute(self, definition: ExtractDefinition, params: Mapping[str, Any] | None = None):
        if not params:
            raise ValueError("Extractor requires criterious")

        return self.extract_between(
            definition=definition,
            start=params["start"],
            end=params["end"],
        )
    
    def extract_between(
            self,
            definition: ExtractDefinition,
            start:datetime,
            end:datetime,
        ) -> Iterable[Indicator]:
    

        logger.info(f"Downloading {definition.alias.value} ({definition.code.value}) from the Central Bank of Brazil API...")

        json_series = self._request_json_series(
            sgs_code=definition.code.value,
            start_date=start,
            end_date=end
        )
        
        indicators = self._parse_indicators(json_series=json_series, definition=definition)
        return indicators

    def _request_json_series(self, sgs_code: str, start_date: datetime, end_date: datetime) -> Optional[Dict]:
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sgs_code}/dados'
        params = {
            'formato': 'json',
            'dataInicial': start_date.strftime('%d/%m/%Y'),
            'dataFinal': end_date.strftime('%d/%m/%Y'),
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Erro ao conectar à API do BCB: {e}", exc_info=True)
            return None
        except ValueError:
            logger.error("Erro ao interpretar a resposta como JSON.", exc_info=True)
            return None
        
    def _parse_indicators(
        self,
        *,
        json_series: Optional[Dict],
        definition: ExtractDefinition,
    ) -> Iterable[Indicator]:

        for item in json_series if json_series else []:
            try:
                yield Indicator(
                    code=definition.code.value,
                    alias=definition.alias.value,
                    timestamp=datetime.strptime(item["data"], "%d/%m/%Y"),
                    value=float(item["valor"]),
                    time_window=definition.time_window,
                )

            except (KeyError, ValueError) as exc:
                logger.warning(
                    "Invalid BCB indicator data for route %s: %s",
                    exc,
                    item,
                    exc_info=True,
                )
                continue
    @property
    def get_by_source(self) -> ExternalSource:
        return ExternalSource("bcb")
    
    @property
    def get_by_kind(self) -> DataKind:
        return DataKind.ECONOMIC_INDICATOR