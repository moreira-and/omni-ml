from datetime import datetime

from ..enums import DataKind, ExternalSource, TimeWindow
from ..events import ExtractRequested
from ..value_objects import DefinitionId, ExternalCode, InternalAlias


class ExtractDefinition:
    def __init__(
        self,
        id: DefinitionId,
        code: ExternalCode,
        alias: InternalAlias,
        source: ExternalSource,
        data_kind: DataKind,
        time_window: TimeWindow,
    ):

        self._id = id
        self._code = code
        self._alias = alias
        self._data_kind = data_kind
        self._source = source
        self._time_window = time_window

        self._events: list[ExtractRequested] = []

    @property
    def id(self) -> DefinitionId:
        return self._id

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
    def alias(self) -> InternalAlias:
        return self._alias

    @property
    def time_window(self) -> TimeWindow:
        return self._time_window

    def mark_as_requested(self, clock: datetime) -> None:
        self._events.append(ExtractRequested(self._id, clock))

    def pull_events(self) -> list[ExtractRequested]:
        events = self._events[:]
        self._events.clear()
        return events
