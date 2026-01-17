from dataclasses import dataclass
import datetime

from .enums import ModelSource
from .value_objects import ModelCode, ModelName, ModelRastreability


@dataclass(frozen=True)
class ModelRouted:
    rastreability: ModelRastreability
    code: ModelCode
    name: ModelName
    source: ModelSource
    occurred_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)