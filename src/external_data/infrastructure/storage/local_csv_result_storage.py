import csv
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from ....config import DATA_DIR
from ...application.interfaces import ExtractResultStore
from ...domain.entities import ExtractDefinition
from ...domain.models import ExtractBatch
from ...domain.models.base import DomainModel


def to_row(item: Any) -> Mapping[str, Any]:
    if isinstance(item, Mapping):
        return {k: v.value if isinstance(v, Enum) else v for k, v in item.items()}

    if is_dataclass(item) and not isinstance(item, type):
        return {k: (v.value if isinstance(v, Enum) else v) for k, v in asdict(item).items()}

    if hasattr(item, "__dict__"):
        return {k: (v.value if isinstance(v, Enum) else v) for k, v in vars(item).items()}

    raise TypeError(f"Cannot serialize item of type {type(item).__name__} to CSV row")


class LocalCsvResultStorage(ExtractResultStore):
    def __init__(
        self,
        base_path: Path | None = None,
    ) -> None:
        self._base_path = base_path or (DATA_DIR / "extraction_results")
        self._base_path.mkdir(parents=True, exist_ok=True)

    def store(self, batch: ExtractBatch) -> None:
        timestamp = batch.executed_at.strftime("%Y%m%d_%H%M%S")

        self._store_csv(
            definition=batch.definition,
            results=batch.results,
            timestamp=timestamp,
        )

    def _store_csv(
        self,
        *,
        definition: ExtractDefinition,
        results: list[DomainModel],
        timestamp: str,
    ) -> None:
        route_dir = self._route_directory(definition)
        file_path = route_dir / f"{timestamp}.csv"

        rows: list[dict[str, Any]] = [self._model_to_row(model) for model in results]
        fieldnames = rows[0].keys()

        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _route_directory(self, route: ExtractDefinition) -> Path:
        path = (
            self._base_path
            / route.source.value
            / route.data_kind.value
            / route.alias.value
            / route.time_window.value
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _model_to_row(self, model: DomainModel) -> dict[str, Any]:
        """
        Converts a DomainModel into a flat dict suitable for CSV output.
        Infrastructure concern only.
        """
        return vars(model)
