from collections.abc import Mapping
from pathlib import Path
import datetime
import pickle
from typing import Any

from ...config import DATA_DIR
from ..domain.entities import ModelRoute

class LocalExtractionResultStorage:
    def __init__(self, base_path: Path | None = None) -> None:
        self._base_path = base_path or DATA_DIR / "extraction_results"
        self._base_path.mkdir(parents=True, exist_ok=True)

    def store(self, results: Mapping[ModelRoute, Any]) -> None:
        timestamp = self._now_timestamp()

        for route, stream in results.items():
            materialized_result = self._materialize(stream)
            self._store_payload(
                route_id=route.id.value,
                payload=materialized_result,
                timestamp=timestamp,
            )

    def _materialize(self, stream: Any) -> list[Any]:
        return list(stream)

    def _store_payload(self, *, route_id: str, payload: Any, timestamp: str) -> None:
        route_dir = self._route_directory(route_id)
        file_path = route_dir / f"{timestamp}.pkl"
        self._serialize(file_path, payload)

    def _route_directory(self, route_id: str) -> Path:
        path = self._base_path / route_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _serialize(self, file_path: Path, payload: Any) -> None:
        with file_path.open("wb") as file:
            pickle.dump(payload, file)

    @staticmethod
    def _now_timestamp() -> str:
        return datetime.datetime.now(
            datetime.timezone.utc
        ).strftime("%Y%m%d_%H%M%S")
