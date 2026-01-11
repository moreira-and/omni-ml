from enum import Enum


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

class ModelType(Enum):
    CANDLESTICK = "candlestick"
    ECONOMIC_INDICATOR = "economic_indicator"