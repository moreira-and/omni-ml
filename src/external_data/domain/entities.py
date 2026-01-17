from .value_objects import ExternalCode, InternalAlias, InternalRastreability

from .enums import DataKind, ExternalSource, TimeWindow
from .events import ExtractedData

from datetime import datetime,timezone

class ExternalDataExtractDefinition:
    def __init__(
        self,
        code: ExternalCode,
        alias: InternalAlias,
        source: ExternalSource,
        data_kind: DataKind,
        time_window: TimeWindow,
        started_at: datetime | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        modified_at: datetime | None = None,
    ):

        self._code = code
        self._alias = alias
        self._data_kind = data_kind
        self._source = source
        self._time_window = time_window
        self._started_at = started_at

        self._rastreability = InternalRastreability(
            id=id,
            created_at=created_at,
            modified_at=modified_at,
        )

        self.events = []

    @property
    def data_kind(self) -> DataKind:
        return self._data_kind
    
    @property
    def source(self) -> ExternalSource:
        return self._source

    @property
    def code(self) -> ExternalCode:
        return self._code
    
    @property
    def time_window(self) -> TimeWindow:
        return self._time_window

    @property
    def alias(self) -> InternalAlias:
        return self._alias

    @property
    def rastreability(self) -> InternalRastreability:
        return self._rastreability

    def _record_event(self, event: ExtractedData):
        self.events.append(event)

    def can_route(self, source: ExternalSource) -> bool:
        return self._source == source


    def route(self, source: ExternalSource) -> None:
        if not self.can_route(source):
            raise ValueError("Route not allowed for this source")
        
        self.last_routed_at = datetime.now(timezone.utc)

        event = ExtractedData(
            rastreability=self._rastreability,
            code=self._code,
            alias=self._alias,
            source=source,
        )

        self._record_event(event)