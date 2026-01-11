from dataclasses import dataclass
import datetime

from .value_objects import ModelCode, ModelName, ModelSource, RouteId

@dataclass(frozen=True)
class ModelRouted:
    route_id: RouteId
    code: ModelCode
    name: ModelName
    source: ModelSource
    occurred_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)