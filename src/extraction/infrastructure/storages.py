from pathlib import Path
from typing import Any, Mapping
import csv
from enum import Enum

from ...config import DATA_DIR
from ..domain.entities import ModelRoute
from ..domain.models import ExtractionBatch


from dataclasses import is_dataclass, asdict


def to_row(item: Any) -> Mapping[str, Any]:
    if isinstance(item, Mapping):
        return {
            k: v.value if isinstance(v, Enum) else v
            for k, v in item.items()
        }

    if is_dataclass(item):
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in asdict(item).items()
        }

    if hasattr(item, "__dict__"):
        return {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in vars(item).items()
        }

    raise TypeError(
        f"Cannot serialize item of type {type(item).__name__} to CSV row"
    )


class LocalResultStorage:
    def __init__(
        self,
        base_path: Path | None = None,
    ) -> None:
        self._base_path = base_path or (DATA_DIR / "extraction_results")
        self._base_path.mkdir(parents=True, exist_ok=True)

    def store(self, batch: ExtractionBatch) -> None:
        timestamp = batch.executed_at.strftime("%Y%m%d_%H%M%S")

        for route, stream in batch.results.items():
            rows = [to_row(item) for item in stream]
            if not rows:
                continue

            self._store_csv(
                route=route,
                rows=rows,
                timestamp=timestamp,
            )

    def _store_csv(
        self,
        *,
        route: ModelRoute,
        rows: list[Mapping[str, Any]],
        timestamp: str,
    ) -> None:
        route_dir = self._route_directory(route.id.value)
        file_path = route_dir / f"{timestamp}.csv"

        fieldnames = rows[0].keys()

        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _route_directory(self, route_id: str) -> Path:
        path = self._base_path / route_id
        path.mkdir(parents=True, exist_ok=True)
        return path