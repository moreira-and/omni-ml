from datetime import datetime

from .value_objects import RouteId, ModelCode, ModelName, ModelSource

from .enums import ModelType
from .events import ModelRouted
from .errors import DomainError

class ModelRoute:
    def __init__(
        self,
        id: RouteId,
        code: ModelCode,
        name: ModelName,
        source: ModelSource,
        type: ModelType
    ):

        self._code = code
        self._name = name
        self._type = type
        self._source = source

        self._id = id
        self._created_at = id.created_at
        self._updated_at = self._created_at

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
    def name(self) -> ModelName:
        return self._name
    
    @property
    def id(self) -> RouteId:
        return self._id



    def _record_event(self, event: ModelRouted):
        # Placeholder for event recording logic
        pass

    def can_route(self, source: ModelSource) -> bool:

        can_route = self._source == source

        if not can_route:
            return False
        
        event = ModelRouted(
            route_id=self._id,
            code=self._code,
            name=self._name,
            source=source
        )

        self._record_event(event)

        return True