import uuid
from datetime import datetime, timezone

from .errors import DomainError    


class ModelRastreability:
    def __init__(
        self,
        id: str | None = None,
        created_at: datetime | None = None,
        modified_at: datetime | None = None,
    ):
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.now(timezone.utc)
        self.modified_at = modified_at or self.created_at

class ModelCode:
    def __init__(self, value: str):
        if not value or not value.strip():
            raise DomainError("ModelCode cannot be empty")

        if " " in value:
            raise DomainError("ModelCode must not contain spaces")

        self._value = value.upper()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other):
        return isinstance(other, ModelCode) and self._value == other._value

    def __hash__(self):
        return hash(self._value)


class ModelName:
    def __init__(self, name: str):
        if not name:
            raise DomainError("ModelName requires name")

        self._value = name

    @property
    def value(self) -> str:
        return self._value
    
    def __eq__(self, other):
        return (
            isinstance(other, ModelName)
            and self._value == other._value
        )

    def __hash__(self):
        return hash(self._value)