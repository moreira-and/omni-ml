from ..errors import DomainError    

class InternalAlias:
    def __init__(self, value: str):
        if not value:
            raise DomainError("InternalAlias requires name")

        self._value = value.strip()

    @property
    def value(self) -> str:
        return self._value
    
    def __eq__(self, other):
        return (
            isinstance(other, InternalAlias)
            and self._value == other._value
        )

    def __hash__(self):
        return hash(self._value)