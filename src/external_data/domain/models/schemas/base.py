from typing import TypeVar


class DomainModel:
    """
    Marker base class for models produced by external data extraction.
    Used only for typing and semantic grouping.
    """

    __slots__ = ()


TModel = TypeVar("TModel", bound=DomainModel)
