from typing import Iterable

from ...config import DATA_DIR, Path

from ..domain.entities import ModelRouteDefinition
from ..domain.enums import ModelType, ModelSource, TimeWindow
from ..domain.value_objects import ModelCode, ModelName

from ..domain.interfaces import ModelRouteRepository

import pandas as pd

class LocalRouteRepository(ModelRouteRepository):

    @property
    def path(self) -> Path:
        return DATA_DIR / "model_route_definition.csv"    

    def by_code(self, code: ModelCode) -> Iterable[ModelRouteDefinition]:
        """
        Retorna todas as policies associadas a um código.
        A decisão de prioridade/fallback é do domínio.
        """
        df = pd.read_csv(self.path)
        rows = df[df["code"] == code.value]
        for _, row in rows.iterrows():
            yield ModelRouteDefinition(
                code=ModelCode(row["code"]),
                name=ModelName(row["name"]),
                source=ModelSource(row["source"]),
                type=ModelType(row["type"]),
                time_window=TimeWindow(row["time_window"]),
            )


    def by_source(self, source: ModelSource) -> Iterable[ModelRouteDefinition]:
        """
        Retorna todas as policies associadas a uma origem.
        A decisão de prioridade/fallback é do domínio.
        """
        df = pd.read_csv(self.path)
        rows = df[df["source"] == source.value]
        for _, row in rows.iterrows():
            yield ModelRouteDefinition(
                code=ModelCode(row["code"]),
                name=ModelName(row["name"]),
                source=ModelSource(row["source"]),
                type=ModelType(row["type"]),
                time_window=TimeWindow(row["time_window"]),
            )
    def all(self) -> Iterable[ModelRouteDefinition]:
        df = pd.read_csv(self.path)
        for _, row in df.iterrows():
            yield ModelRouteDefinition(
                code=ModelCode(row["code"]),
                name=ModelName(row["name"]),
                source=ModelSource(row["source"]),
                type=ModelType(row["type"]),
                time_window=TimeWindow(row["time_window"]),
            )

    def save(self, route: ModelRouteDefinition) -> None:
        df = pd.read_csv(self.path)
        df.loc["code", "name", "source", "type", "time_window"] = [
            route.code.value,
            route.name.value,
            route.source.value,
            route.type.value,
            route.time_window.value,
        ]
        df.to_csv(self.path, index=False)
