import uuid
from .value_objects import ModelCode, ModelName, ModelRastreability

from .enums import ModelType, ModelSource, TimeWindow
from .events import ModelRouted

from datetime import datetime,timezone

class ModelRouteDefinition:
    def __init__(
        self,
        code: ModelCode,
        name: ModelName,
        source: ModelSource,
        type: ModelType,
        time_window: TimeWindow,
        started_at: datetime | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        modified_at: datetime | None = None,
    ):

        self._code = code
        self._name = name
        self._type = type
        self._source = source
        self._time_window = time_window
        self._started_at = started_at

        self._rastreability = ModelRastreability(
            id=id,
            created_at=created_at,
            modified_at=modified_at,
        )

        self.events = []

    @property
    def type(self) -> ModelType:
        return self._type
    
    @property
    def source(self) -> ModelSource:
        return self._source

    @property
    def code(self) -> ModelCode:
        return self._code
    
    @property
    def time_window(self) -> TimeWindow:
        return self._time_window

    @property
    def name(self) -> ModelName:
        return self._name

    @property
    def rastreability(self) -> ModelRastreability:
        return self._rastreability

    def _record_event(self, event: ModelRouted):
        self.events.append(event)

    def can_route(self, source: ModelSource) -> bool:
        return self._source == source


    def route(self, source: ModelSource) -> None:
        if not self.can_route(source):
            raise ValueError("Route not allowed for this source")
        
        self.last_routed_at = datetime.now(timezone.utc)

        event = ModelRouted(
            rastreability=self._rastreability,
            code=self._code,
            name=self._name,
            source=source,
        )

        self._record_event(event)