from datetime import datetime
from typing import Any

from ...domain.entities import ExtractDefinition
from ...domain.enums import DataKind
from ...domain.errors import DomainError
from ..clocks import Clock
from ..interfaces import ExtractParamsResolver
from ...domain.params import TimeRange
from ...domain.params.base import ExtractParams


class DefaultExtractParamsResolver(ExtractParamsResolver):
    def __init__(self, clock: Clock):
        self._clock = clock

    def resolve(
        self,
        definition: ExtractDefinition,
        config: dict[str, Any],
    ) -> ExtractParams:

        if definition.data_kind == DataKind.CANDLESTICK:
            return self._build_time_range(config)

        if definition.data_kind == DataKind.ECONOMIC_INDICATOR:
            return self._build_time_range(config)

        raise DomainError(f"No ExtractionParams available for data kind {definition.data_kind}")

    def _build_time_range(self, raw: dict[str, Any]) -> TimeRange:
        start = self._parse_datetime(raw.get("start"))
        end = self._parse_datetime(raw.get("end"))

        if start is None:
            raise DomainError("Missing required parameter: start")

        if end is None:
            end = self._clock.now()

        return TimeRange(
            start=start,
            end=end,
        )

    def _parse_datetime(self, value: Any) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)

        raise DomainError("Invalid datetime value")
