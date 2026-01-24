import uuid
from datetime import datetime, timezone

class InternalRastreabilityMetadata:
    def __init__(
        self,
        id: str | None = None,
        created_at: datetime | None = None,
        modified_at: datetime | None = None,
    ):
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.now(timezone.utc)
        self.modified_at = modified_at or self.created_at