from enum import Enum

class ModelType(Enum):
    CANDLESTICK = "candlestick"
    ECONOMIC_INDICATOR = "economic_indicator"

class ModelSource(Enum):
    YFINANCE = "yfinance"
    BCB = "bcb"

## TimeWindow Enum represents various time intervals for candlestick data in trading.
class TimeWindow(Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1M"
    ONE_QUARTER = "3M"
    ONE_SEMESTER = "6M"
    ONE_YEAR = "1y"