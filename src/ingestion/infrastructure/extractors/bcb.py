from typing import Dict, Iterable, List, Optional, Mapping, Any
from datetime import datetime

from ....config import logger

from ...domain.enums import ModelType, TimeWindow
from ...domain.models import Indicator
from ...domain.value_objects import ModelSource
from ...domain.entities import ModelRouteDefinition

from ..interfaces import IndicatorExtractor

import requests
import pandas as pd


class BcbLoadingStrategy(IndicatorExtractor):

    def extract(self, route: ModelRouteDefinition, params: Mapping[str, Any] | None = None):
        if not params:
            raise ValueError("IndicatorExtractor requires criterious")

        return self.extract_between(
            route=route,
            start=params["start"],
            end=params["end"],
            time_window=TimeWindow(params["time_window"]),
        )
    
    def extract_between(
            self,
            route: ModelRouteDefinition,
            start:datetime,
            end:datetime,
            time_window: TimeWindow
        ) -> Iterable[Indicator]:
    

        logger.info(f"Downloading {route.name.value} ({route.code.value}) from the Central Bank of Brazil API...")

        json_series = self._request_json_series(
            sgs_code=route.code.value,
            start_date=start,
            end_date=end
        )
        
        indicators = self._parse_indicators(json_series=json_series, route=route, time_window=time_window)
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
        route: ModelRouteDefinition,
        time_window: TimeWindow
    ) -> Iterable[Indicator]:

        for item in json_series if json_series else []:
            try:
                yield Indicator(
                    code=route.code.value,
                    name=route.name.value,
                    timestamp=datetime.strptime(item["data"], "%d/%m/%Y"),
                    value=float(item["valor"]),
                    time_window=time_window,
                )

            except (KeyError, ValueError) as exc:
                logger.warning(
                    "Invalid BCB indicator data for route %s: %s",
                    exc,
                    route.id.value,
                    item,
                    exc_info=True,
                )
                continue
    @property
    def source(self) -> ModelSource:
        return ModelSource("bcb")
    
    @property
    def type(self) -> ModelType:
        return ModelType.ECONOMIC_INDICATOR