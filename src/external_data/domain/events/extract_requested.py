from datetime import datetime
from ..value_objects import DefinitionId

class ExtractRequested:
    def __init__(self, definition_id: DefinitionId, requested_at: datetime):
        self.definition_id = definition_id
        self.requested_at = requested_at