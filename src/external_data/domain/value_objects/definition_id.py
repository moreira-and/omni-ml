import uuid

from ..errors import DomainError


class DefinitionId:
    def __init__(self, value: uuid.UUID | None = None):
        self._value = value or uuid.uuid4()

    @property
    def value(self) -> uuid.UUID:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, DefinitionId) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"DefinitionId({self._value})"
