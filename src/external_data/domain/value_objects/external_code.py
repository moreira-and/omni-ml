from ..errors import DomainError


class ExternalCode:
    def __init__(self, value: str):

        # if not value.isalnum():
        #    raise DomainError("ExternalCode must be alphanumeric")

        if not value or not value.strip():
            raise DomainError("ExternalCode cannot be empty")

        if " " in value:
            raise DomainError("ExternalCode must not contain spaces")

        self._value = value.upper()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other):
        return isinstance(other, ExternalCode) and self._value == other._value

    def __hash__(self):
        return hash(self._value)
