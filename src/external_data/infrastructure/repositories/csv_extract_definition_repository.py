from typing import Iterable

from ....config import DATA_DIR, Path

from ...domain.entities.extract_definition import ExtractDefinition
from ...domain.enums import DataKind, ExternalSource, TimeWindow
from ...domain.value_objects import ExternalCode, InternalAlias

from ...domain.interfaces import ExtractDefinitionRepository

import pandas as pd

class LocalRouteRepository(ExtractDefinitionRepository):

    @property
    def path(self) -> Path:
        return DATA_DIR / "external_data_extract_definition.csv"

    def by_code(self, code: ExternalCode) -> Iterable[ExtractDefinition]:
        """
        Retorna todas as policies associadas a um código.
        A decisão de prioridade/fallback é do domínio.
        """
        df = pd.read_csv(self.path)
        rows = df[df["code"] == code.value]
        for _, row in rows.iterrows():
            yield ExtractDefinition(
                code=ExternalCode(row["code"]),
                alias=InternalAlias(row["alias"]),
                source=ExternalSource(row["source"]),
                data_kind=DataKind(row["kind"]),
                time_window=TimeWindow(row["time_window"]),
            )


    def by_source(self, source: ExternalSource) -> Iterable[ExtractDefinition]:
        """
        Retorna todas as policies associadas a uma origem.
        A decisão de prioridade/fallback é do domínio.
        """
        df = pd.read_csv(self.path)
        rows = df[df["source"] == source.value]
        for _, row in rows.iterrows():
            yield ExtractDefinition(
                code=ExternalCode(row["code"]),
                alias=InternalAlias(row["alias"]),
                source=ExternalSource(row["source"]),
                data_kind=DataKind(row["kind"]),
                time_window=TimeWindow(row["time_window"]),
            )
    def all(self) -> Iterable[ExtractDefinition]:
        df = pd.read_csv(self.path)
        for _, row in df.iterrows():
            yield ExtractDefinition(
                code=ExternalCode(row["code"]),
                alias=InternalAlias(row["alias"]),
                source=ExternalSource(row["source"]),
                data_kind=DataKind(row["kind"]),
                time_window=TimeWindow(row["time_window"]),
            )

    def save(self, route: ExtractDefinition) -> None:
        df = pd.read_csv(self.path)
        df.loc["code", "alias", "source", "kind", "time_window"] = [
            route.code.value,
            route.alias.value,
            route.source.value,
            route.data_kind.value,
            route.time_window.value,
        ]
        df.to_csv(self.path, index=False)
