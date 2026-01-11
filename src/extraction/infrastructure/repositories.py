from typing import Iterable

from ...config import DATA_DIR, Path

from ..domain.entities import ModelRoute
from ..domain.enums import ModelType
from ..domain.value_objects import ModelCode, ModelName, RouteId, ModelSource

from ..domain.interfaces import ModelRouteRepository

import pandas as pd

class LocalRouteRepository(ModelRouteRepository):

    @property
    def path(self) -> Path:
        return DATA_DIR / "model_routes.csv"

    def by_id(self, id: RouteId) -> ModelRoute:
        df = pd.read_csv(self.path)
        row = df[df["id"] == id.value]
        if not row.empty:
            return ModelRoute(
                id=RouteId(row["id"].iloc[0]),
                code=ModelCode(row["code"].iloc[0]),
                name=ModelName(row["name"].iloc[0]),
                source=ModelSource(row["source"].iloc[0]),
                type=ModelType(row["type"].iloc[0].lower()),
            )
        raise ValueError(f"Route with id {id} not found")
    

    def by_code(self, code: ModelCode) -> Iterable[ModelRoute]:
        """
        Retorna todas as policies associadas a um código.
        A decisão de prioridade/fallback é do domínio.
        """
        df = pd.read_csv(self.path)
        rows = df[df["code"] == code.value]
        for _, row in rows.iterrows():
            yield ModelRoute(
                id=RouteId(row["id"]),
                code=ModelCode(row["code"]),
                name=ModelName(row["name"]),
                source=ModelSource(row["source"]),
                type=ModelType(row["type"].lower()),
            )


    def by_source(self, source: ModelSource) -> Iterable[ModelRoute]:
        """
        Retorna todas as policies associadas a uma origem.
        A decisão de prioridade/fallback é do domínio.
        """
        df = pd.read_csv(self.path)
        rows = df[df["source"] == source.value]
        for _, row in rows.iterrows():
            yield ModelRoute(
                id=RouteId(row["id"]),
                code=ModelCode(row["code"]),
                name=ModelName(row["name"]),
                source=ModelSource(row["source"]),
                type=ModelType(row["type"].lower()),
            )

    def all(self) -> Iterable[ModelRoute]:
        df = pd.read_csv(self.path)
        for _, row in df.iterrows():
            yield ModelRoute(
                id=RouteId(row["id"]),
                code=ModelCode(row["code"]),
                name=ModelName(row["name"]),
                source=ModelSource(row["source"]),
                type=ModelType(row["type"].lower()),
            )

    def save(self, route: ModelRoute) -> None:
        df = pd.read_csv(self.path)
        if not df[df["id"] == route._id.value].empty:
            df.loc[df["id"] == route._id.value, ["code", "name", "source", "type"]] = [
                route.code.value,
                route.name.value,
                route.source.value,
                route.type.value,
            ]
        else:
            new_row = {
                "id": route._id.value,
                "code": route.code.value,
                "name": route.name.value,
                "source": route.source.value,
                "type": route.type.value,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.path, index=False)
