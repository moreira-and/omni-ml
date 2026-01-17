from dataclasses import dataclass
import datetime

from .enums import ExternalSource
from .value_objects import ExternalCode, InternalAlias, InternalRastreability


@dataclass(frozen=True)
class ExtractedData:
    rastreability: InternalRastreability
    code: ExternalCode
    alias: InternalAlias
    source: ExternalSource
    occurred_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)