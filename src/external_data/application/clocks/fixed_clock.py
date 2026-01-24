from datetime import datetime

from .clock import Clock


class FixedClock(Clock):
    def __init__(self, fixed_time: datetime):
        self._fixed_time = fixed_time

    def now(self) -> datetime:
        return self._fixed_time
