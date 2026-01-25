from datetime import datetime
from typing import Any

from ...domain.entities import ExtractDefinition
from ...domain.enums import DataKind
from ...domain.errors import DomainError
from ...domain.models.params import TimeRange
from ...domain.models.params.base import ExtractParams
from ..clocks import Clock, ensure_utc
from ..errors import ApplicationError
from ..interfaces import ExtractParamsResolver


class DefaultExtractParamsResolver(ExtractParamsResolver):
    def __init__(self, clock: Clock):
        self._clock = clock

    def resolve(
        self,
        definition: ExtractDefinition,
        config: dict[str, Any],
    ) -> ExtractParams:

        raw = config.get(definition.data_kind.value)

        if raw is None:
            raise ApplicationError(f"Missing config for data kind: {definition.data_kind}")

        if definition.data_kind == DataKind.CANDLESTICK:
            return self._build_time_range(raw)

        if definition.data_kind == DataKind.ECONOMIC_INDICATOR:
            return self._build_time_range(raw)

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
        if isinstance(value, datetime):
            return ensure_utc(value)

        if isinstance(value, str):
            dt = datetime.fromisoformat(value)
            return ensure_utc(dt)

        return None
