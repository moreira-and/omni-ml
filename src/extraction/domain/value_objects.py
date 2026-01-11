import uuid
import datetime

from .errors import DomainError

class RouteId:
    def __init__(self,
                 value: str | None = None,
                 created_at: datetime.datetime | None = None
                 ):
        self._value = value or uuid.uuid4().hex
        self._created_at = created_at or datetime.datetime.now(datetime.timezone.utc)

    @property
    def value(self) -> str:
        return self._value

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    def __eq__(self, other):
        return (
            isinstance(other, RouteId) 
            and self._value == other._value
            and self._created_at == other._created_at
            )

    def __hash__(self):
        return hash((self._value, self._created_at))
    

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


class ModelSource:
    def __init__(self, value: str):
        if not value:
            raise DomainError("TriggerSource cannot be empty")

        self._value = value.lower()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other):
        return isinstance(other, ModelSource) and self._value == other._value

    def __hash__(self):
        return hash(self._value)



class Priority:
    def __init__(self, value: int):
        if value < 0:
            raise DomainError("Priority must be >= 0")

        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other):
        return isinstance(other, Priority) and self._value == other._value

    def __hash__(self):
        return hash(self._value)