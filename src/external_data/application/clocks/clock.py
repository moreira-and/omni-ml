from abc import ABC, abstractmethod
from datetime import datetime, timezone


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        """Return the current time as a timezone-aware UTC datetime."""
        ...
